import logging

from .base import BaseMunger


class ShellMunger(BaseMunger):
    """
    Handles munging of shell data.
    """

    def __init__(self, platform="PC"):
        super().__init__("Shell", platform)

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Shell...")
