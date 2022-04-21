from abc import ABC


class Munger(ABC):
    """
    Abstract base class for all other mungers. Intended to handle common properties such as platform and language,
    as well as paths to common munge-related files and folders.
    """

    def __init__(self, platform="PC"):
        self.platform = platform


class SideMunger(Munger):
    """
    Handles munging of a single side.
    """

    def __init__(self, side, platform="PC"):
        super().__init__(platform)
        self.side = side


class WorldMunger(Munger):
    """
    Handles munging of a single world.
    """

    def __init__(self, world, platform="PC"):
        super().__init__(platform)
        self.world = world
