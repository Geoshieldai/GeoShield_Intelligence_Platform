"""
Base Metadata Extractor
"""

from abc import ABC, abstractmethod


class BaseMetadataExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        metadata: dict,
    ) -> dict:
        """
        Extract standardized metadata.

        Returns
        -------
        Dictionary
        """
        raise NotImplementedError