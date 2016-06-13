#! /bin/bash

# add anaconda2 bin dir in path
export PATH="/infres/ir430/bd/stif/anaconda2/bin:$PATH"

# start conda environment
source activate stif

cd /infres/ir430/bd/stif/PYTHON/WEB_SERVER

# check if web server is running
if [ -f ws.pid ];
then
  PID=`cat ws.pid`
  if kill -0 $PID;
  then
    echo "Web server is already running"
  else
    # start it and keep its pid
    python http_srv.py runserver -h lame14.enst.fr > ws.log 2>&1 &
    echo $! > ws.pid
  fi
else
  # start it and keep its pid
  python http_srv.py runserver > ws.log 2>&1 &
  echo $! > ws.pid
fi

