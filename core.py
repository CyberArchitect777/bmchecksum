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

import hashlib
import os
from datetime import datetime

def start_upgrade_process(base_directory, message_destination=print):

    """
    Upgrade version 1.0 checksums to version 1.1 if the older checksums are detected.
    :param base_directory: The base directory to walk through
    """

    # Check for version 1.0 checksum directories, named bm-md5sums and bm-sha1sums in the base directory

    older_version_found = False
    # Check for the existence of any older versions of checksum data
    if os.path.exists(os.path.join(base_directory, "bm-md5sums")) or os.path.exists(os.path.join(base_directory, "bm-sha1sums")):
        older_version_found = True
    if older_version_found == True:
        start_date = datetime.now()
        files_processed = 0
        # Check for existing MD5 current version checksum directories
        if os.path.exists(os.path.join(base_directory, "bm11-md5sums")):
            output_message("Current version of MD5 checksum data found. Skipping MD5 checksum upgrade...\n", message_destination)
        elif os.path.exists(os.path.join(base_directory, "bm-md5sums")):
            output_message("Upgrading legacy MD5 checksums to current format...\n", message_destination)
            # Rename the bm-md5sums directory to bm11-md5sums
            os.rename(os.path.join(base_directory, "bm-md5sums"), os.path.join(base_directory, "bm11-md5sums"))
            file_paths = create_file_list(os.path.join(base_directory, "bm11-md5sums"))
            for file_path in file_paths:
                # Rename the files in the new bm11-md5sums directory to have an .md5 extension
                os.rename(file_path, file_path + ".md5")
                files_processed += 1
        # Check for existing SHA-1 current version checksum directories
        if os.path.exists(os.path.join(base_directory, "bm11-sha1sums")):
            output_message("Current version of SHA-1 checksum data found. Skipping SHA-1 checksum upgrade...\n", message_destination)
        elif os.path.exists(os.path.join(base_directory, "bm-sha1sums")):
            output_message("Upgrading legacy SHA-1 checksums to current format...\n", message_destination)
            os.rename(os.path.join(base_directory, "bm-sha1sums"), os.path.join(base_directory, "bm11-sha1sums"))
            file_paths = create_file_list(os.path.join(base_directory, "bm11-sha1sums"))
            for file_path in file_paths:
                os.rename(file_path, file_path + ".sha1")
                files_processed += 1
        end_date = datetime.now()
        time_elapsed = end_date - start_date
        output_message("Checksum upgrade complete. " + str(files_processed) + " checksum files(s) upgraded. The operation took " + return_human_readable_time_elapsed(time_elapsed) + "\n", message_destination)
    else:
        output_message("No legacy BMChecksum files found.", message_destination)

def verify_all_checksums_in_all_direct_subdirectories(base_directory, message_destination=print):
    
    """
    Verifies all checksums found in all direct subdirectories in sequence
    :param base_directory: The base directory to walk through
    """
    # Store current date and time for later use
    start_date = datetime.now()
    # Read list of file and folders in base_directory
    entries_list = os.listdir(base_directory)
    dir_list = []
    for entries in entries_list:
        # If entries is a directory, add it to the list
        if os.path.isdir(os.path.join(base_directory, entries)):
            dir_list.append(entries)
    # For each directory in the list, verify the checksums
    for directory in dir_list:
        output_message("Verifying files in directory: " + directory + "\n", message_destination)
        start_verification_process(os.path.join(base_directory, directory), True)
    end_date = datetime.now()
    time_elapsed = end_date - start_date
    output_message("Verification of all direct subdirectories complete. Operation took " + return_human_readable_time_elapsed(time_elapsed) + "\n", message_destination)

