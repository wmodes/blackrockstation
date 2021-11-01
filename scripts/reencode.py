import os
import sys
import subprocess
import string
import random
import re
import subprocess

media_re = '.(mp4|mov|wma|webm)$'

from_dir = "edited"
dest_dir = "final"

# unlike on the command line, complicated cli options don't need
# to be quoted when using subprocess options
ffmpeg_opts = [
    "-vf", # "scale=-1:480, crop=ih/3*4:ih",
    # "scale=w=640:h=480:force_original_aspect_ratio=increase",
    "scale=iw*480/ih:480, crop=ih/3*4:ih",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "23",
    "-c:a", "aac",
    "-strict",
    "-2"
]

media_dir_raw = input ("Enter media folder: ")
media_dir_clean = re.sub('\\\\', '', media_dir_raw)

# if media dir not found, bail
#   isdir() prefers either the escaped version,
#   or a fullpath in quotes. We'll use the latter.
if os.path.isdir(f'"{media_dir_clean}"'):
    print(f"Folder not found: {media_dir_clean}")
    quit()
else:
    print(f"Valid media folder: {media_dir_clean}")

# if source dir not found, bail
#   again, isdir() prefers escapes or quoted, we use quotes
if os.path.isdir(f'"{media_dir_clean}/{from_dir}"'):
    print(f"No folder \"{from_dir}\", recheck media folder.")
    quit()
else:
    print(f"Folder \"{from_dir}\" found.")

# if destination doesn't exist, create it
#   again, isdir() prefers escapes or quoted, we use quotes
if os.path.isdir(f'"{media_dir_raw}/{dest_dir}"'):
    print(f"No destination folder \"{dest_dir}\" found, creating.")
    os.makedirs(f"{media_dir}/{dest_dir}")
else:
    print(f"Destination folder \"{dest_dir}\" found.")

print("Transcoding files")
print("=================")

full_src_dir = f"{media_dir_clean}/{from_dir}"
full_dest_dir = f"{media_dir_clean}/{dest_dir}"

filelist = [f for f in os.listdir(full_src_dir)]

opt_str = " ".join(ffmpeg_opts)

try:
    for file in filelist:
        if re.search(media_re, file):
            basename = os.path.splitext(file)[0]
            # Note source and dest dirs could have spaces and need to be quoted
            source = f"{full_src_dir}/{file}"
            dest = f"{full_dest_dir}/{basename}.mp4"
            # unlike on the command line, complicated cli options don't need
            # to be quoted when using subprocess options
            args = ["ffmpeg", "-i", f'{source}'] + ffmpeg_opts + [f'{dest}']
            # print (args)
            if not os.path.isfile(dest):
                subprocess.call(args)
            else:
                print(f"File {file} already exists, skipping.")
except:
    if dest:
        os.remove(dest)
    pass
