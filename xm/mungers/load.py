import logging
from glob import iglob
from os import remove
from shutil import rmtree

from xm.utils.globals import Settings
from xm.utils.tools import level_pack, mkdir_p, munge
from xm.utils.tools import get_dir_no_case as _
from .base import BaseMunger


class LoadMunger(BaseMunger):
    """
    Handles munging of load screen data.
    """

    temp_name = "__TEMP__"

    def __init__(self, platform="PC"):
        super().__init__("Load", platform)
        self.output_dir = Settings.output_dir / "Load"

    def run(self):
        logger = logging.getLogger("main")
        logger.info("Munge Load...")

        mkdir_p(_(self.munge_dir))
        self._copy_premunged_files()

        munge("Config", "$*.cfg", self.source_dir, self.munge_dir, chunkid="load", ext="config")
        munge("Texture", ["$*.tga", "$*.pic"], self.source_dir, self.munge_dir)
        munge("Model", "$*.msh", self.source_dir, self.munge_dir)

        req_temp_dir = self.source_dir / self.temp_name
        mkdir_p(req_temp_dir)

        backdrop_dir = self.source_dir / "backdrops"
        all_files = []
        for backdrop in backdrop_dir.iterdir():
            if not backdrop.is_dir():
                continue
            tga_files = list(backdrop.glob("*.tga"))
            tga_files += list(backdrop.glob(f"{self.platform}/*.tga"))
            pic_files = list(backdrop.glob("*.pic"))
            pic_files += list(backdrop.glob(f"{self.platform}/*.pic"))
            all_files = tga_files + pic_files
            for file in all_files:
                with open(req_temp_dir / f"{file.stem}.req", "w") as req_file:
                    req_file.write(f"ucft{{ REQN {{ \"texture\" \"{file.stem}\" }} }}")

        level_pack("$*.req", req_temp_dir, self.munge_dir, self.munge_dir, common=[f"Common/MUNGED/{self.platform}/core.files", ])

        for item in iglob(f"{req_temp_dir}/*.*"):
            remove(item)

        for backdrop in backdrop_dir.iterdir():
            if not backdrop.is_dir():
                continue
            with open(req_temp_dir / f"{backdrop.name}.req", "w") as req_file:
                req_file.write(f"ucft{{ REQN {{ \"lvl\"\n")
                for file in all_files:
                    req_file.write(f"\"{file.stem}\"\n")
                req_file.write(f"}} }}")

        mkdir_p(_(self.output_dir))

        # NOTE: If this isn't working I think it's because the input_dir should be the temp dir
        level_pack("$*.req", self.source_dir, self.output_dir, self.munge_dir, common=[f"Common/MUNGED/{self.platform}/core.files", ])

        rmtree(req_temp_dir)
        remove(req_temp_dir)
