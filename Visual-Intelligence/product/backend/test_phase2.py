import asyncio
from app.services.orra_loop import OrraLoop

async def test_orra_loop():
    print("Testing Phase 2 Cognitive Architecture (ORRA Loop)...")
    
    # Mocks
    db = None
    vision = None
    knowledge = None
    honcho = None
    
    loop = OrraLoop(db, vision, knowledge, honcho)
    
    # 1. OBSERVE
    obs_res = await loop.observe("https://image.url/saree.jpg", "user_123")
    print("OBSERVE Phase Output:", obs_res)
    assert obs_res["status"] == "verified", "Observe phase failed verification"
    
    # 2. REASON
    reason_res = await loop.reason(obs_res["attributes"], "Luxury Campaign")
    print("REASON Phase Output:", reason_res)
    assert reason_res["status"] == "pending_green_signal", "Reason phase did not block for green signal"
    
    # 3. ACT (should fail if not approved)
    try:
        await loop.act(reason_res)
        assert False, "Act phase executed without approval!"
    except ValueError as e:
        print("ACT Phase correctly blocked unapproved execution:", str(e))
        
    # Simulate User Approval
    reason_res["status"] = "approved"
    
    # 3. ACT (approved)
    act_res = await loop.act(reason_res)
    print("ACT Phase Output (Approved):", act_res)
    assert act_res["status"] == "rendering", "Act phase did not render"
    
    # 4. REMEMBER
    await loop.remember("campaign_1", {"feedback": "User loved the lighting."})
    print("REMEMBER Phase Output: Logged successfully.")
    
    print("ALL PHASE 2 TESTS PASSED GREEN.")

if __name__ == "__main__":
    asyncio.run(test_orra_loop())
