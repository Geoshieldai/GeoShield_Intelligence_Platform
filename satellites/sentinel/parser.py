"""
Sentinel Metadata Parser
"""


class SentinelParser:

    @staticmethod
    def parse(products):

        parsed = []

        for product in products:

            parsed.append(
                {
                    "id": product.get("Id"),
                    "name": product.get("Name"),
                    "content_date": product.get("ContentDate"),
                    "footprint": product.get("Footprint"),
                }
            )

        return parsed