def start_verification_process(absolute_path, omit_statistics, message_destination=print):

    """
    Start the verification process on the base directory.
    :param absolute_path: The absolute base path to walk through
    :param omit_statistics: Whether to omit the statistics at the end of the verification process
    """

    md5_present = 0
    sha1_present = 0

    # Check to see if the "bm11-md5sums" and "bm11-sha1sums" directories exist
    if os.path.exists(os.path.join(absolute_path, "bm11-md5sums")):
        md5_present = 1
    if os.path.exists(os.path.join(absolute_path, "bm11-sha1sums")):
        sha1_present = 1
    # If neither checksum folder is present, abort the verification process        
    if md5_present == 0 and sha1_present == 0:
        output_message("No verification data could be found. Aborting...\n", message_destination)
    else:
        # Store current date and time for later use if omit_statistics is False
        if omit_statistics == False:
            start_date = datetime.now()
        output_message("Verifying based on files and checksums available...\n", message_destination)
        file_paths = create_file_list(absolute_path)
        error_flag = False
        # Create processed list to hold a count of actual, md5 and sha1 files as well as a count of all errors
        processed = [0, 0, 0, 0]
        for file_path in file_paths:
            processed[0] += 1
            # Calculate the checksums of the current file based on the checksum directories available
            if md5_present == 1:
                file_md5 = calculate_checksum(file_path, "md5")
            if sha1_present == 1:
                file_sha1 = calculate_checksum(file_path, "sha1")
            # Calculate the relative paths of the files
            relative_path = os.path.relpath(file_path, absolute_path)
            if md5_present == 1:
                # Check to see if the md5 checksum file exists and report it if not.
                if not os.path.exists(os.path.join(absolute_path, "bm11-md5sums", relative_path + ".md5")):
                    output_message("* MD5 checksum is missing for file: " + os.path.relpath(file_path, absolute_path), message_destination)
                    processed[3] += 1
                    error_flag = True
                else:
                    # Add one to the count of md5 files found
                    processed[1] += 1
                    # Read the MD5 checksum from the file and check if the stored checksum matches the one from the actual file
                    with open(os.path.join(absolute_path, "bm11-md5sums", relative_path + ".md5"), "r") as md5_file:
                        # Read md5 checksum after stripping newline character for compatibility with Bash version of program
                        checksum_md5 = (md5_file.read()).rstrip()
                        if file_md5 != checksum_md5:
                            output_message("* File does not match MD5 checksum: " + os.path.relpath(file_path, absolute_path), message_destination)
                            processed[3] += 1
                            error_flag = True
                        md5_file.close()
            if sha1_present == 1:
                # Check to see if the sha1 checksum file exists and report it if not.
                if not os.path.exists(os.path.join(absolute_path, "bm11-sha1sums", relative_path + ".sha1")):
                    output_message("* SHA-1 checksum is missing for file: " + os.path.relpath(file_path, absolute_path), message_destination)
                    processed[3] += 1
                    error_flag = True
                else:
                    # Add one to the count of sha1 files found
                    processed[2] += 1
                    # Read the SHA1 checksum from the file and check if the stored checksum matches the one from the actual file
                    with open(os.path.join(absolute_path, "bm11-sha1sums", relative_path + ".sha1"), "r") as sha1_file:
                        # Read sha1 checksum after stripping newline character for compatibility with Bash version of program
                        checksum_sha1 = (sha1_file.read()).rstrip()
                    if file_sha1 != checksum_sha1:
                        output_message("* File does not match SHA-1 checksum: " + os.path.relpath(file_path, absolute_path), message_destination)           
                        processed[3] += 1
                        error_flag = True
                    sha1_file.close()
        if md5_present == 1:
            md5_file_paths = create_file_list(os.path.join(absolute_path, "bm11-md5sums"))
            for md5_file_path in md5_file_paths:
                # Remove bm11-md5sums from the beginning and .md5 from the end of the path
                actual_file_path = os.path.relpath(md5_file_path, absolute_path)
                if not os.path.exists(os.path.join(absolute_path, actual_file_path[13:-4])):
                    output_message("* MD5 Checksum Available For Missing File: " + actual_file_path[13:-4], message_destination)
                    processed[3] += 1
                    error_flag = True
        if sha1_present == 1:
            sha1_file_paths = create_file_list(os.path.join(absolute_path, "bm11-sha1sums"))
            for sha1_file_path in sha1_file_paths:
                actual_file_path = os.path.relpath(sha1_file_path, absolute_path)
                if not os.path.exists(os.path.join(absolute_path, actual_file_path[14:-5])):
                    output_message("* SHA-1 Checksum Available For Missing File: " + actual_file_path[14:-5], message_destination)
                    processed[3] += 1
                    error_flag = True
        if omit_statistics == False:
            end_date = datetime.now()
            time_elapsed = end_date - start_date
            if error_flag == True:
                output_message("\nVerification complete. Operation took " + return_human_readable_time_elapsed(time_elapsed) + "\n", message_destination)
            else:
                output_message("Verification complete. Operation took " + return_human_readable_time_elapsed(time_elapsed) + "\n", message_destination)
            output_message("Files processed: " + str(processed[0]), message_destination)
            output_message("MD5 checksums processed: " + str(processed[1]), message_destination)
            output_message("SHA-1 checksums processed: " + str(processed[2]), message_destination)
            output_message("Errors found: " + str(processed[3]) + "\n", message_destination)
        elif omit_statistics == True and error_flag == True:
            # Insert a new line to make the display better
            output_message("", message_destination)

def return_human_readable_time_elapsed(time_elapsed):
    
    """
    Read in the time in the format hh:mm:ss.000000 and return a human-readable string.
    :param time_elapsed: The time elapsed in the format hh:mm:ss.000000
    :return: A human-readable string of the time elapsed
    """

    # Split up the elapsed time into hours, minutes and seconds
    time_elapsed = str(time_elapsed).split(":")
    # Ensure all numbers are rounded to the nearest integer
    for i in range(len(time_elapsed)):
        time_elapsed[i] = str(round(float(time_elapsed[i])))
    # Only show the hours and minutes if they are more than zero
    if int(time_elapsed[0]) > 0:
        return time_elapsed[0] + " hours, " + time_elapsed[1] + " minutes and " + time_elapsed[2] + " seconds."
    elif int(time_elapsed[1]) > 0:
        return time_elapsed[1] + " minutes and " + time_elapsed[2] + " seconds."
    else:
        return time_elapsed[2] + " seconds."

