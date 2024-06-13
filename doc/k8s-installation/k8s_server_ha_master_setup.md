# K8S HA Master Server Setup

[TOC]

## Preparation

Prepare three VM

| hostname | IP         |
| -------- | ---------- |
| bes06    | 10.13.0.56 |
| bes07    | 10.13.0.57 |
| bes08    | 10.13.0.58 |

## Ref Doc

<https://kube-vip.io/>
[Creating Highly Available clusters with kubeadm | Kubernetes](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)

---

# Setup First Master Server

## Preparation

Make sure finish [K8S_Server_Setup.md](K8S_Server_Setup.md) on Server

## Set variable

```shell
# use command [ip link] to get network interface list
NETWORK_INTERFACE=ens160
VIRTUAL_IP=10.13.0.40
KUBE_VIP_IMAGE_VERSION_TAG=v0.3.5
echo "done"
```

## Download docker image

```shell
sudo docker pull plndr/kube-vip:$KUBE_VIP_IMAGE_VERSION_TAG
```

## Generate kube-vip Pod YAML file

```shell
sudo mkdir -p /etc/kubernetes/manifests/
sudo docker run --network host --rm \
	plndr/kube-vip:$KUBE_VIP_IMAGE_VERSION_TAG manifest pod \
    --interface $NETWORK_INTERFACE \
    --vip $VIRTUAL_IP \
    --controlplane \
    --services \
    --arp \
    --leaderElection | sudo tee /etc/kubernetes/manifests/kube-vip.yaml
echo "done"
```

## Init Cluster by kubeadm

```shell
# --pod-network-cidr must be same as CNI config
# In this case, we use CNI flannel and set to 10.244.0.0/16
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --control-plane-endpoint=$VIRTUAL_IP
```

Example Result :

> You can now join any number of control-plane nodes by copying certificate authorities
> and service account keys on each node and then running the following as root:
>
> kubeadm join 10.13.0.40:6443 --token nu9h4m.a7r5a264e7zfv8ey \
>  --discovery-token-ca-cert-hash sha256:577e52f33268d6485107f16e5c65082a922bfe017c7daf74c63d0752f0465253 \
>  --control-plane
>
> Then you can join any number of worker nodes by running the following on each as root:
>
> kubeadm join 10.13.0.40:6443 --token nu9h4m.a7r5a264e7zfv8ey \
>  --discovery-token-ca-cert-hash sha256:577e52f33268d6485107f16e5c65082a922bfe017c7daf74c63d0752f0465253

## Copy kubectl config for user

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Install CNI plugin (flannel)

```shell
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

---

# Join Other Master Node Server

## Preparation

Make sure finish [K8S_Server_Setup.md](K8S_Server_Setup.md) on **New Master Node** Server

## Copy PKI files

After init cluster, k8s will generate KPI files(**TLS Cert**). We need to copy some of PKI files(**TLS Cert**) to the new master node.
Here we use `scp`command but you can use sftp or any method you want.

Go to **First Master Node** server console, copy PKI files(**TLS Cert**) to **New Master Node**

```shell
REMOTE_LINUX_USER=3fpadm
CONTROL_PLANE_IPS="10.13.0.57 10.13.0.58"
```

```shell
# Execute this command on existed master server console
# This command will ask password many time.
for host in ${CONTROL_PLANE_IPS}; do
	sudo scp -r /etc/kubernetes/pki/ "${REMOTE_LINUX_USER}"@$host:
done
```

Go to **New Master Node** server console, copy files from home folder to PKI folder

```shell
MY_LINUX_USER=3fpadm
```

```shell

ls /home/${MY_LINUX_USER}/
# you should see pki folder in user's home folder
# we only need 8 files in pki
# ca.crt  ca.key  front-proxy-ca.crt  front-proxy-ca.key  sa.key  sa.pub etcd/ca.crt  etcd/ca.key

sudo mkdir -p /etc/kubernetes/pki/
sudo cp /home/${MY_LINUX_USER}/pki/{ca.crt,ca.key,front-proxy-ca.crt,front-proxy-ca.key,sa.key,sa.pub} /etc/kubernetes/pki/

sudo mkdir -p /etc/kubernetes/pki/etcd/
sudo cp /home/${MY_LINUX_USER}/pki/etcd/{ca.crt,ca.key} /etc/kubernetes/pki/etcd/

# show pki folder
ls -R /etc/kubernetes/pki/
```

> /etc/kubernetes/pki/:
> ca.crt ca.key etcd front-proxy-ca.crt front-proxy-ca.key sa.key sa.pub
>
> /etc/kubernetes/pki/etcd:
> ca.crt ca.key

```shell
# for security, remove pki folder from user home folder
rm /home/${MY_LINUX_USER}/pki/etcd/*
rm -d /home/${MY_LINUX_USER}/pki/etcd/
rm /home/${MY_LINUX_USER}/pki/*
rm -d /home/${MY_LINUX_USER}/pki/

# make sure pki folder is removed
ls /home/${MY_LINUX_USER}/pki/
```

> ls: cannot access '/home/3fpadm/pki/': No such file or directory

```shell
# for security, change pki files permission
sudo chmod 600 /etc/kubernetes/pki/*
sudo chmod 755 /etc/kubernetes/pki/etcd
sudo chmod 644 /etc/kubernetes/pki/*.crt

# make sure permission correct
ls -lR /etc/kubernetes/pki/
```

> /etc/kubernetes/pki/:
> total 28
> -rw-r--r-- 1 root root 1066 Jul 8 02:23 ca.crt
> -rw------- 1 root root 1675 Jul 8 02:23 ca.key
> drwxr-xr-x 2 root root 4096 Jul 8 02:23 etcd
> -rw-r--r-- 1 root root 1078 Jul 8 02:23 front-proxy-ca.crt
> -rw------- 1 root root 1679 Jul 8 02:23 front-proxy-ca.key
> -rw------- 1 root root 1675 Jul 8 02:23 sa.key
> -rw------- 1 root root 451 Jul 8 02:23 sa.pub
>
> /etc/kubernetes/pki/etcd:
> total 8
> -rw-r--r-- 1 root root 1058 Jul 8 02:23 ca.crt
> -rw------- 1 root root 1675 Jul 8 02:23 ca.key

## Generate Join Command

Go to the **First Master Node** server console

```shell
echo $(kubeadm token create --print-join-command) --control-plane -v 5
```

> kubeadm join 10.13.0.40:6443 --token 4merxd.66gr6wpf4qpqcjz6 --discovery-token-ca-cert-hash sha256:c84181cc8d9b126147439df606940827d6097fe9aa528e46e48d1e3ffd718c27 --control-plane

## Join New Master to Cluster

Go to **New Master Node** server console

```shell
# exec join command on new master
sudo kubeadm join 10.13.0.40:6443 --token 4merxd.66gr6wpf4qpqcjz6 --discovery-token-ca-cert-hash sha256:c84181cc8d9b126147439df606940827d6097fe9aa528e46e48d1e3ffd718c27 --control-plane

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## Join Worker to Cluster

See [k8s_server_worker_setup.md](k8s_server_worker_setup.md)
