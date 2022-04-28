from pathlib import Path


class Settings:

    platform = "PC"

    # Fixed paths
    root_dir = Path("../..")
    bin_path = Path("../../ToolsFL/bin")

    # Variable paths, will be set later as they depend on the platform or language
    munge_dir = None
    output_dir = None
    override_path = None

    lang_version = "ENGLISH"
    lang_dir = "ENG"

    munge_args = None
    shader_munge_args = None

    wine_prefix = None

    @classmethod
    def set_platform(cls, platform: str) -> None:
        """
        Class method for setting the platform and updating all other members that rely on the platform value.
        :param platform: A string, either "PC", "PS2", or "XBOX"
        :return: None
        """
        cls.platform = platform.upper()

        cls.munge_dir = Path(f"MUNGED/{cls.platform}")
        cls.output_dir = Path(f"../_LVL_{cls.platform}")

        cls.munge_args = f"-checkdate -continue -platform {cls.platform}"
        cls.shader_munge_args = (
            f"-continue -platform {cls.platform}"  # TODO why not checkdate?
        )