def start_checksum_process(absolute_path, mode, message_destination=print):
    
    """
    Start the checksumming process on the base directory.
    :param absolute_path: The absolute base path to walk through
    :param mode: The mode to run the checksumming process
    0 = Both MD5 and SHA-1
    1 = MD5 only
    2 = SHA-1 only
    """

    addition = False
    # Create the directories "bm11-md5sums" and "bm11-sha1sums" if they don't exist
    if not os.path.exists(os.path.join(absolute_path, "bm11-md5sums")) and (mode == 0 or mode == 1):
        os.makedirs(os.path.join(absolute_path, "bm11-md5sums"))
        output_message("MD5 checksum folder not found in starting directory. Creating new checksums for all discovered files...", message_destination)
    elif mode == 0 or mode == 1:
        output_message("MD5 checksum folder found in starting directory. Adding checksums for new files only...", message_destination)
        addition = True
    if not os.path.exists(os.path.join(absolute_path, "bm11-sha1sums")) and (mode == 0 or mode == 2):
        os.makedirs(os.path.join(absolute_path, "bm11-sha1sums"))
        output_message("SHA-1 checksum folder not found in starting directory. Creating new checksums for all discovered files...", message_destination)
    elif mode == 0 or mode == 2:
        output_message("SHA-1 checksum folder found in starting directory. Adding checksums for new files only...", message_destination)
        addition = True
    if addition == True:
        output_message("Existing checksum will not be replaced.", message_destination)
    file_paths = create_file_list(absolute_path)
    # Store current date and time for later use
    start_date = datetime.now()
    output_message("\nCalculating new checksums...", message_destination)
    files_processed = 0
    for file_path in file_paths:
        checksum_written = False
        if mode == 0 or mode == 1:
            md5_checksum = calculate_checksum(file_path, "md5")
        if mode == 0 or mode == 2:
            sha1_checksum = calculate_checksum(file_path, "sha1")
        # Calculate the relative paths of the files and directories
        relative_path = os.path.relpath(file_path, absolute_path)
        relative_dir_path = os.path.relpath(os.path.dirname(file_path), absolute_path)
        # Create a new directory for the new checksums if it doesn't exist
        if not os.path.exists(os.path.join(absolute_path, "bm11-md5sums", relative_dir_path)) and (mode == 0 or mode == 1):
            os.makedirs(os.path.join(absolute_path, "bm11-md5sums", relative_dir_path))
        if not os.path.exists(os.path.join(absolute_path, "bm11-sha1sums", relative_dir_path)) and (mode == 0 or mode == 2):
            os.makedirs(os.path.join(absolute_path, "bm11-sha1sums", relative_dir_path))
        # Write the output of the checksum functions to a mirrored directory structure to the 
        # original files underneath the bm11-md5sums and bm11-sha1sums directories 
        if not os.path.exists(os.path.join(absolute_path, "bm11-md5sums", relative_path + ".md5")) and (mode == 0 or mode == 1):
            with open(os.path.join(absolute_path, "bm11-md5sums", relative_path + ".md5"), "w") as md5_file:
                md5_file.write(md5_checksum)
                checksum_written = True
            md5_file.close()
        if not os.path.exists(os.path.join(absolute_path, "bm11-sha1sums", relative_path + ".sha1")) and (mode == 0 or mode == 2):
            with open(os.path.join(absolute_path, "bm11-sha1sums", relative_path + ".sha1"), "w") as sha1_file:
                sha1_file.write(sha1_checksum)
                checksum_written = True
            sha1_file.close()
        if checksum_written == True:
            files_processed += 1
    end_date = datetime.now()
    time_elapsed = end_date - start_date
    output_message("\nChecksum calculation complete. " + str(files_processed) + " files(s) checksummed. Operation took " + return_human_readable_time_elapsed(time_elapsed) + "\n", message_destination)

def create_file_list(absolute_path):
    
    """
    Create a list of all files in the base directory and all sub-folders
    that are not in the immediate bm11-md5sums and bm11-sha1sums directories.
    
    :param absolute_path: The absolute base path to walk through
    :return: List of file paths
    """
    
    file_paths = []
    for root, dirs, files in os.walk(absolute_path):
        for file in files:
            # Make sure that the "bm11-md5sums" and "bm11-sha1sums" directories are not traversed
            if not root.startswith(os.path.join(absolute_path, "bm11-md5sums")) and not root.startswith(os.path.join(absolute_path, "bm11-sha1sums")):
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

def output_message(message, output_destination=print):

    """
    Output a message to the console or to an alternative passed destination.
    :param message: The message to output
    :param callback: The function to call to output the message
    """

    output_destination(message)
