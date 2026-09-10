"""
Phase 23 Persistence & Recovery Exceptions.
"""

class PersistenceError(Exception):
    """Base exception for persistence and storage errors."""
    pass

class TransactionConflictError(PersistenceError):
    """Raised when an atomic transaction detects a concurrent modification conflict."""
    pass

class CorruptedStateError(PersistenceError):
    """Raised when persistent state fails integrity checksum or schema verification."""
    pass

class LineageBreakError(PersistenceError):
    """Raised when an artifact or ledger record breaks cryptographic hash chaining."""
    pass

class CheckpointNotFoundError(PersistenceError):
    """Raised when requested checkpoint ID cannot be resolved."""
    pass

class BackupIntegrityError(PersistenceError):
    """Raised when a backup archive fails verification or contains illegal secrets."""
    pass

class MigrationError(PersistenceError):
    """Raised when schema migration encounters incompatible delta or failure."""
    pass
