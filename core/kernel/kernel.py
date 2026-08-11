"""
GeoShield Core Kernel

Main orchestration layer for GeoShield intelligence pipelines.
"""

from __future__ import annotations

from typing import Any

from backend.disaster.fire_engine import FireIntelligenceEngine


class GeoShieldKernel:
    """
    Main GeoShield orchestration kernel.

    The kernel coordinates high-level intelligence pipelines
    while individual engines remain responsible for their
    specialized processing.
    """

    def __init__(self) -> None:
        """Initialize the GeoShield kernel."""

        self.fire_engine = FireIntelligenceEngine()

    def run_fire_pipeline(self, filepath: str) -> list[dict[str, Any]]:
        """
        Run the GeoShield fire-intelligence pipeline.

        Args:
            filepath: Path to the fire-events CSV file.

        Returns:
            A list of enriched fire intelligence records.
        """

        print("===================================")
        print(" GEO SHIELD KERNEL STARTED")
        print("===================================")

        fires = self.fire_engine.analyse(filepath)

        print(f"Processed {len(fires)} fire events.")

        return fires