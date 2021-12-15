#!/bin/bash

media_list="announce radio television train"

/bin/echo "This will distro media files to controllers that require them."
/bin/echo "Available controllers: $media_list"
/bin/echo "NOTE: This should be run in brs root dir."
/bin/echo
/bin/echo "You can specify one or more controllers, or hit enter for all."
/bin/echo -n "Controller(s): "
read list

if [ -z $list];then
	list="$media_list"
fi

for sub in $list; do
	/bin/echo "Connecting with brs-$sub.local"
	/bin/echo "=============================="
	rsync --verbose -au $sub/data pi@brs-$sub.local:blackrockstation/$sub/
done
