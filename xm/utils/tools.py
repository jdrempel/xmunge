import logging as log
from pathlib import Path
from re import search
import subprocess as sp
from typing import Union

from .globals import Settings


def get_dir_no_case(dir_path: Path) -> Path:
    """
    Checks if a directory exists in given case, upper case, or lower case. If it exists, append the appropriate case to
    a new path and continue for each part of the path.
    :param dir_path: The path to check
    :return: A path object with possibly case-modified parts
    """
    rebuilt_path = []
    for part in dir_path.parts:
        partial_path = Path("/".join(rebuilt_path)) / part.upper()
        if partial_path.exists():
            rebuilt_path.append(part.upper())
            continue
        partial_path = Path("/".join(rebuilt_path)) / part.lower()
        if partial_path.exists():
            rebuilt_path.append(part.lower())
            continue
        rebuilt_path.append(part)
    return Path("/".join(rebuilt_path))


def mkdir_p(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _setup_wine() -> str:
    """
    Configures the WINEPATH to include the BF2_ModTools/ToolsFL/bin directory and sets the WINEPREFIX if it exists in
    Settings
    :return: A string of the format: "[WINEPREFIX=<prefix-path> ]WINEPATH=<path-to-tools-bin> wine"
    """
    current_dir = Path("")
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
    args = [_setup_wine(), " ".join(command), f"2>>{Settings.platform}_MungeLog.txt"]
    result = sp.run(" ".join(args), shell=True)
    result.check_returncode()


def level_pack(
    input_files: Union[str, list[str]],
    source_dir: Union[str, Path],
    output_dir: Union[str, Path] = None,
    input_dir: Union[str, Path, list[str], list[Path]] = None,
    common: Union[list[str], list[Path]] = None,
    write_files: Union[list[str], list[Path]] = None,
    relative_write: bool = False,
    debug: bool = False,
) -> None:
    """
    Invokes LevelPack.exe in Wine with the specified parameters
    :param input_files: The list of files or glob patterns to pass as inputs
    :param source_dir: The directory from which to load un-processed source files
    :param output_dir: (Optional) The directory in which to place packed .lvl files
    :param input_dir: (Optional) The directory from which to load pre-processed source files
    :param common: (Optional) A list of files from which to draw common info
    :param write_files: (Optional) A list of non-lvl artifact files to be written
    :param relative_write: (Optional) If True, does not prepend write_files entries with source_subdir/munge_dir/
    :param debug: (Optional) If True, starts LevelPack.exe with the -DEBUG flag
    :return: None
    """
    inputs = input_files
    if isinstance(input_files, list):
        inputs = " ".join(input_files)

    input_dirs = input_dir
    if isinstance(input_dir, list):
        input_dirs = " ".join([str(d) for d in input_dir])

    source_subdir = source_dir.stem

    command = [
        "LevelPack",
        f"-inputfile {inputs}",
        f"-inputdir {input_dirs}",
        f"-sourcedir {source_dir}",
        Settings.munge_args,
    ]

    if common:
        common_str = "-common"
        for common_file in [f"{c}.files" for c in common]:
            if (
                common_file.startswith(".")
                or common_file.startswith("Common")
                or common_file.startswith("Worlds")
            ):
                common_str += f" {common_file}"
            else:
                common_str += f" {source_subdir}/{Settings.munge_dir}/{common_file}"

        command.append(common_str)

    if write_files:
        to_write = [f"{w}.files" for w in write_files]
        if relative_write:
            command.append(f"-writefiles {f' '.join(to_write)}")
        else:
            command.append(
                f"-writefiles {source_subdir}/{Settings.munge_dir}/"
                f"{f' {source_subdir}/{Settings.munge_dir}/'.join(to_write)}"
            )

    if output_dir:
        command.append(f"-outputdir {output_dir}")
    else:
        command.append("-onlyfiles")

    if debug:
        command.append("-debug")

    logger = log.getLogger("main")

    try:
        logger.debug(" ".join(command))
        _exec_wine(command)
    except sp.CalledProcessError as err:
        logger.error(
            'LevelPack failed with args "%s"; Status %d.',
            " ".join(command[1:]),
            err.returncode,
        )

    try:
        with open("LevelPack.log", "r") as levelpack_log:
            log_contents = str(levelpack_log.read())
            if len(log_contents) > 70:
                logger.info(log_contents)
    except FileNotFoundError as err:
        logger.warning("Log file %s not found, continuing...", err.filename)


def _prepare_munge():
    pass


def _execute_munge():
    pass


def munge(
    category: str,
    input_files: Union[str, list[str]],
    source_dir: Union[str, Path],
    output_dir: Union[str, Path],
    hash_strings: bool = False,
    debug: bool = False,
) -> None:
    """
    Invokes <category>Munge.exe in Wine with the specified parameters
    :param category: One of "Bin", "Config", "Font", etc
    :param input_files: A list of files or glob patterns to pass as input to the munge process
    :param source_dir: The directory from which to load un-processed source files
    :param output_dir: The directory in which to place the packed .lvl files
    :param hash_strings: (Optional) Flag determining whether strings in input files should be hashed during munge
    :param debug: (Optional) If True, run the munge application with -DEBUG set
    :return: None
    """
    inputs = input_files
    if isinstance(input_files, list):
        inputs = " ".join([f"'{file}'" for file in input_files])
    else:
        if not (input_files.startswith("'") and input_files.endswith("'")):
            inputs = f"'{input_files}'"

    prefix = ""
    if category in ["Model", "Shader", "Texture"]:
        prefix = Settings.platform.lower() + "_"

    command = [
        f"{prefix}{category}Munge",
        f"-inputfile {inputs}",
        f"-sourcedir {source_dir}",
        f"-outputdir {output_dir}",
        Settings.munge_args,
    ]

    if category == "Shader":
        command.append(f"-I {source_dir}/shaders/{Settings.platform}/")

    if hash_strings:
        command.append("-hashstrings")

    if debug:
        command.append("-debug")

    logger = log.getLogger("main")

    try:
        _exec_wine(command)
    except sp.CalledProcessError as err:
        logger.error(
            '%s failed with args "%s"; Status %d.',
            command[0],
            " ".join(command[1:]),
            err.returncode,
        )

    try:
        with open(f"{prefix}{category}Munge.log", "r") as munge_log:
            log_contents = str(munge_log.read())
            if not (
                search(r"0\s+Errors", log_contents)
                and search(r"0\s+Warnings", log_contents)
            ):
                log_contents = f"[{inputs}]\n" + log_contents
                logger.info(log_contents)
    except FileNotFoundError as err:
        logger.warning("Log file %s not found, continuing...", err.filename)


def localize_munge():
    pass


def movie_munge():
    pass


def path_munge():
    pass


def path_planning_munge():
    pass


def soundfl_munge():
    pass


def sprite_munge():
    pass


def world_munge(
    input_files: Union[str, list[str]],
    source_dir: Union[str, Path],
    output_dir: Union[str, Path],
    output_file: Union[str, Path] = None,
    chunk_id: str = None,
    ext: str = None,
    hash_strings: bool = False,
) -> None:
    inputs = input_files
    if isinstance(input_files, list):
        inputs = " ".join([f"'{file}'" for file in input_files])
    else:
        if not (input_files.startswith("'") and input_files.endswith("'")):
            inputs = f"'{input_files}'"

    command = [
        f"ConfigMunge",
        f"-inputfile {inputs}",
        f"-sourcedir {source_dir}",
        f"-outputdir {output_dir}",
        Settings.munge_args,
    ]

    if output_file:
        command.append(f"-outputfile {output_file}")

    if chunk_id:
        command.append(f"-chunkid {chunk_id}")

    if ext:
        command.append(f"-ext {ext}")

    if hash_strings:
        command.append("-hashstrings")

    logger = log.getLogger("main")

    try:
        _exec_wine(command)
    except sp.CalledProcessError as err:
        logger.error(
            '%s failed with args "%s"; Status %d.',
            command[0],
            " ".join(command[1:]),
            err.returncode,
        )

    try:
        with open(f"ConfigMunge.log", "r") as munge_log:
            log_contents = str(munge_log.read())
            if not (
                search(r"0\s+Errors", log_contents)
                and search(r"0\s+Warnings", log_contents)
            ):
                log_contents = f"[{inputs}]\n" + log_contents
                logger.info(log_contents)
    except FileNotFoundError as err:
        logger.warning("Log file %s not found, continuing...", err.filename)
