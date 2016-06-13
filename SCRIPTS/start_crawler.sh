#! /bin/bash

# add anaconda2 bin dir in path
export PATH="/infres/ir430/bd/stif/anaconda2/bin:$PATH"

# start conda environment
source activate stif

cd /infres/ir430/bd/stif/PYTHON
mv *.output OUTPUTS

# check if ES is running
if [ -f crawler.pid ];
then
  PID=`cat crawler.pid`
  if kill -0 $PID;
  then
    echo "Crawler is already running"
  else
    # start it and keep its pid
    python twitter_stream_classif.py &
    echo $! > crawler.pid
  fi
else
  # start it and keep its pid
  python twitter_stream_classif.py &
  echo $! > crawler.pid
fi

