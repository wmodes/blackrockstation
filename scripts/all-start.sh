
full_list="scheduler announce bridge crossing lights radio television train"

opt="-o ConnectTimeout=1"


for sub in $full_list; do
	command="cd blackrockstation;nohup python start.py $sub &"
	/bin/echo "Connecting with brs-$sub.local"
	/bin/echo "=============================="
	ssh $opt pi@brs-$sub.local "$command"
done
