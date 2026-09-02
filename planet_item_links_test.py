import asyncio
import json

from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


SCENE_ID = "20260819_114849_64_24e9"


async def main():
    print("================================================")
    print(" GEOSHIELD PLANET ITEM LINK DIAGNOSTIC")
    print("================================================")

    auth = Auth.from_key(get_planet_key())

    async with Session(auth=auth) as session:
        client = DataClient(session)

        item = await client.get_item(
            "PSScene",
            SCENE_ID,
        )

        print()
        print("===== ITEM LINKS =====")

        print(
            json.dumps(
                item.get("_links", {}),
                indent=2,
            )
        )

        print()
        print("===== ITEM PERMISSIONS =====")

        print(
            json.dumps(
                item.get("_permissions", []),
                indent=2,
            )
        )

        print()
        print("===== ITEM ASSETS =====")

        print(
            json.dumps(
                item.get("assets", []),
                indent=2,
            )
        )

        print()
        print("===== FULL ITEM JSON =====")

        print(
            json.dumps(
                item,
                indent=2,
            )
        )


if __name__ == "__main__":
    asyncio.run(main())