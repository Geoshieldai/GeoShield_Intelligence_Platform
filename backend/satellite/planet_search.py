"""
GeoShield AI Enterprise
Planet Production Scene Search Engine

Searches Planet PSScene imagery and prefers production-quality
scenes over preview/test scenes.
"""

from __future__ import annotations

from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


class PlanetSearchEngine:
    """Search Planet PSScene imagery for production-ready scenes."""

    def __init__(self) -> None:
        self.auth = Auth.from_key(get_planet_key())

    async def latest_images(
        self,
        geometry=None,
        start_date=None,
        end_date=None,
        cloud_cover: float = 0.2,
        limit: int = 10,
    ) -> list[dict]:

        if limit < 1:
            raise ValueError("limit must be at least 1")

        if not 0 <= cloud_cover <= 1:
            raise ValueError(
                "cloud_cover must be between 0 and 1."
            )

        filters = []

        if start_date and end_date:
            filters.append(
                {
                    "type": "DateRangeFilter",
                    "field_name": "acquired",
                    "config": {
                        "gte": start_date,
                        "lte": end_date,
                    },
                }
            )

        filters.append(
            {
                "type": "RangeFilter",
                "field_name": "cloud_cover",
                "config": {
                    "lte": cloud_cover,
                },
            }
        )

        search_filter = {
            "type": "AndFilter",
            "config": filters,
        }

        async with Session(auth=self.auth) as session:

            client = DataClient(session)

            results: list[dict] = []

            async for item in client.search(
                item_types=["PSScene"],
                search_filter=search_filter,
                geometry=geometry,
                sort="published desc",
                limit=100,
            ):

                properties = item.get("properties", {})

                publishing_stage = properties.get(
                    "publishing_stage",
                    "",
                )

                quality_category = properties.get(
                    "quality_category",
                    "",
                )

                # Reject preview/test scenes.
                if publishing_stage.lower() != "standard":
                    continue

                if quality_category.lower() not in {
                    "standard",
                    "quality",
                    "best",
                }:
                    continue

                results.append(
                    {
                        "id": item["id"],
                        "published": properties.get(
                            "published"
                        ),
                        "acquired": properties.get(
                            "acquired"
                        ),
                        "stage": publishing_stage,
                        "quality": quality_category,
                        "cloud": properties.get(
                            "cloud_cover"
                        ),
                        "item_type": properties.get(
                            "item_type"
                        ),
                    }
                )

                if len(results) >= limit:
                    break

            return results