# K8S Server Setup

[TOC]

## Installing Docker

Ref : <https://docs.docker.com/engine/install/ubuntu/>

```shell
sudo apt-get remove -y docker docker-engine docker.io containerd runc

sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
```

```shell
# list what version you can install
apt-cache madison docker-ce

# install the verion you want
sudo apt-get install -y containerd.io docker-ce=5:20.10.7~3-0~ubuntu-focal docker-ce-cli=5:20.10.7~3-0~ubuntu-focal

echo "done"
```

### Check Docker Version

```shell
sudo docker version
```

> Client: Docker Engine - Community
> Version: 20.10.7
> API version: 1.41
> Go version: go1.13.15
> Git commit: f0df350
> Built: Wed Jun 2 11:56:38 2021
> OS/Arch: linux/amd64
> Context: default
> Experimental: true
>
> Server: Docker Engine - Community
> Engine:
> Version: 20.10.7
> API version: 1.41 (minimum version 1.12)
> Go version: go1.13.15
> Git commit: b0f5bc3
> Built: Wed Jun 2 11:54:50 2021
> OS/Arch: linux/amd64
> Experimental: false
> containerd:
> Version: 1.4.6
> GitCommit: d71fcd7d8303cbf684402823e425e9dd2e99285d
> runc:
> Version: 1.0.0-rc95
> GitCommit: b9ee9c6314599f1b4a7f497e1f1f856fe433d3b7
> docker-init:
> Version: 0.19.0
> GitCommit: de40ad0

---

## Config Container Runtimes

Ref : [Container runtimes | Kubernetes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/#docker)

```shell
sudo mkdir /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "done"
```

---

## Installing kubeadm, kubelet and kubectl

Ref : [Installing kubeadm | Kubernetes](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

```shell
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system


sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y \
  kubelet=1.21.2-00 \
  kubeadm=1.21.2-00 \
  kubectl=1.21.2-00
sudo apt-mark hold kubelet kubeadm kubectl

echo "done"
```

### Check kubeadm Version

```shell
apt list kubeadm
```

> Listing... Done
> kubeadm/kubernetes-xenial,now 1.21.2-00 amd64 [installed]
> N: There are 209 additional versions. Please use the '-a' switch to see them.

---

## Download CNI plugin binary files

Ref : <https://github.com/containernetworking/plugins>

```shell
mkdir -p ~/tmp
cd ~/tmp

wget https://github.com/containernetworking/plugins/releases/download/v0.9.1/cni-plugins-linux-amd64-v0.9.1.tgz
sudo mkdir -p /opt/cni/bin
sudo tar -xzvf cni-plugins-linux-amd64-v0.9.1.tgz -C /opt/cni/bin

rm ~/tmp/cni-plugins-linux-amd64*
rm -d ~/tmp

echo "done"
```

### Check plugin files

```shell
ls /opt/cni/bin
```

> bandwidth bridge dhcp firewall flannel host-device host-local ipvlan loopback macvlan portmap ptp sbr static tuning vlan vrf

---

## Turn off swap

```shell
# backup file
sudo cp /etc/fstab /etc/fstab.bak

sudo swapoff -a
sudo sed '/swap.img/d' -i /etc/fstab

echo "done"
```

---

## Set time sync to gov NTP Server

```shell
# set-timezone to hong kong
timedatectl set-timezone Asia/Hong_Kong

# sync time immediately, one time only
sudo apt install ntpdate
sudo ntpdate stdtime.gov.hk

# tools for long term sync, adjust time slowly
sudo apt install ntp

# backup config file
cp /etc/ntp.conf /etc/ntp.conf.bak
```
```
# replace config file
sudo bash -c "cat << EOF > /etc/ntp.conf
# /etc/ntp.conf, configuration for ntpd; see ntp.conf(5) for help
driftfile /var/lib/ntp/ntp.drift

# Leap seconds definition provided by tzdata
leapfile /usr/share/zoneinfo/leap-seconds.list

statistics loopstats peerstats clockstats
filegen loopstats file loopstats type day enable
filegen peerstats file peerstats type day enable
filegen clockstats file clockstats type day enable

# By default, exchange time with everybody, but don't allow configuration.
restrict -4 default kod notrap nomodify nopeer noquery limited
restrict -6 default kod notrap nomodify nopeer noquery limited

# Local users may interrogate the ntp server more closely.
restrict 127.0.0.1
restrict ::1

# Needed for adding pool entries
restrict source notrap nomodify noquery

# Specify one or more NTP servers.
server stdtime.gov.hk prefer iburst
EOF"
```
```
systemctl restart ntp
systemctl enable ntp

# check sync status
ntpq -p
```

Example result: (ip may be diff because gov have multi ntp server ip)

> ```console
>      remote           refid      st t when poll reach   delay   offset  jitter
> ==============================================================================
> *118.143.17.82 ( .MRS.            1 u   42   64    1    4.047  -10.535   1.653
> ```
