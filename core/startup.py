"""
Platform Startup
"""

from core.logger import logger
from core.metadata import PROJECT_NAME
from core.version import __version__


def startup():

    logger.info("--------------------------------")

    logger.info(PROJECT_NAME)

    logger.info(f"Version: {__version__}")

    logger.info("Platform Starting...")

    logger.info("--------------------------------")


if __name__ == "__main__":

    startup()