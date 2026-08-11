import pytest
from planet import Session, Auth
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


ITEM_ID = "20260726_075804_67_254c"


@pytest.mark.asyncio
async def test_asset_check() -> None:
    auth = Auth.from_key(get_planet_key())

    async with Session(auth=auth) as sess:
        client = DataClient(sess)

        item = await client.get_item(
            "PSScene",
            ITEM_ID,
        )

        print("\nASSETS FIELD\n")
        print(item.get("assets"))