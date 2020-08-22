#!/bin/bash
while true;
do
	sleep 4
	echo "begin"
	$(bash ~/sync.sh)
	echo "end"
done
