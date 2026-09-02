from satellites.downloader.download_manager import DownloadManager


def test_download_manager():

    manager = DownloadManager()

    result = manager.download(
        provider="Sentinel",
        product_id="TEST_PRODUCT",
        destination="downloads",
    )

    assert "TEST_PRODUCT" in result