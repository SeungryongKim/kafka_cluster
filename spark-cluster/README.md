# Spark Cluster
> Apache Kafka로 수집한 데이터들을 Docker Swarm 기반의 클러스터를 통해 Spark 기반의 데이터 처리를 지원하는 프로젝트입니다.  
   
   
> 두 대의 서버(Master, Worker)를 사용한 Clustering을 전제로 합니다.

Docker Swarm 클러스터에서 아래의 Docker 컨테이너들이 자동으로 실행됩니다.

* 3개의 Spark Worker 컨테이너(spark-worker-1, spark-worker-2, spark-worker-3)
* 1개의 Spark Master 컨테이너(spark-master)  
  

## 사전 설정 (CentOS7 기준)

Docker Compose를 활용한 서비스의 자동 실행을 위해서는 몇 가지 전제사항을 충족해야 합니다.

### 1. Docker Swarm 기반의 클러스터링 ([참고자료](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/))

Spark Cluster의 마스터 노드가 될 서버에서 아래 명령어를 수행합니다.  
`--advertise-addr` 옵션 뒤에 오는 IP 주소는 Worker 노드에서 접근 가능한 Master 노드의 IP 주소를 입력합니다.

`$ docker swarm init --advertise-addr 192.168.99.100`

새로운 Swarm Cluster가 생성이 되면 아래와 같은 메세지가 출력됩니다.  
출력된 메세지를 복사하여 Worker 노드에서 `docker swarm join --token [토큰] 마스터노드IP:2377` 명령을 실행하여 Cluster에 노드를 추가합니다.

```
Swarm initialized: current node (dxn1zf6l61qsb1josjja83ngz) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```


### 2. 컨테이너간 통신을 위한 네트워크 환경 설정 ([참고자료](https://docs.docker.com/engine/swarm/swarm-tutorial/))

Docker Swarm Cluster의 구성 노드들은 노드 간의 통신을 위해 몇 개의 포트를 사용합니다.

* TCP: 2377 (클러스터 관리)
* TCP/UDP: 7946 (노드 간 통신)
* UDP: 4789 (오버레이 네트워크 트래픽)

모든 서버에서 `firewall-cmd` 명령을 사용하여 해당되는 포트들을 방화벽에서 예외처리하여 노드 간 통신이 가능하도록 설정합니다.
   

```
# firewall-cmd --zone=public --permanent --add-port=2377/tcp
# firewall-cmd --zone=public --permanent --add-port=7946/tcp
# firewall-cmd --zone=public --permanent --add-port=7946/udp
# firewall-cmd --zone=public --permanent --add-port=4789/udp
# firewall-cmd --reload
```



### 3. Kafka Cluster 실행

Spark Cluster에서 처리할 데이터를 제공하는 Kafka Cluster가 구동 중이어야 합니다.

관련 내용은 해당 [README.md](https://github.com/SeungryongKim/kafka_cluster/blob/master/README.md) 파일을 확인 해주십시오.



## 실행 방법 (CentOS7 기준)

### 1. Docker 설치 (Master, Worker 노드)

```
sudo yum install docker-ce
```

### 2. Docker Compose 설치 (Master, Worker 노드)

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Docker Overlay Network 생성 (Master 노드)

컨테이너 간 동신을 위한 별도의 오버레이 네트워크를 생성합니다.

```
$ docker network --attachable create -d overlay spark-network
```

### 4. Spark Cluster 구성 컨테이너 배포 (Master 노드)

`docker-compose.yml` 파일 내에 정의된 서비스를 구성 스택을 Swarm 컨테이너 상에 배포합니다. 서비스의 배포 및 실행을 의미합니다.

```
$ docker stack deploy --compose-file docker-compose.yml test-spark
```

### 5. Spark Cluster 실행 확인 (Master 노드)

서비스의 정상 실행 확인을 위하여, 아래 명령어를 통해 각 노드 별 컨테이너 배포 상황을 확인합니다.

```
$ docker stack ps test-spark
```

더불어 `http://마스터 노드의 IP:18080` 주소로 접속하여 웹 기반 UI를 통해 클러스터 구성과 작업 처리 현황을 확인할 수 있습니다.


### 6. Kafka Consuer 예제 실행 (Master 노드)

* Spark Cluster 구축 뒤에는 `run_kafka_consumer.sh [Kafka Cluster 설치 서버의 IP]` 명령을 통하여,   
Kafka Cluster로 수집한 데이터를 가져온 뒤 WordCount 예제를 수행할 수 있습니다.   

* 명령 실행 후 컨테이너 내에서 stdout으로 출력된 각 메세지 별 WordCount 결과를 실시간으로 확인할 수 있습니다.

* Kafka broker들이 사용하는 포트 번호와 토픽명은 스크립트 내에서 직접 수정할 수 있습니다.

* 실행되는 WordCount 예제는 `PySpark`의 Kafka 라이브러리를 사용하며, 해당 코드 내용의 수정을 통하여 수집한 데이터의 전처리를 지원할 수 있습니다.


## 업데이트 내역

* 0.1.0
    * 첫 배포
    * 기본 서비스 구성 및 예제 스크립트 작성

## 개발자 정보

유클리드소프트 부설연구소  
선임연구원 김승룡 (srkim@euclidsoft.co.kr)
