"""
GeoShield Hazard Detector.

Detects potential environmental hazards from
environmental intelligence outputs.
"""


class HazardDetector:
    """
    Detect potential hazards from environmental indicators.
    """

    def detect(
        self,
        ndvi: float,
        ndwi: float,
        ndbi: float,
        savi: float,
    ) -> list[str]:
        """
        Detect potential environmental hazards.

        Returns:
            List of detected hazard types.
        """

        hazards = []

        # Drought / vegetation stress
        if ndvi < 0.2 and savi < 0.2:
            hazards.append("Drought")

        # Flood / excessive surface water
        if ndwi >= 0.5:
            hazards.append("Flood")

        # Urban/environmental pressure
        if ndbi >= 0.4:
            hazards.append("Urban Expansion")

        # General vegetation degradation
        if ndvi < 0.1:
            hazards.append("Vegetation Degradation")

        return hazards