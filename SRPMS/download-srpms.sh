#!/bin/sh

echo
echo 'Select the operating system you want to download the source RPMs for:'
select os in 'CentOS/Scientific Linux 5' 'CentOS/Scientific Linux 6' 'Fedora 17' 'cancel'
do
	if [ "$os" = 'cancel' ]
	then
		exit
	elif [ "$os" = 'CentOS/Scientific Linux 5' ]
	then
		os='CentOS/5'
		break
	elif [ "$os" = 'CentOS/Scientific Linux 6' ]
	then
		os='CentOS/6'
		break
	elif [ "$os" = 'Fedora 17' ]
	then
		os='Fedora/17'
		break
	fi
done

echo
echo 'Select release or testing version (developers should choose testing):'
select release in 'testing' 'release' 'cancel'
do
	if [ "$os" = 'cancel' ]
	then
		exit
	else
		break
	fi
done
echo "-- $release/$os"

echo
echo 'Remove old SRPMS (Only from this folder)?'
select cleanup in 'yes' 'no'
do
	if [ "$cleanup" = 'yes' ]
	then
		rm -rf *.src.rpm
		break
	else
		break
	fi
done

echo 'Starting download...'
curl "http://lernfunk.de/matterhorn-repo/SRPMS/$release/$os/filelist.py" | \
  xargs -n1 -i curl -O "http://lernfunk.de/matterhorn-repo/SRPMS/$release/$os/{}"
