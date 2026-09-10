"""
Outcome ingestion package for Phase 28 Creative Intelligence Operating Loop.
"""
from .ingestion_pipeline import (
    RawOutcomeFeed,
    OutcomeIngestionPipeline,
)

__all__ = [
    "RawOutcomeFeed",
    "OutcomeIngestionPipeline",
]
