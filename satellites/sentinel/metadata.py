"""
Sentinel Metadata Extractor
"""

from satellites.base.metadata_extractor import (
    BaseMetadataExtractor,
)


class SentinelMetadataExtractor(
    BaseMetadataExtractor
):

    def extract(
        self,
        metadata: dict,
    ) -> dict:

        return {
            "provider": "Sentinel",
            "product_id": metadata.get("Id"),
            "name": metadata.get("Name"),
            "content_type": metadata.get("ContentType"),
            "content_length": metadata.get("ContentLength"),
            "publication_date": metadata.get("PublicationDate"),
            "origin_date": metadata.get("OriginDate"),
            "online": metadata.get("Online"),
            "footprint": metadata.get("Footprint"),
        }