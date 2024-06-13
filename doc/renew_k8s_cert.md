# k8s renew certs

## renew certs in master

this process should run on every master

```bash
su
# check cert expire date
kubeadm certs check-expiration
# renew cert
kubeadm certs renew all
# check cert expire date again
kubeadm certs check-expiration
```

## for kubectl command (Unauthorized)

this process should run on every master

```bash
su
# after renew certificate, backup file
mv  /home/user00/.kube /home/user00/.kube.bak
# copy cert to user .kube directory
mkdir /home/user00/.kube
cp -i /etc/kubernetes/admin.conf /home/user00/.kube/config
# change permissions
chown user00:user00 /home/user00/.kube/config
```

## for kubelet

ref: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/#kubelet-client-cert

```bash

```
