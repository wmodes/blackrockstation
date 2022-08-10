
mediadir="train/data"
echo "Looking in $mediadir for train audio."
echo

cd $mediadir
for file in *.wav; do
dur=`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $file`
echo $dur $file
done
