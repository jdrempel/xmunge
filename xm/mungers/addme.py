import logging
from shutil import copy

from xm.utils.globals import Settings
from xm.utils.tools import munge
from .base import BaseMunger


class AddmeMunger(BaseMunger):

    def __init__(self, platform="PC"):
        super().__init__("addme", platform)

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Addme...")

        addme_output_dir = self.source_dir / "MUNGED"

        munge("Script", "addme.lua", self.source_dir, addme_output_dir)

        copy(self.source_dir / "addme.script", Settings.output_dir)
