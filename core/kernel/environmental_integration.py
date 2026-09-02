"""
GeoShield Environmental Integration

Connects the environmental analysis system to the
GeoShield kernel by creating a structured EnvironmentalContext.
"""

from typing import Any

from core.environmental.analyzer import EnvironmentalAnalyzer
from core.kernel.environmental_context import EnvironmentalContext


class EnvironmentalIntegration:
    """
    Integrates environmental analysis results into the GeoShield kernel.
    """

    def __init__(self) -> None:
        self.analyzer = EnvironmentalAnalyzer()

    def analyze(
        self,
        ndvi: float,
        ndbi: float,
        ndwi: float,
        savi: float,
    ) -> EnvironmentalContext:
        """
        Analyze environmental conditions and create kernel context.
        """

        result: dict[str, Any] = self.analyzer.analyze(
            ndvi=ndvi,
            ndbi=ndbi,
            ndwi=ndwi,
            savi=savi,
        )

        return EnvironmentalContext(
            indices=result.get("indices", {}),
            classifications=result.get("classifications", {}),
            environmental_score=result.get(
                "environmental_score",
                0.0,
            ),
            condition=result.get(
                "condition",
                "",
            ),
            risk_level=result.get(
                "risk_level",
                "",
            ),
            report=result.get(
                "report",
                {},
            ),
        )