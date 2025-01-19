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

import sys
import hashlib
import os

def help():
    
    """
    Outputs help information to the user if asked for or if an invalid function is specified
    """
    
    print("General usage:")
    print("\nbmchecksum <command> <base directory>")
    print("\nCommands:")
    print("\n-c = Create checksums for all subdirectories in the base directory")
    print("-v = Verify file checksums in all subdirectories based on those found in the base directory")
    print("-h = Help\n")

def main():
    
    """
    The first function run upon program start
    """
    
    print("\nBMChecksum")
    print("By Barrie Millar")
    print("A file hashing program to store and later verify the checksums of files\n")

    if len(sys.argv) == 1:
        help()
        sys.exit(1)
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "-h":
            help()
            sys.exit(1)
        elif command == "-c":
            print("Please provide a base directory name to calculate checksums on\n")
    else:
        command = sys.argv[1]
        base_directory = sys.argv[2]
        if command == "-c":
            # Create the directories "bm11-md5sums" and "bm11-sha1sums" if they don't exist
            if not os.path.exists(os.path.join(base_directory, "bm11-md5sums")):
                os.makedirs(os.path.join(base_directory, "bm11-md5sums"))
            if not os.path.exists(os.path.join(base_directory, "bm11-sha1sums")):
                os.makedirs(os.path.join(base_directory, "bm11-sha1sums"))
            file_paths = create_file_list(base_directory)
            for file_path in file_paths:
                md5_checksum = calculate_checksum(file_path, "md5")
                sha1_checksum = calculate_checksum(file_path, "sha1")#
                directory_name = os.path.dirname(file_path)
                # Remove the "." or "./" from the beginning of the directory name
                if directory_name.startswith("."):
                    directory_name = directory_name[1:]
                if directory_name.startswith("/"):
                    directory_name = directory_name[1:]
                print(file_path + " - " + directory_name + " - " + os.path.basename(file_path))
                # Create a new directory for the new checksums if it doesn't exist
                if not os.path.exists(os.path.join(base_directory, "bm11-md5sums", directory_name)):
                    os.makedirs(os.path.join(base_directory, "bm11-md5sums", directory_name))
                if not os.path.exists(os.path.join(base_directory, "bm11-sha1sums", directory_name)):
                    os.makedirs(os.path.join(base_directory, "bm11-sha1sums", directory_name))
                # Write the output of the checksum functions to a mirrored directory structure to the 
                # original files underneath the bm11-md5sums and bm11-sha1sums directories 
                with open(os.path.join(base_directory, "bm11-md5sums", directory_name, os.path.basename(file_path) + ".md5"), "w") as md5_file:
                    md5_file.write(md5_checksum)
                with open(os.path.join(base_directory, "bm11-sha1sums", directory_name, os.path.basename(file_path) + ".sha1"), "w") as sha1_file:
                    sha1_file.write(sha1_checksum)
                # Close the files
                md5_file.close()
                sha1_file.close()
        elif command == "-v":
                print("Verification functionality not implemented yet")

def create_file_list(base_directory):
    """
    Create a list of all files in the base directory and all sub-folders
    that are not in the immediate bm11-md5sums and bm11-sha1sums directories.
    
    :param base_directory: The base directory to walk through
    :return: List of file paths
    """
    file_paths = []
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file not in ["bm11-md5sums", "bm11-sha1sums"]:
                file_paths.append(os.path.join(root, file))
    return file_paths

def calculate_checksum(file_path, algorithm):
    """
    Calculate the checksum of a file using the specified algorithm.
    
    :param file_path: Path to the file
    :param algorithm: Hashing algorithm to use ("md5" or "sha1")
    :return: Checksum of the file
    """
    if algorithm == "md5":
        file_hash = hashlib.md5()
    elif algorithm == "sha1":
        file_hash = hashlib.sha1()

    with open(file_path, "rb") as file:
        for file_chunk in iter(lambda: file.read(4096), b""):
            file_hash.update(file_chunk)
    return file_hash.hexdigest()

if __name__ == "__main__":
    
    """
    Runs the main function if this code is being run directly.
    """
    
    main()
