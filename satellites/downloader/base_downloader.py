"""
Base Downloader

Defines the interface for all satellite download providers.
"""

from abc import ABC, abstractmethod


class BaseDownloader(ABC):
    """
    Base class for every satellite downloader.
    """

    @abstractmethod
    def download(
        self,
        product_id: str,
        destination: str,
    ) -> str:
        """
        Download a satellite product.

        Parameters
        ----------
        product_id : str
            Satellite product identifier.

        destination : str
            Local folder where the product should be saved.

        Returns
        -------
        str
            Local path of the downloaded product.
        """
        raise NotImplementedError