# xmunge

**xmunge** is a drop-in replacement for the Star Wars Battlefront II Classic modtools' batch-file build system.
Its primary goal is to be cross-platform; **xmunge** was created to solve the long-standing problem of Linux and Mac
users being locked out of modding SWBF2.
Other objectives for this software include ease-of-use and portability.

## Project Status

At the moment, **xmunge** is in the proof-of-concept phase. It has basic functionality and can be used to demonstrate
successful munging of a simple addon for SWBF2.

## Dependencies

- SWBF2 modtools (and a legal copy of the SWBF2 game client)
- Wine (if on Linux/Mac)
- Python 3.9
- Poetry (optional)

## Installation

1. Download and install the SWBF2 modtools.
2. Clone this repository (e.g. `cd BF2_ModTools && git clone https://github.com/jdrempel/xmunge.git`).
3. Run `"BF2_ModTools/data/_BUILD/Modtools VisualMunge.exe"` and create a new world, e.g. `data_ABC`.
4. Copy the contents of the cloned `xmunge` directory into `data_ABC/_BUILD`.

The `_BUILD` directory should now contain the file `munge.py` and a directory `xm` which itself contains a number of
other Python modules.

## Usage

Run `python3 munge.py -h` to see a list of available options. Running `munge.py` with no arguments will perform a full 
munge of everything.

On first run, the program will prompt for a path to the SWBF2 GameData directory. The path provided
can be absolute or relative. The resolved directory must already exist. Once entered, the path is saved in a file called
`.swbf2` in the root `BF2_ModTools` directory. If you need to modify the path, you must edit this file directly.

## Limitations

The following is a list of known limitations as of the most recent update of this document (28/04/22). If you are using
**xmunge** and discover a bug or missing functionality, please create an issue on GitHub.

- Sound munge is not implemented
- Non-English languages are not supported
- Xbox file copy is not supported

## Roadmap

These items are ordered by descending priority but may change.

- Add cleaning
- Implement Sound munge
- Create a script that generates a new world from the template
- Add support for non-English languages
- Add support for custom configuration via JSON or YAML
- Add multi-threading
