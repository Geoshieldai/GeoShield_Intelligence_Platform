"""
GeoShield Intelligence Platform

Enterprise Service Registry

Author:
David Omondi Ouma
Founder & Chief Executive Officer (CEO)
"""


class ServiceRegistry:
    """
    Central registry for all platform services.
    """

    def __init__(self):
        self._services = {}

    def register(self, name, service):

        self._services[name] = service

    def get(self, name):

        return self._services.get(name)

    def list_services(self):

        return list(self._services.keys())