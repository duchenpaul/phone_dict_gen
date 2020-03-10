#!/bin/bash

process='aircrack-ng'
processID=`ps x | grep "${process}" | grep -v grep | awk -F ' ' '{print $1}' | tr '\n' ' '`

echo "Found processID: ${processID}"

if [ $# -ne 1 ]; then
  echo -e "Usage: bash $0 [start/stop]"
  exit 1
fi

if [ $1 = 'stop' ]; then
    kill -STOP ${processID}
fi

if [ $1 = 'start' ]; then
    kill -CONT ${processID}
fi