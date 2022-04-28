import logging

from .base import BaseMunger


class SoundMunger(BaseMunger):
    """
    Handles munging of sound data.
    """

    def __init__(self, platform="PC", streams=True):
        super().__init__("Load", platform)
        self.munge_streams = streams

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Sound...")
