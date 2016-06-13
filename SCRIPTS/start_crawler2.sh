#! /bin/bash

# add anaconda2 bin dir in path
export PATH="/infres/ir430/bd/stif/anaconda2/bin:$PATH"

# start conda environment
source activate stif

cd /infres/ir430/bd/stif/PYTHON

# check if ES is running
if [ -f crawler2.pid ];
then
  PID=`cat crawler2.pid`
  if kill -0 $PID;
  then
    echo "Crawler is already running"
  else
    # start it and keep its pid
    python twitter_stream2.py &
    echo $! > crawler2.pid
  fi
else
  # start it and keep its pid
  python twitter_stream2.py &
  echo $! > crawler2.pid
fi

