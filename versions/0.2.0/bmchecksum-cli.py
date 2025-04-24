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

import core as bmc
import sys
import os

def help():
    
    """
    Outputs help information to the user if asked for or if an invalid function is specified
    """
    
    print("General usage:")
    print("\nbmchecksum <command> <base directory>")
    print("\nCommands:")
    print("\n-c = Create all checksums for all subdirectories in the base directory")
    print("-cm = Create only MD5 checksums for all subdirectories in the base directory")
    print("-cs = Create only SHA-1 checksums for all subdirectories in the base directory")
    print("-v = Verify file checksums in all subdirectories based on those found in the base directory")
    print("-s = Verify file checksums in all direct subdirectories found in the base directory")
    print("-u = Upgrade checksums from checksum version 1.0 to the latest version (1.1)")
    print("-h = Help\n")

def main():
    
    """
    The first function run upon program start to provide the command-line interface
    """
    
    print("\nBMChecksum")
    print("Version 0.1.0")
    print("\nPython Edition")
    print("By Barrie Millar")
    print("A file hashing program to store and later verify the checksums of files\n")

    if len(sys.argv) == 1:
        help()
        sys.exit(1)
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "-c" or command == "-cm" or command == "-cs":
            print("Please provide a base directory name to calculate checksums on\n")
        elif command == "-v":
            print("Please provide a base directory name to verify checksums on\n")
        elif command == "-u":
            print("Please provide a base directory name to upgrade checksums on\n")
        elif command == "-s":
            print("Please provide a base directory name to verify checksums in all direct subdirectories in\n")
        else:
            help()
            sys.exit(1)
    else:
        command = sys.argv[1]
        base_directory = sys.argv[2]
        if not os.path.exists(base_directory):
            print("Please provide a valid base directory path\n")
        else:
            absolute_path = os.path.abspath(base_directory)
            if command == "-c":
                bmc.start_checksum_process(absolute_path, 0)
            elif command == "-cm":
                bmc.start_checksum_process(absolute_path, 1)
            elif command == "-cs":
                bmc.start_checksum_process(absolute_path, 2)
            elif command == "-v":
                bmc.start_verification_process(absolute_path, False)
            elif command == "-u":
                bmc.start_upgrade_process(base_directory)
            elif command == "-s":
                bmc.verify_all_checksums_in_all_direct_subdirectories(base_directory)
            else:
                help()
                sys.exit(1)

if __name__ == "__main__":
    
    """
    Runs the main function if this code is being run directly.
    """
    
    main()
