"""
BMChecksum: A file hashing program to store and later verify the checksums of files
Copyright (C) 2025 Barrie Millar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import os
import random
import sys
from datetime import datetime

# Word lists used to build human readable names and readable file content

ADJECTIVES = [
    "amber", "ancient", "brave", "brisk", "calm", "clever", "copper", "crimson",
    "curious", "distant", "eager", "early", "fearless", "gentle", "gilded",
    "golden", "hidden", "humble", "idle", "jolly", "keen", "little", "lively",
    "lucky", "mellow", "merry", "misty", "narrow", "noble", "polished", "proud",
    "quiet", "rapid", "restless", "rugged", "silent", "silver", "solemn",
    "spotted", "steady", "sunny", "tangled", "tidy", "velvet", "wandering",
    "weathered", "willing", "winding", "wise", "zealous",
]

NOUNS = [
    "anchor", "badger", "beacon", "bramble", "canyon", "cavern", "cedar",
    "chapel", "cobble", "compass", "cottage", "falcon",
    "ferry", "garden", "harbour", "hollow", "island", "juniper", "kestrel",
    "lantern", "ledger", "lighthouse", "marble", "meadow", "mill", "orchard",
    "otter", "paddock", "pebble", "quarry", "ribbon", "ridge", "sapling",
    "scholar", "sparrow", "station", "swallow", "thicket", "tunnel", "valley",
    "vessel", "village", "warren", "willow", "windmill", "yarrow",
]

# Extensions used for the generated files, all of which hold plain readable text

FILE_EXTENSIONS = [".txt", ".log", ".md"]


def parse_size(size_text):
    """
    Convert a size written by the user into a number of bytes. Plain numbers are read as
    bytes and the suffixes B, K, M and G are all accepted in either case.
    :param size_text: The size as written on the command-line, such as "512", "64K" or "2M"
    :return: The size in bytes
    """

    multipliers = {"B": 1, "K": 1024, "M": 1024 * 1024, "G": 1024 * 1024 * 1024}
    # The size as typed is kept so that any error can quote the user back to themselves
    original_text = size_text.strip()
    size_text = original_text.upper()
    if size_text == "":
        raise argparse.ArgumentTypeError("A file size must be provided")
    multiplier = 1
    if size_text[-1] in multipliers:
        multiplier = multipliers[size_text[-1]]
        size_text = size_text[:-1]
    try:
        size_in_bytes = int(float(size_text) * multiplier)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "'"
            + original_text
            + "' is not a valid size. Try a value such as 512, 64K or 2M"
        )
    if size_in_bytes < 1:
        raise argparse.ArgumentTypeError("The maximum file size must be at least 1 byte")
    return size_in_bytes


def parse_positive_number(number_text):
    """
    Read a whole number from the command-line and confirm that it is above zero.
    :param number_text: The number as written on the command-line
    :return: The number as an integer
    """

    try:
        number = int(number_text)
    except ValueError:
        raise argparse.ArgumentTypeError("'" + number_text + "' is not a whole number")
    if number < 1:
        raise argparse.ArgumentTypeError("A number of at least 1 must be provided")
    return number


def return_human_readable_size(size_in_bytes):
    """
    Convert a number of bytes into a short string suitable for display to the user.
    :param size_in_bytes: The size in bytes
    :return: A human-readable string of the size
    """

    size = float(size_in_bytes)
    for unit in ["bytes", "KB", "MB", "GB"]:
        if size < 1024 or unit == "GB":
            # Whole bytes read better without a decimal place
            if unit == "bytes":
                return str(int(size)) + " " + unit
            return str(round(size, 1)) + " " + unit
        size = size / 1024


def create_random_name(used_names):
    """
    Build a human readable name in the form "adjective-noun", adding a number on the end
    if that combination has been used already.
    :param used_names: The set of names handed out so far, which is added to here
    :return: A name that has not been used before
    """

    while True:
        name = random.choice(ADJECTIVES) + "-" + random.choice(NOUNS)
        if name not in used_names:
            used_names.add(name)
            return name
        # Fall back on a numbered variation once the plain combination is taken
        numbered_name = name + "-" + str(random.randint(2, 999999))
        if numbered_name not in used_names:
            used_names.add(numbered_name)
            return numbered_name


def return_directory_depth(directory, base_directory):
    """
    Work out how far a directory sits below the base directory.
    :param directory: The directory to measure
    :param base_directory: The directory the depth is counted from
    :return: The number of levels below the base directory, which is itself zero
    """

    relative_path = os.path.relpath(directory, base_directory)
    if relative_path == ".":
        return 0
    return len(relative_path.split(os.sep))


def create_directory_structure(base_directory, directory_count, max_depth, used_names):
    """
    Create a random tree of directories underneath the base directory. Each new directory
    is hung off a randomly chosen existing one, which gives an uneven structure rather
    than a set of identical branches.
    :param base_directory: The directory to build the structure inside
    :param directory_count: The number of directories to create
    :param max_depth: The deepest level any directory may be created at
    :param used_names: The set of names handed out so far
    :return: A list of every directory files may be written to, including the base directory
    """

    directories = [base_directory]
    for _ in range(directory_count):
        # Only directories still short of the maximum depth can take a new child
        candidates = [
            directory
            for directory in directories
            if return_directory_depth(directory, base_directory) < max_depth
        ]
        if len(candidates) == 0:
            break
        new_directory = os.path.join(
            random.choice(candidates), create_random_name(used_names)
        )
        os.makedirs(new_directory, exist_ok=True)
        directories.append(new_directory)
    return directories


def create_random_text(size_in_bytes):
    """
    Build readable nonsense text of exactly the requested size. Sentences are assembled
    from the word lists and grouped into paragraphs before being cut to length.
    :param size_in_bytes: The exact length of the text required
    :return: The generated text
    """

    text = []
    length = 0
    sentences_in_paragraph = 0
    while length < size_in_bytes:
        # Build a single sentence of randomly chosen words
        words = []
        for _ in range(random.randint(6, 16)):
            if random.randint(0, 2) == 0:
                words.append(random.choice(ADJECTIVES))
            words.append(random.choice(NOUNS))
        sentence = " ".join(words).capitalize() + ". "
        sentences_in_paragraph += 1
        # Break the text into paragraphs so that the result looks like a real document
        if sentences_in_paragraph >= random.randint(3, 8):
            sentence = sentence.rstrip() + "\n\n"
            sentences_in_paragraph = 0
        text.append(sentence)
        length += len(sentence)
    # Cut the text down to the exact size asked for, as the last sentence will overshoot
    return "".join(text)[:size_in_bytes]


def create_random_files(directories, file_count, max_size, used_names):
    """
    Write the requested number of text files, each one placed in a randomly chosen
    directory and filled with a random amount of text up to the maximum size.
    :param directories: The list of directories files may be written to
    :param file_count: The number of files to create
    :param max_size: The largest a single file may be in bytes
    :param used_names: The set of names handed out so far
    :return: The total number of bytes written
    """

    bytes_written = 0
    for file_number in range(file_count):
        file_name = create_random_name(used_names) + random.choice(FILE_EXTENSIONS)
        file_path = os.path.join(random.choice(directories), file_name)
        # Every file is given its own random size so that the data set is varied
        file_size = random.randint(1, max_size)
        with open(file_path, "w") as new_file:
            new_file.write(create_random_text(file_size))
        bytes_written += file_size
        # Report progress periodically so that large runs do not look like they have stalled
        if (file_number + 1) % 100 == 0:
            print(str(file_number + 1) + " files written...")
    return bytes_written


def main():
    """
    The first function run upon program start to provide the command-line interface
    """

    print("\nBMChecksum Random Data Generator")
    print("Version 0.1.0")
    print("\nBy Barrie Millar")
    print("A tool to create random test data for checksumming and verification\n")

    parser = argparse.ArgumentParser(
        description="Create a random directory structure filled with human readable "
        "text files, intended as test data for BMChecksum.",
        epilog="Example: random-data-gen.py testdata 250 -s 32K -d 4",
    )
    parser.add_argument(
        "directory",
        help="The directory to create the test data in. It is created if needed and "
        "existing files are never removed or overwritten",
    )
    parser.add_argument(
        "files",
        type=parse_positive_number,
        help="The number of files to create",
    )
    parser.add_argument(
        "-s",
        "--max-size",
        type=parse_size,
        default="64K",
        help="The maximum size of each file, written as bytes or with a B, K, M or G "
        "suffix. Each file is given a random size up to this maximum (default: 64K)",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        default=3,
        help="The deepest level of subdirectory that may be created, where 0 places "
        "every file in the chosen directory (default: 3)",
    )
    parser.add_argument(
        "-f",
        "--folders",
        type=int,
        default=None,
        help="The number of subdirectories to create. Defaults to a quarter of the "
        "number of files, to a maximum of 50",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="A number used to seed the random generator, allowing an identical data "
        "set to be recreated later",
    )
    arguments = parser.parse_args()

    if arguments.max_depth < 0:
        parser.error("The maximum depth cannot be a negative number")
    if arguments.folders is not None and arguments.folders < 0:
        parser.error("The number of folders cannot be a negative number")

    # Work out a sensible number of directories if the user has not asked for a set amount
    folders = arguments.folders
    if folders is None:
        folders = min(50, max(1, arguments.files // 4))
    if arguments.max_depth == 0:
        folders = 0

    if arguments.seed is not None:
        random.seed(arguments.seed)

    try:
        base_directory = os.path.abspath(arguments.directory)
        os.makedirs(base_directory, exist_ok=True)
        start_date = datetime.now()
        used_names = set()

        print("Creating directory structure in: " + base_directory + "\n")
        directories = create_directory_structure(
            base_directory, folders, arguments.max_depth, used_names
        )
        print(str(len(directories) - 1) + " subdirectory(s) created.\n")

        print("Writing files...")
        bytes_written = create_random_files(
            directories, arguments.files, arguments.max_size, used_names
        )
        end_date = datetime.now()
        time_elapsed = end_date - start_date

        print("\nGeneration complete.")
        print("Files created: " + str(arguments.files))
        print("Subdirectories created: " + str(len(directories) - 1))
        print("Total data written: " + return_human_readable_size(bytes_written))
        print(
            "Largest possible file size: "
            + return_human_readable_size(arguments.max_size)
            + "\n"
        )
        print("The operation took " + str(time_elapsed).split(".")[0] + "\n")
    except OSError as error:
        print("\nThe test data could not be written.")
        print("The error reported was: " + str(error) + "\n")
        sys.exit(1)


if __name__ == "__main__":

    """
    Runs the main function if this code is being run directly.
    """

    main()
