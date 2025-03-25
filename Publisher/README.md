# Publisher

## Basic Instructions
This tool publishes a set of markdown files to linked HTML webpages with minimalistic styling.

To use this tool, begin with a project structure like so:

Input files:
```
├── source/
│   ├── file1.md
│   ├── file2.md
│   ├── file3.md
```

Output directories:
```
├── html/
│   ├── Chapters/
```

These directories can overlap, like so:
```
project/
├── source/
│   ├── file1.md
│   ├── file2.md
│   ├── file3.md
├── html/
│   ├── Chapters/
```

When the project is structured appropriately, correct usage of the publisher might resemble the following on a UNIX system:
```
user@host:/home/.../project$ python3 publish.py -s './source/' -o './html/' -z
```

Or like this on a Windows system:
```
C:\Users\Name\Documents> python3 publish.py -s '.\source\' -o '.\html\' -z
```

The resulting files will be structured as such:
```
project/
├── source/
│   ├── file1.md
│   ├── file2.md
│   ├── file3.md
├── html/
│   ├── index.html
│   ├── style.css
│   ├── Chapters/
│   │   ├── file1.html
│   │   ├── file2.html
│   │   ├── file3.html
```

## Specifics
The program accepts command line arguments which are detailed below:
|Flag|Full Option|Purpose|
|-|-|-|
|-h|--help|Show the help menu on the command line and exit|
|-s|--source|Specify the directory containing the Markdown source files|
|-o|--output|Specify where the generated HTML webpages should be stored|
|-z|--zip|Produce a ZIP archive in addition to the raw HTML|

## Installation
The program can be run with Python3 from the command line. However, this can lead to the cumbersome requirement of potentially long paths to source and output directories. Binaries for Windows and Linux are coming soon, and can be added to the system environment variables of the installation machine to make the tool accessible from anywhere in the filesystem.
