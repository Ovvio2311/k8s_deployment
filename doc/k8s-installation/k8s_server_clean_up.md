# K8S Cleanup

## Safely Remove a Node

Execute below command on **master** server

```shell
NODE_NAME_TO_REMOVE=bes06
kubectl drain $NODE_NAME_TO_REMOVE --delete-emptydir-data --force --ignore-daemonsets
kubectl delete node $NODE_NAME_TO_REMOVE
```



## Reset Worker Node Server 

Execute below command on **worker node** server

```shell
sudo kubeadm reset

# clear up docker containers, volumes, images
sudo docker rm -f $(sudo docker ps -qa)
sudo docker volume rm $(sudo docker volume ls -q)
# sudo docker rmi -f $(sudo docker images -q)

# stop kubelet and docker 
sudo systemctl stop kubelet
sudo systemctl stop docker

# unmount folder
for mount in $(mount | grep tmpfs | grep '/var/lib/kubelet' | awk '{ print $3 }') /var/lib/kubelet /var/lib/rancher; do sudo umount $mount; done

# rm files
sudo rm -rf ~/.kube
sudo rm -rf /opt/cni/!(bin)
sudo rm -rf /etc/ceph \
       /etc/cni \
       /etc/kubernetes \
       /opt/rke \
       /run/secrets/kubernetes.io \
       /run/calico \
       /run/flannel \
       /var/lib/calico \
       /var/lib/etcd \
       /var/lib/cni \
       /var/lib/kubelet \
       /var/lib/rancher/rke/log \
       /var/log/containers \
       /var/log/kube-audit \
       /var/log/pods \
       /var/run/calico

# clear network setting
sudo ip link delete cni0
sudo ip link delete flannel.1
sudo iptables -F 
sudo iptables -t nat -F 
sudo iptables -t mangle -F 
sudo iptables -X
sudo iptables --flush

# check if any interface left, delete it
sudo ip address show

# start kubelet and docker 
sudo systemctl start docker
sudo systemctl start kubelet

echo "done"
```

> Ref doc :
> - https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-reset/
> - https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cleaning-cluster-nodes/

