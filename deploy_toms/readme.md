# deploy toms

## download images

use **`Git Bash`** to execute script `dl_toms_img.sh`, will get file like `toms-api-master-v2023.0322.111301.249.zip`

upload image file to related linux docker  
ttom1: toms-api, auth-api  
itom2: toms-portal  
itom1: toms-middleware

## deploy toms trust zone

1. login v511 remote desktop
   > ip: 172.20.150.4:39833  
   > login: autotolladmin1 / Atxxxxxx
2. upload image to `ttom1` docker
   ```bash
   unzip toms-api-master-v2023.0322.111301.249.zip
   docker load -i toms-api-master-v2023.0322.111301.249.tar
   ```
3. tag image as `p2`
   ```bash
   docker tag toms-api:master-v2023.0215.195425.253 toms-api:p2
   ```
4. check image version with command `docker images`, should looks like below
   ```bash
   REPOSITORY     TAG                            IMAGE ID       CREATED        SIZE
   bes/toms-api   latest                         670dac26934f   3 months ago   248MB
   bes/toms-api   master                         670dac26934f   3 months ago   248MB
   bes/toms-api   master-v2023.0215.195425.253   670dac26934f   3 months ago   248MB
   bes/toms-api   p2                             670dac26934f   3 months ago   248MB
   ```
5. upload folder `deploy_toms/p2-toms-api-auth-api` to `ttom1`, path should be `/mnt/data/toms/`.
   ```bash
   ls -l /mnt/data/toms
   ```
   ```bash
   -rw------- 1 user00 user00 1359 Feb  3 16:38 auth-api.appsettings.nonprod.json
   -rw------- 1 user00 user00  972 Feb  7 17:32 docker-compose.yml
   drwx------ 2 user00 user00 4096 Feb 17 11:51 images
   drwxr-xr-x 2 user00 user00    6 Feb 17 11:51 tmp
   -rw------- 1 user00 user00  768 Feb  7 17:00 toms-api.appsettings.nonprod.json
   -rw------- 1 user00 user00 2072 Feb  7 17:28 toms-ca-chain.pem
   ```
6. start container
   ```bash
   cd /mnt/data/toms
   docker-compose up -d
   ```
7. setup crontab, see file `crontab` in folder.

## deploy toms-middleware

1. login v630 remote desktop
   > ip: 172.20.151.109:39833  
   > login: autotolladmin1 / Atxxxxxx
2. upload image to `itom1` docker
3. tag image as `p2`
4. check image version with command `docker images`
5. upload folder `deploy_toms/p2-toms-middleware` to `itom1`, path should be `/mnt/data/toms/`
6. start container
   ```bash
   cd /mnt/data/toms
   docker-compose up -d
   ```

## deploy toms-portal

1. login v504 remote desktop
   > ip: 172.20.148.120:39833  
   > login: autotolladmin1 / Atxxxxxx
2. upload image to `itom2` docker
3. tag image as `p2`
4. check image version with command `docker images`
5. upload folder `deploy_toms/p2-toms-portal` to `itom2`, path should be `/mnt/data/toms/`
6. start container
   ```bash
   cd /mnt/data/toms
   docker-compose up -d
   ```

## toms connection info (P2)

### toms trust zone (toms-api, toms-auth-api)

- remote desktop v511
  - ip: 172.20.150.4:39833
  - user: autotolladmin1
  - pass: AtlXXXXX
- toms-api (ttom1)
  - url: `http://172.20.150.2:31001/swagger/index.html`
- toms-auth-api (ttom1)
  - url: `http://172.20.150.2:31004/swagger/index.html`
- keycloak (ttom2)
  - url: `http://172.20.150.3:8080/`
  - user: keycloak
  - pass: AtlXXXXX
- mongodb (ttom2)
  - connect str: `mongodb://root:Atl%402022@172.20.150.3:27017/?directConnection=true`
  - user: root
  - pass: AtlXXXXX
- toms db
  - host: p2vdbs-tdffsbe-ptomsdb4-ha1.dbaas.gcis.hksarg
  - schema: toms
  - user: besdb_owner / besdb_user
  - pass:
- keycloak db
  - host: p2vdbs-tdffsbe-ptomsdb2-ha1.dbaas.gcis.hksarg
  - schema: keycloak
  - user: keycloak
  - pass: AtlXXXXX

### itom1 (toms-middleware)

- remote desktop v630

  - ip: 172.20.151.109:39833
  - user: autotolladmin1
  - pass: AtlXXXXX

- toms-middleware (ttom1)
  - url: `http://172.20.151.121:31002/swagger/index.html`
  - url: `https://172.20.151.121:32002/swagger/index.html`
  - view log: `plink -t -no-antispoof user00@172.20.151.121 "su -c 'docker logs toms-middleware --tail 500 -f'"`

### itom2 (toms-portal)

- remote desktop v504
  - ip: 172.20.148.120:39833
  - user: autotolladmin1
  - pass: AtlXXXXX
- toms-portal (ttom1)
  - url: `https://172.20.148.125:32030/`
  - view log: `plink -t -no-antispoof user00@172.20.148.125 "su -c 'docker logs toms-portal --tail 500 -f'"`

## server cert

only toms-middleware need server cert  
server cert should container below ips, can create in toms portal  
ask fu for further question

- 127.0.0.1 (localhost ip)
- 172.20.151.121 (v630 internal ip, for ik8s access)
- 172.20.150.71 (kong gateware v630 load balancer ip, for das access)
- 172.20.150.73 (ik8s v630 load balancer ip, for das access)
- 172.20.151.110 (ik8s v630 worker 1 ip, for das access)
- 172.20.151.111 (ik8s v630 worker 2 ip, for das access)
- 172.20.151.112 (ik8s v630 worker 3 ip, for das access)

download toms-middleware (APP00234) server cert from toms-api

```shell
curl -X 'POST' 'http://192.168.64.170:31001/CertManage/TOMS_CRT016_GetServerCertFile' -d '{"app_id": "APP00234"}' -o toms-middleware-server-cert.zip
```

## toms diagram

```mermaid
%%{ init: { 'flowchart': { 'curve': 'basis' } } }%%
flowchart LR;
    subgraph dmz
        subgraph i_k8s
            das_middleware
            bes_wmm2
            other_apps
        end
        subgraph itom1 v630
            toms_middleware
            i_mongodb
        end
        subgraph itom2 v504
            toms_portal
        end
    end
    subgraph v511 toms trust zone
        subgraph ttom1
            toms_api
            auth_api
        end
        subgraph ttom2 - setup by IGSL
            t_mongodb
            keycloak
        end
    end
    subgraph gov_dbaas_mariadb
        ptomsdb2
        ptomsdb4
    end
    subgraph DAS zone
        das
    end
    subgraph TSP zone
        tsp_ik8s
    end

keycloak --> ptomsdb4
auth_api --> t_mongodb
auth_api --> keycloak
toms_api --> ptomsdb2
toms_api <--> toms_middleware
toms_portal --> auth_api
toms_portal --> toms_api
toms_middleware --> i_mongodb
das_middleware <--> toms_middleware
bes_wmm2 --> toms_middleware
tsp_ik8s --> bes_wmm2
das <--> das_middleware

i_mongodb[mongo.token_service]
t_mongodb[mongo.bes_web_config]
```
