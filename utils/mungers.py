import logging
import shutil
from abc import ABC, abstractmethod
from glob import iglob
from pathlib import Path

from .globals import Settings
from .logs import setup_logging
from .tools import level_pack, mkdir_p, munge, soundfl_munge, world_munge
from .tools import get_dir_no_case as _


class BaseMunger(ABC):
    """
    Abstract base class for all other mungers. Intended to handle common properties such as platform and language,
    as well as paths to common munge-related files and folders.
    """

    def __init__(self, source_subdir: str, platform: str = "PC"):
        self.platform: str = platform
        self.source_dir = _(Path("..") / source_subdir)
        self.munge_dir = _(Path(source_subdir) / "MUNGED" / platform)

    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError

    def _copy_premunged_files(self):
        pre_munged_dir = _(self.source_dir / "munged")
        if not pre_munged_dir.exists():
            return
        files = list(pre_munged_dir.iterdir())
        if len(files) > 0:
            logger = logging.getLogger("main")
            logger.info("Copying premunged files from %s", pre_munged_dir)
            for file in files:
                shutil.copy(file, self.munge_dir)
                logger.info("Copied %s", file.name)


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

    def run(self, localize: bool = True, shaders: bool = True, sprites: bool = True, fpm: bool = True):
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
        munge("Model", ["$effects/*.msh", "$MSHs/*.msh"], self.source_dir, self.munge_dir)
        if shaders is True and self.platform != "PS2":
            munge("Shader", ["shaders/*.xml", "shaders/*.vsfrag"], self.source_dir, self.munge_dir)

        common_sound_path = _(self.source_dir / "Sound")
        munge("Config", ["*.snd", "*.mus"], common_sound_path, self.munge_dir, hash_strings=True)
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
            shutil.rmtree(self.munge_temp_name)

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
            common_files = [f"{common_munge_dir}/{file}" for file in ["core", "common", "ingame"]]
            level_pack("req/*.req", self.source_dir, self.munge_dir, input_dir=input_dirs, common=common_files)
            level_pack("*.req", self.source_dir, self.output_dir, input_dir=input_dirs)


class WorldMunger(BaseMunger):
    """
    Handles munging of a single world.
    """

    def __init__(self, world: str, platform="PC"):
        self.world = world
        super().__init__(f"Worlds/{self.world}", platform)
        self.output_dir = Settings.output_dir / self.world.upper()

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Worlds/%s...", self.world)

        mkdir_p(self.munge_dir)

        self._copy_premunged_files()

        munge("Odf", "$*.odf", self.source_dir, self.munge_dir)
        munge("Model", "$*.msh", self.source_dir, self.munge_dir)
        munge("Texture", ["$*.tga", "$*.pic"], self.source_dir, self.munge_dir)
        munge("Terrain", "$*.ter", self.source_dir, self.munge_dir)
        munge("World", "$*.lyr", self.source_dir, self.munge_dir)
        munge("World", "$*.wld", self.source_dir, self.munge_dir)

        for wld_file in self.source_dir.glob("**/*.wld"):
            world_munge(
                f"${wld_file.stem}*.pth",
                self.source_dir,
                self.munge_dir,
                output_file=wld_file.stem,
                chunk_id="path",
                ext="path"
            )

        munge("PathPlanning", "$*.pln", self.source_dir, self.munge_dir)
        munge("Config", "$effects/*.fx", self.source_dir, self.munge_dir)
        munge("Config", "$*.combo", self.source_dir, self.munge_dir)

        world_munge("$*.sky", self.source_dir, self.munge_dir, chunk_id="sky")
        world_munge("$*.fx", self.source_dir, self.munge_dir, chunk_id="fx", ext="envfx")
        world_munge("$*.prp", self.source_dir, self.munge_dir, hash_strings=True, chunk_id="prp", ext="prop")
        world_munge("$*.bnd", self.source_dir, self.munge_dir, hash_strings=True, chunk_id="bnd", ext="boundary")

        munge("Config", ["$*.snd", "$*.mus", "$*.tsr"], _(self.source_dir / "Sound"), self.munge_dir, hash_strings=True)

        world_munge("$*.lgt", self.source_dir, self.munge_dir, hash_strings=True, chunk_id="lght", ext="light")
        world_munge("$*.pvs", self.source_dir, self.munge_dir, chunk_id="PORT", ext="povs")

        common_munge_dir = _(Path(f"Common/MUNGED/{self.platform}"))
        worlds_common_munge_dir = _(Path(f"Worlds/Common/MUNGED/{self.platform}"))

        mkdir_p(self.output_dir)

        if self.world != "Common":
            input_dirs = [self.munge_dir, worlds_common_munge_dir, common_munge_dir]
            common_files = [f"{common_munge_dir}/{file}" for file in ["core", "common", "ingame"]]
            for world in self.source_dir.glob("world*"):
                level_pack(
                    "*.req",
                    world,
                    input_dir=input_dirs,
                    common=common_files,
                    write_files=[f"{self.munge_dir}/MZ", ],
                    relative_write=True
                )
                level_pack(
                    "*.mrq",
                    world,
                    output_dir=self.munge_dir,
                    input_dir=input_dirs,
                    common=common_files + [f"{self.munge_dir}/MZ"],
                )
                level_pack(
                    "*.req",
                    world,
                    output_dir=self.output_dir,
                    input_dir=input_dirs,
                    common=common_files
                )

            level_pack(
                "*.req",
                _(self.source_dir / "sky" / "REQ"),
                self.output_dir,
                input_dir=input_dirs,
                common=common_files
            )
            level_pack(
                "*.req",
                _(self.source_dir / "sky"),
                self.output_dir,
                input_dir=input_dirs,
                common=common_files
            )


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
