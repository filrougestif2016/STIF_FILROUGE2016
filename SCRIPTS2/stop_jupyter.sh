#! /bin/bash

cd /infres/ir430/bd/stif/IPYNB

# check if jupyter is running
if [ -f jupyter.pid ];
then
  PID=`cat jupyter.pid`
  if kill -TERM $PID;
  then
    echo "jupyter has just been stopped"
  fi
else
    echo "File jupyter not found in IPYNB directory"
    echo "Unable to stop."
fi

