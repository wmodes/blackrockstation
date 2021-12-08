#!/bin/bash

full_list="scheduler announce bridge crossing lights radio television train"

opt="-o ConnectTimeout=1"
/bin/echo "param: $1"
command="$1"

if [ -z "$1" ]; then
	/bin/echo "Run this shell command on every subsystem."
	/bin/echo "Subsystems: $full_list"
	/bin/echo "Note: Use single quotes. We use doubles to surround the command."
	/bin/echo -n "Command: "
	read command
fi

/bin/echo
/bin/echo "Running command: \"$command\""
/bin/echo


for sub in $full_list; do
	/bin/echo "Connecting with brs-$sub.local"
	/bin/echo "=============================="
	ssh $opt pi@brs-$sub.local "$command"
done
