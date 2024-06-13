# Kong Enterprise installation

ref doc : <https://docs.konghq.com/enterprise/2.5.x/deployment/installation/kong-on-kubernetes/>

## Set Variables

```shell
PASSWORD=123456
NAMESPACE=kong
```

## Prepare

```shell
helm repo add kong https://charts.konghq.com
helm repo update
kubectl create namespace $NAMESPACE

# make sure you have two files : toms_chain_ca.pem, values-ffts.yaml
ls
```

## Create ca cert chain secret from `toms_chain_ca.pem`

```shell
# prepare trusted cert for valify portal server cert, ask admin for portal ca cert.
kubectl create secret generic ca-chain-secret \
  --from-file='ca.crt=toms_chain_ca.pem' \
  --namespace=$NAMESPACE
```

## Create admin password secret

```shell
mkdir kong-install-temp
cd kong-install-temp
  
# create super user password
kubectl create secret generic kong-enterprise-superuser-password -n $NAMESPACE --from-literal=password=$PASSWORD

# create session config
echo "{\"cookie_name\":\"admin_session\",\"cookie_samesite\":\"off\",\"secret\":\"$PASSWORD\",\"cookie_secure\":false,\"storage\":\"kong\"}" > admin_gui_session_conf
kubectl create secret generic kong-session-config -n $NAMESPACE --from-file=admin_gui_session_conf

cd ../
rm ./kong-install-temp -R
```

## helm Install

```shell
helm install kong kong/kong -n $NAMESPACE --values ./values-ffts.yaml
```

## Uninstall

```shell
helm uninstall kong -n $NAMESPACE
kubectl delete namespace $NAMESPACE
kubectl delete crd kongclusterplugins.configuration.konghq.com
kubectl delete crd kongconsumers.configuration.konghq.com
kubectl delete crd kongingresses.configuration.konghq.com
kubectl delete crd kongplugins.configuration.konghq.com
kubectl delete crd tcpingresses.configuration.konghq.com
kubectl delete crd udpingresses.configuration.konghq.com
```
