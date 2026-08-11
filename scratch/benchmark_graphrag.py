# scratch/benchmark_graphrag.py
# Benchmarks Flat-File RAG against the new GraphRAG KnowledgeAdapter in terms of retrieved characters and RAG accuracy.

import os
import sys
import glob

# Ensure backend path is on sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Visual-Intelligence", "product", "backend"))
sys.path.append(backend_path)

from app.models.campaign import ProductDNA, ConfidenceField
from app.adapters.knowledge_adapter import KnowledgeAdapter

# Mock the old Flat-File KnowledgeAdapter for comparison
class OldKnowledgeAdapter:
    def __init__(self, vault_path: str, ontology_path: str):
        self.vault_path = vault_path
        self.ontology_path = ontology_path

    def _read_file_safe(self, filepath: str) -> str:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            return ""

    def retrieve_context(self, dna: ProductDNA) -> str:
        material = str(dna.material.value).lower()
        technique = str(dna.weaving_technique.value).lower()
        
        context_chunks = []
        all_md_files = []
        if os.path.exists(self.vault_path):
            all_md_files.extend(glob.glob(os.path.join(self.vault_path, "*.md")))
        if os.path.exists(self.ontology_path):
            all_md_files.extend(glob.glob(os.path.join(self.ontology_path, "*.md")))
            
        for file_path in all_md_files:
            filename = os.path.basename(file_path).lower()
            if material in filename:
                content = self._read_file_safe(file_path)
                if content:
                    context_chunks.append(content)
            elif technique in filename or "handloom" in filename or "textile" in filename:
                content = self._read_file_safe(file_path)
                if content:
                    context_chunks.append(content)
            elif "interaction-ontology" in filename or "fabric-physics" in filename or "domain-fashion" in filename:
                content = self._read_file_safe(file_path)
                if content:
                    context_chunks.append(content)
                        
        return "\n\n".join(context_chunks)

def run_benchmarks():
    vault_p = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\obsidian-vault"
    ontology_p = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\knowledge\ontology"
    graph_p = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\product\backend\data\graph.json"

    old_adapter = OldKnowledgeAdapter(vault_p, ontology_p)
    new_adapter = KnowledgeAdapter(vault_path=vault_p, ontology_path=ontology_p, graph_path=graph_p)

    scenarios = [
        {
            "name": "Silk Saree with Banarasi technique",
            "dna": ProductDNA(
                material=ConfidenceField(value="Silk", confidence=1.0),
                weaving_technique=ConfidenceField(value="Banarasi", confidence=1.0),
                primary_features=ConfidenceField(value="Zari border", confidence=1.0)
            )
        },
        {
            "name": "Cotton Kurta with Ikkat technique",
            "dna": ProductDNA(
                material=ConfidenceField(value="Cotton", confidence=1.0),
                weaving_technique=ConfidenceField(value="Ikkat", confidence=1.0),
                primary_features=ConfidenceField(value="Geometric pattern", confidence=1.0)
            )
        },
        {
            "name": "Woolen Shawl with Handloom technique",
            "dna": ProductDNA(
                material=ConfidenceField(value="Wool", confidence=1.0),
                weaving_technique=ConfidenceField(value="Handloom", confidence=1.0),
                primary_features=ConfidenceField(value="Embroidery", confidence=1.0)
            )
        }
    ]

    print("# RAG Performance & Token Size Comparison Benchmarks\n")
    print("| Scenario | Flat-File Size (Chars) | GraphRAG Size (Chars) | Reduction (%) | Flat Est. Tokens | GraphRAG Est. Tokens |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- |")

    for s in scenarios:
        old_ctx = old_adapter.retrieve_context(s["dna"])
        new_ctx = new_adapter.retrieve_context(s["dna"])

        old_size = len(old_ctx)
        new_size = len(new_ctx)
        
        reduction = ((old_size - new_size) / old_size) * 100 if old_size > 0 else 0
        old_tok = int(old_size / 4)
        new_tok = int(new_size / 4)

        print(f"| {s['name']} | {old_size:,} | {new_size:,} | {reduction:.1f}% | {old_tok:,} | {new_tok:,} |")

if __name__ == "__main__":
    run_benchmarks()
