# How to deploy new project

## Concept

1.  perpare k8s yaml app folder in deployment project  
    https://192.168.64.188/bes/k8s_deployment  
    `(k8s_yaml/<zone-folder>/<app-folder>/<helm-charts>)`  
    you can copy folder `helm_charts_example/dotnet_web_api`
1.  perpare argocd yaml file  
    you can use `/scripts/generate_appsettings.py` help to generate it.
    example below:

    ```yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: "auth-api"
      namespace: argocd
    spec:
      destination:
        namespace: "bes"
        server: https://kubernetes.default.svc
      project: "default"
      source:
        path: "k8s_yaml/bes/auth-api"
        repoURL: "https://192.168.64.188/bes/k8s_deployment.git"
        targetRevision: master
        helm:
          valueFiles:
            - values-dev-common.yaml
      syncPolicy:
        automated:
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
    ```

1.  apply argocd yaml file to k8s

    ```bash
     kubectl apply -f argo-auth-api.yaml
    ```

## User linux command

```bash
# $DEPLOY_ZONE_FOLDER=["bes" | "bes-job" | "dmz-bes" | "toms"]
# $PROJECT_TYPE=["dotnet_web_api" | "dotnet_cron_job"]
# node port 30000-32767

PROJECT_TYPE="dotnet_web_api"

DEPLOY_ZONE_FOLDER="bes"
PROJECT_NAME="Tx_Validation_Backlog"

HTTP_NODE_PORT=	31033
HTTPS_NODE_PORT=32033

# convert project name to lower case and hyphen only
PROJECT_NAME=$(echo "$PROJECT_NAME" | iconv -t ascii//TRANSLIT | sed -r s/[^a-zA-Z0-9]+/-/g | sed -r s/^-+\|-+$//g | tr A-Z a-z)
```

## Download k8s deployment project

```bash
mkdir ~/temp
cd ~/temp

git clone --depth=1 -c http.sslVerify=false https://192.168.64.188/bes/k8s_deployment.git
cd ~/temp/k8s_deployment/
```

## Create k8s deployment yaml files

```bash
cd ~/temp/k8s_deployment/
# copy example helm chart
cp -r "helm_charts_example/$PROJECT_TYPE/" "k8s_yaml/$DEPLOY_ZONE_FOLDER/"
# rename folder
mv "k8s_yaml/$DEPLOY_ZONE_FOLDER/$PROJECT_TYPE" "k8s_yaml/$DEPLOY_ZONE_FOLDER/$PROJECT_NAME"
# go in folder
cd "k8s_yaml/$DEPLOY_ZONE_FOLDER/$PROJECT_NAME"
# replace <app-name> with project name
sed -i "s/<app-name>/$PROJECT_NAME/g" values.yaml

# replace node port
sed -i "s/<http-node-port>/$HTTP_NODE_PORT/g" values.yaml
sed -i "s/<https-node-port>/$HTTPS_NODE_PORT/g" values.yaml
cd ../../../

git add .
git commit --all --message "add project $PROJECT_NAME"
git push
```

## Update gitlab branch

```bash
# "227" or "bes/notification/bes_cre_im011_notification_result"
GITLAB_PROJECT_ID="279"
sudo python ./scripts/update_gitlab_branchs.py -p $GITLAB_PROJECT_ID
```

## Config argocd to dev

Linux command

```bash
cd ~/temp/k8s_deployment/

# make sure you have kube config file before start
# /var/tmp/.kube/config-bes-dev

sudo python ./scripts/generate_argocd_application.py
kubectl apply -f ./k8s_argocd_yaml/dev/$DEPLOY_ZONE_FOLDER/argo-$PROJECT_NAME.yaml --kubeconfig="/var/tmp/.kube/config-bes-dev"
```

## Config argocd to stg

Linux command

```bash
cd ~/temp/k8s_deployment/

# make sure you have kube config file before start
# /var/tmp/.kube/config-bes-stg-turst
# /var/tmp/.kube/config-bes-stg-dmz
# /var/tmp/.kube/config-bes-stg-toms

# choose which k8s you wanna deploy to
STG_CONFIG_PATH=/var/tmp/.kube/config-bes-stg-turst
# STG_CONFIG_PATH=/var/tmp/.kube/config-bes-stg-dmz
# STG_CONFIG_PATH=/var/tmp/.kube/config-bes-stg-toms

sudo python ./scripts/generate_argocd_application.py
kubectl apply -f ./k8s_argocd_yaml/stg/$DEPLOY_ZONE_FOLDER/argo-$PROJECT_NAME.yaml --kubeconfig=$STG_CONFIG_PATH


kubectl apply -f ./k8s_argocd_yaml/stg/bes/ --kubeconfig=/var/tmp/.kube/config-bes-stg-turst
kubectl apply -f ./k8s_argocd_yaml/stg/dmz-bes/ --kubeconfig=/var/tmp/.kube/config-bes-stg-dmz
kubectl apply -f ./k8s_argocd_yaml/stg/bes-job/ --kubeconfig=/var/tmp/.kube/config-bes-stg-turst
```
