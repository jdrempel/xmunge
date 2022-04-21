# munge.py
# jedimoose32
#
# The main entrypoint for the munge process


from abc import ABC
from argparse import ArgumentParser
import logging as log
from pathlib import Path


def setup_logging():
    """
    Initializes the level, formatting, and file/console handlers for the main logger.
    The main logger has a file handler with level INFO and a console handler with level DEBUG.
    TODO Make the console handler log level configurable
    :return: None
    """

    logger = log.getLogger("main")
    logger.setLevel(log.DEBUG)
    formatter = log.Formatter(fmt="%(asctime)s [%(levelname)s]:  %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")

    log_filename = f"{args.platform.upper()}_MungeLog.txt"
    file_handler = log.FileHandler(log_filename, "w")
    file_handler.setLevel(log.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = log.StreamHandler()
    console_handler.setLevel(log.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class ArgumentValidator:
    """
    A utility class for validating command-line argument values.
    """

    platforms = [
        "PC",
        "PS2",
        "XBOX",
    ]

    languages = [
        "ENGLISH",
        "FRENCH",
        "GERMAN",
        "ITALIAN",
        "JAPANESE"
        "SPANISH",
        "UK",
    ]

    def __init__(self, args_):
        self.args = args_

    def _validate_platform(self):
        """
        Determines whether the platform supplied in the args is valid.
        :return: True if the platform is None or in the list of valid platform strings, False otherwise
        """
        return self.args.platform is None or self.args.platform.upper() in self.platforms

    def _validate_language(self):
        """
        Determines whether the language supplied in the args is valid.
        :return: True if the language is None or in the list of valid language strings, False otherwise
        """
        return self.args.language is None or self.args.language.upper() in self.languages

    def validate_args(self):
        """
        Performs a full validation of all applicable args (platform, language), raising an exception if validation
        fails for some reason.
        :raise: RuntimeError if either the platform or the language is invalid
        :return: None
        """
        if not self._validate_platform():
            raise RuntimeError(f"Invalid platform {self.args.platform}")

        if not self._validate_language():
            raise RuntimeError(f"Invalid language {self.args.language}")


class Munger(ABC):

    def __init__(self, platform="PC"):
        self.platform = platform


class WorldMunger(Munger):

    def __init__(self, world, platform="PC"):
        super().__init__(platform)
        self.world = world


class SideMunger(Munger):

    def __init__(self, side, platform="PC"):
        super().__init__(platform)
        self.side = side


if __name__ == "__main__":

    ###################
    # Parse arguments #
    ###################

    parser = ArgumentParser()
    parser.add_argument("--platform", nargs="?", type=str, default="PC")
    parser.add_argument("--language", nargs="?", type=str)
    parser.add_argument("--world", nargs="+", type=str, dest="worlds")
    parser.add_argument("--side", nargs="+", type=str, dest="sides")
    parser.add_argument("--load", action="store_true")
    parser.add_argument("--sound", action="store_true")
    parser.add_argument("--common", action="store_true")
    parser.add_argument("--shell", action="store_true")
    parser.add_argument("--movies", action="store_true")
    parser.add_argument("--localize", action="store_true")
    parser.add_argument("--noxboxcopy", action="store_true", dest="no_xbox")

    args = parser.parse_args()

    validator = ArgumentValidator(args)
    validator.validate_args()

    munge_all = True
    munge_list = vars(args)
    munge_list.pop("platform")
    munge_list.pop("language")
    munge_list.pop("no_xbox")
    if any(munge_list.values()):
        munge_all = False

    # Setup logging
    setup_logging()

    ###################
    # Post processing #
    ###################

    munge_platform = args.platform.upper()

    if munge_all:
        munge_list["worlds"] = ["EVERYTHING"]
        munge_list["sides"] = ["EVERYTHING"]
        munge_list["load"] = True
        munge_list["sides"] = True
        munge_list["common"] = True
        munge_list["shell"] = True
        munge_list["movies"] = True
        munge_list["localize"] = True
        munge_list["sound"] = True

    # Language stuff
    munge_lang_ver = "ENGLISH"
    munge_lang_dir = "ENG"
    munge_override_path = None

    if args.language is not None:
        munge_platform = args.language.upper()
        munge_lang_dir = munge_platform
        munge_lang_ver = munge_platform

        if munge_platform == "ENGLISH":
            munge_lang_dir = "ENG"
            munge_lang_ver = ""
        elif munge_platform == "UK":
            munge_lang_dir = "UK_"
            munge_lang_ver = munge_lang_dir

    if munge_lang_ver != "ENGLISH":
        munge_override_path = Path(f"{munge_platform}_{munge_lang_dir}")

    ##########
    # Munge! #
    ##########

    munge_bin_path = Path("../../ToolsFL/bin")

    if munge_list["common"]:
        pass

    if munge_list["shell"]:
        pass

    if munge_list["load"]:
        pass

    if munge_list["sides"]:
        pass

    if munge_list["worlds"]:
        pass

    if munge_list["sounds"]:
        pass

    if munge_platform == "XBOX" and not args.no_xbox:
        pass

    # Done!
