#!/bin/bash

WEATHER_HOME=`pwd`

SUBMIT_SH=$WEATHER_HOME/scripts/submit.sh
TF_PY=$WEATHER_HOME/scripts/temperature_predictor.py
ASOS_FILE=$WEATHER_HOME/Meteorological_Data/ASOS.Ulsan.6hr.1980-2017.csv
#ONI_FILE=$WEATHER_HOME/Meteorological_Data/ONI_v5.csv
ONI_FILE=$WEATHER_HOME/Meteorological_Data/ONI_v5_parsed.csv
MODEL_DIR=$WEATHER_HOME/model
RESULT=$WEATHER_HOME/results
EPOCH_DAT=$WEATHER_HOME/epoch.dat

epoch_count=`cat $EPOCH_DAT`

pid=`bash $SUBMIT_SH $TF_PY $ASOS_FILE $ONI_FILE $MODEL_DIR`
echo $pid
sleep 1
live=`qstat | grep $pid`
while [ "$live" != "" ]; do
	sleep 1
	live=`qstat | grep $pid`
done
tail -n 1 $RESULT/temperature_predictor.o

cp -r $MODEL_DIR ${MODEL_DIR}_$epoch_count
mv $RESULT ${RESULT}_$epoch_count
epoch_count=$(($epoch_count+1))

echo $epoch_count > $EPOCH_DAT
echo "Done"
