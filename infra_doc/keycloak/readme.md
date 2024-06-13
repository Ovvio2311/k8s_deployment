# Install  Keycloak

Ref Doc

<https://artifacthub.io/packages/helm/codecentric/keycloak/16.0.5>

<https://hub.docker.com/r/jboss/keycloak>

## Prepare
1. makesure database already exists

## Set variables      
```
VALUE_YAML_PATH=values-keycloak-ffts.yaml
## remember to change secret config in values file

RELEASE=keycloak
NAMESPACE=keycloak
```

## Install
```
kubectl create namespace $NAMESPACE

helm repo add codecentric https://codecentric.github.io/helm-charts
helm repo update codecentric
helm install $RELEASE codecentric/keycloak -n $NAMESPACE -f $VALUE_YAML_PATH 
```

## Uninstall

```
helm uninstall $RELEASE -n $NAMESPACE 
kubectl delete namespace $NAMESPACE
```

## Helpful command

```
## render yaml from chart template and values, only for debug usage
##helm template $RELEASE codecentric/keycloak -n $NAMESPACE -f $VALUE_YAML_PATH \
##--output-dir=./otuput-dir --dry-run \
##--set secrets.db.stringData.KEYCLOAK_USER="$KEYCLOAK_USER" \
##--set secrets.db.stringData.KEYCLOAK_PASSWORD="$KEYCLOAK_PASSWORD" 

```
