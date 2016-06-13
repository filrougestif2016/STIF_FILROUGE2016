#! /bin/sh

curl -XPUT http://lame14.enst.fr:$1/_template/stif_info_trafic_tpl -d '
{
        "template" : "stif_info_trafic",
        "mappings" : {

      "stif_info_trafic" : {
        "properties" : {
          "pub_date" : {
	    "type": "date", "format": "EEE, dd MMM yyyy HH:mm:ss"
          },
          "description" : {
            "type" : "string"
          },
          "texte" : {
            "type" : "string"
          },
          "titre" : {
            "type" : "string"
          }
        }
      }
    }
}'
