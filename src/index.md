---
pagetitle: Mowgli
...

### Mowgli

#### About | [Syntax](syntax/index.html) | [Other Section](other_section/index.html)

## My Own Website Generator Light and Intuitive

#### Repository

[https://github.com/nst/Mowgli](https://github.com/nst/Mowgli)

#### Idea

- only one file with < 150 lines of Python
- copy src/ into dst/
- convert .md into .html along the way

#### Installation

    pip3 install markdown

#### Usage

    python3 mowgli.py 
    usage: mowgli.py [-h] [-c] [-m]
    
    optional arguments:
      -h, --help   show this help message and exit
      -c, --clean  clean web site
      -m, --make   make web site
