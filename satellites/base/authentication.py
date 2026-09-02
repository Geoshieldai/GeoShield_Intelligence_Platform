"""
GeoShield Intelligence Platform

Satellite Authentication Base

Author:
David Omondi Ouma
Founder & Chief Executive Officer (CEO)
"""


class AuthenticationManager:

    def __init__(self):

        self.authenticated = False

    def login(self):

        self.authenticated = True

    def logout(self):

        self.authenticated = False

    def status(self):

        return self.authenticated