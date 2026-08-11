import pytest
import planet

from planet import Auth, Session
from planet.clients import DataClient

from backend.satellite.auth import get_planet_key


@pytest.mark.asyncio
async def test_planet_auth_live() -> None:
    """
    Live test for Planet API authentication and Data API access.
    """

    # Load Planet API key
    key = get_planet_key()

    assert key, "PLANET_API_KEY was not loaded."
    assert isinstance(key, str), "Planet API key must be a string."
    assert len(key) > 20, "Planet API key appears to be invalid."

    # Create Planet authentication object
    auth = Auth.from_key(key)

    assert auth is not None, "Failed to create Planet Auth object."

    # Create authenticated Planet session
    async with Session(auth=auth) as session:

        # Create Data API client
        client = DataClient(session)

        # Request the known Planet item
        item = await client.get_item(
            "PSScene",
            "20200617_204449_0f17",
        )

        # Verify that Planet returned an item
        assert item is not None, "Planet returned no imagery item."

        # Output useful information
        print()
        print("Planet authentication: SUCCESS")
        print("Planet Data API: SUCCESS")
        print("Item ID:", item.get("id"))