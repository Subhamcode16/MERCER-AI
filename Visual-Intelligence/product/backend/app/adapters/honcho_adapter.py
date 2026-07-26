import os
import json
from typing import List, Dict
from datetime import datetime

class HonchoAdapter:
    """
    Adapter for Honcho Dialectic Memory.
    For this MVP, it mocks the Honcho backend by writing to a local JSON file.
    In production, this will use the official honcho-sdk to connect to the Honcho cloud.
    """

    def __init__(self, data_dir: str = "data"):
        self.memory_file = os.path.join(data_dir, "honcho_memory.json")
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as f:
                json.dump({"conclusions": []}, f)

    def conclude(self, conclusion: str, peer: str = "user") -> None:
        """
        Equivalent to `honcho_conclude`. Writes a permanent, actionable conclusion.
        Called when the user corrects the AI or provides new brand guidelines.
        """
        print(f"[HonchoAdapter] Saving conclusion for peer '{peer}': {conclusion}")
        
        with open(self.memory_file, "r") as f:
            data = json.load(f)
            
        data["conclusions"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "peer": peer,
            "content": conclusion
        })
        
        with open(self.memory_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_context(self, peer: str = "user") -> str:
        """
        Equivalent to `honcho_context`. Fetches the unified User Representation.
        Returns a synthesized string of past conclusions to prime the LLM.
        """
        with open(self.memory_file, "r") as f:
            data = json.load(f)
            
        peer_conclusions = [c["content"] for c in data.get("conclusions", []) if c["peer"] == peer]
        
        if not peer_conclusions:
            return "No prior user memory available."
            
        return "\n".join([f"- {c}" for c in peer_conclusions])
