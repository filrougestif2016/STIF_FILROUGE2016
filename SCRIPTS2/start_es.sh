#! /bin/bash

cd /infres/ir430/bd/stif
#ulimit -n 4096

# check if ES is running
if [ -f elasticsearch-2.1.1/bin/elasticsearch.pid ];
then
  PID=`cat elasticsearch-2.1.1/bin/elasticsearch.pid`
  if kill -0 $PID;
  then
    echo "ElasticSearch is already running"
  else
    # start it and keep its pid
    elasticsearch-2.1.1/bin/elasticsearch &
    echo $! > elasticsearch-2.1.1/bin/elasticsearch.pid
  fi
else
  # start it and keep its pid
  elasticsearch-2.1.1/bin/elasticsearch &
  echo $! > elasticsearch-2.1.1/bin/elasticsearch.pid
fi

