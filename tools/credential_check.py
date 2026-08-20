"""
GeoShield AI Enterprise
Credential Safety Check

Never prints credential values.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv


load_dotenv(".env", override=False)


def credential_status(name: str) -> str:
    """Return credential state without exposing its value."""

    value = os.getenv(name)

    if value is None:
        return "NOT_SET"

    if not value.strip():
        return "EMPTY"

    return "SET"


def main() -> None:
    print("===== GEOSHIELD CREDENTIAL SAFETY CHECK =====")

    credentials = [
        "CDSE_USERNAME",
        "CDSE_PASSWORD",
    ]

    for name in credentials:
        print(f"{name}: {credential_status(name)}")

    print()
    print(
        "SECURITY RULE: credential values are never printed."
    )


if __name__ == "__main__":
    main()
