import asyncio
from app.models.core_models import Workspace, Brand, Product, KnowledgeClaim, GraphEdge

async def test_models():
    print("Testing Phase 1 Models...")
    
    workspace = Workspace(name="Acme Corp", owner_id="user_123")
    print(f"Created Workspace: {workspace.id} - {workspace.name}")
    
    brand = Brand(workspace_id=workspace.id, name="Acme Luxury")
    print(f"Created Brand: {brand.id} - {brand.name}")
    
    product = Product(brand_id=brand.id, name="Silk Saree", domain="Human Expression")
    print(f"Created Product: {product.id} - {product.name}")
    
    kc = KnowledgeClaim(
        subject=product.id,
        predicate="has_material",
        object_value="Silk",
        evidence="Visual extraction confidence 98%",
        source="Gemini Vision v3.1",
        confidence=0.98,
        context="studio lighting"
    )
    print(f"Created KnowledgeClaim: {kc.id} | {kc.subject} {kc.predicate} {kc.object_value}")
    
    edge = GraphEdge(source_id=product.id, target_id=brand.id, edge_type="OWNED_BY")
    print(f"Created Edge: {edge.source_id} -> {edge.edge_type} -> {edge.target_id}")

    print("ALL PHASE 1 TESTS PASSED GREEN.")

if __name__ == "__main__":
    asyncio.run(test_models())
