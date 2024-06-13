# K8S Signel Master Server Setup

[TOC]

## Preparation

Prepare one VM

| hostname | IP         |
| -------- | ---------- |
| bes06    | 10.13.0.56 |

## Ref Doc

[Creating a cluster with kubeadm | Kubernetes](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

---



# Setup Master Server

## Preparation

Make sure finish [K8S_Server_Setup.md](K8S_Server_Setup.md) on Server



## Init Cluster by kubeadm

```shell
# --pod-network-cidr must be same as CNI config
# In this case, we use CNI flannel and set to 10.244.0.0/16
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

Example Result : 

> You can now join any number of control-plane nodes by copying certificate authorities
> and service account keys on each node and then running the following as root:
>
>   kubeadm join 10.13.0.40:6443 --token nu9h4m.a7r5a264e7zfv8ey \
>         --discovery-token-ca-cert-hash sha256:577e52f33268d6485107f16e5c65082a922bfe017c7daf74c63d0752f0465253 \
>         --control-plane 
>
> Then you can join any number of worker nodes by running the following on each as root:
>
> kubeadm join 10.13.0.40:6443 --token nu9h4m.a7r5a264e7zfv8ey \
>         --discovery-token-ca-cert-hash sha256:577e52f33268d6485107f16e5c65082a922bfe017c7daf74c63d0752f0465253 

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

## Join Worker to Cluster

See [k8s_server_worker_setup.md](k8s_server_worker_setup.md) 