import asyncio

from backend.satellite.planet_assets import PlanetAssetEngine
from backend.satellite.test_assets import SCENE_ID


async def main():
    print("===== GEOSHIELD PLANET ASSET DIAGNOSTIC =====")
    print("Scene:", SCENE_ID)
    print()

    engine = PlanetAssetEngine()

    assets = await engine.list_assets(SCENE_ID)

    print("Asset response type:", type(assets).__name__)

    if hasattr(assets, "keys"):
        print("Asset keys:")
        for key in assets.keys():
            print(" -", key)

    print()
    print("Number of assets:", len(assets))

    print()
    print("===== ASSET DETAILS =====")

    if hasattr(assets, "items"):
        for name, asset in assets.items():
            print()
            print("Asset:", name)
            print("Type:", type(asset).__name__)
            print("Value:", asset)

    print()
    print("===== DIAGNOSTIC COMPLETE =====")


if __name__ == "__main__":
    asyncio.run(main())