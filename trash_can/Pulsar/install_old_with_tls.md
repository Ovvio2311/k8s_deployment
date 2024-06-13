
## Prepare Variable
```
RELEASE_NAME=pulsar
NAMESPACE=pulsar

NODEPORT_PROXY=30222
NODEPORT_MANAGER=30223

CA_SECRET_NAME=$RELEASE_NAME-ca-tls
ISSUER_CA_SECRET_NAME=$RELEASE_NAME-issuer-ca
CA_ISSUER_NAME=$RELEASE_NAME-internal-cert-issuer-ca-issuer

INIT_PULSAR_CLUSTER=true
```

## Install cert-manager(only if not installed)
```
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.6.0/cert-manager.yaml
```

## Prepare cert issuer
```
# make sure you have three cert file : toms_ca_cert.pem, toms_ca_key.pem, toms_ca_chain.pem

kubectl create namespace $NAMESPACE

kubectl create secret tls $ISSUER_CA_SECRET_NAME \
  --cert=toms_ca_crt.pem \
  --key=toms_ca_key.pem \
  --namespace=$NAMESPACE

kubectl create secret generic $CA_SECRET_NAME \
  --from-file='ca.crt=toms_ca_chain.pem' \
  --namespace=$NAMESPACE

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: $CA_ISSUER_NAME
  namespace: $NAMESPACE
spec:
  ca:
    secretName: $ISSUER_CA_SECRET_NAME
EOF

# check result
kubectl get secret -n $NAMESPACE
kubectl get issuer -n $NAMESPACE
```

## Prepare cert
```
# create cert for each component (bookie recovery toolset proxy broker zookeeper)

for PULSAR_COMPONENT in bookie recovery toolset proxy broker zookeeper
do
  cat <<EOF | kubectl apply -f -
  apiVersion: "cert-manager.io/v1"
  kind: Certificate
  metadata:
    name: "$RELEASE_NAME-tls-$PULSAR_COMPONENT"
    namespace: $NAMESPACE
  spec:
    secretName: "$RELEASE_NAME-tls-$PULSAR_COMPONENT"
    duration: "2160h"
    renewBefore: "360h"
    subject:
      organizations:
        - $RELEASE_NAME
    commonName: "$RELEASE_NAME-$PULSAR_COMPONENT"
    isCA: false
    privateKey:
      algorithm: RSA
      encoding: PKCS8
      size: 4096
    usages:
      - server auth
      - client auth
    dnsNames:
      -  "localhost"
      -  "*.$RELEASE_NAME-$PULSAR_COMPONENT.$NAMESPACE.svc.cluster.local"
      -  "$RELEASE_NAME-$PULSAR_COMPONENT"
      -  "$RELEASE_NAME-$PULSAR_COMPONENT.$NAMESPACE"
      -  "$RELEASE_NAME-$PULSAR_COMPONENT.$NAMESPACE.svc"
      -  "$RELEASE_NAME-$PULSAR_COMPONENT.$NAMESPACE.svc.cluster"
      -  "$RELEASE_NAME-$PULSAR_COMPONENT.$NAMESPACE.svc.cluster.local"
    ipAddresses:
      - 127.0.0.1
      - 192.168.64.170
      - 192.168.64.191
      - 192.168.64.200
      - 192.168.64.120
      - 192.168.64.121
      - 192.168.64.122
      - 192.168.64.123
    issuerRef:
      name: $CA_ISSUER_NAME
      kind: Issuer
      group: cert-manager.io
EOF
#^^ left aligned, don't indent it.
done

# Check created cert
kubectl get Certificate -n $NAMESPACE

# Check created secret, wait until `cert-manager` create secret
watch -n 1 kubectl get secret -n $NAMESPACE
```

## Install helm chart
```
helm repo add apache https://pulsar.apache.org/charts

helm install $RELEASE_NAME apache/pulsar \
-n $NAMESPACE \
--values=values-minikube-with-tls.yaml \
--set namespaceCreate=false \
--set initialize=$INIT_PULSAR_CLUSTER

# only for debug, print all generated yaml file without apply to k8s
# helm template $RELEASE_NAME apache/pulsar \
# -n $NAMESPACE \
# --values=values-minikube-with-tls.yaml \
# --set namespaceCreate=false \
# --set initialize=$INIT_PULSAR_CLUSTER \
# --dry-run \
# --output-dir out_template
```

## Add NodePort Service (only for development !!!)
```
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
      port: 443
      targetPort: 443
    - name: pulsarssl
      protocol: TCP
      port: 6651
      targetPort: 6651
      nodePort: $NODEPORT_PROXY
  selector:
    app: pulsar
    component: proxy
    release: $RELEASE_NAME
  type: NodePort
EOF
```

## Add Manager NodePort Service (only for development !!!)
```
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

## Watch k8s resource 
```
watch -n 1 kubectl get all -n $NAMESPACE
```

## Uninstall pulsar
```
helm uninstall $RELEASE_NAME -n $NAMESPACE
kubectl delete namespace $NAMESPACE

# get all pv relared to pulsar
kubectl get pv | grep $NAMESPACE/$RELEASE_NAME

# manually remove persistent volume by below command !! this will delete all data in pulsar
`kubectl delete pv <pv-name> -n $NAMESPACE`
```

## Uninstall cert-manager
```
kubectl delete -f https://github.com/jetstack/cert-manager/releases/download/v1.6.0/cert-manager.yaml
```