import logging as log
from shutil import move
from pathlib import Path
import subprocess as sp
from typing import Union

from globals import Settings
from logs import setup_logging


def _setup_wine() -> str:
    """
    Configures the WINEPATH to include the BF2_ModTools/ToolsFL/bin directory and sets the WINEPREFIX if it exists in
    Settings
    :return: A string of the format: "[WINEPREFIX=<prefix-path> ]WINEPATH=<path-to-tools-bin> wine"
    """
    current_dir = Path(".")
    tools_dir = current_dir / Settings.bin_path
    wine_str = ""
    if Settings.wine_prefix:
        wine_str = f"WINEPREFIX={Settings.wine_prefix} "
    wine_str = f"{wine_str}WINEPATH={tools_dir.resolve()} wine"
    return wine_str


def _exec_wine(command: list[str]) -> None:
    """
    Invokes Wine with the executable and parameters specified in the command list
    :raise CalledProcessError: If the return status of the executable or Wine is non-zero
    :param command: The list of strings for the executable and its arguments
    :return: None
    """
    args = [
        _setup_wine(),
        " ".join(command),
        f"2>>{Settings.platform}_MungeLog.txt"
    ]
    result = sp.run(" ".join(args), shell=True)
    result.check_returncode()


def level_pack(input_files: Union[str, list[str]], source_dir: Union[str, Path], output_dir: Union[str, Path],
               input_dir: Union[str, Path] = None, common: Union[list[str], list[Path]] = None,
               write_files: Union[list[str], list[Path]] = None, debug: bool = False) -> None:
    """
    Invokes LevelPack.exe in Wine with the specified parameters
    :param input_files: The list of files or glob patterns to pass as inputs
    :param source_dir: The directory from which to load un-processed source files
    :param output_dir: The directory in which to place packed .lvl files
    :param input_dir: (Optional) The directory from which to load pre-processed source files
    :param common: (Optional) A list of files from which to draw common info
    :param write_files: (Optional) A list of non-lvl artifact files to be written
    :param debug: (Optional) If True, starts LevelPack.exe with the -DEBUG flag
    :return: None
    """
    inputs = input_files
    if isinstance(input_files, list):
        inputs = " ".join(input_files)

    inputdir = input_dir if not None else Settings.munge_dir

    command = [
        "LevelPack",
        f"-inputfile {inputs}",
        f"-outputdir {output_dir}",
        f"-inputdir {inputdir}",
        f"-sourcedir {source_dir}",
        Settings.munge_args
    ]

    if common:
        common_str = "-common"
        for common_file in [f"{c}.files" for c in common]:
            if common_file.startswith("."):
                common_str += f" {common_file}"
            else:
                common_str += f" {Settings.munge_dir}/{common_file}"

        command.append(common_str)

    if write_files:
        to_write = [f"{w}.files" for w in write_files]
        command.append(f"-writefiles {Settings.munge_dir}/{f' {Settings.munge_dir}/'.join(to_write)}")

    if debug:
        command.append("-debug")

    logger = log.getLogger("main")

    try:
        _exec_wine(command)
    except sp.CalledProcessError as err:
        logger.error("LevelPack failed with args \"%s\"; Status %d.", " ".join(command[1:]), err.returncode)

    try:
        with open("LevelPack.log", "r") as levelpack_log:
            log_contents = str(levelpack_log.read())
            logger.info(log_contents)
    except FileNotFoundError as err:
        logger.warning("Log file %s not found, continuing...", err.filename)


def munge(category: str, input_files: Union[str, list[str]], source_dir: Union[str, Path],
          output_dir: Union[str, Path], hash_strings: bool = False) -> None:
    """
    Invokes <category>Munge.exe in Wine with the specified parameters
    :param category: One of "Bin", "Config", "Font", etc
    :param input_files: A list of files or glob patterns to pass as input to the munge process
    :param source_dir: The directory from which to load un-processed source files
    :param output_dir: The directory in which to place the packed .lvl files
    :param hash_strings: (Optional) Flag determining whether strings in input files should be hashed during munge
    :return: None
    """
    inputs = input_files
    if isinstance(input_files, list):
        inputs = " ".join(input_files)

    prefix = ""
    if category in ["Model", "Shader", "Texture"]:
        prefix = Settings.platform.lower() + "_"

    command = [
        f"{prefix}{category}Munge",
        f"-inputfile {inputs}",
        f"-sourcedir {source_dir}",
        f"-outputdir {output_dir}",
        Settings.munge_args
    ]

    if category == "Shader":
        command.append(f"-I {source_dir}/shaders/{Settings.platform}/")

    # TODO hashing
    if hash_strings:
        command.append("-hashstrings")

    logger = log.getLogger("main")

    try:
        _exec_wine(command)
    except sp.CalledProcessError as err:
        logger.error("%s failed with args \"%s\"; Status %d.", command[0], " ".join(command[1:]), err.returncode)

    if category in ["Config", ]:
        try:
            with open(f"{category}Munge.log", "r") as munge_log:
                log_contents = str(munge_log.read())
                logger.info(log_contents)
        except FileNotFoundError as err:
            logger.warning("Log file %s not found, continuing...", err.filename)


def bin_munge():
    pass


def config_munge():
    pass


def font_munge():
    pass


def localize_munge():
    pass


def movie_munge():
    pass


def odf_munge(input_files: Union[str, list[str], Path, list[Path]], source: Union[str, Path], output: Union[str, Path]):
    inputs = input_files
    if isinstance(input_files, str):
        inputs = [input_files, ]
    munge("Odf", inputs, source_dir=source, output_dir=output)


def path_munge():
    pass


def path_planning_munge():
    pass


def model_munge():
    pass


def shader_munge():
    pass


def texture_munge():
    pass


def script_munge():
    pass


def shadow_munge():
    pass


def soundfl_munge():
    pass


def sprite_munge():
    pass


def terrain_munge():
    pass


def world_munge():
    pass


if __name__ == "__main__":
    # Settings.wine_prefix = Path(".") / ".." / ".." / "ToolsFL" / "bin"
    # Settings.wine_prefix = Settings.wine_prefix.resolve()
    Settings.set_platform("PC")
    setup_logging("PC")
    level_pack(["a", "b", "c"], "source", "output", input_dir="inputdir", common=["com1", "../com2"],
               write_files=["write1", "write2"], debug=True)
    _munge("Config", ["*.mcfg", "*.sanm"])
