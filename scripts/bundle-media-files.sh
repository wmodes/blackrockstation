echo "Hold your horses. This might take a minute"
find . -name '*.mp3' -exec tar -rvf media.tar {} \;
gzip media.tar

