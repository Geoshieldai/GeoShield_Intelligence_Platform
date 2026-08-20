import asyncio

from backend.satellite.planet_search import PlanetSearchEngine
from backend.satellite.planet_assets import PlanetAssetEngine


async def main():
    print("===== GEOSHIELD PLANET ASSET SEARCH =====")
    print()

    search_engine = PlanetSearchEngine()
    asset_engine = PlanetAssetEngine()

    print("Searching Planet for recent scenes...")

    scenes = await search_engine.latest_images(
        cloud_cover=0.2,
        limit=10,
    )

    print("Scenes returned:", len(scenes))
    print()

    if not scenes:
        print("NO SCENES FOUND")
        return

    for index, scene in enumerate(scenes, start=1):

        scene_id = scene["id"]

        print(f"[{index}] Scene: {scene_id}")

        try:
            assets = await asset_engine.list_assets(scene_id)

            print("    Assets:", len(assets))

            if assets:
                print("    Asset types:")

                for asset_name in assets.keys():
                    print("      -", asset_name)

                print()
                print("===== FIRST SCENE WITH ASSETS =====")
                print("Scene ID:", scene_id)
                print("Assets:", list(assets.keys()))
                print()

                break

        except Exception as exc:
            print(
                "    Asset lookup failed:",
                type(exc).__name__,
                str(exc),
            )

        print()

    print("===== DIAGNOSTIC COMPLETE =====")


if __name__ == "__main__":
    asyncio.run(main())