import logging

from .base import BaseMunger


class LoadMunger(BaseMunger):
    """
    Handles munging of load screen data.
    """

    def __init__(self, platform="PC"):
        super().__init__("Load", platform)

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Load...")
