#!/bin/bash

#installing 'spc'
$(sudo mv "spc" /usr/bin/)

#installing 'man' page for 'spc'
if [ ! -d "/usr/local/share/man/" ];
	then
	$(mkdir "/usr/local/share/man/")
fi
if [ ! -d "/usr/local/share/man/man1/" ];
	then
	$(mkdir "/usr/local/share/man/man1/")
$(sudo mv "spc.1" "/usr/local/share/man/man1/")
$(sudo mandb)

#moving files of linux client to home
$(mv *.py  ~ )
$(mv lastsync.txt ~)
$(mv lstmod.txt ~)
$(mv not.sh ~)
$(mv sync_run.sh ~)
$(mv syncrun.sh ~)

#for crontab
$(echo "Enter path of a directory on which cronjob should be run :")
read direc
$(echo "* * * * * bash ~/not.sh '$direc'" >crontab.cron)
$(crontab crontab.cron)