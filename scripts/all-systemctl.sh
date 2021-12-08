#!/bin/bash

full_list="scheduler announce bridge crossing lights radio television train"

opt="-o ConnectTimeout=1"
/bin/echo "param: $1"
cmd="$1"

for sub in $full_list; do
	fullcmd="sudo systemctl $cmd brs.service"
	/bin/echo "Connecting with brs-$sub.local"
	/bin/echo "=============================="
	ssh $opt pi@brs-$sub.local "$fullcmd"
done
