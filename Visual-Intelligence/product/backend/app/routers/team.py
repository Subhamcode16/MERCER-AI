import asyncio
import json
import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.team_orchestrator import TeamOrchestrator, get_sse_queues
from app.auth import AuthenticatedUser, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/team", tags=["Team Mode"])

class StartRequest(BaseModel):
    prompt: str

@router.post("/start")
async def start_team_session(request: StartRequest, background_tasks: BackgroundTasks):
    """
    Starts a new multi-agent session. Runs the initial analysis pipeline in the background.
    """
    user_id = "default_user" # Mocked or taken from dependencies.
    
    try:
        session_id = await TeamOrchestrator.create_session(user_id, request.prompt)
        
        # Spawn the initial pipeline tasks asynchronously
        background_tasks.add_task(
            TeamOrchestrator.execute_initial_pipeline, 
            session_id, 
            user_id
        )
        
        return {"session_id": session_id}
    except Exception as e:
        logger.error("Failed to start team session: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream/{session_id}")
async def stream_team_session(session_id: str):
    """
    Server-Sent Events endpoint to stream real-time bot replies and typing indicators.
    Replays previous chat messages first so refreshing the page is fully supported.
    """
    async def sse_generator():
        queue = asyncio.Queue()
        get_sse_queues(session_id).append(queue)
        
        # 1. Replay existing conversation history
        session = await TeamOrchestrator.get_session(session_id)
        if session:
            for msg in session.get("messages", []):
                yield f"data: {json.dumps({'type': 'message', 'payload': msg})}\n\n"
            yield f"data: {json.dumps({'type': 'status', 'payload': session.get('status', 'pending')})}\n\n"
            
        # 2. Yield events as they are broadcasted
        try:
            while True:
                event = await queue.get()
                yield f"data: {json.dumps(event)}\n\n"
                queue.task_done()
        except asyncio.CancelledError:
            # Clean up queue references on client disconnect
            if queue in get_sse_queues(session_id):
                get_sse_queues(session_id).remove(queue)
            logger.info("SSE client disconnected from session: %s", session_id)
            raise

    return StreamingResponse(sse_generator(), media_type="text/event-stream")

@router.post("/approve/{session_id}")
async def approve_team_session(session_id: str, background_tasks: BackgroundTasks):
    """
    Handles user clicking the "Approve" button, updating state and kicking off renderer.
    """
    session = await TeamOrchestrator.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    try:
        await TeamOrchestrator.update_status(session_id, "approved")
        
        # Add approval notification message
        approval_msg = {
            "id": "user-approved",
            "sender": "user",
            "senderName": "User",
            "avatarColor": "from-zinc-700 to-zinc-900",
            "time": "14:10",
            "text": "Art direction parameters approved. Synthesize campaign.",
        }
        await TeamOrchestrator.add_message(session_id, approval_msg)
        
        # Fire rendering pipeline as background tasks
        background_tasks.add_task(TeamOrchestrator.execute_rendering_pipeline, session_id)
        
        return {"status": "approved"}
    except Exception as e:
        logger.error("Failed to approve team session: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
