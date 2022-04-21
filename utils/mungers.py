from abc import ABC


class BaseMunger(ABC):
    """
    Abstract base class for all other mungers. Intended to handle common properties such as platform and language,
    as well as paths to common munge-related files and folders.
    """

    def __init__(self, platform="PC"):
        self.platform = platform


class CommonMunger(BaseMunger):
    """
    Handles munging of common data.
    """

    def __init__(self, platform="PC"):
        super().__init__(platform)


class ShellMunger(BaseMunger):
    """
    Handles munging of shell data.
    """

    def __init__(self, platform="PC"):
        super().__init__(platform)


class LoadMunger(BaseMunger):
    """
    Handles munging of load screen data.
    """

    def __init__(self, platform="PC"):
        super().__init__(platform)


class SoundMunger(BaseMunger):
    """
    Handles munging of sound data.
    """

    def __init__(self, platform="PC", streams=True):
        super().__init__(platform)
        self.munge_streams = streams


class SideMunger(BaseMunger):
    """
    Handles munging of a single side.
    """

    def __init__(self, side, platform="PC"):
        super().__init__(platform)
        self.side = side


class WorldMunger(BaseMunger):
    """
    Handles munging of a single world.
    """

    def __init__(self, world, platform="PC"):
        super().__init__(platform)
        self.world = world
