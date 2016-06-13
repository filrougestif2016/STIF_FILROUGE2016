#!/bin/sh

curl -XMGET 'lame14.enst.fr:50012/'$1'/_search?pretty' -d '{
"query" : { 
        "match_all" : {} 
    },
  "fields" : ["text"]
}'
