#! /bin/bash

HOMEDIR=build/
HOMEDIRDOC=docs/
HOMEDIR_ORIX=/home/travis/build/oric-software/orix

mkdir -p ../orix/usr/share/basic11/ 
mkdir -p ../orix/usr/share/ftdos/
mkdir -p ../orix/usr/share/sedoric/

LIST_COMMAND=`ls ../orix/usr/share/basic11/*/*.md`

echo Generate hlp

for I in $LIST_COMMAND
do
	echo Generate $I

	DESTFILE=`basename $I | cut -d '.' -f1`
	DESTFILE="${DESTFILE}.hlp"
	firstletter=${DESTFILE:0:1}
	echo $firstletter

	cat $I | python3 md2hlp/src/md2hlp.py3 -c md2hlp_basic11.cfg > ../orix/usr/share/basic11/$firstletter/$DESTFILE
done 

LIST_COMMAND=`ls ../orix/usr/share/ftdos/*/*.md`

echo Generate hlp ftdos

for I in $LIST_COMMAND
do
	echo Generate $I

	DESTFILE=`basename $I | cut -d '.' -f1`
	DESTFILE="${DESTFILE}.hlp"
	firstletter=${DESTFILE:0:1}
	echo $firstletter

	cat $I | python3 md2hlp/src/md2hlp.py3 -c md2hlp_basic11.cfg > ../orix/usr/share/ftdos/$firstletter/$DESTFILE
done 

LIST_COMMAND=`ls ../orix/usr/share/sedoric/*/*.md`

echo Generate hlp sedoric

for I in $LIST_COMMAND
do
	echo Generate $I

	DESTFILE=`basename $I | cut -d '.' -f1`
	DESTFILE="${DESTFILE}.hlp"
	firstletter=${DESTFILE:0:1}
	echo $firstletter

	cat $I | python3 md2hlp/src/md2hlp.py3 -c md2hlp_basic11.cfg > ../orix/usr/share/sedoric/$firstletter/$DESTFILE
done 

