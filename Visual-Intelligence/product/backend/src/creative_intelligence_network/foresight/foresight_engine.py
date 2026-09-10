"""
Foresight & Scenario Engine for generating bounded scenarios without collapsing into false deterministic forecasts.
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional
import hashlib
from .scenario_types import StrategicScenario, ScenarioArchetype
from ..graph.models import IntelligenceClassification, GraphEntity, GraphRelationship, EntityType, RelationType
from ..graph.intelligence_graph import OrganizationalIntelligenceGraph


class ForesightEngine:
    def __init__(self, graph: Optional[OrganizationalIntelligenceGraph] = None):
        self.graph = graph or OrganizationalIntelligenceGraph()
        self._scenarios: Dict[str, StrategicScenario] = {}

    def construct_scenario_matrix(
        self,
        tenant_id: str,
        scope: str,
        topic: str,
        initiating_signals: List[str],
        base_assumptions: List[str],
        supporting_evidence: Optional[List[str]] = None,
        contradictory_evidence: Optional[List[str]] = None,
        classification: IntelligenceClassification = IntelligenceClassification.CLIENT_PRIVATE,
    ) -> Dict[ScenarioArchetype, StrategicScenario]:
        """
        Constructs the mandatory 5-Scenario Matrix: BASELINE, UPSIDE, DOWNSIDE, DISRUPTION, and UNKNOWN.
        """
        supp = supporting_evidence or []
        count = contradictory_evidence or []
        matrix = {}

        archetypes = [
            (
                ScenarioArchetype.BASELINE,
                f"Baseline Progression: {topic}",
                "Current trends and historical performance metrics persist with standard market variance.",
                0.40,
                0.20,
                ["Stable CPM", "Historical CTR retention"],
                ["Steady customer lifetime value"],
            ),
            (
                ScenarioArchetype.UPSIDE,
                f"Upside Accelerated Growth: {topic}",
                "Key visual innovations and new channel dynamics produce upper-quartile lift.",
                0.25,
                0.45,
                ["Early surge in engagement velocity", "Lower initial CAC"],
                ["Sustained ROAS > 3.0"],
            ),
            (
                ScenarioArchetype.DOWNSIDE,
                f"Downside Creative Fatigue: {topic}",
                "Rapid consumer habituation and ad-platform algorithmic shifts cause conversion decay.",
                0.20,
                0.40,
                ["Declining view-through rate", "Rising CPM rates"],
                ["Drop in ROAS < 1.2"],
            ),
            (
                ScenarioArchetype.DISRUPTION,
                f"Market Disruption Shock: {topic}",
                "Competitor pivot or platform policy update fundamentally alters conversion topology.",
                0.10,
                0.70,
                ["Sudden shift in platform ad formats", "New viral competitor creative"],
                ["Structural conversion drop"],
            ),
            (
                ScenarioArchetype.UNKNOWN,
                f"Unobserved Counterfactual State: {topic}",
                "Uncertainty remains materially unresolvable without targeted experimental intervention.",
                0.05,
                0.95,
                ["Conflicting signal indicators", "Insufficient baseline samples"],
                ["Indeterminate payoff"],
            ),
        ]

        for arch, title, desc, likelihood, uncert, leading, lagging in archetypes:
            scenario_id = f"SCE-{hashlib.sha256(f'{tenant_id}:{scope}:{arch.value}:{datetime.now(timezone.utc).isoformat()}'.encode()).hexdigest()[:12]}"

            scenario = StrategicScenario(
                scenario_id=scenario_id,
                tenant_id=tenant_id,
                classification=classification,
                archetype=arch,
                title=title,
                description=desc,
                scope=scope,
                initiating_signals=initiating_signals,
                assumptions=base_assumptions,
                supporting_evidence=supp,
                contradictory_evidence=count,
                bounded_likelihood=likelihood,
                uncertainty_score=uncert,
                leading_indicators=leading,
                lagging_indicators=lagging,
                potential_consequences=[f"Outcome profile under {arch.value}"],
                monitoring_actions=[f"Track {leading[0]}"],
            )

            self._scenarios[scenario_id] = scenario
            matrix[arch] = scenario

            # Sync with Graph
            entity = GraphEntity(
                entity_id=scenario_id,
                entity_type=EntityType.SCENARIO,
                tenant_id=tenant_id,
                classification=classification,
                name=title,
                properties={
                    "archetype": arch.value,
                    "likelihood": likelihood,
                    "uncertainty": uncert,
                    "scope": scope,
                },
            )
            self.graph.add_entity(entity)

            # Link initiating signals
            for sig_id in initiating_signals:
                if self.graph.get_entity(sig_id):
                    self.graph.add_relationship(
                        GraphRelationship(
                            relationship_id=f"REL-{sig_id}-{scenario_id}",
                            source_id=sig_id,
                            target_id=scenario_id,
                            relation_type=RelationType.INFORMS,
                            tenant_id=tenant_id,
                            classification=classification,
                            scope=scope,
                        )
                    )

        return matrix

    def get_scenario(self, scenario_id: str, tenant_id: Optional[str] = None) -> Optional[StrategicScenario]:
        sce = self._scenarios.get(scenario_id)
        if not sce:
            return None
        if tenant_id and sce.classification == IntelligenceClassification.CLIENT_PRIVATE:
            if sce.tenant_id != tenant_id:
                return None
        return sce

    def list_scenarios(self, tenant_id: str, archetype: Optional[ScenarioArchetype] = None) -> List[StrategicScenario]:
        return [
            s for s in self._scenarios.values()
            if (s.tenant_id == tenant_id or s.classification != IntelligenceClassification.CLIENT_PRIVATE)
            and (archetype is None or s.archetype == archetype)
            and s.is_active
        ]
