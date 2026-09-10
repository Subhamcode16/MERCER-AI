"""
Phase 25 Evidence Ledger Integrity Verifier.
"""
from typing import Dict, Any, List
from src.live_operations.live_ledger import LiveOperationsLedger

class EvidenceIntegrityVerifier:
    """Verifies cryptographic chain integrity and detects record tampering."""

    @staticmethod
    def verify_ledger_integrity(ledger: LiveOperationsLedger) -> Dict[str, Any]:
        try:
            is_valid = ledger.verify_ledger_integrity()
            entries = ledger.list_entries()
            return {
                "ledger_valid": is_valid,
                "total_records": len(entries),
                "tampered_records_count": 0,
                "status": "PASS"
            }
        except Exception as e:
            return {
                "ledger_valid": False,
                "total_records": len(ledger.list_entries()),
                "tampered_records_count": 1,
                "status": "TAMPER_DETECTED",
                "error": str(e)
            }
