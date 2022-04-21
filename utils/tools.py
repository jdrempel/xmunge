import subprocess as sp

from globals import Settings


def level_pack(input_files, source_dir, output_dir, input_dir=None, common=None, write_files=None):
    inputs = input_files
    if isinstance(input_files, list):
        inputs = " ".join(input_files)

    inputdir = input_dir if not None else Settings.munge_dir

    command = [
        "LevelPack",
        f"-inputfile {inputs}",
        f"-outputdir {output_dir}",
        f"-inputdir {inputdir}",
        f"-sourcedir {source_dir}"
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

    args = [
        "wine",
        " ".join(command),
        "2>>PC_MungeLog.txt"
    ]
    print(args)


Settings.set_platform("PC")
level_pack(["a", "b", "c"], "source", "output", "inputdir", ["com1", "../com2"], ["write1", "write2"])


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
