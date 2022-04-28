import logging
from pathlib import Path

from xm.utils.globals import Settings
from xm.utils.tools import level_pack, mkdir_p, munge
from xm.utils.tools import get_dir_no_case as _
from .base import BaseMunger


class SideMunger(BaseMunger):
    """
    Handles munging of a single side.
    """

    def __init__(self, side: str, platform="PC"):
        self.side = side
        super().__init__(f"Sides/{self.side}", platform)
        self.output_dir = Settings.output_dir / "SIDE"

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Sides/%s...", self.side)

        mkdir_p(self.munge_dir)

        self._copy_premunged_files()

        munge("Odf", "$*.odf", self.source_dir, self.munge_dir)
        munge("Config", "$effects/*.fx", self.source_dir, self.munge_dir)
        munge("Config", "$*.combo", self.source_dir, self.munge_dir)
        munge("Model", "$*.msh", self.source_dir, self.munge_dir)
        munge("Texture", ["$*.tga", "$*.pic"], self.source_dir, self.munge_dir)
        munge("Config", ["*.snd", "*.mus"], self.source_dir / "Sound", self.munge_dir)

        common_munge_dir = _(Path(f"Common/MUNGED/{self.platform}"))
        sides_common_munge_dir = _(Path(f"Sides/Common/MUNGED/{self.platform}"))

        mkdir_p(self.output_dir)

        if self.side != "Common":
            input_dirs = [self.munge_dir, sides_common_munge_dir, common_munge_dir]
            common_files = [
                f"{common_munge_dir}/{file}" for file in ["core", "common", "ingame"]
            ]
            level_pack(
                "req/*.req",
                self.source_dir,
                self.munge_dir,
                input_dir=input_dirs,
                common=common_files,
            )
            level_pack("*.req", self.source_dir, self.output_dir, input_dir=input_dirs)
