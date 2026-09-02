"""
Live Planet Data API item test.
"""

import pytest
from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


@pytest.mark.live
@pytest.mark.asyncio
async def test_planet_item_lookup():
    """
    Verify that Planet Data API can retrieve a PSScene item.
    """

    item_id = "20260726_175350_76_254f"

    auth = Auth.from_key(get_planet_key())

    async with Session(auth=auth) as session:
        client = DataClient(session)

        item = await client.get_item("PSScene", item_id)

    assert item is not None
    assert item["id"] == item_id