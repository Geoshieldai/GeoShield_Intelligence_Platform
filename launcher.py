"""
GeoShield Launcher
"""

from core.application import GeoShieldApplication


def main():

    app = GeoShieldApplication()

    app.initialize()

    print()
    print("=" * 60)
    print("GeoShield Intelligence Platform")
    print("=" * 60)

    print(app.status())

    print("=" * 60)
    print("GeoShield Ready")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()