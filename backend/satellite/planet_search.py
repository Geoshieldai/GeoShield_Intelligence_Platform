"""
GeoShield AI Enterprise
Planet Production Scene Search Engine

Searches Planet PSScene imagery and returns scenes that are:

1. Production quality
2. Within the requested cloud-cover threshold
3. Authorized for asset download
4. Suitable for the requested asset type
"""

from __future__ import annotations

from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


class PlanetSearchEngine:
    """Search Planet PSScene imagery for downloadable production scenes."""

    def __init__(self) -> None:
        self.auth = Auth.from_key(get_planet_key())

    async def latest_images(
        self,
        geometry=None,
        start_date=None,
        end_date=None,
        cloud_cover: float = 0.2,
        limit: int = 10,
        asset_type: str = "ortho_visual",
    ) -> list[dict]:
        """
        Return production Planet scenes that contain the requested
        asset and are downloadable by the authenticated account.

        Args:
            geometry:
                Optional GeoJSON geometry used to constrain the search.

            start_date:
                Optional acquisition start date.

            end_date:
                Optional acquisition end date.

            cloud_cover:
                Maximum cloud-cover fraction.

            limit:
                Maximum number of scenes returned.

            asset_type:
                Planet asset type required for acquisition.

        Returns:
            List of downloadable production scene metadata.
        """

        if limit < 1:
            raise ValueError("limit must be at least 1")

        if not 0 <= cloud_cover <= 1:
            raise ValueError(
                "cloud_cover must be between 0 and 1."
            )

        if not asset_type:
            raise ValueError(
                "asset_type must not be empty."
            )

        filters = []

        # ---------------------------------------------------------
        # DATE FILTER
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # CLOUD FILTER
        # ---------------------------------------------------------

        filters.append(
            {
                "type": "RangeFilter",
                "field_name": "cloud_cover",
                "config": {
                    "lte": cloud_cover,
                },
            }
        )

        # ---------------------------------------------------------
        # ASSET FILTER
        # ---------------------------------------------------------

        filters.append(
            {
                "type": "AssetFilter",
                "config": [
                    asset_type,
                ],
            }
        )

        # ---------------------------------------------------------
        # DOWNLOAD PERMISSION FILTER
        # ---------------------------------------------------------

        filters.append(
            {
                "type": "PermissionFilter",
                "config": [
                    "assets:download",
                ],
            }
        )

        search_filter = {
            "type": "AndFilter",
            "config": filters,
        }

        async with Session(
            auth=self.auth
        ) as session:

            client = DataClient(session)

            results: list[dict] = []

            async for item in client.search(
                item_types=["PSScene"],
                search_filter=search_filter,
                geometry=geometry,
                sort="published desc",
                limit=100,
            ):

                properties = item.get(
                    "properties",
                    {},
                )

                publishing_stage = properties.get(
                    "publishing_stage",
                    "",
                )

                quality_category = properties.get(
                    "quality_category",
                    "",
                )

                # -------------------------------------------------
                # PRODUCTION QUALITY CHECK
                # -------------------------------------------------

                if publishing_stage.lower() != "standard":
                    continue

                if quality_category.lower() not in {
                    "standard",
                    "quality",
                    "best",
                }:
                    continue

                # -------------------------------------------------
                # ITEM ASSET CHECK
                # -------------------------------------------------

                assets = item.get(
                    "assets",
                    [],
                )

                if asset_type not in assets:
                    continue

                # -------------------------------------------------
                # RESULT
                # -------------------------------------------------

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
                        "asset_type": asset_type,
                        "download_permission": True,
                    }
                )

                if len(results) >= limit:
                    break

            return results


__all__ = [
    "PlanetSearchEngine",
]