import asyncio

from planet import Auth, DataClient
from planet.http import Session

from backend.satellite.auth import get_planet_key


async def main():
    print("===== GeoShield Planet API Test =====")

    # Load Planet API key
    key = get_planet_key()
    print("Planet key loaded: True")
    print("Key length:", len(key))

    # Create Planet authentication
    auth = Auth.from_key(key)
    print("Planet authentication created: True")

    # Create authenticated HTTP session
    session = Session(auth=auth)
    print("Planet HTTP session created: True")

    # Create DataClient using the session
    client = DataClient(session)
    print("Planet DataClient created: True")

    try:
        print("Testing Planet API search...")

        results = client.search(
            item_types=["PSScene"],
            limit=1,
        )

        async for item in results:
            print("Planet API request completed: True")
            print("Returned item ID:", item.get("id"))
            print("Returned item type:", item.get("properties", {}).get("item_type"))
            break
        else:
            print("Planet API request completed: True")
            print("No matching items returned.")

    except Exception as e:
        print("API request failed:", type(e).__name__)
        print("Error:", e)

    finally:
        await session.aclose()
        print("Planet API test finished.")


if __name__ == "__main__":
    asyncio.run(main())
