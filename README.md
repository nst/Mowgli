# Mowgli
Generate a static website from Markdown files with &lt;150 lines of Python

## My Own Website Generator Light and Intuitive

#### Idea

- only one file with < 150 lines of Python
- copy `src/` into `dst/`
- convert `.md` into `.html` along the way

#### Installation

    pip3 install markdown

#### Usage

    python3 mowgli.py 
    usage: mowgli.py [-h] [-c] [-m]
    
    optional arguments:
      -h, --help   show this help message and exit
      -c, --clean  clean web site
      -m, --make   make web site

#### File upload

Mowgli plays well with [kaa.py](https://gist.github.com/nst/6703da0b26f796fd2429310c7dda13cf) for FTP upload.
