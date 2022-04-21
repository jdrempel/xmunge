# munge.py
# jedimoose32
#
# The main entrypoint for the munge process


from argparse import ArgumentParser


if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("--platform", nargs="?", type=str, default="pc")
    parser.add_argument("--language", nargs="?", type=str, const=True)
    parser.add_argument("--world", nargs="+", type=str, dest="worlds")
    parser.add_argument("--side", nargs="+", type=str, dest="sides")
    parser.add_argument("--load", nargs="?", type=str, const=True)
    parser.add_argument("--sound", nargs="?", type=str, const=True)
    parser.add_argument("--common", nargs="?", type=str, const=True)
    parser.add_argument("--shell", nargs="?", type=str, const=True)
    parser.add_argument("--movies", nargs="?", type=str, const=True)
    parser.add_argument("--localize", nargs="?", type=str, const=True)
    parser.add_argument("--noxboxcopy", nargs="?", type=str, dest="no_xbox",
                        const=True)

    args = parser.parse_args()

    print(args)
    # Post process
    # Setup logging
    # Munge!
