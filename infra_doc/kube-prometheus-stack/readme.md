# Install
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n kube-prometheus-stack --create-namespace --dependency-update
```

## expose
```shell
cat <<EOF | kubectl apply -n kube-prometheus-stack -f -
apiVersion: v1
kind: Service
metadata:
  name: kube-prometheus-stack-grafana-nodeport
  namespace: kube-prometheus-stack
spec:
  ports:
    - name: http-web
      protocol: TCP
      port: 80
      targetPort: 3000
      nodePort: 30058
  selector:
    app.kubernetes.io/instance: kube-prometheus-stack
    app.kubernetes.io/name: grafana
  type: NodePort
EOF
```