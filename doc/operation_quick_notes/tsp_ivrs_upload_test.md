```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: "tsp-ivrs-isaac-test"
  namespace: argocd
spec:
  destination:
    namespace: "tsp"
    server: https://kubernetes.default.svc
  project: default
  source:
    repoURL: 'http://192.168.8.6/tsp/bes-to-tsp-deployment.git'
    path: k8s_yaml/tsp/tsp-ivrs
    targetRevision: HEAD
    helm:
      valueFiles:
        - values-nonprod-app-settings.yaml
        - values-nonprod-common.yaml
        - values-nonprod-image-tag.yaml
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: tsp
  syncPolicy:
    automated: {}
    syncOptions:
      - CreateNamespace=true
```

```bash
docker pull 192.168.8.6:8083/test/tsp-ivrs:isaac-test
```

```bash
cd /mnt/data/user00/trash_can/testing/
unzip tsp-ivrs_isaac-test.zip
docker load -i tsp-ivrs_isaac-test.tar
docker tag tsp-ivrs:isaac-test 192.168.8.6:8083/test/tsp-ivrs:isaac-test
docker push 192.168.8.6:8083/test/tsp-ivrs:isaac-test

cd /mnt/data/user00/isaac-test
truncate -s 1M 1_mb.file
truncate -s 10M 10_mb.file
truncate -s 100M 100_mb.file
truncate -s 150M 150_mb.file
truncate -s 200M 200_mb.file


curl --location --request POST 'http://192.168.0.8:30005/NoSignature/attx08_upload_voice_record' \
--header 'accept: text/plain' \
--form "call_id=_isaac_test_$(date +%m%d_%M%S)" \
--form 'case_id=""' \
--form 'record_time=""' \
--form 'checksum=""' \
--form 'voice_record=@/mnt/data/user00/isaac-test/10_mb.file' \
-w "@curl-format.txt"
```

create file with random data

```bash
head -c 10M /dev/urandom > 10_mb.file
head -c 50M /dev/urandom > 50_mb.file
head -c 100M /dev/urandom > 100_mb.file
head -c 150M /dev/urandom > 150_mb.file
head -c 200M /dev/urandom > 200_mb.file

sudo sh -c 'head -c 1024M /dev/urandom > delete_me_if_disk_full_1_gb'
```

```json
{
  "S3Config": {
    "Prod": true,
    "EndPoint": "https://tdffsts.t1cosg-obj001.gcisdctr.hksarg/",
    "AccessKeyID": "dGRmZnN0c19hZG1pbg==",
    "AccessSecret": "e3129fd0cda9ae466f8cc484c0ca84f9",
    "Enabled": true,
    "Bucket": "ivr"
  }
}
```
