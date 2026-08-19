"""
Live Planet authentication and Data API tests.
"""

import pytest
from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


@pytest.mark.live
@pytest.mark.asyncio
async def test_planet_auth_live() -> None:
    """
    Verify Planet authentication and Data API access.
    """

    key = get_planet_key()

    assert key
    assert len(key) == 36

    auth = Auth.from_key(key)

    assert auth is not None

    async with Session(auth=auth) as session:
        client = DataClient(session)

        # Use a known PSScene item that was previously confirmed
        # to be accessible through the Planet Data API.
        item_id = "20200617_204449_0f17"

        item = await client.get_item(
            "PSScene",
            item_id,
        )

    assert item is not None
    assert item["id"] == item_id

    print("Planet authentication: SUCCESS")
    print("Planet Data API: SUCCESS")
    print("Item ID:", item["id"])