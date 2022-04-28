import logging
from pathlib import Path

from xm.utils.globals import Settings
from xm.utils.tools import level_pack, mkdir_p, munge, world_munge
from xm.utils.tools import get_dir_no_case as _
from .base import BaseMunger


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
                ext="path",
            )

        munge("PathPlanning", "$*.pln", self.source_dir, self.munge_dir)
        munge("Config", "$effects/*.fx", self.source_dir, self.munge_dir)
        munge("Config", "$*.combo", self.source_dir, self.munge_dir)

        world_munge("$*.sky", self.source_dir, self.munge_dir, chunk_id="sky")
        world_munge(
            "$*.fx", self.source_dir, self.munge_dir, chunk_id="fx", ext="envfx"
        )
        world_munge(
            "$*.prp",
            self.source_dir,
            self.munge_dir,
            hash_strings=True,
            chunk_id="prp",
            ext="prop",
        )
        world_munge(
            "$*.bnd",
            self.source_dir,
            self.munge_dir,
            hash_strings=True,
            chunk_id="bnd",
            ext="boundary",
        )

        munge(
            "Config",
            ["$*.snd", "$*.mus", "$*.tsr"],
            _(self.source_dir / "Sound"),
            self.munge_dir,
            hash_strings=True,
        )

        world_munge(
            "$*.lgt",
            self.source_dir,
            self.munge_dir,
            hash_strings=True,
            chunk_id="lght",
            ext="light",
        )
        world_munge(
            "$*.pvs", self.source_dir, self.munge_dir, chunk_id="PORT", ext="povs"
        )

        common_munge_dir = _(Path(f"Common/MUNGED/{self.platform}"))
        worlds_common_munge_dir = _(Path(f"Worlds/Common/MUNGED/{self.platform}"))

        mkdir_p(self.output_dir)

        if self.world != "Common":
            input_dirs = [self.munge_dir, worlds_common_munge_dir, common_munge_dir]
            common_files = [
                f"{common_munge_dir}/{file}" for file in ["core", "common", "ingame"]
            ]
            for world in self.source_dir.glob("world*"):
                level_pack(
                    "*.req",
                    world,
                    input_dir=input_dirs,
                    common=common_files,
                    write_files=[
                        f"{self.munge_dir}/MZ",
                    ],
                    relative_write=True,
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
                    common=common_files,
                )

            level_pack(
                "*.req",
                _(self.source_dir / "sky" / "REQ"),
                self.output_dir,
                input_dir=input_dirs,
                common=common_files,
            )
            level_pack(
                "*.req",
                _(self.source_dir / "sky"),
                self.output_dir,
                input_dir=input_dirs,
                common=common_files,
            )
