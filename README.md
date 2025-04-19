# BMChecksum
## By Barrie Millar
### A file hashing program to store and later verify the checksums of files

### Version 0.1.0

## Introduction

BMChecksum is a program to hash files recursively using standard algorithms and then store those codes in relative directories. At a later date, the original files can then be verified against the calculated checksums to confirm the byte integrity of the processed files. The language chosen to produce the initial version of this project is Python.

This program is based on a legacy software product I created long ago but never released. The original application was written as a Java GUI program and has been used for a number of years. A separate Bash script was also created to achieve the same purpose from the command-line. The codebases of both are currently outdated though and it is the purpose of this repository to create new versions of this application in any required language. Any versions produced here will be compatible with past checksum creations or offer a way to upgrade older hash codes to the newest standards. The latter will be achieved without requiring any checksum recalculations. 

The latest version of the original software application was compatible with checksum version 1.1, which used the MD5 and SHA1 hashing algorithms. It can be assumed that the first official version of this program will be compatible with this standard, despite the flaws that exist with these algorithms today.

## Running The Application

### Latest stable release

No packaged releases of the application have been created yet. However, the latest stable version (and indeed all versions of the application) can be found under the tags section of this repository here:-

https://github.com/CyberArchitect777/bmchecksum/tags

To run version 0.1.0, the standard Python 3 interpreter must be installed and available. The BMChecksum compressed archive should then be extracted to a new directory. The following command can then be run from this directory via the command-line:-

`python3 bmchecksum.py`

The help instructions given can then be followed to proceed further.

### Latest source code

To acquire and run the latest source code, the following can be done. 

- If needed, download Git and install it.
- If needed, download the standard Python 3 interpreter and install it.
- Create a new directory and open a command-line terminal in this location. 
- Run the following to download this game repository:-

    `git clone https://github.com/CyberArchitect777/bmchecksum.git`

- From the project directory, run the following as a starting point:

    `python3 bmchecksum.py`

## Repository

The GitHub repository is [here](https://github.com/CyberArchitect777/bmchecksum)

The main development branch is located in the root directory. However, branches tagged in the versions/ directory contained stable editions. All versions of this software are tagged and can also be acquired with Git. An example of how to do this with the v0.1.0 codebase is:-

`git checkout v0.1.0`

## Technical

### Program construction

This program was created using the following technologies:

- Python 3

### BM-Checksum Versions

0.1.0 - 23rd of March, 2025

- Initial release of command-line edition

### Checksum format versions

Version 1.1

Having checksum files with the same extension as the original files proved problematic and thus the extensions .md5 and .sha1 was added to each checksum file. To separate this version of the checksum system with the original, the checksum folders were renamed bm11-md5sums and bm11-sha1sums. An upgrade facility has been built into every bmchecksum tool to bring old checksums up to this version.

Version 1.0

In version 1.0, BMChecksum stored checksum files in the base directory being checksummed. If we assume this folder is called "home", then the directories bm-md5sums and bm-sha1sums were created inside this. A file clone of "home" is then created in the two checksum folders minus bm11-md5sums and bm11-sha1sums, although the content of the files created is only a md5 or sha1 checksum.

## Credits

- Github Copilot for rapid development.
- ChatGPT for technical assistance and image generation.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
