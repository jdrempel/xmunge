import logging
from abc import ABC, abstractmethod
from pathlib import Path
from shutil import copy

from xm.utils.tools import get_dir_no_case as _


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
                copy(file, self.munge_dir)
                logger.info("Copied %s", file.name)


