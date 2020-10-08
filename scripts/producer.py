from kafka import KafkaProducer
from json import dumps
import time
from time import sleep

def on_send_success(record_metadata):
    # 보낸데이터의 매타데이터를 출력한다
    print("record_metadata:", record_metadata)
    
# 카프카 서버
bootstrap_servers = ["localhost:9092","localhost:9093","localhost:9094"]

# 카프카 공급자 생성
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         key_serializer=None,
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

# 카프카 토픽
str_topic_name = 'test'

# 카프카 공급자 토픽에 데이터를 보낸다
data = {"time": time.time()}
while(True):
    producer.send(str_topic_name, value=data).add_callback(on_send_success)\
                                         .get(timeout=100) # blocking maximum timeout
    print('data:', data)
    sleep(1)
