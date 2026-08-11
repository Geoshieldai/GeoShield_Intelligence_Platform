"""
GeoShield Hazard Classifier.

Converts detected hazards into standardized
hazard classifications.
"""


class HazardClassifier:
    """
    Classify environmental hazards.
    """

    def classify(self, hazards: list[str]) -> dict:
        """
        Convert a hazard list into structured classifications.

        Returns:
            Dictionary containing hazard classifications.
        """

        classifications = {}

        for hazard in hazards:

            if hazard == "Drought":
                classifications[hazard] = {
                    "category": "Climate",
                    "description": "Potential vegetation and water stress.",
                }

            elif hazard == "Flood":
                classifications[hazard] = {
                    "category": "Hydrological",
                    "description": "Potential excessive surface-water conditions.",
                }

            elif hazard == "Urban Expansion":
                classifications[hazard] = {
                    "category": "Land Use",
                    "description": "High built-up intensity or expansion.",
                }

            elif hazard == "Vegetation Degradation":
                classifications[hazard] = {
                    "category": "Environmental",
                    "description": "Potential deterioration of vegetation conditions.",
                }

            else:
                classifications[hazard] = {
                    "category": "Unknown",
                    "description": "Unclassified environmental hazard.",
                }

        return classifications