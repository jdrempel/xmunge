from xm.utils.args import build_actions_list, parse_args
from xm.utils.logs import setup_logging


if __name__ == "__main__":

    ###################
    # Parse arguments #
    ###################

    args = parse_args(clean=True)

    clean_list = build_actions_list(args)

    setup_logging(debug=args.debug_mode, platform=args.platform)
