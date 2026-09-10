"""
Tests for Phase 27 Studio Command Interface and Evidence Explorer.
"""
import pytest
from src.control_plane.context import OperatorContext
from src.control_plane.models import OperatorRole
from src.campaign_studio.command_interface import StudioCommandParser, ParsedCommandType
from src.campaign_studio.evidence_explorer import EvidenceExplorer


def test_command_parser_rbac_and_invariants():
    parser = StudioCommandParser()
    
    # Non-elevated operator attempting /approve
    viewer_op = OperatorContext(operator_id="op_viewer_01", role=OperatorRole.CLIENT_VIEWER, department="Guest")
    res1 = parser.parse_and_validate("/approve asset ast_01", viewer_op, "camp_01")
    assert res1.is_authorized is False
    assert res1.status == "DENIED"
    assert "Natural Language Command ≠ Permission" in res1.message

    # Elevated operator attempting /approve
    cd_op = OperatorContext(operator_id="op_cd_01", role=OperatorRole.CREATIVE_DIRECTOR, department="Creative Direction")
    res2 = parser.parse_and_validate("/approve asset ast_01", cd_op, "camp_01")
    assert res2.is_authorized is True
    assert res2.status == "SUCCESS"


def test_evidence_explorer_cards():
    explorer = EvidenceExplorer()
    card = explorer.create_explainability_card(
        target_entity_type="DIRECTION",
        target_entity_id="dir_01",
        title="Why Monolithic Stillness Was Selected",
        rationale="Matches brand heritage of architectural silhouettes and austere minimalism.",
    )
    assert card.target_entity_id == "dir_01"
    assert len(card.evidence_items) >= 1
    assert "Intelligence ≠ Authorization" in card.invariants_validated
