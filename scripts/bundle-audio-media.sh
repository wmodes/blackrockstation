#!/bin/bash

echo "Hold your horses. This might take a minute"
find . -name "*.mp3" | tar -cvzf audio.tar.gz -T -
