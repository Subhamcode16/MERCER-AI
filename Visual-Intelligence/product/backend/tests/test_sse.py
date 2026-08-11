import pytest
import asyncio
import time
import jwt
import httpx
from app.main import app as fastapi_app
from app.config import get_settings
from app.database import get_db, connect_db, close_db
from app.models.campaign import Campaign, MemoryNode
from app.storage.campaign_store import CampaignStore
from app.utils.cache import in_memory_pubsub

settings = get_settings()

def generate_mock_jwt(user_id: str, email: str, email_confirmed: bool = True):
    payload = {
        "sub": user_id,
        "email": email,
        "email_confirmed": email_confirmed,
        "exp": int(time.time()) + 3600
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")

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

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="module", autouse=True)
async def init_database():
    await connect_db()
    fastapi_app.state.limiter.enabled = False
    yield
    await close_db()

@pytest.mark.anyio
async def test_sse_thought_stream():
    """
    Test the SSE streaming endpoint `/api/campaigns/{campaign_id}/stream`.
    Verify that the stream is established, receives a heartbeat,
    and streams messages published to the in-memory fallback pubsub.
    """
    user_id = "test_sse_user"
    email = "sse@test.ai"
    token = generate_mock_jwt(user_id, email, email_confirmed=True)
    headers = {"Authorization": f"Bearer {token}"}

    db = get_db()
    store = CampaignStore()

    # Clean previous test campaign if any
    campaign_id = "test_sse_campaign"
    await db.campaigns.delete_one({"id": campaign_id})

    # Create and save a mock campaign owned by this user
    campaign = Campaign(id=campaign_id, name="SSE Test Campaign", user_id=user_id)
    await store.save_campaign(campaign)

    # Use AsyncClient to hit the SSE endpoint
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=fastapi_app), base_url="http://test") as client:
        # We start the stream request in a separate async task because it's a long-running streaming response
        async def read_stream():
            received = []
            try:
                async with client.stream("GET", f"/api/campaigns/{campaign_id}/stream", headers=headers) as response:
                    assert response.status_code == 200
                    async for line in response.iter_lines():
                        if line:
                            received.append(line)
                            if len(received) >= 2:  # Heartbeat + 1 data line
                                break
            except Exception as e:
                print(f"Error in stream reader: {e}")
            return received

        stream_task = asyncio.create_task(read_stream())

        # Wait a brief moment for the connection to establish and heartbeat to be sent
        await asyncio.sleep(0.5)

        # Publish a test memory node event to the fallback pubsub
        node = MemoryNode(type="observation", content="Test SSE message from verification suite")
        channel_name = f"campaign:{campaign_id}:stream"
        await in_memory_pubsub.publish(channel_name, node.model_dump_json())

        # Wait for the stream reader task to finish
        received_lines = await stream_task

        # Verify stream content
        assert len(received_lines) >= 2  # At least heartbeat lines
        
        # Verify first message is heartbeat
        assert any("Connected to thought stream" in line for line in received_lines)
        # Verify second message has our test message
        assert any("Test SSE message from verification suite" in line for line in received_lines)

        print("\n[SSE Test] Successfully verified Server-Sent Events flow with In-Memory fallback!")
