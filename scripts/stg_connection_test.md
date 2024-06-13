# Connection Test

## DMZ k8s to internal k8s

ssh esso@10.14.0.93
kubectl run -it --rm --image=wbitt/network-multitool --restart=Never test-pod-curl -- ping -c 3 -W 5 10.14.0.54

## DMZ k8s to TOMS

ssh esso@10.14.0.93
kubectl run -it --rm --image=wbitt/network-multitool --restart=Never test-pod-curl -- ping -c 3 -W 5 10.14.0.103

## Internal k8s to mariadb01

ssh esso@10.14.0.51
kubectl run -it --rm --image=mariadb --restart=Never test-pod-mariadb -- bash
mysql -h 10.14.0.91 -u admin -p
create database testing_db;
drop database testing_db;

## Internal k8s to mongodb in k8s

ssh esso@10.14.0.51
kubectl run -it --rm --image=mongo --restart=Never test-pod-mongodb -- bash
mongo "mongodb://root@mongodb-c1-0.mongodb-c1-headless.mongodb-c1.svc,mongodb-c1-1.mongodb-c1-headless.mongodb-c1.svc,mongodb-c1-2.mongodb-c1-headless.mongodb-c1.svc/?authSource=admin&replicaSet=rs0&readPreference=primary"
use testing_db
db.new_collection.insert({ some_key: "some_value" })

## Internal k8s to pulsar

ssh esso@10.14.0.51
kubectl run -it --rm \
--image=harbor.atlsmartsolutions.com/library/pulsar-tester/pulsartester \
--env='URL=pulsar://10.14.0.77:6650' \
--env='TOPIC=persistent://public/default/test-topic' \
--restart=Never \
test-pod-pulsar

## TOMS to mongodb standalone

ssh esso@10.14.0.103
sudo docker pull mongo
sudo docker run -it --rm mongo bash
mongo "mongodb://admin@10.14.0.102/?authSource=admin"
use testing_db
db.new_collection.insert({ some_key: "some_value" })

## TOMS to keycloay standalone

ssh esso@10.14.0.103
curl <https://10.14.0.101:8443/> --insecure -I
curl <http://10.14.0.101:8080/> -I
curl <http://10.14.0.101:8080/auth/realms/master>

## TOMS to mariadb02

ssh esso@10.14.0.103
sudo docker pull mariadb
sudo docker run -it --rm mariadb mysql -h 10.14.0.92 -u admin -p
create database testing_db;
drop database testing_db;
