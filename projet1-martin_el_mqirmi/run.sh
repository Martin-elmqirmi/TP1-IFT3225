#!/bin/bash

FILENAME=$1
REPOSITORY=$2
for file in ${FILENAME}/*.html
do
     python3 ${0%/*}/transf.py --file_name=${file} --repository=${REPOSITORY}
done