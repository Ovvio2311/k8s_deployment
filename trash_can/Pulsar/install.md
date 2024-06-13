
## Prepare Variable
```
K8S_IP=192.168.64.170
RELEASE_NAME=pulsar
NAMESPACE=pulsar

NODEPORT_PROXY=30222
NODEPORT_MANAGER=30223
NODEPORT_GRAFANA=30224
NODEPORT_PROMETHEUS=30225

INIT_PULSAR_CLUSTER=true
```

## Install helm chart
```bash
kubectl create ns $NAMESPACE

helm repo add apache https://pulsar.apache.org/charts

helm install $RELEASE_NAME apache/pulsar \
-n $NAMESPACE \
--version=2.9.2 \
--values=values-ffts-pulsar.yaml \
--set namespaceCreate=false \
--set initialize=$INIT_PULSAR_CLUSTER

# only for debug, print all generated yaml file without apply to k8s
# helm template $RELEASE_NAME apache/pulsar \
# -n $NAMESPACE \
# --values=values-ffts-pulsar.yaml \
# --set namespaceCreate=false \
# --set initialize=$INIT_PULSAR_CLUSTER \
# --dry-run \
# --output-dir out_template
```

## Watch k8s resource 
```bash
watch -n 1 kubectl get all -n $NAMESPACE
```

## Add NodePort Service (only for development !!!)
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: $RELEASE_NAME-proxy-nodeport
  namespace: $NAMESPACE
  labels:
    app: pulsar
    component: proxy
    release: $RELEASE_NAME
spec:
  ports:
    - name: https
      protocol: TCP
      port: 80
      targetPort: 80
    - name: pulsarssl
      protocol: TCP
      port: 6650
      targetPort: 6650
      nodePort: $NODEPORT_PROXY
  selector:
    app: pulsar
    component: proxy
    release: $RELEASE_NAME
  type: NodePort
EOF
```

## Add Manager NodePort Service
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: $RELEASE_NAME-pulsar-manager-nodeport
  namespace: $NAMESPACE
  labels:
    app: pulsar
    component: pulsar-manager
    release: $RELEASE_NAME
spec:
  ports:
    - name: server
      protocol: TCP
      port: 9527
      targetPort: 9527
      nodePort: $NODEPORT_MANAGER
  selector:
    app: pulsar
    component: pulsar-manager
    release: $RELEASE_NAME
  type: NodePort	
EOF
```

## Add grafana NodePort Service
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: $RELEASE_NAME-grafana-nodeport
  namespace: $NAMESPACE
  labels:
    app: pulsar
    component: pulsar-grafana
    release: $RELEASE_NAME
spec:
  ports:
    - name: server
      protocol: TCP
      port: 3000
      targetPort: 3000
      nodePort: $NODEPORT_GRAFANA
  selector:
    app: pulsar
    component: grafana
    release: $RELEASE_NAME
  type: NodePort
EOF
```

## Add prometheus NodePort Service
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: $RELEASE_NAME-prometheus-nodeport
  namespace: $NAMESPACE
  labels:
    app: pulsar
    component: pulsar-prometheus
    release: $RELEASE_NAME
spec:
  ports:
    - name: server
      protocol: TCP
      port: 9090
      targetPort: 9090
      nodePort: $NODEPORT_PROMETHEUS
  selector:
    app: pulsar
    component: prometheus
    release: $RELEASE_NAME
  type: NodePort
EOF
```
      
## Add user to pulsar manager
```bash
CSRF_TOKEN=$(curl http://$K8S_IP:$NODEPORT_MANAGER/pulsar-manager/csrf-token)
echo $CSRF_TOKEN

curl \
    -H "X-XSRF-TOKEN: $CSRF_TOKEN" \
    -H "Cookie: XSRF-TOKEN=$CSRF_TOKEN;" \
    -H 'Content-Type: application/json' \
    -X PUT http://$K8S_IP:$NODEPORT_MANAGER/pulsar-manager/users/superuser \
    -d '{"name": "pulsar", "password": "pulsar", "description": "description", "email": "pulsar@pulsar.com"}'
```

## Add env to pulsar manager

login and click new environment
Service URL: 
```bash
echo http://$RELEASE_NAME-broker.$NAMESPACE.svc:8080
```

## Add tenant and namespace

```bash
CREATE_TENANT_CMD="./bin/pulsar-admin tenants create bes"
CREATE_NS_CMD="./bin/pulsar-admin namespaces create bes/notification-service"
CREATE_TEST_NS_CMD="./bin/pulsar-admin namespaces create bes/testing"

kubectl exec $RELEASE_NAME-broker-0 -n $NAMESPACE -- $CREATE_TENANT_CMD
kubectl exec $RELEASE_NAME-broker-0 -n $NAMESPACE -- $CREATE_NS_CMD
kubectl exec $RELEASE_NAME-broker-0 -n $NAMESPACE -- $CREATE_TEST_NS_CMD
```

## Uninstall 

```bash
helm uninstall $RELEASE_NAME -n $NAMESPACE
kubectl delete namespace $NAMESPACE

# get all pv relared to pulsar
# kubectl get pv | grep $NAMESPACE/$RELEASE_NAME

# manually remove persistent volume by below command !! this will delete all data in pulsar
# `kubectl delete pv <pv-name> -n $NAMESPACE`
```

## Q&A

bug fix - cannot display clusters list
```bash
kubectl exec -i -t -n $NAMESPACE $RELEASE_NAME-broker-0 -- sh -c "clear; (bash || ash || sh)"

NAMESPACE=xxxxxx
RELEASE_NAME=xxxxxx
./bin/pulsar-admin clusters update $RELEASE_NAME --url http://$RELEASE_NAME-broker.$NAMESPACE.svc:8080
exit
```
