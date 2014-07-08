#!/bin/sh

tree=$(ps -ef | grep -i 'py\|jar' | awk '{print $2}')
for pid in $tree; do
	echo $pid
	kill -9 $pid
done
