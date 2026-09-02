"""
Live Planet Data API permission test.
"""

import pytest
from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


@pytest.mark.live
@pytest.mark.asyncio
async def test_planet_item_permissions():
    """
    Verify that a Planet PSScene item exposes its permissions metadata.
    """

    item_id = "20260726_181751_21_24d1"

    auth = Auth.from_key(get_planet_key())

    async with Session(auth=auth) as session:
        client = DataClient(session)

        item = await client.get_item("PSScene", item_id)

    assert item is not None
    assert "_permissions" in item
    assert item["_permissions"] is not None