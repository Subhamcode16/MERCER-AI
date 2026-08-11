import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class OrraLoop:
    """
    The Cognitive Architecture (ORRA Loop) defined in COG-001.
    Observe -> Reason -> Remember -> Act
    """
    def __init__(self, db, vision_adapter, knowledge_adapter, honcho_adapter):
        self.db = db
        self.vision = vision_adapter
        self.knowledge = knowledge_adapter
        self.honcho = honcho_adapter

    async def observe(self, image_url: str, user_id: str) -> Dict[str, Any]:
        """
        Phase 1: OBSERVE (LAW-001 - Knowledge)
        Extracts raw visual data, applies taxonomies using Gemini Vision.
        """
        logger.info(f"ORRA OBSERVE: Processing image {image_url}")
        
        import asyncio
        dna, creative_direction, is_mock = await asyncio.to_thread(self.vision.analyze_product, image_url)
        
        return {
            "status": "verified",
            "dna": dna.model_dump() if dna else None,
            "creative_direction": creative_direction,
            "is_mock": is_mock,
        }

    async def reason(self, product_knowledge: Dict[str, Any], campaign_objective: str) -> Dict[str, Any]:
        """
        Phase 2: REASON (LAW-002, LAW-004)
        Resolves optimal composition, lighting, environment, and styling layout.
        Outputs the Creative State.
        """
        logger.info("ORRA REASON: Compiling strategy based on Intelligence Layer...")
        
        from app.models.campaign import ProductDNA
        from app.adapters.prompt_engine import PromptEngine
        import asyncio
        
        dna = ProductDNA(**product_knowledge) if product_knowledge else None
        
        # Pull competitive, experience, and market strategies from Knowledge Engine
        if dna and self.knowledge:
            context = await asyncio.to_thread(self.knowledge.retrieve_context, dna)
        else:
            context = "No specific domain knowledge retrieved from graph."

        # Generate strategy using the PromptEngine
        prompt_engine = PromptEngine()
        if dna:
            strategy = await asyncio.to_thread(prompt_engine.generate_recommendations, dna, context)
        else:
            strategy = {
                "background": {"value": "Cinematic Studio", "reason": "Default fallback."},
                "lighting": {"value": "High-Key Window Doorway", "reason": "Default fallback."},
                "pose": {"value": "Editorial Close-Up Gaze", "reason": "Default fallback."}
            }
        
        # Flatten strategy to match V3 expectations
        flat_strategy = {
            "background": strategy.get("background", {}).get("value", "Cinematic Studio"),
            "lighting": strategy.get("lighting", {}).get("value", "High-Key Window Doorway"),
            "pose": strategy.get("pose", {}).get("value", "Editorial Close-Up Gaze")
        }
        
        creative_state = {
            "product": product_knowledge,
            "objective": campaign_objective,
            "strategy": flat_strategy,
            "status": "pending_green_signal" # Requires explicit user approval
        }
        return creative_state

    async def act(self, campaign: Any) -> Dict[str, Any]:
        """
        Phase 3: ACT (LAW-005 - Autonomy)
        Executes prompt compilation and submits to rendering engine.
        """
        status = campaign.v3_creative_state.status if hasattr(campaign.v3_creative_state, "status") else campaign.v3_creative_state.get("status")
        if status not in ["approved", "rendering"]:
            raise ValueError("Creative state must be approved (Green Signal) before ACT.")
            
        logger.info(f"ORRA ACT: Compiling prompts for campaign {campaign.id}")
        
        from app.adapters.prompt_engine import PromptEngine
        import asyncio
        prompt_engine = PromptEngine()
        
        result = await asyncio.to_thread(prompt_engine.generate_campaign_assets, campaign)
        
        job_id = f"job_{datetime.utcnow().timestamp()}"
        result["job_id"] = job_id
        result["status"] = "rendering"
        return result

    async def remember(self, campaign_id: str, feedback: Dict[str, Any]) -> None:
        """
        Phase 4: REMEMBER (LAW-003 - Memory)
        Captures user overrides, updates Memory graphs.
        """
        logger.info(f"ORRA REMEMBER: Storing feedback for campaign {campaign_id}")
        # Insert feedback into honcho memory or vector DB to compound intelligence
        pass
