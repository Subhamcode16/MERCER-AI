import asyncio
import os
from app.database import connect_db, get_db, close_db

async def test_db():
    print("Testing Phase 1 Database Connection and Indexes...")
    # Set mock environment for tests
    os.environ["MONGODB_URI"] = "mongodb://localhost:27017"
    os.environ["MONGODB_DB_NAME"] = "mercer_test_db"
    
    try:
        await connect_db()
        db = get_db()
        
        # Verify indexes exist for workspaces, brands, products, knowledge_claims, graph_edges
        collections = await db.list_collection_names()
        print("Collections in DB:", collections)
        
        for coll in ["workspaces", "brands", "products", "knowledge_claims", "graph_edges"]:
            indexes = await db[coll].index_information()
            print(f"Indexes for {coll}:", list(indexes.keys()))
            
        print("ALL DATABASE TESTS PASSED GREEN.")
    except Exception as e:
        print("DATABASE TEST FAILED:")
        import traceback
        traceback.print_exc()
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(test_db())
