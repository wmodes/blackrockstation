
full_list="scheduler announce bridge crossing lights radio television train"

/bin/echo "Propagate changes from one subsystem main.py to others."
/bin/echo "Subsystems: $full_list"
/bin/echo "WARNING: Get the next question right or you will be overwriting your changes."
/bin/echo -n "Which main.py do you want to propagate? "
read prop
/bin/echo
/bin/echo "Propagating: $prop"
/bin/echo

prop_lower=$prop
prop_upper=$prop
prop_upper="$(tr '[:lower:]' '[:upper:]' <<< ${prop_upper:0:1})${prop_upper:1}"

for sub in $full_list; do
	if [ "$prop" != "$sub" ]; then
		/bin/echo "-> $sub"
		sub_upper=$sub
		sub_lower=$sub
		sub_upper="$(tr '[:lower:]' '[:upper:]' <<< ${sub_upper:0:1})${sub_upper:1}"
		#echo $sub_upper $sub_lower
		#echo $prop_upper $prop_lower
		sed "s/$prop_lower/$sub_lower/g;s/$prop_upper/$sub_upper/g" $prop/main.py > $sub/main.py
	fi
done
