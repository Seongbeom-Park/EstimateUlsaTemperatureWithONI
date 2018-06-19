#!/bin/bash

PACKING=$1
EPOCH=50

echo "epoch,average_loss,global_step,loss"
for ((epoch=0; epoch<$EPOCH; epoch++)) ; do
	#echo $PACKING/results_$i/temperature_predictor.o
	result=`tail -n 1 $PACKING/results_$epoch/temperature_predictor.o`
	IFS_back=$IFS
	IFS="\{\}:, \'"
	data=($result)
	average_loss=${data[4]}
	global_step=${data[8]}
	loss=${data[12]}
	IFS=$IFS_back
	echo $epoch,$average_loss,$global_step,$loss
done
