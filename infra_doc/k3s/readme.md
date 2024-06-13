# K3S

## Install K3S

download and exec install script
```shell
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --docker --no-deploy=traefik --cluster-init --write-kubeconfig-mode='0644'" sh
# curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --docker --no-deploy=traefik --write-kubeconfig-mode='0644'" sh
```

add retain storage class and set it to default

```shell
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
  labels:
    app.kubernetes.io/instance: local-path-storage
  name: retain-local-path
provisioner: rancher.io/local-path
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer 
EOF
```

## Ref Document

- <https://rancher.com/docs/k3s/latest/en/installation/install-options/>
- <https://github.com/k3s-io/k3s/blob/master/README.md>
- <https://k3s.io/>
