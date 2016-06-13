#! /bin/sh

curl -XPUT http://lame14.enst.fr:$1/_template/stif_tpl -d '
{
 "template": "stif-*",
      "mappings": {
         "stif": {
            "properties": {
               "@timestamp": {
                  "type": "date",
                  "format": "strict_date_optional_time||epoch_millis"
               },
               "@version": {
                  "type": "string"
               },
               "datasetid": {
                  "type": "string"
               },
               "fields": {
                  "properties": {
                     "agency_name": {
                        "type": "string"
                     },
                     "id_line": {
                        "type": "string"
                     },
                     "pointgeo": {
			"type": "geo_point"
                     },
                     "route_id": {
                        "type": "string"
                     },
                     "route_long_name": {
                        "type": "string"
                     },
                     "route_short_name": {
                        "type": "string"
                     },
                     "route_type": {
                        "type": "long"
                     },
                     "stop_id": {
                        "type": "string"
                     },
                     "stop_lat": {
                        "type": "double"
                     },
                     "stop_lon": {
                        "type": "double"
                     },
                     "stop_name": {
                        "type": "string"
                     },
                     "zder_id_ref_a": {
                        "type": "long"
                     }
                  }
               },
               "geometry": {
                  "properties": {
                     "coordinates": {
                        "properties": {
                           "lat": {
                              "type": "double"
                           },
                           "lon": {
                              "type": "double"
                           }
                        }
                     },
                     "type": {
                        "type": "string"
                     }
                  }
               },
               "host": {
                  "type": "string"
               },
               "record_timestamp": {
                  "type": "date",
                  "format": "strict_date_optional_time||epoch_millis"
               },
               "recordid": {
                  "type": "string"
               }
            }
         }
      }
}'
