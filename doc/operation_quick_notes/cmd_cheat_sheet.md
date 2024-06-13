# K8S_Deployment

## Helpful Commands

## create das middleware cert

```bash
APPNAME=das-middleware-tsc
kubectl create secret tls $APPNAME-server-tls --cert=_common_server_crt.pem --key=_common_server_key.pem -n bes
# ------------------------------------------------------------------------------------------------------------------------
APPNAME=das-middleware
kubectl create secret tls $APPNAME-server-tls --cert=$APPNAME.crt --key=$APPNAME.key -n bes

APPNAME=das-middleware-tsc
kubectl create secret tls $APPNAME-server-tls --cert=$APPNAME.crt --key=$APPNAME.key -n bes

APPNAME=das-middleware-lrt
kubectl create secret tls $APPNAME-server-tls --cert=$APPNAME.crt --key=$APPNAME.key -n bes

APPNAME=das-middleware-smt
kubectl create secret tls $APPNAME-server-tls --cert=$APPNAME.crt --key=$APPNAME.key -n bes


```

## Stop all das-middleware from argocd

```bash
# exec this command on NP, P1, P2, dmz k8s master ikubm1

# login argocd
kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd login 127.0.0.1:8080 --insecure --username admin --password 'Atl@2022'

# change all das-middleware replicaCount to 0
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep 'das-middleware');do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app set -p replicaCount=0 $app_name && echo $app_name; done

# remove overrided parameters
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep 'das-middleware');do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app unset -p replicaCount $app_name && echo $app_name; done
```

## Stop all consumer from argocd

```bash
# exec this command on NP, P1, P2, dmz k8s master tkubm1
# login argocd
kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd login 127.0.0.1:8080 --insecure --username admin --password 'Atl@2022'

# change all consumer replicaCount to 0
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep consumer | grep -v bes-notification-pulsar-consumer-services);do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app set -p replicaCount=0 $app_name; done

# remove overrided parameters
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep consumer | grep -v bes-notification-pulsar-consumer-services);do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app unset -p replicaCount $app_name; done
```

## Stop service from argocd

```bash
# stop service by change pod number to zero
kubectl patch Application --type=merge -n=argocd -p '{"spec":{"source":{"helm":{"parameters":[{"name":"replicaCount","value":"0"}]}}}}' my-app

kubectl exec deploy/argocd-server -n argocd -- bash -c "argocd app set my-app -p replicaCount=0"

# start service by change pod number to one
kubectl patch Application --type=merge -n=argocd -p '{"spec":{"source":{"helm":{"parameters":[{"name":"replicaCount","value":"1"}]}}}}' das-data-consumer
```

## remove finalizers

```bash
# get list all object with finalizers
kubectl get $(kubectl api-resources --namespaced=true --no-headers -o name | grep -v -E 'events|bindings$|localsubjectaccessreviews' | paste -s -d, - ) -o custom-columns=NS:.metadata.namespace,Kind:.kind,Name:.metadata.name,Finalizers:.metadata.finalizers --all-namespaces | grep wrangler.cattle.io

# remove finalizer
kubectl patch -n argocd RoleBinding argocd-application-controller -p '{"metadata":{"finalizers":null}}' --type=merge
```

## install ingress-nginx

```bash
helm template ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace \
  --set controller.service.externalIPs=["192.168.64.170"]
```

## das middleware pulsar

```bash
kubectl rollout restart -n pulsar-das-middleware statefulset.apps/pulsar-das-middleware-zookeeper
kubectl logs -n pulsar-das-middleware -f --since=0s -l component=zookeeper
```

## kube exec first pod by label

```bash
LABEL=app=flannel
NAMESPACE=kube-system
kubectl exec -i -t -n $NAMESPACE $(kubectl get pod -l "$LABEL" -o name -n $NAMESPACE | head -n 1) -- bash
```

### scp file transfer

```bash
scp -r "C:\Users\isaacyip\Desktop\Projects\gitlab_repo\k8s_deployment\k8s_argocd_yaml" esso@10.14.0.93:~/k8s_argocd_yaml/
```

