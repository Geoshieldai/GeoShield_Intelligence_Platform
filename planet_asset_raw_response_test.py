import asyncio

from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


SCENE_ID = "20260819_114849_64_24e9"


async def main():
    print("================================================")
    print(" GEOSHIELD PLANET RAW ASSET RESPONSE TEST")
    print("================================================")

    auth = Auth.from_key(get_planet_key())

    async with Session(auth=auth) as session:
        client = DataClient(session)

        print()
        print("===== STEP 1: GET ITEM =====")

        item = await client.get_item(
            "PSScene",
            SCENE_ID,
        )

        print("Item type:", type(item).__name__)
        print("Item ID:", item.get("id"))
        print("Item type ID:", item.get("type"))
        print("Item properties available:", list(item.keys()))

        print()
        print("===== STEP 2: ITEM ASSETS =====")

        item_assets = item.get("assets", [])

        print("Asset response type:", type(item_assets).__name__)
        print("Assets:", item_assets)

        print()
        print("===== STEP 3: SDK LIST_ITEM_ASSETS =====")

        raw_assets = await client.list_item_assets(
            "PSScene",
            SCENE_ID,
        )

        print("Raw /assets response type:", type(raw_assets).__name__)
        print("Raw /assets response:", raw_assets)

        if isinstance(raw_assets, dict):
            print()
            print("Asset keys:", list(raw_assets.keys()))

        print()
        print("===== STEP 4: END =====")


if __name__ == "__main__":
    asyncio.run(main())