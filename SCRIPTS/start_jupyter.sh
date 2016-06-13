#! /bin/bash

# add anaconda2 bin dir in path
export PATH="/infres/ir430/bd/stif/anaconda2/bin:$PATH"

# start conda environment
source activate stif

cd /infres/ir430/bd/stif/IPYNB

# check if jupyter is running
if [ -f jupyter.pid ];
then
  PID=`cat jupyter.pid`
  if kill -0 $PID;
  then
    echo "Jupyter is already running"
  else
    # start it and keep its pid
    jupyter notebook --no-browser > jupyter.log 2>&1 &
    echo $! > jupyter.pid
  fi
else
  # start it and keep its pid
  jupyter notebook --no-browser > jupyter.log 2>&1 &
  echo $! > jupyter.pid
fi

