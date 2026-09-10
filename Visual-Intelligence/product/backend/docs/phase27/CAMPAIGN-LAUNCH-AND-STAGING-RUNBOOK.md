# Phase 27: Campaign Launch & Staging Runbook

## 1. Staging Workflow
1. **Channel Allocation:** Map approved assets to destination channels (`E-commerce Hero`, `Lookbook`, `Instagram`, `Press Package`).
2. **Pre-Launch Checklist Verification:**
   - All assigned assets must have valid, unexpired approval records.
   - Cryptographic lineage graph must pass SHA-256 integrity check.
   - Campaign version must match current workspace version.
3. **Execution Gate:** Operator triggers `/launch` command or clicks "Execute Launch" in UI.

## 2. Rollback & Emergency Pause
- Operators can immediately transition a campaign from `LAUNCHED` to `PAUSED` using emergency killswitch controls.
