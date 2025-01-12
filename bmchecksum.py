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

if __name__ == "__main__":
    
    """
    Runs the main function if this code is being run directly.
    """
    
    main()
