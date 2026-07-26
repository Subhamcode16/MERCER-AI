import pytest
import asyncio
import time
import jwt
from fastapi.testclient import TestClient
import httpx
from datetime import datetime, timezone

from app.main import app as fastapi_app
from app.config import get_settings
from app.database import get_db, connect_db, close_db
from app.models.user import Tier
from app.models.generation import JobStatus, CREDIT_COSTS

# Load settings
settings = get_settings()

# Generate valid mock JWT tokens
def generate_mock_jwt(user_id: str, email: str, email_confirmed: bool = True):
    payload = {
        "sub": user_id,
        "email": email,
        "email_confirmed": email_confirmed,
        "exp": int(time.time()) + 3600
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")

# Globally mock the generator service to avoid calling Gemini API and prevent Key Errors
import app.routers.generate
import app.utils.jwt

async def mock_generate_nano_banana_2(prompt: str) -> str:
    await asyncio.sleep(0.1)
    return "mock_image_bytes_base64"

app.routers.generate.generate_nano_banana_2 = mock_generate_nano_banana_2

# Globally mock Supabase JWT decoding to bypass JWKS network requests during tests
import app.auth.dependencies

def mock_decode_supabase_jwt(token: str) -> dict:
    return jwt.decode(
        token,
        settings.supabase_jwt_secret,
        algorithms=["HS256"],
        options={"verify_aud": False},
    )

app.auth.dependencies.decode_supabase_jwt = mock_decode_supabase_jwt

# Test setup and cleanup helpers
async def get_test_db():
    return get_db()

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="module", autouse=True)
async def init_database():
    await connect_db()
    # Disable rate limiting for other tests by default to avoid cross-test interference
    fastapi_app.state.limiter.enabled = False
    yield
    await close_db()

@pytest.fixture(autouse=True)
async def clean_database():
    # Setup test credentials
    db = await get_test_db()
    # Clean test users
    await db.users.delete_many({"email": {"$regex": "@stress-test\\.ai$"}})
    await db.credit_transactions.delete_many({"user_id": {"$regex": "^stress_test_"}})
    await db.jobs.delete_many({"user_id": {"$regex": "^stress_test_"}})
    yield
    # Cleanup after tests
    await db.users.delete_many({"email": {"$regex": "@stress-test\\.ai$"}})
    await db.credit_transactions.delete_many({"user_id": {"$regex": "^stress_test_"}})
    await db.jobs.delete_many({"user_id": {"$regex": "^stress_test_"}})


@pytest.mark.anyio
async def test_rate_limiting():
    """
    Test rate limiting of 10/minute on /auth/provision endpoint.
    Sends 11 requests sequentially. The 11th should return 429.
    """
    # Dynamically enable rate limiting just for this test
    fastapi_app.state.limiter.enabled = True
    try:
        token = generate_mock_jwt("stress_test_rl", "rl@stress-test.ai", email_confirmed=True)
        headers = {"Authorization": f"Bearer {token}"}
        
        # We use a clean AsyncClient to make fast sequential requests
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=fastapi_app), base_url="http://test") as client:
            status_codes = []
            for _ in range(11):
                response = await client.post("/auth/provision", json={"receive_marketing": False}, headers=headers)
                status_codes.append(response.status_code)
            
            # Verify rate limiting triggered (429 code is present)
            assert 429 in status_codes
            print(f"\n[Rate Limit Test] Status codes received: {status_codes}")
    finally:
        fastapi_app.state.limiter.enabled = False


@pytest.mark.anyio
async def test_ledger_concurrency_and_double_spend():
    """
    Verify concurrency protection on credit deductions.
    1. Provision user & set credits to exactly 4.
    2. Fire 5 parallel generation requests (each costs 2 credits for nano_banana_2).
    3. Assert exactly 2 requests succeed (200) and 3 fail (402).
    4. Assert final DB balance is exactly 0 and no negative balances exist.
    """
    user_id = "stress_test_race"
    email = "race@stress-test.ai"
    token = generate_mock_jwt(user_id, email, email_confirmed=True)
    headers = {"Authorization": f"Bearer {token}"}

    db = await get_test_db()

    # Step 1: Provision the user via API first
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=fastapi_app), base_url="http://test") as client:
        prov_res = await client.post("/auth/provision", json={"receive_marketing": False}, headers=headers)
        assert prov_res.status_code == 200

        # Overwrite user's credit balance to exactly 4 credits in DB (2 jobs * 2 credits = 4 credits)
        await db.users.update_one({"_id": user_id}, {"$set": {"credit_balance": 4}})

        # Step 2: Fire 5 concurrent image generation requests
        tasks = []
        for i in range(5):
            payload = {
                "prompt": f"Stress test clothing item {i}",
                "idempotency_key": f"stress_test_job_{i}"
            }
            tasks.append(
                client.post("/generate/nano_banana_2", json=payload, headers=headers)
            )

        responses = await asyncio.gather(*tasks)
        status_codes = [r.status_code for r in responses]

        # Step 3: Assert exactly 2 got queued (200) and 3 got rejected (402)
        successes = status_codes.count(200)
        failures = status_codes.count(402)

        print(f"\n[Concurrency Test] Successes (200): {successes}, Failures (402): {failures}")
        assert successes == 2
        assert failures == 3

        # Step 4: Verify ledger integrity in DB
        updated_user = await db.users.find_one({"_id": user_id})
        assert updated_user["credit_balance"] == 0

        # Verify transaction logs
        tx_count = await db.credit_transactions.count_documents({"user_id": user_id, "type": "reserve"})
        assert tx_count == 2


@pytest.mark.anyio
async def test_async_jobs_and_polling():
    """
    Submit a generation request, then immediately verify the job is in the 'queued' status,
    and simulate status polling.
    """
    user_id = "stress_test_job"
    email = "job@stress-test.ai"
    token = generate_mock_jwt(user_id, email, email_confirmed=True)
    headers = {"Authorization": f"Bearer {token}"}

    db = await get_test_db()

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=fastapi_app), base_url="http://test") as client:
        # Provision first
        await client.post("/auth/provision", json={"receive_marketing": False}, headers=headers)
        await db.users.update_one({"_id": user_id}, {"$set": {"credit_balance": 10}})

        # Submit generation request
        job_id = "stress_test_polling_key"
        payload = {
            "prompt": "Stunning dress",
            "idempotency_key": job_id
        }
        gen_res = await client.post("/generate/nano_banana_2", json=payload, headers=headers)
        assert gen_res.status_code == 200
        assert gen_res.json()["job_id"] == job_id

        # Verify job state in DB immediately is queued, processing, or completed (due to synchronous test execution)
        job = await db.jobs.find_one({"_id": job_id})
        assert job is not None
        assert job["status"] in [JobStatus.queued.value, JobStatus.processing.value, JobStatus.completed.value]

        # Call polling endpoint /jobs/{job_id} and assert fast latency
        start_poll = time.time()
        poll_res = await client.get(f"/jobs/{job_id}", headers=headers)
        end_poll = time.time()
        
        assert poll_res.status_code == 200
        poll_data = poll_res.json()
        assert poll_data["job_id"] == job_id
        
        # Verify polling latency is extremely low
        latency = (end_poll - start_poll) * 1000
        print(f"\n[Polling Latency Test] Status check took: {latency:.2f} ms")
        assert latency < 500  # polling must be sub-500ms
