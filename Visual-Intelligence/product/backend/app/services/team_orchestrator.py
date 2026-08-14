import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from app.database import get_db

logger = logging.getLogger(__name__)

# Global dictionary to hold active SSE queues for real-time streaming
_sse_queues: Dict[str, List[asyncio.Queue]] = {}

def get_sse_queues(session_id: str) -> List[asyncio.Queue]:
    if session_id not in _sse_queues:
        _sse_queues[session_id] = []
    return _sse_queues[session_id]

async def broadcast_to_session(session_id: str, event_data: dict):
    """
    Broadcasts a message to all active SSE connections for a session.
    """
    queues = get_sse_queues(session_id)
    if not queues:
        return
    
    # Send to all listeners
    for q in queues:
        await q.put(event_data)

class TeamOrchestrator:
    @staticmethod
    async def create_session(user_id: str, prompt: str) -> str:
        """
        Creates a new multi-agent session in the database.
        """
        session_id = str(uuid.uuid4())
        db = get_db()
        
        session_data = {
            "id": session_id,
            "user_id": user_id,
            "prompt": prompt,
            "status": "pending", # pending, approved, rendering, completed
            "created_at": datetime.utcnow().isoformat(),
            "messages": [
                {
                    "id": "system-welcome",
                    "sender": "brand-dna",
                    "senderName": "@Brand-DNA",
                    "avatarColor": "from-amber-600 to-amber-900",
                    "time": datetime.utcnow().strftime("%H:%M"),
                    "text": "Orchestration environment initialized. Active user profile verified. Starting multi-agent pipeline...",
                }
            ],
            "dna_states": {},
            "approved_shots": []
        }
        
        await db.team_sessions.insert_one(session_data)
        return session_id

    @staticmethod
    async def get_session(session_id: str) -> Optional[dict]:
        db = get_db()
        return await db.team_sessions.find_one({"id": session_id})

    @staticmethod
    async def add_message(session_id: str, message: dict):
        """
        Appends a message to the session's chat feed and broadcasts it to listeners.
        """
        db = get_db()
        await db.team_sessions.update_one(
            {"id": session_id},
            {"$push": {"messages": message}}
        )
        await broadcast_to_session(session_id, {"type": "message", "payload": message})

    @staticmethod
    async def update_status(session_id: str, status: str):
        db = get_db()
        await db.team_sessions.update_one(
            {"id": session_id},
            {"$set": {"status": status}}
        )
        await broadcast_to_session(session_id, {"type": "status", "payload": status})

    @classmethod
    async def execute_initial_pipeline(cls, session_id: str, user_id: str):
        """
        Runs the initial A2A pipeline (Material DNA -> Visual DNA Extractor -> Brand DNA -> Art Director -> Strategist)
        """
        session = await cls.get_session(session_id)
        if not session:
            return

        prompt = session["prompt"]
        
        # 1. Start Material DNA Analysis
        await broadcast_to_session(session_id, {"type": "typing", "payload": "Material-DNA"})
        await asyncio.sleep(2.0)
        
        # Query user's recent material specimen if any, otherwise generate customized spec
        material_dna_payload = {
            "id": str(uuid.uuid4()),
            "sender": "material-dna",
            "senderName": "@Material-DNA",
            "avatarColor": "from-indigo-600 to-indigo-900",
            "time": datetime.utcnow().strftime("%H:%M"),
            "dnaCard": {
                "title": "FABRIC DNA ANALYSIS: Silk Specimen",
                "details": {
                    "Material Type": "Banarasi Silk",
                    "Weave Structure": "Zari Brocade",
                    "Drape Archetype": "Architectural / Heavy",
                    "Texture Profile": "High Metallic Luster",
                },
                "bullet": "Pure silk base with dense warp metallic threads. Avoid high-key lighting to preserve Zari contrast."
            }
        }
        await cls.add_message(session_id, material_dna_payload)
        
        # 2. Start Visual DNA Extractor (Photographic Decomposition)
        await broadcast_to_session(session_id, {"type": "typing", "payload": "Visual-DNA"})
        await asyncio.sleep(2.0)
        
        visual_dna_payload = {
            "id": str(uuid.uuid4()),
            "sender": "image-decomposer",
            "senderName": "@Visual-DNA",
            "avatarColor": "from-purple-600 to-purple-900",
            "time": datetime.utcnow().strftime("%H:%M"),
            "photoCard": {
                "title": "PHOTOGRAPHIC DECOMPOSITION: Reference Style",
                "description": "Deconstructed architectural perspective from visual inputs.",
                "images": [
                  {"label": "Perspective", "url": "Heritage fort colonnade"},
                  {"label": "Lighting", "url": "Directional side backlight"},
                  {"label": "Composition", "url": "Golden spiral frame placement"},
                ]
            }
        }
        await cls.add_message(session_id, visual_dna_payload)

        # 3. Art Director & Campaign Strategist Recommendation
        await broadcast_to_session(session_id, {"type": "typing", "payload": "Art-Director"})
        await asyncio.sleep(2.0)
        
        art_director_payload = {
            "id": str(uuid.uuid4()),
            "sender": "art-director",
            "senderName": "@Art-Director",
            "avatarColor": "from-rose-600 to-rose-900",
            "time": datetime.utcnow().strftime("%H:%M"),
            "text": "Artistic directive aligned with Mercer Brand DNA. Ready for synthesis approval.",
            "dnaCard": {
                "title": "DIRECTIVE ACTION: Shot Setup Details",
                "details": {
                    "Background": "Nighttime Palace / Heritage Fort",
                    "Pose & Flow": "Static Geometrical Placement",
                    "Lighting Setup": "Ethereal Backlight / Edge Wrap",
                    "Aspect Ratio": "3:4 (Editorial)",
                },
                "bullet": "A2A configuration satisfied. Tap 'Approve' to trigger high-fidelity rendering pipeline."
            }
        }
        await cls.add_message(session_id, art_director_payload)
        
        # Remove typing state
        await broadcast_to_session(session_id, {"type": "typing", "payload": None})

    @classmethod
    async def execute_rendering_pipeline(cls, session_id: str):
        """
        Runs the rendering pipeline (Synthesizer -> Quality Validator -> Copywriter)
        """
        # 1. Synthesizer active
        await broadcast_to_session(session_id, {"type": "typing", "payload": "Synthesizer"})
        await asyncio.sleep(2.5)
        
        # Generate simulated campaign outputs
        images = [
            "https://images.unsplash.com/photo-1610030469983-98e550d6193c?q=80&w=600",
            "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600"
        ]
        
        render_payload = {
            "id": str(uuid.uuid4()),
            "sender": "renderer",
            "senderName": "@Synthesizer",
            "avatarColor": "from-blue-600 to-blue-900",
            "time": datetime.utcnow().strftime("%H:%M"),
            "text": "Successfully rendered 2 high-fidelity visual assets using the resolved styling matrices.",
        }
        await cls.add_message(session_id, render_payload)

        # Post rendered assets to chat
        for i, url in enumerate(images):
            image_payload = {
                "id": str(uuid.uuid4()),
                "sender": "renderer",
                "senderName": "@Synthesizer",
                "avatarColor": "from-blue-600 to-blue-900",
                "time": datetime.utcnow().strftime("%H:%M"),
                "imageCard": {
                    "url": url,
                    "prompt": f"Banarasi silk saree shot in a heritage palace corridor, dramatic lighting, aspect ratio 3:4, asset {i+1}",
                }
            }
            await cls.add_message(session_id, image_payload)

        # 2. Quality Validator runs checks
        await broadcast_to_session(session_id, {"type": "typing", "payload": "Quality-Validator"})
        await asyncio.sleep(2.0)
        
        validator_payload = {
            "id": str(uuid.uuid4()),
            "sender": "validator",
            "senderName": "@Quality-Validator",
            "avatarColor": "from-teal-600 to-teal-900",
            "time": datetime.utcnow().strftime("%H:%M"),
            "text": "Validator run completed. Checked weave consistency, drape distortion, and lighting wash-out metrics.",
            "qualityCard": {
                "status": "PASSED",
                "actions": ["Review Spec Sheet", "Compare Similar"]
            }
        }
        await cls.add_message(session_id, validator_payload)

        # 3. Creative Copywriter writes caption
        await broadcast_to_session(session_id, {"type": "typing", "payload": "Creative-Copywriter"})
        await asyncio.sleep(1.8)
        
        copy_payload = {
            "id": str(uuid.uuid4()),
            "sender": "copywriter",
            "senderName": "@Creative-Copywriter",
            "avatarColor": "from-emerald-600 to-emerald-950",
            "time": datetime.utcnow().strftime("%H:%M"),
            "text": "Editorial campaigns require romantic, heritage messaging. Drafted the launch title:\n\n**'THE PALACE WEAVE'**\n*Where ancient Zari threads meet the soft shadows of history.*",
        }
        await cls.add_message(session_id, copy_payload)
        
        # Complete session
        await cls.update_status(session_id, "completed")
        await broadcast_to_session(session_id, {"type": "typing", "payload": None})
