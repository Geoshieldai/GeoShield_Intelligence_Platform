"""
Environment Configuration
"""

import os


def get_environment():

    return os.getenv("GEOSHIELD_ENV", "development")


def is_development():

    return get_environment() == "development"


def is_production():

    return get_environment() == "production"


def is_testing():

    return get_environment() == "testing"