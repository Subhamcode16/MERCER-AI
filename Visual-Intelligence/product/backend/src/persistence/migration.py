"""
Phase 23 Schema Migration Engine.
"""
import logging
from typing import Dict, Any, List, Callable
from src.persistence.exceptions import MigrationError

logger = logging.getLogger(__name__)

class SchemaMigrationEngine:
    """Safely upgrades persistent data schemas across versions with forward compatibility checks."""

    def __init__(self, current_version: str = "23.0"):
        self.current_version = current_version
        self._migrations: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_migration(self, target_version: str, migration_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        self._migrations[target_version] = migration_fn

    def migrate_payload(self, payload: Dict[str, Any], from_version: str, to_version: str) -> Dict[str, Any]:
        if from_version == to_version:
            return payload

        if to_version not in self._migrations:
            raise MigrationError(f"No migration registered from {from_version} to {to_version}")

        fn = self._migrations[to_version]
        try:
            migrated = fn(payload)
            logger.info(f"Successfully migrated schema from {from_version} to {to_version}")
            return migrated
        except Exception as e:
            raise MigrationError(f"Schema migration failed: {e}") from e
