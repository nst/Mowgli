#!/usr/bin/env python3

# Nicolas Seriot
# 2021-09-17
# mowgli.py
# My Own Website GEnerator LIght

# Copy src/ into dst/
# Convert .md into .html along the way

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
</head>
<body>
$body
</body>
</html>
"""
    
def clean():

    print("clean dst")
    
    s = datetime.now().strftime("%Y%m%d%H%M%S")
    dst_dir = os.path.expanduser("~/.Trash/%s" % s)
    os.mkdir(dst_dir)

    for file_name in os.listdir("dst"):
        shutil.move(os.path.join("dst", file_name), dst_dir)

def make():

    if not os.path.isdir("src"):
        os.mkdir("src")

    if not os.path.isdir("dst"):
        os.mkdir("dst")    

    md = markdown.Markdown(extensions=["tables", "meta"])

    for root, dirnames, filenames in os.walk('src'):

        print("\nroot:", root, "\ndirnames:", dirnames, "\nfilenames", filenames)
         
        short_root = os.path.relpath(root, 'src')
        
        dst_root = os.path.join("dst", short_root)

        levels_count = root.count("/")
        file_path = "../" * levels_count

        if not os.path.isdir(dst_root):
            os.mkdir(dst_root)
            print("** create", dst_root)
        
        for f in filenames:

            if f.startswith('.'):
                print(f"-- skip {f}")
                continue

            _, ext = os.path.splitext(f)
            
            is_md = ext == ".md"
            
            src = os.path.join(root, f)
            dst = None
            
            if is_md:
                html_file_name = os.path.splitext(f)[0]+'.html'
                dst = os.path.sep.join(["dst", short_root, html_file_name])
            else:
                dst = os.path.join("dst", short_root, f)
            
            if os.path.exists(dst):
                    
                ts_src = os.path.getmtime(src)
                ts_dst = os.path.getmtime(dst)
                            
                if ts_dst >= ts_src:
                    print("  skip", dst)
                    continue # file is up to date
            
            if is_md:

                print(f"-- convert {src} -> {dst}")

                with open(src) as f:
                    s = f.read()
                    
                css = file_path + "style.css"
                body = md.convert(s)

                print(md.Meta)
                if "pagetitle" not in md.Meta:
                    print(f"-- Error: page '{src}' lacks 'pagetitle' metadata")
                    sys.exit(1)

                pagetitle = md.Meta["pagetitle"].pop()
                extraheader = md.Meta.get("extraheader", None)
                                
                h = extraheader.pop() if extraheader else ""

                t = Template(template)
                html_doc = t.substitute(pagetitle=pagetitle,
                                        css=css,
                                        extraheader=h,
                                        body=body)
                
                with open(dst, "w") as f:
                    f.write(html_doc)

            else:
                print(f"-- copy {f}")
                shutil.copy2(src, dst)

if __name__ == "__main__":
        
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clean", action='store_true', help="clean web site")
    parser.add_argument("-m", "--make", action='store_true', help="make web site")

    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)    
        sys.exit(1)
    
    if args.clean:
        clean()
      
    if args.make:
        make()
