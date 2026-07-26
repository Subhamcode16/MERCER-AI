import os
import glob
from typing import List, Dict
from app.models.campaign import ProductDNA

class KnowledgeAdapter:
    """
    Retrieves static domain knowledge from the Obsidian vault based on extracted ProductDNA.
    This acts as the static RAG layer for the Prompt Engine.
    """

    def __init__(self, vault_path: str = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\obsidian-vault", ontology_path: str = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\knowledge\ontology"):
        self.vault_path = vault_path
        self.ontology_path = ontology_path

    def _read_file_safe(self, filepath: str) -> str:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"[KnowledgeAdapter] Failed to read {filepath}: {e}")
            return ""

    def retrieve_context(self, dna: ProductDNA) -> str:
        """
        Gathers relevant markdown files based on the material and weaving technique.
        Returns a concatenated string of the relevant knowledge chunks.
        """
        if not os.path.exists(self.vault_path):
            print(f"[KnowledgeAdapter] Vault not found at {self.vault_path}")
            return "No domain knowledge available."

        context_chunks = []
        
        material = str(dna.material.value).lower()
        technique = str(dna.weaving_technique.value).lower()
        
        all_md_files = []
        if os.path.exists(self.vault_path):
            all_md_files.extend(glob.glob(os.path.join(self.vault_path, "*.md")))
        if os.path.exists(self.ontology_path):
            all_md_files.extend(glob.glob(os.path.join(self.ontology_path, "*.md")))
            
        for file_path in all_md_files:
            filename = os.path.basename(file_path).lower()
            
            # Check for material matches (e.g., Silk.md, Cotton.md)
            if material in filename:
                print(f"[KnowledgeAdapter] Found material match: {filename}")
                content = self._read_file_safe(file_path)
                if content:
                    context_chunks.append(f"--- KNOWLEDGE SOURCE: {os.path.basename(file_path)} ---\n{content}")
                    
            # Check for technique/cultural matches
            elif technique in filename or "handloom" in filename or "textile" in filename:
                print(f"[KnowledgeAdapter] Found technique/context match: {filename}")
                content = self._read_file_safe(file_path)
                if content:
                    context_chunks.append(f"--- KNOWLEDGE SOURCE: {os.path.basename(file_path)} ---\n{content}")
            
            # Specifically pull in the Interaction Ontology and Fabric Physics Database for physics constraints (RES-009)
            elif "interaction-ontology" in filename or "fabric-physics" in filename or "domain-fashion" in filename:
                 print(f"[KnowledgeAdapter] Found core constraint ontology match: {filename}")
                 content = self._read_file_safe(file_path)
                 if content:
                     context_chunks.append(f"--- ONTOLOGY SOURCE: {os.path.basename(file_path)} ---\n{content}")
                        
        if not context_chunks:
            return "No specific domain knowledge found for these attributes."
            
        # Optional: truncate if context is too large, but for now we append them all.
        return "\n\n".join(context_chunks)
