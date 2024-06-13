# K8S Worker Server Setup

[TOC]

## Ref Doc

Ref :
[kubeadm join | Kubernetes](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)

---

# Join Worker Node Server

## Preparation

Make sure finish [K8S_Server_Setup.md](K8S_Server_Setup.md) on **New Worker Node** Server

## Generate Join command

Go to the **Master Node** server console

```shell
kubeadm token create --print-join-command
```

> kubeadm join 10.13.0.40:6443 --token 4qjdhx.n593bv4jfeiqxt04 --discovery-token-ca-cert-hash sha256:c84181cc8d9b126147439df606940827d6097fe9aa528e46e48d1e3ffd718c27

## Join New Worker to Cluster

Go to **New Worker Node** server console

```shell
# exec join command on new worker
sudo kubeadm join 10.13.0.40:6443 --token ke5egi.4l0d486zri96vqr6 --discovery-token-ca-cert-hash sha256:c84181cc8d9b126147439df606940827d6097fe9aa528e46e48d1e3ffd718c27
```
