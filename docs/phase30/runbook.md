# Phase 30: Operational Runbook

## Verification & Execution

### Running the Test Suite
```powershell
cd "c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\Visual-Intelligence\product\backend"
.venv\Scripts\python.exe run_phase30_tests.py
```

### Integration with FastAPI
The Phase 30 router is mounted at `/institutional-intelligence` and can be included in `app/main.py` or consumed standalone:

```python
from src.institutional_intelligence.api.routes import router as institutional_router

app.include_router(institutional_router)
```

### Routine Cadence Executions
- **Daily Preparation**: Invoked via scheduled task to ingest signals and summarize changes without executing initiatives.
- **Weekly Review**: Generates Strategic Brief for human leadership review.
- **Drift Escalations**: Any detected drift above severity 0.7 triggers high-priority items in the Intelligence Attention Queue.