### remote apply

```shell
ssh esso@10.14.0.51 'rm -r ~/k8s_argocd_yaml/'
scp -r "C:\Users\isaacyip\Desktop\Projects\gitlab_repo\k8s_deployment\k8s_argocd_yaml" esso@10.14.0.51:~/k8s_argocd_yaml/

ssh esso@10.14.0.51 'kubectl apply -n argocd -f ~/k8s_argocd_yaml/'
kubectl apply -n argocd -f ~/k8s_argocd_yaml/bes/stg/argo-das-data-consumer.yaml
```

### login by key

```shell
scp C:\Users\isaacyip\.ssh\id_rsa.pub esso@10.14.0.51:~/.ssh/authorized_keys
scp ~/.ssh/id_rsa.pub esso@10.14.0.51:~/.ssh/authorized_keys
```

### Watch resource by app name

```shell
watch -n 1 kubectl get all --namespace=bes -l="app=ffts-k8s-dashborad"
```

### Watch resource by namespace

```
watch -n 1 kubectl get $(kubectl api-resources --namespaced=true --no-headers -o name | egrep -v 'events|nodes' | paste -s -d, - ) --namespace kong
```

### Show pod cpu and memory config

```
kubectl get pod -n bes -o custom-columns=CONTAINER:.spec.containers[0].name,IMAGE:.spec.containers[0].image,MIN_CPU:.spec.containers[0].resources.requests.cpu,MAX_CPU:.spec.containers[0].resources.limits.cpu,MIN_MEMORY:.spec.containers[0].resources.requests.memory,MAX_MEMORY:.spec.containers[0].resources.limits.memory,STATUS:.status.phase

kubectl get pod -n bes -o custom-columns="\
APP_NAME:.metadata.labels.app,\
CONTAINER:.spec.containers[0].name,\
IMAGE:.spec.containers[0].image,\
MIN_CPU:.spec.containers[0].resources.requests.cpu,\
MAX_CPU:.spec.containers[0].resources.limits.cpu,\
MIN_MEMORY:.spec.containers[0].resources.requests.memory,\
MAX_MEMORY:.spec.containers[0].resources.limits.memory,\
STATUS:.status.phase" | uniq

kubectl get pod -n bes -o custom-columns="\
APP_NAME:.metadata.labels.app,\
MIN_CPU:.spec.containers[0].resources.requests.cpu,\
MAX_CPU:.spec.containers[0].resources.limits.cpu,\
MIN_MEMORY:.spec.containers[0].resources.requests.memory,\
MAX_MEMORY:.spec.containers[0].resources.limits.memory" | uniq


kubectl get deploy -n bes -o custom-columns="\
APP_NAME:.metadata.labels.app,\
REPLICA_COUNT:.spec.replicas"

```

### Streaming logs by app name

```shell
kubectl logs --follow --tail=10 --since=1h --namespace=poc -l="app=ffts-k8s-dashborad"
```

### List all nodeport in k8s

```shell
kubectl get svc --all-namespaces -o go-template='{{range .items}}{{ $svc := . }}{{range.spec.ports}}{{if .nodePort}}{{.nodePort}}{{","}}{{if .name}}{{printf "%-10s" .name}}{{else}}{{printf "%-10s" ""}}{{end}}{{","}}{{$svc.metadata.namespace}}{{","}}{{$svc.metadata.name}}{{"\n"}}{{end}}{{end}}{{end}}'
```

### Check max pod of node

```shell
kubectl get node -o custom-columns=NAME:.metadata.name,MAX_PODS:.status.allocatable.pods
```

### download helm charts

```shell
helm pull bitnami/redis --untar --untardir ./redis-helm-charts
```

### Render k8s yaml files from helm charts

```shell
RELEASE=secondocr-webapi
CHARTS_PATH=~/k8s_deployment/BES/secondocr_webapi
helm template $RELEASE $CHARTS_PATH --output-dir=./otuput-dir --dry-run
```

### k8s, docker Run container

