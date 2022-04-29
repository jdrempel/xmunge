from argparse import ArgumentParser, Namespace
from typing import Any

from .globals import Settings
from .validators import ArgumentValidator


def parse_args(clean: bool = False) -> Namespace:
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
    if not clean:
        parser.add_argument("--noxboxcopy", action="store_true", dest="no_xbox_copy")

    # "Add-on" arguments (for convenience)
    parser.add_argument("--addme", action="store_true")
    if not clean:
        parser.add_argument("--wine-prefix", nargs="?", type=str)

    parser.add_argument("-d", action="store_true", dest="debug_mode")

    args = parser.parse_args()

    if args.wine_prefix:
        Settings.wine_prefix = args.wine_prefix

    validator = ArgumentValidator(args)
    validator.validate_args()

    Settings.set_platform(args.platform.upper())

    return args


def build_actions_list(args: Namespace) -> dict[Any]:
    action_all = True
    action_list = dict(vars(args))
    action_list.pop("platform")
    action_list.pop("language")
    action_list.pop("no_xbox_copy")
    action_list.pop("wine_prefix")
    action_list.pop("debug_mode")
    if any(action_list.values()):
        action_all = False

    if action_all:
        action_list["worlds"] = "EVERYTHING"
        action_list["sides"] = "EVERYTHING"
        action_list["load"] = True
        action_list["common"] = True
        action_list["shell"] = True
        action_list["movies"] = True
        action_list["localize"] = True
        action_list["sound"] = True

    return action_list
