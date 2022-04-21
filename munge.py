# munge.py
# jedimoose32
#
# The main entrypoint for the munge process


from argparse import ArgumentParser
import logging as log


def setup_logging():

    logger = log.getLogger("main")
    logger.setLevel(log.DEBUG)
    formatter = log.Formatter(fmt="%(asctime)s [%(levelname)s]:  %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")

    log_filename = f"{args.platform.upper()}_MungeLog.txt"
    file_handler = log.FileHandler(log_filename, "w")
    file_handler.setLevel(log.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = log.StreamHandler()
    console_handler.setLevel(log.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


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
    parser.add_argument("--load", action="store_true")
    parser.add_argument("--sound", action="store_true")
    parser.add_argument("--common", action="store_true")
    parser.add_argument("--shell", action="store_true")
    parser.add_argument("--movies", action="store_true")
    parser.add_argument("--localize", action="store_true")
    parser.add_argument("--noxboxcopy", action="store_true", dest="no_xbox")

    args = parser.parse_args()

    validator = ArgumentValidator(args)
    validator.validate_args()

    setup_logging()

    munge_all = True
    munge_list = vars(args)
    munge_list.pop("platform")
    munge_list.pop("language")
    munge_list.pop("no_xbox")
    if any(munge_list.values()):
        munge_all = False

    log.getLogger("main").debug("munge_all %d", munge_all)

    # Post process
    if munge_all:
        munge_list["worlds"] = ["EVERYTHING"]
        munge_list["sides"] = ["EVERYTHING"]
        munge_list["load"] = True
        munge_list["sides"] = True
        munge_list["common"] = True
        munge_list["shell"] = True
        munge_list["movies"] = True
        munge_list["localize"] = True
        munge_list["sound"] = True

    # Setup logging
    # Munge!
