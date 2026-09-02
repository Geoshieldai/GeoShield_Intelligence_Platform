from satellites.auth.token_manager import TokenManager


def test_token_manager():

    manager = TokenManager()

    token = manager.get_token()

    assert token is not None
    assert manager.token_valid()
    assert manager.expires_at() is not None