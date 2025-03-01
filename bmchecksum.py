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
    print("-u = Upgrade checksums from checksum version 1.0 to the latest version (1.1)")
    print("-h = Help\n")

def main():
    
    """
    The first function run upon program start
    """
    
    print("\nBMChecksum")
    print("\nPython Edition")
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
        elif command == "-v":
            print("Please provide a base directory name to verify checksums on\n")
        elif command == "-u":
            print("Please provide a base directory name to upgrade checksums on\n")
    else:
        command = sys.argv[1]
        base_directory = sys.argv[2]
        if command == "-c":
            start_checksum_process(base_directory)
        elif command == "-v":
            start_verification_process(base_directory)
        elif command == "-u":
            start_upgrade_process(base_directory)

def start_upgrade_process(base_directory):
    """
    Upgrade version 1.0 checksums to version 1.1 if the older checksums are detected.
    :param base_directory: The base directory to walk through
    """

    # Check for version 1.0 checksum directories, named bm-md5sums and bm-sha1sums in the base directory

    older_version_found = False
    if os.path.exists(os.path.join(base_directory, "bm-md5sums")):
        older_version_found = True
    # Rename the bm-md5sums directory to bm11-md5sums
        os.rename(os.path.join(base_directory, "bm-md5sums"), os.path.join(base_directory, "bm11-md5sums"))
        file_paths = create_file_list(os.path.join(base_directory, "bm11-md5sums"))
        for file_path in file_paths:
            # Rename the files in the new bm11-md5sums directory to have an .md5 extension
            os.rename(file_path, file_path + ".md5")
    if os.path.exists(os.path.join(base_directory, "bm-sha1sums")):
        older_version_found = True
        os.rename(os.path.join(base_directory, "bm-sha1sums"), os.path.join(base_directory, "bm11-sha1sums"))
        file_paths = create_file_list(os.path.join(base_directory, "bm11-sha1sums"))
        for file_path in file_paths:
            os.rename(file_path, file_path + ".sha1")
    if older_version_found == True:
        print("Upgrade complete\n")
    else:
        print("Directory does not contain older BMChecksum files\n")

def start_verification_process(base_directory):
    """
    Start the verification process on the base directory.
    :param base_directory: The base directory to walk through
    """
    # Check to see if the "bm11-md5sums and "bm11-sha1sums" directories exist
    if not os.path.exists(os.path.join(base_directory, "bm11-md5sums")) or not os.path.exists(os.path.join(base_directory, "bm11-sha1sums")):
        print("No verification data could be found. Aborting...\n")
        sys.exit(1)
    else:
        print("Verifying based on files and checksums available...\n")
        file_paths = create_file_list(base_directory)
        error_flag = False
        for file_path in file_paths:
            # Calculate the checksums of the current file
            file_md5 = calculate_checksum(file_path, "md5")
            file_sha1 = calculate_checksum(file_path, "sha1")
            directory_name = os.path.dirname(file_path)
            # Remove the ".", "./" or ".\" from the beginning of the directory name
            if directory_name.startswith("." + os.sep):
                directory_name = directory_name[2:]
            elif directory_name.startswith("."):
                directory_name = directory_name[1:]
            # Check to see if the md5 checksum file exists and report it if not.
            if not os.path.exists(os.path.join(base_directory, "bm11-md5sums", directory_name, os.path.basename(file_path) + ".md5")):
                print("* MD5 checksum is missing for file: " + file_path[2:])
                error_flag = True
            else:
                # Read the MD5 checksum from the file and check if the stored checksum matches the one from the actual file
                with open(os.path.join(base_directory, "bm11-md5sums", directory_name, os.path.basename(file_path) + ".md5"), "r") as md5_file:
                    # Read md5 checksum after stripping newline character for compatibility with Bash version of program
                    checksum_md5 = (md5_file.read()).rstrip()
                    if file_md5 != checksum_md5:
                        print("* File does not match MD5 checksum: " + file_path[2:])
                        error_flag = True
                    md5_file.close()
            # Check to see if the sha1 checksum file exists and report it if not.
            if not os.path.exists(os.path.join(base_directory, "bm11-sha1sums", directory_name, os.path.basename(file_path) + ".sha1")):
                print("* SHA-1 checksum is missing for file: " + file_path[2:])
                error_flag = True
            else:
                # Read the SHA1 checksum from the file and check if the stored checksum matches the one from the actual file
                with open(os.path.join(base_directory, "bm11-sha1sums", directory_name, os.path.basename(file_path) + ".sha1"), "r") as sha1_file:
                    # Read sha1 checksum after stripping newline character for compatibility with Bash version of program
                    checksum_sha1 = (sha1_file.read()).rstrip()
                if file_sha1 != checksum_sha1:
                    print("* File does not match SHA-1 checksum: " + file_path[2:])           
                    error_flag = True
                sha1_file.close()
        md5_file_paths = create_file_list(os.path.join(base_directory, "bm11-md5sums"))
        for md5_file_path in md5_file_paths:
            # Remove bm11-md5sums from the beginning and .md5 from the end of the path
            actual_file_path = "." + md5_file_path[14:-4]
            if not os.path.exists(actual_file_path):
                print("* MD5 Checksum Available For Missing File: " + actual_file_path[2:])
                error_flag = True
        sha1_file_paths = create_file_list(os.path.join(base_directory, "bm11-sha1sums"))
        for sha1_file_path in sha1_file_paths:
            actual_file_path = "." + sha1_file_path[15:-5]
            if not os.path.exists(actual_file_path):
                print("* SHA-1 Checksum Available For Missing File: " + actual_file_path[2:])
                error_flag = True
        if error_flag == True:
            print("\nVerification complete\n")
        else:
            print("Verification complete\n")

