# Backup and recovery

---

## Backup and recovery by linux command line

https://argoproj.github.io/argo-cd/operator-manual/disaster_recovery/

Download tools

```shell
wget https://github.com/argoproj/argo-cd/releases/download/v2.0.3/argocd-util-linux-amd64

# execute permission
sudo chmod 700 argocd-util-linux-amd64
```

Backup

```shell
./argocd-util-linux-amd64 --namespace argocd export > backup.yaml
```

Recovery

```shell
./argocd-util-linux-amd64 import - < backup.yaml
```

## Backup and recovery by docker

https://argoproj.github.io/argo-cd/operator-manual/disaster_recovery/

Backup

```shell
# check argocd version
argocd version | grep argocd
# example : argocd: v2.0.1+33eaf11

export VERSION=v2.0.1
sudo chown 777 $HOME/.kube/config

sudo docker run -v ~/.kube:/home/argocd/.kube --rm argoproj/argocd:$VERSION argocd-util -n argocd export > backup.yaml

sudo chown $(id -u):$(id -g) $HOME/.kube/config
unset VERSION

```

Recovery

```shell
# check argocd version
argocd version | grep argocd
# example : argocd: v2.0.1+33eaf11

export VERSION=v2.0.1
sudo chown 777 $HOME/.kube/config

sudo docker run -v ~/.kube:/home/argocd/.kube --rm argoproj/argocd:$VERSION argocd-util -n argocd import - < backup.yaml

sudo chown $(id -u):$(id -g) $HOME/.kube/config
unset VERSION
```
