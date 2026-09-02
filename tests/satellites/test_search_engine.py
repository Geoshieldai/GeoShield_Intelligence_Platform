from engines.satellite_search_engine import SatelliteSearchEngine


def test_search_engine():

    engine = SatelliteSearchEngine()

    results = engine.search_all(
        latitude=-1.2921,
        longitude=36.8219,
        start_date="2026-08-01",
        end_date="2026-08-03",
        limit=5,
    )

    assert len(results) > 0

    print("\nReturned Products:\n")

    for item in results:

        print(item)

    print("\nSatellite Search Engine Passed\n")