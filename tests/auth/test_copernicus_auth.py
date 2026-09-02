"""
GeoShield AI Enterprise
Copernicus Authentication Unit Tests

These tests do not contact Copernicus.
"""

from __future__ import annotations

import time

from core.auth import (
    CopernicusAuthManager,
    TokenState,
)


def test_empty_token_is_invalid() -> None:
    manager = CopernicusAuthManager()

    assert manager.is_token_valid() is False
    assert manager.seconds_remaining() == 0.0


def test_valid_token_state() -> None:
    manager = CopernicusAuthManager()

    manager.state = TokenState(
        access_token="TEST_TOKEN",
        expires_at=time.time() + 300,
    )

    assert manager.is_token_valid() is True
    assert manager.seconds_remaining() > 0


def test_expired_token_state() -> None:
    manager = CopernicusAuthManager()

    manager.state = TokenState(
        access_token="TEST_TOKEN",
        expires_at=time.time() - 1,
    )

    assert manager.is_token_valid() is False
    assert manager.seconds_remaining() == 0.0
