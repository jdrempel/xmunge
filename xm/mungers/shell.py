import logging

from xm.utils.globals import Settings
from xm.utils.tools import level_pack, mkdir_p, movie_munge, munge
from xm.utils.tools import get_dir_no_case as _
from .base import BaseMunger


class ShellMunger(BaseMunger):
    """
    Handles munging of shell data.
    """

    def __init__(self, platform="PC"):
        super().__init__("Shell", platform)
        self.output_dir = Settings.output_dir / "Shell"
        self.movies_output_dir = Settings.output_dir / "Movies"

    def _munge_movies(self):
        movies_dir = _(self.source_dir / "movies")
        munge("Config", "*.mcfg", movies_dir, self.munge_dir)
        mlst_dir = _(movies_dir / self.platform)
        if not mlst_dir.exists():
            logger = logging.getLogger("main")
            logger.error("Movies directory %s does not exist - skipping movie munge!", mlst_dir)
            return
        for mlst_file in mlst_dir.iterdir():
            movie_munge(
                mlst_file.name,
                self.movies_output_dir / f"{mlst_file.stem}.mvs",
                debug=True,
            )

    def run(self, movies=False):
        logger = logging.getLogger("main")
        logger.info("Munge Shell...")

        if movies:
            self._munge_movies()

        munge("Config", "effects/*.fx", self.source_dir, self.munge_dir)
        munge("Script", "scripts/*.lua", self.source_dir, self.munge_dir)
        munge("Texture", "$*.tga", self.source_dir, self.munge_dir)
        munge("Font", "fonts/*.fff", self.source_dir, self.munge_dir)
        munge("Model", "$*.msh", self.source_dir, self.munge_dir)

        if self.platform == "PS2":
            munge("Bin", "ps2bin/*.ps2bin", self.source_dir, self.munge_dir)

        common_files = [
            f"Common/MUNGED/{self.platform}/{f}" for f in ["core", "common"]
        ]
        level_pack(
            "shell.req",
            self.source_dir,
            self.output_dir,
            self.munge_dir,
            common=common_files,
        )
        if self.platform == "PS2":
            level_pack(
                "shellps2.req",
                self.source_dir,
                self.output_dir,
                self.munge_dir,
                common=common_files,
            )

        pass
