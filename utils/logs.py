import logging as log


def setup_logging(debug=False, platform="PC"):
    """
    Initializes the level, formatting, and file/console handlers for the main logger.
    The main logger has a file handler with level INFO and a console handler with level DEBUG.
    TODO Make the console handler log level configurable
    :return: None
    """

    logger = log.getLogger("main")

    if debug:
        logger.setLevel(log.DEBUG)
    else:
        logger.setLevel(log.INFO)

    formatter = log.Formatter(
        fmt="%(asctime)s [%(levelname)s]:  %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    log_filename = f"{platform}_MungeLog.txt"
    file_handler = log.FileHandler(log_filename, "w")
    file_handler.setLevel(log.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = log.StreamHandler()
    console_handler.setLevel(log.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
