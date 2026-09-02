"""
GeoShield Sentinel Provider Test
"""

from satellites.sentinel.provider import SentinelProvider


provider = SentinelProvider()

print()

print("Provider")
print(provider.info())

print()

print("Authentication")
print(provider.authenticate())

print()

print("Search Results")
print(provider.search())

print()

print("Metadata")
print(provider.metadata("S2A_TEST_001"))

print()

print("Download")
provider.download("S2A_TEST_001")