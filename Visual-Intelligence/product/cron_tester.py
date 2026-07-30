import requests
import time
import sys

API_URL = "http://localhost:8000/api/campaigns"

def test_api():
    print("--- Starting Campaign API Tests ---")
    
    # 1. List Campaigns
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        print("[SUCCESS] GET /api/campaigns")
    except Exception as e:
        print(f"[FAIL] GET /api/campaigns: {e}")
        return False

    # 2. Create Campaign
    campaign_id = None
    try:
        res = requests.post(API_URL, json={"name": "Cron Test Campaign"})
        res.raise_for_status()
        data = res.json()
        campaign_id = data.get("id")
        print(f"[SUCCESS] POST /api/campaigns (Created ID: {campaign_id})")
    except Exception as e:
        print(f"[FAIL] POST /api/campaigns: {e}")
        return False

    if not campaign_id:
        return False

    # 3. Get Campaign
    try:
        res = requests.get(f"{API_URL}/{campaign_id}")
        res.raise_for_status()
        print(f"[SUCCESS] GET /api/campaigns/{campaign_id}")
    except Exception as e:
        print(f"[FAIL] GET /api/campaigns/{campaign_id}: {e}")
    
    print("--- Tests Completed Successfully ---")
    return True

if __name__ == "__main__":
    success = test_api()
    if not success:
        sys.exit(1)
