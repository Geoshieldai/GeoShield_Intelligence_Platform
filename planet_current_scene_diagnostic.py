import asyncio

from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


async def main():
    print("==============================================")
    print(" GEOSHIELD PLANET CURRENT SCENE DIAGNOSTIC")
    print("==============================================")

    auth = Auth.from_key(get_planet_key())

    async with Session(auth=auth) as session:

        client = DataClient(session)

        print()
        print("Searching current Planet PSScene imagery...")

        results = client.search(
            item_types=["PSScene"],
            limit=10,
            sort="published desc",
        )

        count = 0

        async for item in results:
            count += 1

            properties = item.get("properties", {})

            print()
            print(f"===== SCENE {count} =====")
            print("ID:", item.get("id"))
            print("Acquired:", properties.get("acquired"))
            print("Published:", properties.get("published"))
            print("Cloud cover:", properties.get("cloud_cover"))
            print(
                "Publishing stage:",
                properties.get("publishing_stage"),
            )
            print(
                "Quality category:",
                properties.get("quality_category"),
            )
            print(
                "Item type:",
                properties.get("item_type"),
            )

            assets = item.get("assets", [])

            print("Assets type:", type(assets).__name__)
            print("Assets:", assets)

        print()
        print("==============================================")
        print("Scenes inspected:", count)
        print("DIAGNOSTIC COMPLETE")
        print("==============================================")


if __name__ == "__main__":
    asyncio.run(main())