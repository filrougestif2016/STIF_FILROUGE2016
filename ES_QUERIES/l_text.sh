#!/bin/sh

curl -XMGET 'lame14.enst.fr:50012/'$1'/_search?size='$2'&from='$3'&pretty' -d '{
"query" : { 
        "match_all" : {} 
    },
  "fields" : ["text"]
}'
