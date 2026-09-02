"""
GeoShield AI Enterprise
Local Token Expiration Test
"""

import time

from core.auth import CopernicusAuthManager


def main() -> None:
    manager = CopernicusAuthManager()

    token = manager.get_token()

    print("===== TOKEN EXPIRATION TEST =====")
    print("Initial authentication:", bool(token))
    print("Initial valid:", manager.is_token_valid())

    # Force local expiration.
    manager.state.expires_at = time.time() - 1

    print("After forced expiration:", manager.is_token_valid())
    print("Remaining lifetime:", manager.seconds_remaining())

    if manager.is_token_valid():
        raise RuntimeError(
            "Token should be expired in the local simulation."
        )

    print("Expiration detection: PASSED")
    print("Token value: [HIDDEN]")


if __name__ == "__main__":
    main()
