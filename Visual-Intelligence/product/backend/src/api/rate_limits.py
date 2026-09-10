"""
Phase 25 API Rate Limiting Configuration.
"""
from typing import Dict, Any

RATE_LIMIT_POLICIES: Dict[str, str] = {
    "dashboard_snapshot": "60/minute",
    "approval_action": "20/minute",
    "campaign_action": "30/minute",
    "evidence_query": "100/minute",
    "event_stream": "10/minute"
}
