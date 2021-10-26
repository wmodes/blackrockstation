import os
import sys
import subprocess
import string
import random
import re
import subprocess

media_re = '.(mp4|mov|wma)$'

from_dir = "ready-for-glitch"
overlay_dir = "overlays"
dest_dir = "final"

overlay_file = "tv-interference-overlay.mp4"

# unlike on the command line, complicated cli options don't need
# to be quoted when using subprocess options
ffmpeg_opts = [
  "-filter_complex",
  # "[1:0]scale=-1:480, crop=ih/3*4:ih, setdar=dar=1, format=rgba[a]; \
  #  [0:0]scale=-1:480, crop=ih/3*4:ih, setdar=dar=1, format=rgba[b]; \
  #  [b][a]blend=all_mode='overlay':all_opacity=0.8"

  # "[1]split[m][a]; \
  #  [a]geq='if(gt(lum(X,Y),16),255,0)',hue=s=0[al]; \
  #  [m][al]alphamerge[ovr]; \
  #  [0][ovr]overlay",

  # "[1]colorkey=0x000000:0.02:0.03[ckout]; \
  #  [ckout]scale=-1:480, crop=ih/3*4:ih[scaleout]; \
  #  [0][scaleout]overlay=154:170[out];"

  "[0:a]volume=1.0[a0]; \
   [1:a]volume=0.2[a1]; \
   [a0][a1]amix=inputs=2:duration=shortest; \
   [0:v]scale=-1:480, crop=ih/3*4:ih[basevid]; \
   [1:v]scale=-1:480, crop=ih/3*4:ih[overlay]; \
   [overlay]colorkey=0x000000:0.2:0.2[keyout]; \
   [basevid][keyout]overlay=shortest=1[out]",
  "-map", "[out]",
  # "-acodec", "copy",

  # this works but has hard edges around the key, and doesn't scale
  # "[1:v]colorkey=0x000000:0.1:0.1[ckout]; \
  #  [0:v][ckout]overlay[out]",
  # "-map", "[out]",

  # this works but the blend mode is not quite right
  # "[1:0]scale=-1:480, crop=ih/3*4:ih, format=rgba[a]; \
  #  [0:0]scale=-1:480, crop=ih/3*4:ih, format=rgba[b]; \
  #  [b][a]blend=all_mode='overlay':all_opacity=0.8",

  # glitch mods
  # "-x265-params", "b-frames=0",

  "-shortest",
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
full_over_dir = f"{media_dir_clean}/{overlay_dir}"
full_dest_dir = f"{media_dir_clean}/{dest_dir}"

filelist = [f for f in os.listdir(full_src_dir)]

opt_str = " ".join(ffmpeg_opts)

try:
    for file in filelist:
        if re.search(media_re, file):
            basename = os.path.splitext(file)[0]
            # Note source and dest dirs could have spaces and need to be quoted
            source = f"{full_src_dir}/{file}"
            overlay = f"{full_over_dir}/{overlay_file}"
            dest = f"{full_dest_dir}/{basename}.mp4"
            # unlike on the command line, complicated cli options don't need
            # to be quoted when using subprocess options
            # ffmpeg -i orig-vid.mp4 -i overlay.mp4 opts result.mp3
            args = ["ffmpeg", "-i", f'{source}', "-i", f'{overlay}'] + ffmpeg_opts + [f'{dest}']
            # print (args)
            if not os.path.isfile(dest):
                subprocess.call(args)
            else:
                print(f"File {file} already exists, skipping.")
except:
    if dest:
        os.remove(dest)
    pass
