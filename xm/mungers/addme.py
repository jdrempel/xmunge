import logging
from shutil import copy

from xm.utils.globals import Settings
from xm.utils.tools import mkdir_p, munge
from .base import BaseMunger


class AddmeMunger(BaseMunger):
    """
    Handles munging of the addme.lua script.
    """

    def __init__(self, platform="PC"):
        super().__init__("addme", platform)

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Addme...")

        addme_output_dir = self.source_dir / "munged"

        mkdir_p(addme_output_dir)

        munge("Script", "addme.lua", self.source_dir, addme_output_dir)

        copy(addme_output_dir / "addme.script", Settings.output_dir)
