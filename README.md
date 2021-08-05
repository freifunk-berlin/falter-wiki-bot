# Falter wiki-bot

This script uploads some automatic generated documentation to the Freifunk wiki.

## How to use

```sh
$ ./edit_section.py -h
usage: edit_section.py [-h] -s SECTION -t TITLE (--text TEXT | -f FILE)

optional arguments:
  -h, --help            show this help message and exit
  -s SECTION, --section SECTION
                        give the section where the text should be pasted. (integer)
  -t TITLE, --title TITLE
                        article which should be edited.
  --text TEXT           String which should be posted into section.
  -f FILE, --file FILE  Read text from a file
```

For example:

```sh
./edit_section.py -s 1 -t Spielwiese -f txt
```
