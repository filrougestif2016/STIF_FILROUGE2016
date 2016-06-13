/infres/ir430/bd/stif/spark-1.5.2/bin/spark-submit --master spark://lame14.enst.fr:7077 sparkSample.py
# local ==> le master est en local
# [4] ==> 4 core
/infres/ir430/bd/stif/spark-1.5.2/bin/spark-submit --master spark://lame14.enst.fr:7077 --conf "spark.driver.extraClassPath=/infres/ir430/bd/stif/spark_connector_cass/spark-cassandra-connector-assembly-1.4.0-M1-SNAPSHOT.jar --conf "spark.jars=/infres/ir430/bd/stif/spark_connector_cass/spark-cassandra-connector-assembly-1.4.0-M1-SNAPSHOT.jar" sparkCassandraSample.py

