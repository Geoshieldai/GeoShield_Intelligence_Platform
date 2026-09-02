"""
GeoShield AI Enterprise
Planet Asset Download Manager

Handles Planet asset discovery and activation.

This module intentionally keeps credential handling inside
GeoShield's centralized authentication layer.
"""

from __future__ import annotations

from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


class PlanetDownloadEngine:
    """Manage Planet imagery asset activation."""

    def __init__(self) -> None:
        """Initialize authenticated Planet access."""

        self.auth = Auth.from_key(get_planet_key())

    async def get_asset(
        self,
        scene_id: str,
        asset_type: str = "ortho_visual",
    ):
        """
        Retrieve a specific asset from a Planet scene.

        Returns:
            The Planet asset metadata.

        Raises:
            RuntimeError: If the scene or asset cannot be found.
        """

        print("===== GEOSHIELD PLANET ASSET LOOKUP =====")
        print("Scene:", scene_id)
        print("Asset:", asset_type)

        async with Session(auth=self.auth) as session:

            client = DataClient(session)

            item = await client.get_item(
                "PSScene",
                scene_id,
            )

            if not item:
                raise RuntimeError(
                    f"Planet scene {scene_id} was not returned."
                )

            assets = item.get("assets", [])

            print("Raw asset response type:", type(assets).__name__)

            # Planet may return asset names as a list.
            if isinstance(assets, list):

                print("Available assets:", assets)

                if asset_type not in assets:
                    raise RuntimeError(
                        f"Asset '{asset_type}' is not available for "
                        f"Planet scene {scene_id}. "
                        f"Available assets: {assets}"
                    )

                # Retrieve the full asset metadata.
                asset = await client.get_asset(
                    "PSScene",
                    scene_id,
                    asset_type,
                )

                return asset

            # Some API responses may expose assets as a dictionary.
            if isinstance(assets, dict):

                print(
                    "Available assets:",
                    list(assets.keys()),
                )

                if asset_type not in assets:
                    raise RuntimeError(
                        f"Asset '{asset_type}' is not available for "
                        f"Planet scene {scene_id}. "
                        f"Available assets: {list(assets.keys())}"
                    )

                return assets[asset_type]

            raise RuntimeError(
                "Unexpected Planet asset response type: "
                f"{type(assets).__name__}"
            )

    async def activate_download(
        self,
        scene_id: str,
        asset_type: str = "ortho_visual",
    ):
        """
        Locate a Planet asset and prepare it for activation.

        Returns:
            Planet asset metadata.
        """

        print("===== GEOSHIELD PLANET ASSET ACTIVATION =====")
        print("Scene:", scene_id)
        print("Asset:", asset_type)

        asset = await self.get_asset(
            scene_id=scene_id,
            asset_type=asset_type,
        )

        if not asset:
            raise RuntimeError(
                f"Planet returned an empty asset for "
                f"scene {scene_id}, asset {asset_type}."
            )

        print()
        print("PLANET ASSET LOOKUP: SUCCESS")

        if isinstance(asset, dict):

            print("Asset type:", asset.get("type"))
            print("Asset status:", asset.get("status"))
            print("Permissions:", asset.get("permissions"))
            print(
                "Download location available:",
                bool(asset.get("location")),
            )

            links = asset.get("_links", {})

            if isinstance(links, dict):
                print(
                    "Activation link available:",
                    bool(links.get("activate")),
                )

                print(
                    "Self link available:",
                    bool(links.get("_self") or links.get("self")),
                )

        return asset


__all__ = [
    "PlanetDownloadEngine",
]