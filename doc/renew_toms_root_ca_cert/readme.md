# renew root ca cert

## generate new root cert with **same** public & private key

```bash
# generate csr using old root ca cert, the new csr have public key and cert info in it
openssl x509 -x509toreq -in toms_root_ca.crt -signkey toms_root_ca.key -out new_toms_root_ca.csr

# sign new csr file with private key and set expire date
openssl x509 -req -days 36500 -in new_toms_root_ca.csr -extfile=v3_ca.cnf -extensions v3_ca -signkey toms_root_ca.key -out new_toms_root_ca.crt

# verify new root cert and key are match
KEY_MD5=$(openssl rsa -noout -modulus -in toms_root_ca.key | openssl md5 | cut -c 10-)
CERT_MD5=$(openssl x509 -noout -modulus -in new_toms_root_ca.crt | openssl md5 | cut -c 10-)
if [ "$KEY_MD5" = "$CERT_MD5" ]; then echo "match"; else echo "not match"; fi

# verify old server cert using new root cert
openssl verify -CAfile new_toms_root_ca.crt -verbose toms-middleware-server-crt.pem
```

# deploy new root ca cert

## import new root ca to toms portal

ask fu

## apply new root ca to all k8s

all k8s including

- dev-k8s (192.168.64.170)
- np-trust-k8s, np-dmz-k8s
- p1-trust-k8s, p1-dmz-k8s
- p2-trust-k8s, p2-dmz-k8s

```bash
kubectl delete secret ca-chain-secret -n bes
kubectl create secret generic ca-chain-secret -n bes --from-file=ca.crt=_toms_new_root_ca.crt
```

## notify das apply new root ca

ask faichi
