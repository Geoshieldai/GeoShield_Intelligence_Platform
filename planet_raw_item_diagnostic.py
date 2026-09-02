import asyncio

from planet import Auth, Session
from planet.clients import DataClient

from core.auth.planet import PlanetAuthManager


SCENE_ID = "20260819_161914_57_254a"


async def main():
    print("===== GEOSHIELD PLANET RAW ITEM DIAGNOSTIC =====")
    print("Scene:", SCENE_ID)
    print()

    manager = PlanetAuthManager()

    auth = Auth.from_key(
        manager.get_api_key()
    )

    async with Session(auth=auth) as session:

        client = DataClient(session)

        print("Requesting raw PSScene item...")

        item = await client.get_item(
            "PSScene",
            SCENE_ID,
        )

        print("Item returned:", bool(item))
        print()

        print("Item ID:")
        print(item.get("id"))
        print()

        print("Item type:")
        print(item.get("type"))
        print()

        properties = item.get("properties", {})

        print("===== PROPERTIES =====")

        for key in [
            "acquired",
            "published",
            "cloud_cover",
            "quality_category",
            "publishing_stage",
            "item_type",
        ]:
            print(f"{key}:", properties.get(key))

        print()
        print("===== RAW ASSETS FIELD =====")

        assets = item.get("assets")

        print("Assets type:", type(assets).__name__)
        print("Assets value:", assets)

        if isinstance(assets, dict):
            print()
            print("Asset count:", len(assets))
            print("Asset names:", list(assets.keys()))

    print()
    print("===== DIAGNOSTIC COMPLETE =====")


if __name__ == "__main__":
    asyncio.run(main())