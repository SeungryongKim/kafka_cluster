# kafka_cluster
> Apache Kafka를 활용한 데이터 수집을 위한 Docker 기반 컨테이너들을 Docker Compose를 활용하여 배포하는 간단한 프로젝트입니다.

로컬 환경에서 아래의 Docker 컨테이너들이 자동으로 실행됩니다.

* 3개의 Kafka brokers 컨테이너와(kafka-1, kafka-2, kafka-3)
* 1개의 Zookeeper 컨테이너(zookeeper-1)
* 1개의 topic 설정 컨테이너(컨테이너명: kafka-setup, 토픽명: test)
* 현재 시각을 메세지에 담아 전송하는 producer 컨테이너 1개(컨테이너명: sample_producer)
* test 토픽으로 전달된 메세지를 stdout으로 출력하는 consumer 컨테이너 1개(컨테이너명: sample_consumer)

Producer, consumer 컨테이너에서는 kafka-python 라이브러리를 사용하는 파이썬 스크립트가 실행됩니다.  
해당 스크립트들은 `scripts` 경로 아래에 저장되어 있습니다.

## 실행 방법 (CentOS 7 기준)

1. Docker 설치

```sh
sudo yum install docker-ce
```

2. Docker Compose 설치

```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. `docker-compose.yml` 파일이 위치한 경로로 작업 폴더를 이동하여 서비스 실행
```sh
cd kafka_cluster
docker-compose up -d
```

## 실행 결과 확인

정상적으로 서비스가 실행되면, 아래와 같은 메세지가 출력됩니다.

`Creating kafka_cluster_zookeeper-1_1 ... done`  
`Creating kafka_cluster_kafka-3_1     ... done`  
`Creating kafka_cluster_kafka-2_1     ... done`  
`Creating kafka_cluster_kafka-1_1     ... done`  
`Creating kafka_cluster_kafka-setup_1 ... done`  
`Creating kafka_cluster_sample_producer_1 ... done`  
`Creating kafka_cluster_sample_consumer_1 ... done` 


## Kafka를 통해 전달된 메세지 확인

아래와 같이 `docker logs` 명령을 입력하면 컨테이너 내에서 stdout으로 출력된 메세지 내용을 확인할 수 있습니다.
```sh
docker logs kafka_cluster_sample_producer_1
docker logs kafka_cluster_sample_consumer_1
```


## Custom Producer, Consumer 작성

Producer, consumer 컨테이너는 Kafka 라이브러리를 활용하는 Python 스크립트를 실행합니다.  
따라서 실행하는 스크립트의 내용을 적절히 수정하면 원하는 기능을 수행하는 producer 및 consumer를 작성할 수 있습니다.  

상세한 내용은 `scripts/producer.py`와 `scripts/consumer.py` 파일의 내용과, 공식 홈페이지에서 제공하는 [문서](https://kafka-python.readthedocs.io/en/master/usage.html)를 참조하시기 바랍니다.

## 업데이트 내역

* 0.1.0
    * 첫 배포
    * 기본 서비스 구성 및 예제 스크립트 작성

## 개발자 정보

유클리드소프트 부설연구소  
선임연구원 김승룡 (srkim@euclidsoft.co.kr)
