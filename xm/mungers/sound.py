import logging

from xm.utils.globals import Settings
from xm.utils.tools import level_pack, mkdir_p, munge
from xm.utils.tools import get_dir_no_case as _
from .base import BaseMunger


class SoundMunger(BaseMunger):
    """
    Handles munging of sound data.
    """

    def __init__(self, platform="PC", streams=True):
        super().__init__("Load", platform)
        self.munge_streams = streams
        self.output_dir = Settings.output_dir / "Sound"

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Sound...")

        if self.platform == "PC":
            bank_option = " -template"

        # insert soundmunge.bat stuff here
