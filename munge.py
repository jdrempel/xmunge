# munge.py
# jedimoose32
#
# The main entrypoint for the munge process


from argparse import ArgumentParser


class ArgumentValidator:

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
        return self.args.platform is None or self.args.platform.upper() in self.platforms

    def _validate_language(self):
        return self.args.language is None or self.args.language.upper() in self.languages

    def validate_args(self):
        if not self._validate_platform():
            raise RuntimeError(f"Invalid platform {self.args.platform}")

        if not self._validate_language():
            raise RuntimeError(f"Invalid language {self.args.language}")


if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("--platform", nargs="?", type=str, default="PC")
    parser.add_argument("--language", nargs="?", type=str, default="ENGLISH")
    parser.add_argument("--world", nargs="+", type=str, dest="worlds")
    parser.add_argument("--side", nargs="+", type=str, dest="sides")
    parser.add_argument("--load", nargs="?", type=str, const=False)
    parser.add_argument("--sound", nargs="?", type=str, const=False)
    parser.add_argument("--common", nargs="?", type=str, const=False)
    parser.add_argument("--shell", nargs="?", type=str, const=False)
    parser.add_argument("--movies", nargs="?", type=str, const=False)
    parser.add_argument("--localize", nargs="?", type=str, const=False)
    parser.add_argument("--noxboxcopy", nargs="?", type=str, dest="no_xbox",
                        const=False)

    args = parser.parse_args()

    validator = ArgumentValidator(args)
    validator.validate_args()

    munge_all = True
    munge_list = vars(args)
    munge_list.pop("platform")
    munge_list.pop("language")
    munge_list.pop("no_xbox")

    if any([v for k, v in munge_list.items()]):
        munge_all = False

    print(munge_all)
    # Post process
    # Setup logging
    # Munge!
