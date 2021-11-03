
full_list="scheduler announce bridge crossing lights radio tv train"

/bin/echo "Run this shell command on every subsystem."
/bin/echo "Subsystems: $full_list"
/bin/echo "Note: Use single quotes. We use doubles to surround the command."
/bin/echo -n "Command: "
read command
/bin/echo
/bin/echo "Running command: \"$prop\""
/bin/echo

for sub in $full_list; do
	/bin/echo "Connecting with brs-$sub.local"
	/bin/echo "=============================="
	ssh pi@brs-$sub.local "$command"
done
