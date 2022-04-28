class ArgumentValidator:
    """
    A utility class for validating command-line argument values.
    """

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
        "JAPANESE" "SPANISH",
        "UK",
    ]

    def __init__(self, args_):
        self.args = args_

    def _validate_platform(self):
        """
        Determines whether the platform supplied in the args is valid.
        :return: True if the platform is None or in the list of valid platform strings, False otherwise
        """
        return (
            self.args.platform is None or self.args.platform.upper() in self.platforms
        )

    def _validate_language(self):
        """
        Determines whether the language supplied in the args is valid.
        :return: True if the language is None or in the list of valid language strings, False otherwise
        """
        return (
            self.args.language is None or self.args.language.upper() in self.languages
        )

    def validate_args(self):
        """
        Performs a full validation of all applicable args (platform, language), raising an exception if validation
        fails for some reason.
        :raise: RuntimeError if either the platform or the language is invalid
        :return: None
        """
        if not self._validate_platform():
            raise RuntimeError(f"Invalid platform {self.args.platform}")

        if not self._validate_language():
            raise RuntimeError(f"Invalid language {self.args.language}")
