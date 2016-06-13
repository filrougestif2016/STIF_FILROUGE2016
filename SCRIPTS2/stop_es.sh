#! /bin/bash

cd /infres/ir430/bd/stif

# check if ES is running
if [ -f elasticsearch-2.1.1/bin/elasticsearch.pid ];
then
  PID=`cat elasticsearch-2.1.1/bin/elasticsearch.pid`
  if kill -TERM $PID;
  then
    echo "ElasticSearch has just been stopped"
  fi
else
    echo "File elasticsearch.pid not found in es bin directory"
    echo "Unable to stop."
fi

