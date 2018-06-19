#!/bin/bash

TARGET_DIR=packing_F1990_C2010_L2015_100_20_NOONI
mkdir $TARGET_DIR
mv results* $TARGET_DIR
mv model* $TARGET_DIR
cp epoch.dat $TARGET_DIR
bash reset.sh
