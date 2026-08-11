import pytest

from planet import Session, Auth
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


ITEM_ID = "20200617_204449_0f17"


@pytest.mark.asyncio
async def test_asset_live():
    auth = Auth.from_key(get_planet_key())

    async with Session(auth=auth) as sess:
        client = DataClient(sess)

        assets = await client.list_item_assets(
            "PSScene",
            ITEM_ID,
        )

        print("\nASSETS\n")
        print(type(assets))
        print(assets)