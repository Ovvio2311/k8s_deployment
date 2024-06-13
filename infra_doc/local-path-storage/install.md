# Install local path storage

!!! This local path storage should only for deployment and testing usage.
Doc ref: <https://github.com/rancher/local-path-provisioner>

```shell
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.22/deploy/local-path-storage.yaml
kubectl apply -f ./retain-local-path-storage-class.yaml
```
