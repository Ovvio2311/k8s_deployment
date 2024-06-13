## create service account in k8s

```bash
kubectl apply -f ./prometheus-k8s-acc.yaml
```

## create kube config file

```bash
NAMESPACE=default
USER_NAME=prometheus

USER_TOKEN_NAME=$(kubectl get serviceaccount ${USER_NAME} -n ${NAMESPACE} -o=jsonpath='{.secrets[0].name}')
USER_TOKEN_VALUE=$(kubectl get secret/${USER_TOKEN_NAME} -n ${NAMESPACE} -o=go-template='{{.data.token}}' | base64 --decode)
CURRENT_CONTEXT=$(kubectl config current-context)
CURRENT_CLUSTER=$(kubectl config view --raw -o=go-template='{{range .contexts}}{{if eq .name "'''${CURRENT_CONTEXT}'''"}}{{ index .context "cluster" }}{{end}}{{end}}')
CLUSTER_CA=$(kubectl config view --raw -o=go-template='{{range .clusters}}{{if eq .name "'''${CURRENT_CLUSTER}'''"}}"{{with index .cluster "certificate-authority-data" }}{{.}}{{end}}"{{ end }}{{ end }}')
CLUSTER_SERVER=$(kubectl config view --raw -o=go-template='{{range .clusters}}{{if eq .name "'''${CURRENT_CLUSTER}'''"}}{{ .cluster.server }}{{end}}{{ end }}')


sudo tee ${USER_NAME}.kubeconfig <<EOF
apiVersion: v1
kind: Config
current-context: ${CURRENT_CONTEXT}
contexts:
- name: ${CURRENT_CONTEXT}
  context:
    cluster: ${CURRENT_CONTEXT}
    user: kommander-cluster-admin
    namespace: kube-system
clusters:
- name: ${CURRENT_CONTEXT}
  cluster:
    certificate-authority-data: ${CLUSTER_CA}
    server: ${CLUSTER_SERVER}
users:
- name: kommander-cluster-admin
  user:
    token: ${USER_TOKEN_VALUE}
EOF

kubectl get pods --kubeconfig=${USER_NAME}.kubeconfig

```

## start container



```bash
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v /path/to/prometheus.kubeconfig:/etc/prometheus/prometheus.kubeconfig \
  prom/prometheus:v2.43.1
  docker run -d -p 3000:3000 --name grafana grafana/grafana:9.5.1
```

## 
```bash
docker run -d -p 3000:3000 --name grafana grafana/grafana-enterprise:8.2.0
```

## run on powershell

```powershell
docker run -d --name prometheus -p 9090:9090 `
-v E:\Projects\gitlab_repo\k8s_deployment\infra_doc\prometheus\prometheus.yml:/etc/prometheus/prometheus.yml `
-v E:\Projects\gitlab_repo\k8s_deployment\infra_doc\prometheus\prometheus.kubeconfig:/etc/prometheus/prometheus.kubeconfig `
prom/prometheus:v2.43.1
```
