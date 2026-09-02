"""
GeoShield Intelligence Platform

Satellite Intelligence Engine

Author:
David Omondi Ouma
Founder & Chief Executive Officer (CEO)
"""


class SatelliteEngine:
    """
    Responsible for managing satellite data sources.
    """

    def __init__(self):

        self.providers = []

    def register_provider(self, provider):

        self.providers.append(provider)

    def list_providers(self):

        return self.providers

    def provider_count(self):

        return len(self.providers)