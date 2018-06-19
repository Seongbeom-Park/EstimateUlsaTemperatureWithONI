#!/bin/bash
# parse ONI_v5.csv to add event to GlobalEvents.csv

# format: year\tDJF\tJFM\tFMA\tMAM\tAMJ\tMJJ\tJJA\tJAS\tASO\tSON\tOND\tNDJ

IFS_back=$IFS
IFS="	"
echo "Year,ppastMonth,pastMonth,currMonth,ONI"
while read -r line; do
	data=($line)
	year=${data[0]}
	if [ "$year" == "Year" ]; then
		continue
	fi
	for ((i=1; i<13; i++)); do
		if [ "${data[$i]}" == "" ]; then
			continue
		fi
		past=$((($i+10)%12+1))
		last=$((($i+11)%12+1))
		curr=$((($i+12)%12+1))
		echo ${year},$past,$last,$curr,${data[$i]}
	done
done < "$1"
IFS=$IFS_back
