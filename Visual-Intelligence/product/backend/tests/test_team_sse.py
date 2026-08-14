import pytest
import asyncio
import json
import httpx
from app.main import app as fastapi_app
from app.database import get_db, connect_db, close_db

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
async def test_team_orchestrator_sse_flow():
    """
    Test the multi-agent orchestration team endpoints:
    - POST /api/team/start
    - GET /api/team/stream/{session_id}
    - POST /api/team/approve/{session_id}
    """
    # 1. Start the team session
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=fastapi_app), base_url="http://test") as client:
        start_response = await client.post(
            "/api/team/start", 
            json={"prompt": "Create an editorial campaign for Banarasi Zari Silk"}
        )
        assert start_response.status_code == 200
        session_id = start_response.json()["session_id"]
        assert session_id is not None

        # 2. Open the SSE stream and read the initial execution messages (up to Art Director)
        received_messages = []
        status_updates = []
        typing_notifications = []

        async def read_stream():
            try:
                async with client.stream("GET", f"/api/team/stream/{session_id}") as response:
                    assert response.status_code == 200
                    async for line in response.iter_lines():
                        if line and line.startswith("data: "):
                            data = json.loads(line[6:])
                            if data["type"] == "message":
                                payload = data["payload"]
                                received_messages.append(payload)
                                # Break when we reach Art-Director which is the end of Phase 1 pipeline
                                if payload["sender"] == "art-director":
                                    break
                            elif data["type"] == "status":
                                status_updates.append(data["payload"])
                            elif data["type"] == "typing":
                                typing_notifications.append(data["payload"])
            except Exception as e:
                print(f"Stream error: {e}")

        # Run the stream reader
        await read_stream()

        # Verify initial agent pipeline messages were streamed and parsed
        assert len(received_messages) >= 4 # welcome + material-dna + visual-dna + art-director
        assert any(m["sender"] == "brand-dna" for m in received_messages)
        assert any(m["sender"] == "material-dna" for m in received_messages)
        assert any(m["sender"] == "image-decomposer" for m in received_messages)
        assert any(m["sender"] == "art-director" for m in received_messages)

        # 3. Approve the setup to trigger Phase 2 (Rendering pipeline)
        approve_response = await client.post(f"/api/team/approve/{session_id}")
        assert approve_response.status_code == 200
        assert approve_response.json()["status"] == "approved"

        # 4. Open the stream again (plays back all messages first, then streams Phase 2 renderer nodes)
        final_messages = []
        final_status = None

        async def read_final_stream():
            try:
                async with client.stream("GET", f"/api/team/stream/{session_id}") as response:
                    assert response.status_code == 200
                    async for line in response.iter_lines():
                        if line and line.startswith("data: "):
                            data = json.loads(line[6:])
                            if data["type"] == "message":
                                final_messages.append(data["payload"])
                            elif data["type"] == "status":
                                final_status = data["payload"]
                                if final_status == "completed":
                                    break
            except Exception as e:
                print(f"Final stream error: {e}")

        await read_final_stream()

        # Verify all agent messages are compiled, including renderer, validator, and copywriter
        assert any(m["sender"] == "renderer" for m in final_messages)
        assert any(m["sender"] == "validator" for m in final_messages)
        assert any(m["sender"] == "copywriter" for m in final_messages)
        assert final_status == "completed"

        print(f"\n[Team SSE Test] Successfully verified A2A pipeline: session {session_id} runs and completes.")
