"""
GeoShield Fire Intelligence Engine

Processes fire events through spatial enrichment,
risk assessment, and decision intelligence.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.connectors.firms_connector import FIRMSConnector
from backend.spatial.data_manager import GeoDataManager

from core.decision_engine import DecisionEngine
from core.event_enrichment import EventEnrichmentEngine
from core.risk_engine import RiskEngine


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class FireIntelligenceEngine:
    """
    Main fire intelligence processing engine.
    """

    def __init__(self) -> None:
        """Initialize the fire intelligence pipeline."""

        self.connector = FIRMSConnector()

        self.data_manager = GeoDataManager()

        counties_path = (
            PROJECT_ROOT
            / "data"
            / "boundaries"
            / "Kenya_county.shp"
        )

        roads_path = (
            PROJECT_ROOT
            / "data"
            / "roads"
            / "ken_roads.shp"
        )

        self.data_manager.load_layer(
            "counties",
            str(counties_path),
        )

        self.data_manager.load_layer(
            "roads",
            str(roads_path),
        )

        self.enrichment = EventEnrichmentEngine(
            self.data_manager
        )

        self.risk = RiskEngine()
        self.decision = DecisionEngine()

    def analyse(
        self,
        filepath: str,
    ) -> list[dict[str, Any]]:
        """
        Analyze fire events from a CSV dataset.

        Args:
            filepath: Path to the fire-events CSV.

        Returns:
            Enriched fire intelligence records.
        """

        fire_path = Path(filepath)

        if not fire_path.is_absolute():
            fire_path = PROJECT_ROOT / fire_path

        if not fire_path.exists():
            raise FileNotFoundError(
                f"Fire dataset not found: {fire_path}"
            )

        self.connector.load_csv(str(fire_path))

        enriched: list[dict[str, Any]] = []

        for fire in self.connector.get_disasters():
            location = self.enrichment.enrich(
                fire["longitude"],
                fire["latitude"],
            )

            risk = self.risk.calculate_fire_risk(
                fire
            )

            decision = self.decision.recommend(
                risk
            )

            enriched.append(
                {
                    **fire,
                    **location,
                    **risk,
                    **decision,
                }
            )

        return enriched