import logging
from os import remove
from pathlib import Path
from shutil import rmtree
from typing import Union

from xm.utils.args import build_actions_list, parse_args
from xm.utils.dirs import get_swbf2_path, get_world_id
from xm.utils.globals import Settings
from xm.utils.logs import setup_logging
from xm.utils.tools import get_dir_no_case as _


def clean_addme() -> None:
    """
    Performs a clean of the munged addme.script file in _BUILD/../addme/munged/
    :return: None
    """
    addme_script = Path.cwd().parent / "addme" / "munged" / "addme.script"
    if not addme_script.exists():
        return
    remove(addme_script)


def clean_subdir(subdir: Union[str, Path]) -> None:
    """
    Performs a clean of the munged files in _BUILD/<subdir>/MUNGED/**/
    :param subdir: The subdirectory of _BUILD to clean inside of
    :return: None
    """
    clean_dir = Path.cwd() / subdir / "MUNGED"
    if not clean_dir.exists():
        return
    for item in clean_dir.iterdir():
        if item.is_dir():
            rmtree(item)
        else:
            remove(item)


def clean_outputs() -> None:
    """
    Removes all items in _BUILD/../_LVL_<platform>/ and <SWBF2-GameData>/addon/<ABC>/
    :return: None
    """
    mLogger = logging.getLogger("main")
    if not Settings.output_dir.exists():
        return

    mLogger.info("Deleting contents of %s...", Settings.output_dir)
    for item in Settings.output_dir.iterdir():
        if item.is_dir():
            rmtree(item)
        else:
            remove(item)

    addon_dir = get_swbf2_path() / "addon" / get_world_id()
    if not addon_dir.exists():
        return

    mLogger.info("Removing %s from %s...", get_world_id(), get_swbf2_path() / "addon")
    rmtree(addon_dir)


if __name__ == "__main__":

    ###################
    # Parse arguments #
    ###################

    args = parse_args(clean=True)

    clean_list = build_actions_list(args)

    setup_logging(debug=args.debug_mode, platform=args.platform)

    gamedata_dir = get_swbf2_path()

    logger = logging.getLogger("main")

    if clean_list["common"]:
        logger.info("Cleaning Common...")
        clean_subdir("Common")

    if clean_list["shell"]:
        logger.info("Cleaning Shell...")
        clean_subdir("Shell")

    if clean_list["load"]:
        logger.info("Cleaning Load...")
        clean_subdir("Load")

    if clean_list["sides"]:
        sides_to_clean = clean_list["sides"]
        if clean_list["sides"] == "EVERYTHING":
            sides_to_clean = [i.name for i in Path("../Sides").iterdir() if i.is_dir()]
        for side in sides_to_clean:
            logger.info("Cleaning Sides/%s...", side.upper())
            side_path = Path(f"Sides/{side}")
            clean_subdir(_(side_path))

    if clean_list["worlds"]:
        worlds_to_clean = clean_list["worlds"]
        if clean_list["worlds"] == "EVERYTHING":
            worlds_to_clean = [i.name for i in Path("../Worlds").iterdir() if i.is_dir()]
        for world in worlds_to_clean:
            logger.info("Cleaning Worlds/%s...", world.upper())
            world_path = Path(f"Worlds/{world}")
            clean_subdir(_(world_path))

    if clean_list["sound"]:
        logger.info("Cleaning Sound...")
        clean_subdir("Sound")

    if clean_list["addme"]:
        logger.info("Cleaning addme...")
        clean_addme()

    if clean_list["all"]:
        clean_outputs()

    logger.info("Done cleaning!")
