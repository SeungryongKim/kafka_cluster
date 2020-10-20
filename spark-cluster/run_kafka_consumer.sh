#!/bin/bash

master_cid=$(docker ps --filter name=master -q)
kafka_ip=${1}

# Just one master container excutes command.
docker exec -it "$master_cid" sh -c "/spark/bin/spark-submit --master spark://spark-master:7077 --jars /kafka-consumer/spark-streaming-kafka-0-8-assembly_2.11-2.4.5.jar /kafka-consumer/direct_kafka_wordcount.py $kafka_ip 9092,9093,9094 test"

echo $kafka_ip
echo "/spark/bin/spark-submit --master spark://spark-master:7077 --jars /jars/spark-streaming-kafka-0-8-assembly_2.11-2.4.5.jar /spark/direct_kafka_wordcount.py $kafka_ip 9092,9093,9094 test"


