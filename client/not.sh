#!/bin/sh
stamp_fold="$1"
st=$(find "$1" -exec stat  -c "%n %y" {} \;)
echo "$st" > lstmod.txt
#cat lstmod.txt
dmax=0
while read LINE
do
id="$( cut -d ' ' -f 1 <<< "$LINE" )"
string="$( cut -d ' ' -f 2- <<< "$LINE" )"
d1=$(date -d "$string")
d11=$(date -d "$d1" "+%s")
if (( $dmax < $d11 ))
then
dmax=$d11
fi
done < lstmod.txt
#echo $dmax
dlast=$(cat lastsync.txt)
#echo $dlast
span=$(( $dmax - $dlast ))
#echo $span
if (( $span > 1 ))
then
zenity --info --title "Secure Personal Cloud" --text "Alert:You have not synced since a week." --timeout=5
fi
#lastUpdate=$(date -r sync.py +%s)
#now=$(date +%s)
# file_age=$(( $d1 - $d2 ))
# echo $file_age
#if [ $delta -ge $interval ]
#then
#zenity --info --title "Secure Personal Cloud" --text "Alert:You have not synced since a week." --timeout=5
#fi
#echo $delta
#echo $now
#echo $stamp
