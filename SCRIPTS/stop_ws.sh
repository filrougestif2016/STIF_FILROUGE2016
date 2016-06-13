#! /bin/bash

cd /infres/ir430/bd/stif/PYTHON/WEB_SERVER

# check if ES is running
if [ -f ws.pid ];
then
  PID=`cat ws.pid`
  if kill -TERM $PID;
  then
    echo "Web server has just been stopped"
  fi
else
    echo "File ws.pid not found in directory"
    echo "Unable to stop."
fi

