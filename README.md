# Falter wiki-bot

This script uploads some automatic generated documentation to the Freifunk wiki. In the given article, it will search for a section with a title similar to `*bbb-configs*` (as regex). Afterwards it will modify this section with the given text.

The text can be handled to the script via cli (`--text`) oder via a file (`-f`). Please note, that the mediawiki API calls will modify the whole section, including the title. So your new section text must contain the section title too.

## How to use

```sh
$ ./edit_section.py -h
usage: edit_section.py [-h] -s SECTION -t TITLE (--text TEXT | -f FILE)

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        article which should be edited.
  --text TEXT           String which should be posted into section.
  -f FILE, --file FILE  Read text from a file
```

For example:

```sh
./edit_section.py -t Spielwiese -f txt
```
