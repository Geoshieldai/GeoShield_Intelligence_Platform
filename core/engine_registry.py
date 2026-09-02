"""
GeoShield Intelligence Platform

Enterprise Engine Registry

Author:
David Omondi Ouma
Founder & Chief Executive Officer (CEO)
"""


class EngineRegistry:
    """
    Stores and manages all intelligence engines
    available within the GeoShield Platform.
    """

    def __init__(self):
        self._engines = {}

    def register(self, name, engine):

        self._engines[name] = engine

    def get(self, name):

        return self._engines.get(name)

    def exists(self, name):

        return name in self._engines

    def list_engines(self):

        return list(self._engines.keys())