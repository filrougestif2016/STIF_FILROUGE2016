#!/bin/sh

curl -XMGET 'lame14.enst.fr:50014/'$1'/_search?size=10000&pretty' -d '{
"query" : { 
        "match_all" : {} 
    },
  "fields" : ["text"]
}'
