"""
GeoShield AI Enterprise
Planet Asset Engine

Provides access to assets belonging to Planet scenes.
"""

from __future__ import annotations

from planet import Auth, Session
from planet.clients import DataClient

from core.auth.planet import PlanetAuthManager


class PlanetAssetEngine:
    """Manage Planet scene assets."""

    def __init__(self) -> None:
        """Initialize the Planet asset engine."""

        self.auth_manager = PlanetAuthManager()

        self.auth = Auth.from_key(
            self.auth_manager.get_api_key()
        )

    async def list_assets(
        self,
        item_id: str,
    ) -> list[str]:
        """
        Return the asset types available for a Planet PSScene.

        Args:
            item_id: Planet PSScene identifier.

        Returns:
            List of available Planet asset type names.
        """

        async with Session(
            auth=self.auth
        ) as session:

            client = DataClient(session)

            item = await client.get_item(
                "PSScene",
                item_id,
            )

            assets = item.get(
                "assets",
                [],
            )

            if not isinstance(assets, list):
                raise TypeError(
                    "Unexpected Planet assets response. "
                    f"Expected list, got {type(assets).__name__}."
                )

            return assets

    async def get_asset(
        self,
        item_id: str,
        asset_type: str,
    ) -> str | None:
        """
        Return an asset type if it is available.

        Args:
            item_id: Planet PSScene identifier.
            asset_type: Planet asset type.

        Returns:
            Asset type name when available, otherwise None.
        """

        assets = await self.list_assets(
            item_id
        )

        if asset_type in assets:
            return asset_type

        return None


__all__ = [
    "PlanetAssetEngine",
]