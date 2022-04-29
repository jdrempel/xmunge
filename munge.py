#!/usr/bin/python3
# munge.py
# jedimoose32
#
# The main entrypoint for the munge process
import logging
from os import remove
from pathlib import Path
from shutil import copytree, move

from xm.mungers import *
from xm.utils.args import build_actions_list, parse_args
from xm.utils.globals import Settings
from xm.utils.logs import setup_logging
from xm.utils.tools import mkdir_p


if __name__ == "__main__":

    ###################
    # Parse arguments #
    ###################

    args = parse_args()

    munge_list = build_actions_list(args)

    setup_logging(debug=args.debug_mode, platform=args.platform)

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
        with open("../../.swbf2", "r") as swbf2_file:
            gamedata_dir = Path(swbf2_file.readline())

    except FileNotFoundError:
        input_dir = Path(input("Enter the path to your SWBF2 GameData folder: "))
        gamedata_dir = input_dir.resolve()
        while not gamedata_dir.exists():
            print(f"The path {gamedata_dir} does not exist.")
            input_dir = Path(input("Enter the path to your SWBF2 GameData folder: "))
            gamedata_dir = input_dir.resolve()

        with open("../../.swbf2", "w") as swbf2_file:
            swbf2_file.write(str(gamedata_dir))
            print(
                f"Saved {gamedata_dir} to the file .swbf2 in the BF2_ModTools root directory."
            )

    ##########
    # Munge! #
    ##########

    if munge_list["common"]:
        munger = CommonMunger(Settings.platform)
        munger.run()

    if munge_list["shell"]:
        munger = ShellMunger(Settings.platform)
        munger.run(movies=munge_list["movies"])

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

    if munge_list["common"] or munge_list["addme"]:
        munger = AddmeMunger(Settings.platform)
        munger.run()

    if Settings.platform == "XBOX" and not args.no_xbox_copy:
        pass

    #########################################
    # Copy _LVL_platform to SWBF2 directory #
    #########################################

    copy_source = Settings.output_dir
    world_id = Path.cwd().parent.name.upper().split("_")[-1]
    copy_dest = gamedata_dir / "addon" / world_id / "data" / f"_LVL_{Settings.platform}"

    mkdir_p(copy_dest)

    logger = logging.getLogger("main")
    logger.info("Copying output files to SWBF2 GameData/addon/%s...", world_id)
    copytree(copy_source, copy_dest, dirs_exist_ok=True)

    # Move addme.script from ABC/data/_LVL_PC/ up to just ABC/
    remove(copy_dest.parent.parent / "addme.script")
    move(copy_dest / "addme.script", copy_dest.parent.parent)
