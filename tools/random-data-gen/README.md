# BMChecksum Random Data Generator
## By Barrie Millar
### A tool to create random test data for checksumming and verification

### Version 0.1.0

## Introduction

The Random Data Generator is a command-line tool that fills a directory with randomly generated text files, placed inside a randomly generated directory structure. It exists to provide realistic test data for BMChecksum, allowing checksum creation, verification and upgrading to be exercised against a varied set of files and folders without having to assemble one by hand.

Both the files and the directories are given human readable names taken from built-in word lists, in the form "adjective-noun", so that the resulting structure can be read and discussed as easily as any other. The content of each file is readable nonsense text arranged into sentences and paragraphs. The number of files and the maximum size of each one are both chosen by the user.

Nothing is ever deleted or overwritten by this tool. Directories are created as needed and every file written carries a name that has not been used before in the same run.

## Running The Application

The standard Python 3 interpreter must be installed and available. No additional requirements are needed as the tool uses only the standard library.

From this directory, the general usage is as follows:-

`python3 random-data-gen.py <directory> <number of files>`

An example creating 250 files of no more than 32KB each, in a structure up to four levels deep:-

`python3 random-data-gen.py testdata 250 -s 32K -d 4`

### Arguments

`<directory>` - The directory to create the test data in. It is created if it does not exist and any files already present are left untouched.

`<number of files>` - The number of files to create.

### Options

`-s` or `--max-size` - The maximum size of each file, written either as a plain number of bytes or with a B, K, M or G suffix in either case. Each file is given its own random size up to this maximum, so that the data set is varied. The default is 64K.

`-d` or `--max-depth` - The deepest level of subdirectory that may be created. A value of 0 places every file directly in the chosen directory. The default is 3.

`-f` or `--folders` - The number of subdirectories to create. By default this is a quarter of the number of files requested, up to a maximum of 50.

`--seed` - A number used to seed the random generator. Supplying the same seed twice recreates an identical set of directories, file names and file content, which is useful when the same test data is needed more than once.

`-h` or `--help` - Help.

## Repository

This tool forms part of the BMChecksum repository, which is [here](https://github.com/CyberArchitect777/bmchecksum)

## Technical

### Program construction

This tool was created using the following technologies:

- Python 3

### Random Data Generator Versions

0.1.0 - 12th of September, 2026

* Initial release of the random data generator.

## Credits

- Claude Code for rapid development.
- Black for code formatting.

## License

This tool is licensed under the GNU General Public License v3.0, in common with the rest of BMChecksum - see the [LICENSE](../../LICENSE) file for details.
