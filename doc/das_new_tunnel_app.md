# das new tunnel apps

1. create bucket [doc/object_storage/create_bucket.md](object_storage/create_bucket.md)  
   s1/o1 object storage: abt, eht, smt, wht, tsca  
   s2/o2 object storage: cht, lrt, tct, tlt, tko
2. add appsettings yaml file in gitlab  
   in `k8s_yaml/{zone}/{app}/values-others/values-{env}-{app}-yaml}`
   - bes/das-evidence-record-consumer
   - bes/das-imageobj-consumer
   - bes/das-transaction-record-consumer
   - bes/tx-validation
   - bes/txv-process-consumer
   - bes/txv-stat-consumer
   - dmz-bes/das-middleware
     - das-middleware nodeport: 3x1yz, example: (smt,https,video)nodeport: 32114
       ```
       x: 1=http, 2=https
       y: 1=api,  2=video
       z: ti_toll_domain_id (edited)
       ```
3. create topic in pulsar. [doc/pulsar_command.md](pulsar_command.md)
4. create app in argocd, helpful script `generate_argocd_application.py`
5. double check appsetting, useful script `compare_das_config.py`

## update toms-middleware appsettings

- update `k8s_deployment/deploy_toms/{env}-toms-middleware/toms-middleware.appsettings.{env}.json`
- connect VPN
- login remote desktop v630
  - ip: 172.24.151.107:39833
  - user: autotolladmin1
  - pass: AtlXXXXX
- login linux itom1 (172.24.151.119)
- copy appsettings to /mnt/data/toms/toms-middleware.appsettings.{env}.json

## deploy server cert

1. ask fu for tunnel app id
2. create server cert using toms-api,
   only change the domain name `das-middleware-lrt.bes.svc`, other ip should be same on all tunnel
   https://192.168.64.170:32001/swagger/index.html
   `POST ​/CertManage​/TOMS_CRT014_CreateServerCert`
   ```json
   {
     "app_id": "APPxxxxx",
     "cert_san": "das-middleware-lrt.bes.svc, localhost, 127.0.0.1, 172.24.150.71, 172.24.150.73, 172.24.151.109, 172.24.151.110, 172.24.151.111, 172.20.150.71, 172.20.150.73, 172.20.151.110, 172.20.151.111, 172.20.151.112, 172.16.150.71, 172.16.150.72, 172.16.151.110, 172.16.151.111, 172.16.151.112",
     "effective_year": 100
   }
   ```
3. download server cert and unzip
   `POST ​/CertManage​/TOMS_CRT016_GetServerCertFile`
   ```json
   {
     "app_id": "APPxxxxx"
   }
   ```

#openssl x509 -in APP00270-server-crt.pem -out das-middleware-wht.crt
#openssl rsa -in APP00270-server-key.pem -out das-middleware-wht.key

4. apply server cert to dmz k8s, currently np, p1, p2 using same server cert
   ```bash
   APPNAME=das-middleware-lrt
   kubectl create secret tls $APPNAME-server-tls --cert=$APPNAME.crt --key=$APPNAME.key -n bes
   ```

## config kong gateway (optional)

see [doc/config_kong_gateway](config_kong_gateway/readme.md)
