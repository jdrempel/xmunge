import logging
from glob import iglob
from pathlib import Path
from shutil import rmtree

from xm.utils.globals import Settings
from xm.utils.tools import level_pack, mkdir_p, munge, soundfl_munge
from xm.utils.tools import get_dir_no_case as _
from .base import BaseMunger


class CommonMunger(BaseMunger):
    """
    Handles munging of common data.
    """

    munge_temp_name = "MungeTemp"

    def __init__(self, platform="PC"):
        super().__init__("Common", platform)

    def _munge_sprites(self):
        pass

    def _munge_fpm(self):
        pass

    def _merge_localize_files(self) -> None:
        """
        Helper method for iterating through each language of localization files and concatenating the contents of
        those with identical (case-insensitive) names
        :return: None
        """
        munge_temp = Path(self.munge_temp_name)
        localize_path = self.source_dir / "Localize"
        localize_platform_path = localize_path / self.platform
        logger = logging.getLogger("main")
        logger.info("Merge localization files...")
        mkdir_p(munge_temp)
        for item in list(localize_platform_path.iterdir()) + list(
                localize_path.iterdir()
        ):
            if not item.is_file():
                continue
            if not item.suffix == ".cfg":
                continue
            contents = ""
            with open(item, "r") as source_file:
                contents = source_file.read()
            with open(munge_temp / item.name.lower(), "a") as merged_file:
                merged_file.write(contents)
                logger.info("Merged %s", item.name)

    def run(
            self,
            localize: bool = True,
            shaders: bool = True,
            sprites: bool = True,
            fpm: bool = True,
    ):
        logger = logging.getLogger("main")
        logger.info("Munge Common...")

        mkdir_p(Settings.output_dir)
        mkdir_p(self.munge_dir)

        munge("Odf", "$*.odf", self.source_dir, self.munge_dir)
        munge("Config", "$*.fx", self.source_dir, self.munge_dir)
        munge("Config", "$*.combo", self.source_dir, self.munge_dir)
        munge("Script", "$*.lua", self.source_dir, self.munge_dir)
        munge("Config", "$*.mcfg", self.source_dir, self.munge_dir)
        munge("Config", "$*.sanm", self.source_dir, self.munge_dir)
        munge("Config", "$*.hud", self.source_dir, self.munge_dir)
        munge("Font", "$*.fff", self.source_dir, self.munge_dir)
        munge("Texture", ["$*.tga", "$*.pic"], self.source_dir, self.munge_dir)
        munge(
            "Model", ["$effects/*.msh", "$MSHs/*.msh"], self.source_dir, self.munge_dir
        )
        if shaders is True and self.platform != "PS2":
            munge(
                "Shader",
                ["shaders/*.xml", "shaders/*.vsfrag"],
                self.source_dir,
                self.munge_dir,
            )

        common_sound_path = _(self.source_dir / "Sound")
        munge(
            "Config",
            ["*.snd", "*.mus"],
            common_sound_path,
            self.munge_dir,
            hash_strings=True,
        )
        for sfx in iglob(str(common_sound_path / "*.sfx")):
            print(sfx)
            soundfl_munge()  # TODO
        for stm in iglob(str(common_sound_path / "*.stm")):
            print(stm)
            soundfl_munge()  # TODO

        if sprites:
            self._munge_sprites()

        if localize:
            self._merge_localize_files()
            munge("Localize", "*.cfg", self.munge_temp_name, self.munge_dir)
            rmtree(self.munge_temp_name)

        level_pack(
            "core.req",
            self.source_dir,
            Settings.output_dir,
            self.munge_dir,
            write_files=[
                "core",
            ],
        )
        level_pack(
            "common.req",
            self.source_dir,
            Settings.output_dir,
            self.munge_dir,
            common=[
                "core",
            ],
            write_files=[
                "common",
            ],
        )
        level_pack(
            "ingame.req",
            self.source_dir,
            Settings.output_dir,
            self.munge_dir,
            common=["core", "common"],
            write_files=[
                "ingame",
            ],
        )
        level_pack(
            "inshell.req",
            self.source_dir,
            Settings.output_dir,
            self.munge_dir,
            common=["core", "common"],
            write_files=[
                "inshell",
            ],
        )
        level_pack(
            "mission/*.req",
            self.source_dir,
            self.munge_dir,
            self.munge_dir,
            common=["core", "common", "ingame"],
            write_files=[
                "core",
            ],
        )
        level_pack(
            "mission.req",
            self.source_dir,
            Settings.output_dir,
            self.munge_dir,
            write_files=[
                "core",
            ],
        )

        if fpm:
            self._munge_fpm()
