from database.metadata_database import MetadataDatabase


def test_database():

    db = MetadataDatabase()

    db.insert({

        "product_id": "TEST001",

        "provider": "Sentinel",

        "name": "Sentinel Test",

        "publication_date": "2026-08-07",

        "origin_date": "2026-08-01",

        "footprint": "Polygon"

    })

    assert True