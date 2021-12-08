#!/bin/bash

media_list="announce radio television train"

for sub in $media_list; do
	/bin/echo "Connecting with brs-$sub.local"
	/bin/echo "=============================="
	rsync --verbose -au $sub/data pi@brs-$sub.local:blackrockstation/$sub/
done
