#!/usr/bin/env python3

# Nicolas Seriot
# My Own Website Generator Light and Intuitive
# https://github.com/nst/Mowgli

import os
import sys
import shutil
import argparse
import markdown
from string import Template
from datetime import datetime

template = """
<!DOCTYPE html>
<head>
    <title>$pagetitle</title>
    <link rel="stylesheet" href="$css">
    $extraheader
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
$body
</body>
</html>
"""
    
def clean():
    s = datetime.now().strftime("%Y%m%d%H%M%S")
    dst_dir = os.path.expanduser(f"~/.Trash/{s}")
    os.mkdir(dst_dir)

    for file_name in os.listdir("dst"):
        shutil.move(os.path.join("dst", file_name), dst_dir)

def make():
    # copy src into dst, convert .md into .html along the way

    md = markdown.Markdown(extensions=["tables", "meta", "admonition"])

    for root, dirnames, filenames in os.walk('src'):

        short_root = os.path.relpath(root, 'src')
        dst_root = os.path.join("dst", short_root)
        css = "../" * root.count("/") + "style.css"

        os.makedirs(dst_root, exist_ok=True)

        for f in filenames:

            if f.startswith('.'):
                continue

            is_md = f.endswith(".md")
            dst_name = f[:-3] + ".html" if is_md else f
            src = os.path.join(root, f)
            dst = os.path.join(dst_root, dst_name)

            if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                continue

            if is_md:
                print(f"-- MD {dst}")

                md.reset()
                with open(src) as fh:
                    body = md.convert(fh.read())

                if "pagetitle" not in md.Meta:
                    print(f"-- Error: page '{src}' lacks 'pagetitle' metadata")
                    sys.exit(1)

                html_doc = Template(template).substitute(
                    pagetitle=md.Meta["pagetitle"][0],
                    css=css,
                    extraheader="\n".join(md.Meta.get("extraheader", [])),
                    body=body,
                )

                with open(dst, "w") as fh:
                    fh.write(html_doc)
            else:
                shutil.copy2(src, dst)

if __name__ == "__main__":

    os.makedirs("src", exist_ok=True)
    os.makedirs("dst", exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["clean", "make"])
    args = parser.parse_args()

    {"clean": clean, "make": make}[args.command]()
