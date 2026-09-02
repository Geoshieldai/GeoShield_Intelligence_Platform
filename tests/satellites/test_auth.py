from satellites.auth.copernicus_auth import CopernicusAuth


def test_copernicus_authentication():

    auth = CopernicusAuth()

    token = auth.authenticate()

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 100