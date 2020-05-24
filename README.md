# hppo
**H**ouse**p**arty **P**arsing **O**utputer

Parses Houseparty app data exported to JSON format

Blog post with details: https://www.bluesmoke4n6.com/2020/05/get-your-red-solo-cup-its-time-for.html

## Steps:
1. Locate and export Houseparty Realm database
2. Open database file in Realm Studio
3. In Realm Studio:  Select File > Save data > JSON
4. Run HPPO on the JSON file

## Installation

Pre-requisites:
Python 3

To install dependencies, run:

```
pip install -r requirements.txt
```

## Usage

### CLI

```
$ python hppo.py -j <path_to_JSON_file> -o <path_to_output_directory>
```
Optional Argument:
  -a    Parses ALL tables

### Help
```
$ python hppo.py --help
```
