#!/bin/bash

echo "Hold your horses. This might take a minute"
find . -name "*.mp4" | tar -cvzf video.tar.gz -T -
