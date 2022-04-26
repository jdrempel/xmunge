import logging
import shutil
from abc import ABC, abstractmethod
from glob import iglob
from pathlib import Path

from .globals import Settings
from .logs import setup_logging
from .tools import level_pack, munge, soundfl_munge


class BaseMunger(ABC):
    """
    Abstract base class for all other mungers. Intended to handle common properties such as platform and language,
    as well as paths to common munge-related files and folders.
    """

    def __init__(self, source_subdir: str, platform: str = "PC"):
        self.platform: str = platform
        self.source_dir = Path("..") / source_subdir
        self.munge_dir = Path(source_subdir) / "MUNGED" / platform

    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError


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

    def _merge_localize_files(self):
        munge_temp = Path(self.munge_temp_name)
        localize_path = self.source_dir / "Localize"
        localize_platform_path = localize_path / self.platform
        logger = logging.getLogger("main")
        logger.info("Merge localization files...")
        munge_temp.mkdir(parents=True, exist_ok=True)
        for item in list(localize_platform_path.iterdir()) + list(localize_path.iterdir()):
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

    def _munge_localize(self):
        munge("Localize", "*.cfg", self.munge_temp_name, self.munge_dir)
        shutil.rmtree(self.munge_temp_name)

    def run(self, localize: bool = True, shaders: bool = True, sprites: bool = True, fpm: bool = True):
        logger = logging.getLogger("main")
        logger.info("Munge Common...")

        Settings.output_dir.mkdir(parents=True, exist_ok=True)
        self.munge_dir.mkdir(parents=True, exist_ok=True)

        munge("Odf", "$*.odf", self.source_dir, self.munge_dir)
        munge("Config", "$*.fx", self.source_dir, self.munge_dir)
        munge("Config", "$*.combo", self.source_dir, self.munge_dir)
        munge("Script", "$*.lua", self.source_dir, self.munge_dir)
        munge("Config", "$*.mcfg", self.source_dir, self.munge_dir)
        munge("Config", "$*.sanm", self.source_dir, self.munge_dir)
        munge("Config", "$*.hud", self.source_dir, self.munge_dir)
        munge("Font", "$*.fff", self.source_dir, self.munge_dir)
        munge("Texture", ["$*.tga", "$*.pic"], self.source_dir, self.munge_dir)
        munge("Model", ["$effects/*.msh", "$MSHs/*.msh"], self.source_dir, self.munge_dir)
        if shaders is True and self.platform != "PS2":
            munge("Shader", ["shaders/*.xml", "shaders/*.vsfrag"], self.source_dir, self.munge_dir)

        common_sound_path = self.source_dir / "Sound"
        munge("Config", ["*.snd", "*.mus"], common_sound_path, self.munge_dir, hash_strings=True)
        for sfx in iglob(str(common_sound_path / "*.sfx")):
            soundfl_munge()  # TODO
        for stm in iglob(str(common_sound_path / "*.stm")):
            soundfl_munge()  # TODO

        if sprites:
            self._munge_sprites()

        if localize:
            self._merge_localize_files()
            self._munge_localize()

        level_pack("core.req", self.source_dir, Settings.output_dir, self.munge_dir, write_files=["core", ])
        level_pack("common.req", self.source_dir, Settings.output_dir, self.munge_dir, common=["core", ],
                   write_files=["common", ])
        level_pack("ingame.req", self.source_dir, Settings.output_dir, self.munge_dir,
                   common=["core", "common"], write_files=["ingame", ])
        level_pack("inshell.req", self.source_dir, Settings.output_dir, self.munge_dir,
                   common=["core", "common"], write_files=["inshell", ])
        level_pack("mission/*.req", self.source_dir, self.munge_dir, self.munge_dir,
                   common=["core", "common", "ingame"], write_files=["core", ])
        level_pack("mission.req", self.source_dir, Settings.output_dir, self.munge_dir, write_files=["core", ])

        if fpm:
            self._munge_fpm()


class ShellMunger(BaseMunger):
    """
    Handles munging of shell data.
    """

    def __init__(self, platform="PC"):
        super().__init__("Shell", platform)

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Shell...")


class LoadMunger(BaseMunger):
    """
    Handles munging of load screen data.
    """

    def __init__(self, platform="PC"):
        super().__init__("Load", platform)

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Load...")


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


class SideMunger(BaseMunger):
    """
    Handles munging of a single side.
    """

    def __init__(self, side, platform="PC"):
        super().__init__("Sides", platform)
        self.side = side

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Sides/%s...", self.side)


class WorldMunger(BaseMunger):
    """
    Handles munging of a single world.
    """

    def __init__(self, world, platform="PC"):
        super().__init__("Worlds", platform)
        self.world = world

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Worlds/%s...", self.world)


if __name__ == "__main__":
    platform = "PC"
    setup_logging(platform)
    Settings.set_platform(platform)
    mungers = [
        CommonMunger(platform),
        ShellMunger(platform),
        LoadMunger(platform),
        SoundMunger(platform),
        SideMunger("ALL", platform),
        WorldMunger("YAV", platform)
    ]
    for munger in mungers:
        munger.run()
