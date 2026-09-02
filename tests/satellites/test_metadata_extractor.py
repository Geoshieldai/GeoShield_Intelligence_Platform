from satellites.sentinel.metadata import (
    SentinelMetadataExtractor,
)


def test_metadata():

    sample = {
        "Id": "ABC123",
        "Name": "Sentinel Test",
        "ContentType": "application/octet-stream",
        "ContentLength": 500,
        "PublicationDate": "2026-08-07",
        "OriginDate": "2026-08-01",
        "Online": True,
        "Footprint": "POLYGON(...)",
    }

    extractor = SentinelMetadataExtractor()

    result = extractor.extract(sample)

    assert result["provider"] == "Sentinel"
    assert result["product_id"] == "ABC123"