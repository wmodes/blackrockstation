#!/usr/bin/env python3

import os
import sys
import subprocess
import string
import random
import re
import subprocess

media_re = '.(wav|mp3|mp4|mov|wma|webm)$'

from_dir = "edited"
dest_dir = "final"

if not sys.argv[1]:
    media_dir_raw = input ("Enter media folder: ")
else:
    media_dir_raw = sys.argv[1]
media_dir_clean = re.sub('\\\\', '', media_dir_raw)


# if media dir not found, bail
#   isdir() prefers either the escaped version,
#   or a fullpath in quotes. We'll use the latter.
if os.path.isdir(f'"{media_dir_clean}"'):
    print(f"Folder not found: {media_dir_clean}")
    quit()
else:
    print(f"Valid media folder: {media_dir_clean}")

def safeFilename(filename):
    basename, ext = os.path.splitext(filename)
    basename = re.sub(r'[\W_]+', '-', basename)
    basename = re.sub(r'^[ -]', '', basename)
    basename = re.sub(r'[ -]$', '', basename)
    return f"{basename}{ext}"

print("Renaming files")
print("==============")

full_src_dir = f"{media_dir_clean}"

filelist = [f for f in os.listdir(full_src_dir)]

try:
    for file in filelist:
        if re.search(media_re, file):
            # Note source and dest dirs could have spaces and need to be quoted
            source = f"{full_src_dir}/{file}"
            dest = f"{full_src_dir}/{safeFilename(file)}"
            # unlike on the command line, complicated cli options don't need
            # to be quoted when using subprocess options
            if not os.path.isfile(dest):
                print(f"Renaming {source} to {dest}")
                os.rename(source, dest)
            else:
                print(f"File {file} already exists, skipping.")
except:
    pass
