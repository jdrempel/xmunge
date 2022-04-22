from pathlib import Path
import subprocess as sp

from globals import Settings


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


def level_pack(input_files: list[str], source_dir: str, output_dir: str, input_dir: str = None,
               common: list[str] = None, write_files: list[str] = None, debug: bool = False) -> None:
    """
    Invokes LevelPack.exe in Wine with the specified parameters
    :raise CalledProcessError: If the return status of LevelPack.exe or wine is non-zero
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
        for common_file in common:
            if common_file.startswith("."):
                common_str += f" {common_file}"
            else:
                common_str += f" {Settings.munge_dir}/{common_file}"

        command.append(common_str)

    if write_files:
        command.append(f"-writefiles {Settings.munge_dir}/{f' {Settings.munge_dir}/'.join(write_files)}")

    if debug:
        command.append("-debug")

    args = [
        _setup_wine(),
        " ".join(command),
        f"2>>{Settings.platform}_MungeLog.txt"
    ]
    result = sp.run(" ".join(args), shell=True)
    result.check_returncode()


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


def odf_munge():
    pass


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
    level_pack(["a", "b", "c"], "source", "output", input_dir="inputdir", common=["com1", "../com2"],
               write_files=["write1", "write2"], debug=True)
