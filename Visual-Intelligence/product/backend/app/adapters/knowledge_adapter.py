import os
import glob
from typing import List, Dict
from app.models.campaign import ProductDNA

import os
import json
import glob
from typing import List, Dict, Set
from app.models.campaign import ProductDNA

class KnowledgeAdapter:
    """
    Retrieves static domain knowledge using a GraphRAG approach over the compiled graph.json.
    Traverses Louvain communities and 1-hop connections to load precise context nodes.
    """

    def __init__(self, 
                 vault_path: str = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\obsidian-vault", 
                 ontology_path: str = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\knowledge\ontology",
                 graph_path: str = None):
        self.vault_path = vault_path
        self.ontology_path = ontology_path
        
        # Determine graph path with standard fallback locations
        if graph_path:
            self.graph_path = graph_path
        else:
            # Check relative to backend directory first
            rel_path = os.path.join("data", "graph.json")
            if os.path.exists(rel_path):
                self.graph_path = rel_path
            else:
                self.graph_path = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\product\backend\data\graph.json"

        self.graph_data = self._load_graph()

    def _load_graph(self) -> Dict:
        """Loads the compiled knowledge graph from disk."""
        if not os.path.exists(self.graph_path):
            print(f"[KnowledgeAdapter] Graph not found at {self.graph_path}. Falling back to empty graph.")
            return {"nodes": [], "links": []}
        try:
            with open(self.graph_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"[KnowledgeAdapter] Loaded graph with {len(data.get('nodes', []))} nodes and {len(data.get('links', []))} links.")
                return data
        except Exception as e:
            print(f"[KnowledgeAdapter] Failed to load graph: {e}")
            return {"nodes": [], "links": []}

    def _read_file_safe(self, filepath: str) -> str:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"[KnowledgeAdapter] Failed to read {filepath}: {e}")
            return ""

    def _resolve_junction_path(self, rel_path: str) -> str:
        """Maps relative paths stored in graphify (e.g. 'obsidian-vault/Silk.md') to absolute disk paths."""
        parts = rel_path.replace("\\", "/").split("/", 1)
        if len(parts) < 2:
            return ""
        junction_name, sub_path = parts[0], parts[1]
        
        mapping = {
            "obsidian-vault": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\obsidian-vault",
            "Cognitive Architecture": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Cognitive Architecture",
            "System Architecture": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\System Architecture",
            "System Laws": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\System Laws",
            "System Specs": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\System Specs",
            "Intelligence Layer": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Intelligence Layer",
            "Glossary trilogy": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Glossary trilogy",
            "Knowledge engine expansion": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Knowledge engine expansion",
            "Ontology": r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\knowledge\ontology"
        }
        
        base_dir = mapping.get(junction_name)
        if base_dir and os.path.exists(base_dir):
            return os.path.join(base_dir, sub_path)
        return ""

    def retrieve_context(self, dna: ProductDNA) -> str:
        """
        Gathers relevant markdown files using GraphRAG traversals (Louvain expansion + 1-hop).
        Keeps token sizes minimal by selecting matching community partitions.
        """
        nodes = self.graph_data.get("nodes", [])
        links = self.graph_data.get("links", [])

        if not nodes:
            print("[KnowledgeAdapter] No graph nodes available. Falling back to flat-file scanner.")
            return self._fallback_flat_retrieve(dna)

        # 1. Collect search terms from DNA attributes
        search_terms = set()
        if dna.material:
            search_terms.add(str(dna.material.value).lower())
        if dna.weaving_technique:
            search_terms.add(str(dna.weaving_technique.value).lower())
        if hasattr(dna, "product_domain") and dna.product_domain:
            search_terms.add(str(dna.product_domain.value).lower())

        # 2. Step A: Find direct matching nodes
        direct_node_ids = set()
        matched_communities = set()
        
        for node in nodes:
            node_id = node.get("id", "").lower()
            label = node.get("label", "").lower()
            norm_label = node.get("norm_label", "").lower()
            source_file = node.get("source_file", "").lower()
            
            # Check if any search term is contained in node metadata
            for term in search_terms:
                if term in node_id or term in label or term in norm_label or term in source_file:
                    direct_node_ids.add(node.get("id"))
                    comm = node.get("community")
                    if comm is not None:
                        matched_communities.add(comm)

        # 3. Step B: Perform Louvain Community Expansion
        community_node_ids = set()
        if matched_communities:
            for node in nodes:
                comm = node.get("community")
                if comm in matched_communities:
                    community_node_ids.add(node.get("id"))

        # 4. Step C: Find 1-Hop Neighbor nodes
        neighbor_node_ids = set()
        for link in links:
            source = link.get("source")
            target = link.get("target")
            if source in direct_node_ids:
                neighbor_node_ids.add(target)
            if target in direct_node_ids:
                neighbor_node_ids.add(source)

        # 5. Resolve relative path files for direct matches, neighbors, and communities
        # Prioritize files: Direct matches first, then neighbors, then community nodes
        file_priorities: Dict[str, str] = {}  # maps rel_path -> priority_class
        
        # Resolve helper
        def add_nodes_to_list(node_ids: Set[str], priority_class: str):
            for n_id in node_ids:
                node = next((n for n in nodes if n.get("id") == n_id), None)
                if node:
                    rel_path = node.get("source_file")
                    if rel_path and rel_path.endswith(".md"):
                        # Keep the highest priority if duplicate
                        if rel_path not in file_priorities:
                            file_priorities[rel_path] = priority_class
                        elif priority_class == "direct":
                            file_priorities[rel_path] = "direct"
                        elif priority_class == "neighbor" and file_priorities[rel_path] == "community":
                            file_priorities[rel_path] = "neighbor"

        add_nodes_to_list(direct_node_ids, "direct")
        add_nodes_to_list(neighbor_node_ids, "neighbor")
        add_nodes_to_list(community_node_ids, "community")

        # Sort files: direct first, neighbors second, community third
        sorted_files = []
        for rel_path, prio in file_priorities.items():
            sorted_files.append((rel_path, prio))
        
        # Custom sorting logic
        def prio_val(item):
            prio = item[1]
            if prio == "direct": return 1
            if prio == "neighbor": return 2
            return 3
            
        sorted_files.sort(key=prio_val)

        # 6. Read and assemble content up to a target token/size budget (e.g. 8 files max)
        context_chunks = []
        used_files = set()
        
        # Always guarantee core ontology files are present
        core_ontologies = ["interaction-ontology.md", "fabric-physics.md", "domain-fashion.md"]
        core_files_to_add = []
        
        for core in core_ontologies:
            # Look up if these files exist in ontology path
            path = os.path.join(self.ontology_path, core)
            if os.path.exists(path):
                core_files_to_add.append(path)

        # Process the prioritized GraphRAG list
        # Limit community expansion documents to avoid token bloat
        direct_and_neighbor_count = sum(1 for f, p in sorted_files if p in ("direct", "neighbor"))
        max_community_files = max(2, 6 - direct_and_neighbor_count)
        
        community_added = 0
        for rel_path, prio in sorted_files:
            if len(context_chunks) >= 8:
                break
                
            if prio == "community":
                if community_added >= max_community_files:
                    continue
                community_added += 1

            abs_path = self._resolve_junction_path(rel_path)
            if abs_path and os.path.exists(abs_path):
                filename = os.path.basename(abs_path).lower()
                used_files.add(filename)
                content = self._read_file_safe(abs_path)
                if content:
                    context_chunks.append(f"--- GRAPH SOURCE [{prio.upper()}]: {os.path.basename(abs_path)} ---\n{content}")

        # Ensure core constraint ontologies are appended if not already gathered
        for path in core_files_to_add:
            filename = os.path.basename(path).lower()
            if filename not in used_files:
                content = self._read_file_safe(path)
                if content:
                    context_chunks.append(f"--- CORE ONTOLOGY: {os.path.basename(path)} ---\n{content}")

        if not context_chunks:
            return "No specific domain knowledge retrieved from graph."

        return "\n\n".join(context_chunks)

    def _fallback_flat_retrieve(self, dna: ProductDNA) -> str:
        """Fallback flat-file retrieval if graph loading fails entirely."""
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
            if material in filename or technique in filename or "handloom" in filename or "textile" in filename:
                content = self._read_file_safe(file_path)
                if content:
                    context_chunks.append(f"--- KNOWLEDGE SOURCE: {os.path.basename(file_path)} ---\n{content}")
            elif "interaction-ontology" in filename or "fabric-physics" in filename or "domain-fashion" in filename:
                content = self._read_file_safe(file_path)
                if content:
                    context_chunks.append(f"--- ONTOLOGY SOURCE: {os.path.basename(file_path)} ---\n{content}")
                        
        if not context_chunks:
            return "No specific domain knowledge found."
            
        return "\n\n".join(context_chunks)

