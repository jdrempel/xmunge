# munge.py
# jedimoose32
#
# The main entrypoint for the munge process

from argparse import ArgumentParser
from pathlib import Path

from utils.logging import setup_logging
from utils.mungers import SideMunger, WorldMunger
from utils.validators import ArgumentValidator


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
    parser.add_argument("--noxboxcopy", action="store_true", dest="no_xbox_copy")

    args = parser.parse_args()

    validator = ArgumentValidator(args)
    validator.validate_args()

    munge_all = True
    munge_list = dict(vars(args))
    munge_list.pop("platform")
    munge_list.pop("language")
    munge_list.pop("no_xbox_copy")
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
        for side in munge_list["sides"]:
            munger = SideMunger(side, munge_platform)

    if munge_list["worlds"]:
        for world in munge_list["worlds"]:
            munger = WorldMunger(world, munge_platform)

    if munge_list["sound"]:
        pass

    if munge_platform == "XBOX" and not args.no_xbox_copy:
        pass

    # Done!
