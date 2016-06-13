#! /bin/bash

cd /infres/ir430/bd/stif/PYTHON

# check if ES is running
if [ -f crawler.pid ];
then
  PID=`cat crawler.pid`
  if kill -TERM $PID;
  then
    echo "Crawler has just been stopped"
  fi
else
    echo "File crawler not found in PYTHON directory"
    echo "Unable to stop."
fi