```shell
sudo docker run -it --rm -v ~/bes_web_config:/my-mongodb/ mongo bash
kubectl run -it --rm --image=nicolaka/netshoot --restart=Never my-con bash
kubectl run -it --rm --image=mongo --restart=Never my-con bash
```

### restore mongodb

```shell
DB_FILE_PATH=~/bes_web_config
sudo docker run -it --rm -v $DB_FILE_PATH:/my-mongodb/ mongo mongorestore -u=root "mongodb://10.14.0.54:32100,10.14.0.57:32101,10.14.0.59:32102/?authSource=admin&replicaSet=rs0&readPreference=primary&ssl=false" /my-mongodb/
```

### Add nodePort service

```shell
$NAMESPACE=bes
$SVC_NAME=my-svc-nodeport
$LABEL_APP=toms-api
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: $SVC_NAME
  namespace: $NAMESPACE
  labels:
    app: $LABEL_APP
spec:
  ports:
    - name: https
      protocol: TCP
      port: 443
      targetPort: 443
      nodePort: 30222
  selector:
    app: $LABEL_APP
  type: NodePort
EOF
```

### copy values file

```shell
find ./ -name values.yaml -exec mkdir -p "../temp/{}"  \;
find ../temp/ -name *.yaml -delete

find ./ -name values.yaml -exec cp "{}" "../temp/{}"  \;
find ./ -name values-*.yaml -exec cp "{}" "../temp/{}"  \;
```

### clear docker images

```bash
docker image prune -f
df -H
docker image rm $(docker images --filter=reference='172*/*/*:*' --filter=reference='bes/*:*' | awk '{if(NR > 1 && $2 != "<none>" && $2 != "p1") {print $1":"$2}}')
```

### delete filter older than 7 days

```bash
find /mnt/data/tmp_upload_images/trash_can/ -mtime +7 -delete
```

### create folder for deploy script

```bash
mkdir -p /mnt/data/tmp_upload_images/trash_can

chmod -R 774 /mnt/data/tmp_upload_images/
chown -R user00 /mnt/data/tmp_upload_images/
ln -s /mnt/data/tmp_upload_images /home/user00/tmp_upload_images
chmod 774 /home/user00/tmp_upload_images
chown user00 /home/user00/tmp_upload_images
```

### delete index in elasticsearch

```bash
curl 'http://172.16.148.145:9200/_cat/indices' -H 'Authorization:Basic bG9nc3Rhc2hfaW50ZXJuYWw6QXRsQDIwMjI=' > elastic_indexs.txt

cat elastic_indexs.txt | awk '{print $3}' | grep 2023.02 > elastic_indexs_delete.txt

cat elastic_indexs_delete.txt | wc -l

for e_index_name in $(cat elastic_indexs_delete.txt);do curl -H 'Authorization:Basic bG9nc3Rhc2hfaW50ZXJuYWw6QXRsQDIwMjI=' -X DELETE http://172.16.148.145:9200/${e_index_name}; done
```

### copy only values-nonprod-common.yaml for deployment

```bash
mkdir ./k8s_yaml_appsettings
find ./k8s_yaml -name "values-nonprod-common.yaml" -exec cp --parents {} ./k8s_yaml_appsettings/ \;
find ./k8s_yaml -name "values-nonprod-app-settings.yaml" -exec cp --parents {} ./k8s_yaml_appsettings/ \;
find ./k8s_yaml -name "values-nonprod-image-tag.yaml" -exec cp --parents {} ./k8s_yaml_appsettings/ \;
find ./k8s_yaml -path "*/values-others/values-nonprod-*" -exec cp --parents {} ./k8s_yaml_appsettings/ \;


find ./k8s_yaml_appsettings/k8s_yaml -name "values-nonprod-common.yaml" -delete
```

### delete non used values file

```shell
find ./ -name values-dev-*.yaml -delete
find ./ -name values-stg-*.yaml -delete
find ./ -name values-nonprod-*.yaml -delete
find ./ -name values-p1-*.yaml -delete
find ./ -name values-p2-*.yaml -delete
```

### show mariadb status

```sql
SHOW GLOBAL STATUS WHERE Variable_name LIKE '%Threads%'
```
