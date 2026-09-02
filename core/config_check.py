"""
GeoShield AI Enterprise
Configuration Validation

Never prints credential values.
"""

from __future__ import annotations

from core.config import settings


def validate_configuration() -> dict[str, object]:
    """Validate required GeoShield configuration."""

    checks = {
        "application": bool(settings.app_name),
        "environment": bool(settings.environment),
        "cdse_username": bool(settings.cdse_username),
        "cdse_password": bool(settings.cdse_password),
        "cdse_client_id": bool(settings.cdse_client_id),
        "cdse_token_url": bool(settings.cdse_token_url),
        "cdse_catalog_url": bool(settings.cdse_catalog_url),
        "http_timeout": settings.http_timeout > 0,
    }

    return checks


def main() -> None:
    checks = validate_configuration()

    print("===== GEOSHIELD CONFIGURATION CHECK =====")

    all_valid = True

    for name, valid in checks.items():
        status = "OK" if valid else "MISSING/INVALID"
        print(f"{name}: {status}")

        if not valid:
            all_valid = False

    print()

    if all_valid:
        print("CONFIGURATION STATUS: READY")
    else:
        print("CONFIGURATION STATUS: INCOMPLETE")


if __name__ == "__main__":
    main()
