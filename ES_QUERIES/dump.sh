#!/bin/sh
curl -XPUT 'lame14.enst.fr:50012/_snapshot/my_backup' -d '{
    "type": "fs",
    "settings": {
        "location": "my_backup",
        "compress": true
    }
}'
