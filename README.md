# BMChecksum
## By Barrie Millar
### A file hashing program to store and later verify the checksums of files

## Introduction

BMChecksum is a program to hash files recursively using standard algorithms and then store those codes in relative directories. At a later date, the original files can then be verified against the calculated checksums to confirm the byte integrity of the processed files. The language chosen to produce the initial version of this project is Python.

This program is based on a legacy software product I created long ago but never released. The original application was written as a Java GUI program and has been used for a number of years. A separate Bash script was also created to achieve the same purpose from the command-line. The codebases of both are currently outdated though and it is the purpose of this repository to create new versions of this application in any required language. Any versions produced here will be compatible with past checksum creations or offer a way to upgrade older hash codes to the newest standards. The latter will be achieved without requiring any checksum recalculations. 

The latest version of the original software application was compatible with checksum version 1.1, which used the MD5 and SHA1 hashing algorithms. It can be assumed that the first official version of this program will be compatible with this standard.

## Running The Application

No official releases of the application have been created yet.

However, to run the application in the current form, the following can be done. 

- If needed, download Git and install it.
- If needed, download the standard Python 3 interpreter and install it.
- Create a new directory and open a command-line terminal in this location. 
- Run the following to download this game repository:-

    `git clone https://github.com/CyberArchitect777/bmchecksum.git`

- From the project directory, run the following to start the application:

    `python3 bmchecksum.py`

## Repository

The GitHub repository is [here](https://github.com/CyberArchitect777/bmchecksum)

## Technical

This program was created using the following technologies:

- Python 3

## Credits

- ChatGPT for reference and learning material.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
