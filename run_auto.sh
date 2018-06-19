#!/bin/bash

max_epoch=50

for ((i=0; i<$max_epoch; i++)) ; do
	echo epoch: $i
	./run.sh
done
bash pack.sh
