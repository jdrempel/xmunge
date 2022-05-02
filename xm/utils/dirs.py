from pathlib import Path


def get_swbf2_path():
    """
    Reads the GameData path from the file BF2_ModTools/.swbf2 if that file exists, otherwise
    prompts for it on the command line and saves the input text to that file
    :return: A Path instance corresponding to the SWBF2 GameData directory
    """
    try:
        with open("../../.swbf2", "r") as swbf2_file:
            gamedata_dir = Path(swbf2_file.readline())

    except FileNotFoundError:
        input_dir = Path(input("Enter the path to your SWBF2 GameData folder: "))
        gamedata_dir = input_dir.resolve()
        while not gamedata_dir.exists():
            print(f"The path {gamedata_dir} does not exist.")
            input_dir = Path(input("Enter the path to your SWBF2 GameData folder: "))
            gamedata_dir = input_dir.resolve()

        with open("../../.swbf2", "w") as swbf2_file:
            swbf2_file.write(str(gamedata_dir))
            print(
                f"Saved {gamedata_dir} to the file .swbf2 in the BF2_ModTools root directory."
            )

    return gamedata_dir


def get_world_id():
    return Path.cwd().parent.name.upper().split("_")[-1]
