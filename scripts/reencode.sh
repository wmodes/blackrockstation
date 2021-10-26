
fromDir="edited"
destDir="transcode"

ffmpegOpt="-vf 'scale=-1:480, crop=ih/3*4:ih' -c:v libx264 -preset veryslow -crf 23 -c:a aac -strict -2"

/bin/echo -n "Enter media folder: "
read mediaDir

if [ ! -d "$mediaDir" ]; then
  echo "Folder not found: \"$mediaDir\""
  exit 1
else
  echo "Valid media folder: \"$mediaDir\""
fi

cd "$mediaDir"

if [ ! -d "$fromDir" ]; then
  echo "No folder \"$fromDir\", recheck media folder."
  exit 1
else
  echo "Origin folder \"$fromDir\" found"
fi

# if destination doesn't exist, create it
[ ! -d "$destDir" ] && mkdir $destDir

if [ ! -d "$destDir" ]; then
  echo "No destination folder \"$destDir\" found, creating."
  mkdir $destDir
else
  echo "Destination folder \"$destDir\" found."
fi

echo "Transcoding files"
echo "================="

list=`cd edited;ls`

for i in $list; do
  ffmpeg -i "$fromDir/$i" $ffmpegOpt "$destDir/${i%.*}.mp4"
done

cd "$fromDir"
find . -type f -exec sh -c '