def start_checksum_process(base_directory):
    """
    Start the checksumming process on the base directory.
    :param base_directory: The base directory to walk through
    """
    addition = False
    # Create the directories "bm11-md5sums" and "bm11-sha1sums" if they don't exist
    if not os.path.exists(os.path.join(base_directory, "bm11-md5sums")):
        os.makedirs(os.path.join(base_directory, "bm11-md5sums"))
        print("Creating parent md5 checksum directory...")
    else:
        print("Adding to current md5 checksum directory...")
        addition = True
    if not os.path.exists(os.path.join(base_directory, "bm11-sha1sums")):
        os.makedirs(os.path.join(base_directory, "bm11-sha1sums"))
        print("Creating parent sha1 checksum directory...")
    else:
        print("Adding to current sha1 checksum directory...")
        addition = True
    if addition == True:
        print("\nExisting checksum will not be replaced")
    file_paths = create_file_list(base_directory)
    print("\nCalculating new checksums...")
    for file_path in file_paths:
        md5_checksum = calculate_checksum(file_path, "md5")
        sha1_checksum = calculate_checksum(file_path, "sha1")
        directory_name = os.path.dirname(file_path)
        # Remove the ".", "./" or ".\" from the beginning of the directory name
        if directory_name.startswith("." + os.sep):
            directory_name = directory_name[2:]
        elif directory_name.startswith("."):
            directory_name = directory_name[1:]
        # Create a new directory for the new checksums if it doesn't exist
        if not os.path.exists(os.path.join(base_directory, "bm11-md5sums", directory_name)):
            os.makedirs(os.path.join(base_directory, "bm11-md5sums", directory_name))
        if not os.path.exists(os.path.join(base_directory, "bm11-sha1sums", directory_name)):
            os.makedirs(os.path.join(base_directory, "bm11-sha1sums", directory_name))
        # Write the output of the checksum functions to a mirrored directory structure to the 
        # original files underneath the bm11-md5sums and bm11-sha1sums directories 
        if not os.path.exists(os.path.join(base_directory, "bm11-md5sums", directory_name, os.path.basename(file_path) + ".md5")):
            with open(os.path.join(base_directory, "bm11-md5sums", directory_name, os.path.basename(file_path) + ".md5"), "w") as md5_file:
                md5_file.write(md5_checksum)
            md5_file.close()
        if not os.path.exists(os.path.join(base_directory, "bm11-sha1sums", directory_name, os.path.basename(file_path) + ".sha1")):
            with open(os.path.join(base_directory, "bm11-sha1sums", directory_name, os.path.basename(file_path) + ".sha1"), "w") as sha1_file:
                sha1_file.write(sha1_checksum)
            sha1_file.close()
    print("\nChecksum calculation complete\n")

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
            # Make sure that the "bm11-md5sums" and "bm11-sha1sums" directories are not traversed
            if not root.startswith(os.path.join(base_directory, "bm11-md5sums")) and not root.startswith(os.path.join(base_directory, "bm11-sha1sums")):
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
