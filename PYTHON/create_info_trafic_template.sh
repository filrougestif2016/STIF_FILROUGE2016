#! /bin/sh

curl -XPUT http://lame14.enst.fr:$1/_template/info_trafic_tpl -d '
{
        "template" : "info_trafic",
        "mappings" : {

      "info_trafic" : {
        "properties" : {
          "id" : {
	    "type": "date", "format": "EEE, dd MMM yyyy HH:mm:ss"
          },
          "infos" : {
            "properties" : {
              "description" : {
                "type" : "string"
              },
              "pub_date" : {
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
      }
    }
}'
