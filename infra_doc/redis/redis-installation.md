# Redis installation

## Definde Var

```shell
REDIS_PASSWORD="xxxxxx"
REDIS_NAMESPACE=redis-api-cache
RELEASES_NAME=redis-api-cache
WOKRING_FOLDER=~/k8s_deployment/infra_doc/redis/
```

## Install Redis

```shell
cd $WOKRING_FOLDER

# create k8s namespace
kubectl create namespace $REDIS_NAMESPACE

# install redis cluster
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install $RELEASES_NAME bitnami/redis \
-n=$REDIS_NAMESPACE \
--set global.redis.password="$REDIS_PASSWORD" \
--set sentinel.enabled=true \
--set sentinel.masterSet=$RELEASES_NAME 

# wait for redis 3 pods to be ready
watch -n 1 kubectl get -n $REDIS_NAMESPACE all
## 
## NAME                              READY   STATUS    RESTARTS   AGE
## pod/redis-portal-session-node-0   2/2     Running   0          2m39s
## pod/redis-portal-session-node-1   2/2     Running   0          2m
## pod/redis-portal-session-node-2   2/2     Running   0          45s
```

## Validify Redis

```shell
## get password 
REDIS_PASSWORD=$(kubectl get secret --namespace $REDIS_NAMESPACE $RELEASES_NAME -o jsonpath="{.data.redis-password}" | base64 --decode)

# create redis client pod and go into container, auto remove when exit
kubectl run --namespace $REDIS_NAMESPACE redis-client --rm --tty -i \
--restart='Never' \
--image docker.io/bitnami/redis-cluster:6.2.5-debian-10-r9 \
--env="RELEASES_NAME=$RELEASES_NAME" \
--env="REDIS_PASSWORD=$REDIS_PASSWORD" \
-- bash

# go into redis-cli
redis-cli -c -h $RELEASES_NAME -a "$REDIS_PASSWORD" -p 26379

# show redis info
info

# exit redis cli
exit
# exit container
exit
```

## (optional) Install GUI tools (Redis insight)

## Definde Var

```shell
REDIS_INSIGHT_NODEPORT=31003
K8S_MASTER_IP=192.168.64.170
```

## Install Redis insight

```shell
# download redisinsight (redis GUI tools)
wget https://docs.redislabs.com/latest/pkgs/redisinsight-chart-0.1.0.tgz

# install redisinsight
helm install redis-insight redisinsight-chart-0.1.0.tgz -n=$REDIS_NAMESPACE --set nameOverride=redis-insight,fullnameOverride=redis-insight,image.tag=1.11.1



# expose gui in nodeport
cat <<EOF | kubectl apply -n=$REDIS_NAMESPACE -f -
apiVersion: v1
kind: Service
metadata:
  name: redis-insight-nodeport
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8001
      nodePort: $REDIS_INSIGHT_NODEPORT
  selector:
    app.kubernetes.io/instance: redis-insight
    app.kubernetes.io/name: redis-insight
  type: NodePort
EOF

# add database to gui
curl --location --request POST "http://$K8S_MASTER_IP:$REDIS_INSIGHT_NODEPORT/api/instance/" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"connectionType\": \"STANDALONE\",
    \"host\": \"$RELEASES_NAME.$REDIS_NAMESPACE\",
    \"name\": \"$RELEASES_NAME\",
    \"password\": \"$REDIS_PASSWORD\",
    \"port\": 6379,
    \"tls\": 
        {
            \"clientAuth\": false,
            \"useTls\": false,
            \"verifyServerCert\": true
        }
}"

# Success Response
# {"db":{"id":"0998dc3d-2904-45f5-a9d6-89f675022a0c","type":"STANDALONE","name":"redis-portal-session","host":"redis-portal-session.redis-portal-session","port":6379,"tls":false,"verifyServerCert":true,"caCertName":null,"tlsClientAuthRequired":false,"tlsClientCertId":null,"username":null,"password":"123456"},"msg":"Instance created successfully."}

# now you can view db in browser by below url
echo http://$K8S_MASTER_IP:$REDIS_INSIGHT_NODEPORT/
```

## Uninstall redis

```shell
helm uninstall $RELEASES_NAME -n=$REDIS_NAMESPACE
helm uninstall redis-insight -n=$REDIS_NAMESPACE
kubectl delete namespace $REDIS_NAMESPACE
```
