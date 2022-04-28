# munge.py
# jedimoose32
#
# The main entrypoint for the munge process

from argparse import ArgumentParser
from pathlib import Path

from utils.globals import Settings
from utils.logs import setup_logging
from utils.mungers import (
    CommonMunger,
    LoadMunger,
    ShellMunger,
    SideMunger,
    SoundMunger,
    WorldMunger,
)
from utils.validators import ArgumentValidator


if __name__ == "__main__":

    ###################
    # Parse arguments #
    ###################

    parser = ArgumentParser()

    # "Built-in" arguments (from old munge.bat)
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

    # "Add-on" arguments (for convenience)
    parser.add_argument("--wine-prefix", nargs="?", type=str)
    parser.add_argument("-d", action="store_true", dest="debug_mode")

    args = parser.parse_args()

    if args.wine_prefix:
        Settings.wine_prefix = args.wine_prefix

    validator = ArgumentValidator(args)
    validator.validate_args()

    Settings.set_platform(args.platform.upper())

    munge_all = True
    munge_list = dict(vars(args))
    munge_list.pop("platform")
    munge_list.pop("language")
    munge_list.pop("no_xbox_copy")
    if any(munge_list.values()):
        munge_all = False

    # Setup logging
    setup_logging(debug=args.debug_mode, platform=args.platform)

    ###################
    # Post processing #
    ###################

    if munge_all:
        munge_list["worlds"] = "EVERYTHING"
        munge_list["sides"] = "EVERYTHING"
        munge_list["load"] = True
        munge_list["common"] = True
        munge_list["shell"] = True
        munge_list["movies"] = True
        munge_list["localize"] = True
        munge_list["sound"] = True

    # Language stuff
    if args.language is not None:
        Settings.platform = args.language.upper()
        Settings.lang_dir = Settings.platform
        Settings.lang_version = Settings.platform

        if Settings.platform == "ENGLISH":
            Settings.lang_dir = "ENG"
            Settings.lang_version = ""
        elif Settings.platform == "UK":
            Settings.lang_dir = "UK_"
            Settings.lang_version = Settings.lang_dir

    if Settings.lang_version != "ENGLISH":
        Settings.override_path = Path(f"{Settings.platform}_{Settings.lang_dir}")

    ################################################################################
    # Get SWBF2 GameData directory from file if it exists, otherwise prompt for it #
    ################################################################################

    try:
        with open(".swbf2", "r") as swbf2_file:
            gamedata_dir = Path(swbf2_file.readline())

    except FileNotFoundError:
        input_dir = Path(input("Enter the path to your SWBF2 GameData folder: "))
        gamedata_dir = input_dir.resolve()
        while not gamedata_dir.exists():
            print(f"The path {gamedata_dir} does not exist.")
            input_dir = Path(input("Enter the path to your SWBF2 GameData folder: "))
            gamedata_dir = input_dir.resolve()

        with open(".swbf2", "w") as swbf2_file:
            swbf2_file.write(str(gamedata_dir))
            print(f"Saved {gamedata_dir} to the file .swbf2 in this directory.")

    ##########
    # Munge! #
    ##########

    if munge_list["common"]:
        munger = CommonMunger(Settings.platform)
        munger.run()

    if munge_list["shell"]:
        munger = ShellMunger(Settings.platform)
        munger.run()

    if munge_list["load"]:
        munger = LoadMunger(Settings.platform)
        munger.run()

    if munge_list["sides"]:
        sides_to_munge = munge_list["sides"]
        # TODO detect whether Common and Sides/Common are already munged and if not, always munge them first
        if munge_list["sides"] == "EVERYTHING":
            sides_to_munge = [i.name for i in Path("../Sides").iterdir() if i.is_dir()]
        for side in sides_to_munge:
            munger = SideMunger(side, Settings.platform)
            munger.run()

    if munge_list["worlds"]:
        worlds_to_munge = munge_list["worlds"]
        if munge_list["worlds"] == "EVERYTHING":
            worlds_to_munge = [
                i.name for i in Path("../Worlds").iterdir() if i.is_dir()
            ]
        for world in worlds_to_munge:
            munger = WorldMunger(world, Settings.platform)
            munger.run()

    if munge_list["sound"]:
        munge_sound_streams = True
        munger = SoundMunger(Settings.platform, munge_sound_streams)
        munger.run()

    if Settings.platform == "XBOX" and not args.no_xbox_copy:
        pass

    # Done!

    ###############
    # Munge addme #
    ###############

    pass
