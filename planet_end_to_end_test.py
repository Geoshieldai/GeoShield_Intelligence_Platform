"""
GeoShield AI Enterprise
Planet End-to-End Acquisition Test

Verifies the complete Planet Data API workflow:

1. Search for recent PSScene imagery.
2. Inspect scene quality and publishing stage.
3. Discover available assets.
4. Select ortho_visual.
5. Check whether the asset is downloadable.
6. Activate the asset when permitted.

IMPORTANT:
This test does not assume that preview/test imagery is production imagery.
It reports the actual Planet account state instead.
"""

import asyncio

from backend.satellite.planet_search import PlanetSearchEngine
from backend.satellite.planet_assets import PlanetAssetEngine
from backend.satellite.planet_download import PlanetDownloadEngine


REQUESTED_ASSET = "ortho_visual"


async def main():
    print("================================================")
    print(" GEOSHIELD PLANET END-TO-END ACQUISITION TEST")
    print("================================================")

    # -------------------------------------------------
    # 1. SEARCH
    # -------------------------------------------------

    print()
    print("===== STEP 1: PLANET SCENE SEARCH =====")

    search_engine = PlanetSearchEngine()

    scenes = await search_engine.latest_images(
        cloud_cover=0.20,
        limit=10,
    )

    print("Scenes returned:", len(scenes))

    if not scenes:
        raise RuntimeError(
            "Planet returned no PSScene imagery."
        )

    for index, scene in enumerate(scenes, start=1):
        print()
        print(f"[{index}]")
        print("Scene ID:", scene.get("id"))
        print("Acquired:", scene.get("acquired"))
        print("Published:", scene.get("published"))
        print("Cloud:", scene.get("cloud"))
        print("Stage:", scene.get("stage"))
        print("Quality:", scene.get("quality"))

    # -------------------------------------------------
    # 2. SELECT A SCENE
    # -------------------------------------------------

    print()
    print("===== STEP 2: SCENE SELECTION =====")

    # Prefer standard-quality imagery if the account returns it.
    standard_scenes = [
        scene
        for scene in scenes
        if str(scene.get("quality", "")).lower() == "standard"
    ]

    if standard_scenes:
        scene = standard_scenes[0]
        print("Standard-quality scene found.")
    else:
        # We deliberately allow a preview/test scene for
        # API integration diagnostics.
        scene = scenes[0]
        print("No standard-quality scene returned.")
        print("Using a returned preview/test scene for API verification.")

    scene_id = scene["id"]

    print("Selected scene:", scene_id)
    print("Quality:", scene.get("quality"))
    print("Publishing stage:", scene.get("stage"))

    # -------------------------------------------------
    # 3. ASSET DISCOVERY
    # -------------------------------------------------

    print()
    print("===== STEP 3: ASSET DISCOVERY =====")

    asset_engine = PlanetAssetEngine()

    assets = await asset_engine.list_assets(scene_id)

    if not assets:
        raise RuntimeError(
            f"No assets were returned for scene {scene_id}."
        )

    print("Asset response type:", type(assets).__name__)

    if hasattr(assets, "keys"):
        asset_names = list(assets.keys())
    else:
        asset_names = list(assets)

    print("Assets available:", asset_names)

    # -------------------------------------------------
    # 4. ASSET SELECTION
    # -------------------------------------------------

    print()
    print("===== STEP 4: ASSET SELECTION =====")
    print("Requested asset:", REQUESTED_ASSET)

    if REQUESTED_ASSET not in asset_names:
        raise RuntimeError(
            f"{REQUESTED_ASSET} is not available. "
            f"Available assets: {asset_names}"
        )

    print("Requested asset: AVAILABLE")

    # -------------------------------------------------
    # 5. ASSET STATUS / ACTIVATION
    # -------------------------------------------------

    print()
    print("===== STEP 5: ASSET ACTIVATION =====")

    download_engine = PlanetDownloadEngine()

    asset = await download_engine.activate_download(
        scene_id=scene_id,
        asset_type=REQUESTED_ASSET,
    )

    if not asset:
        raise RuntimeError(
            "Planet returned an empty asset response."
        )

    print()
    print("PLANET ASSET RESPONSE: SUCCESS")
    print("Scene:", scene_id)
    print("Asset:", REQUESTED_ASSET)

    print()
    print("Returned asset information:")

    if isinstance(asset, dict):
        print("Status:", asset.get("status"))
        print("Permissions:", asset.get("permissions"))
        print("Location available:", bool(asset.get("location")))
        print("Activation link available:", bool(
            asset.get("_links", {}).get("activate")
        ))

    else:
        print(asset)

    # -------------------------------------------------
    # 6. FINAL STATUS
    # -------------------------------------------------

    print()
    print("================================================")
    print(" PLANET END-TO-END TEST FINISHED")
    print("================================================")

    print()
    print("IMPORTANT RESULT:")
    print("Planet API connectivity: SUCCESS")
    print("Scene search: SUCCESS")
    print("Asset discovery: SUCCESS")
    print("Requested asset:", REQUESTED_ASSET)
    print("Scene quality:", scene.get("quality"))
    print("Publishing stage:", scene.get("stage"))

    if str(scene.get("quality", "")).lower() == "standard":
        print("Download-quality imagery: STANDARD")
    else:
        print("Download-quality imagery: NOT STANDARD")
        print(
            "The account currently returned preview/test imagery "
            "for this search."
        )


if __name__ == "__main__":
    asyncio.run(main())