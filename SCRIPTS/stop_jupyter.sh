#! /bin/bash

process=`ps -ef|grep jupyter|awk '{print $2}'`

kill -TERM $process
