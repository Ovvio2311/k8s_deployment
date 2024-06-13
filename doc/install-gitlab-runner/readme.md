# install gitlab runner

```bash

#!/bin/bash

GITLAB_HOST=192.168.64.188
GITLAB_PORT=443
GITLAB_URL="https://${GITLAB_HOST}:${GITLAB_PORT}/"
REGISTRATION_TOKEN="AUy1Hd1jrej3XKXJs_ww"

HARBOR_HOST=192.168.64.186
HARBOR_PORT=443

DEPLOY_FOLDER=/srv/gitlab-runner

##=============================================

mkdir -p ${DEPLOY_FOLDER}/config/certs
cd ${DEPLOY_FOLDER}

# download gitlab server certificate
openssl s_client -showcerts -connect ${GITLAB_HOST}:${GITLAB_PORT} </dev/null 2>/dev/null | openssl x509 -outform PEM >${DEPLOY_FOLDER}/config/certs/${GITLAB_HOST}.crt

# download harbor server certificate
openssl s_client -showcerts -connect ${HARBOR_HOST}:${HARBOR_PORT} </dev/null 2>/dev/null | openssl x509 -outform PEM >${DEPLOY_FOLDER}/${HARBOR_HOST}.crt

sudo docker run --rm -v ${DEPLOY_FOLDER}/config:/etc/gitlab-runner/ docker.io/gitlab/gitlab-runner register \
  --name="shell-runner" \
  --url=${GITLAB_URL} \
  --executor "shell" \
  --builds-dir="/srv/gitlab-runner/builds" \
  --cache-dir="/srv/gitlab-runner/cache" \
  --env='GIT_CLONE_PATH=$CI_BUILDS_DIR/$CI_CONCURRENT_ID/$CI_PROJECT_NAME' \
  --custom_build_dir-enabled \
  --registration-token=${REGISTRATION_TOKEN} \
  --non-interactive \
  --run-untagged="false" \
  --tag-list="shell-runner"

sudo docker run --rm -v ${DEPLOY_FOLDER}/config:/etc/gitlab-runner/ docker.io/gitlab/gitlab-runner register \
  --name="docker-dind-runner" \
  --request-concurrency 5 \
  --url=${GITLAB_URL} \
  --executor "docker" \
  --builds-dir="/builds" \
  --cache-dir="/cache" \
  --env='GIT_CLONE_PATH=$CI_BUILDS_DIR/$CI_CONCURRENT_ID/$CI_PROJECT_NAME' \
  --custom_build_dir-enabled \
  --docker-tlsverify="false" \
  --docker-image "docker:23" \
  --docker-volumes="/var/run/docker.sock:/var/run/docker.sock" \
  --docker-volumes="/etc/docker/certs.d:/etc/docker/certs.d" \
  --docker-volumes="/builds:/builds" \
  --docker-volumes="/cache:/cache" \
  --registration-token=${REGISTRATION_TOKEN} \
  --non-interactive \
  --run-untagged="true" \
  --tag-list="docker-dind-runner"

sudo docker run --rm -v ${DEPLOY_FOLDER}/config:/etc/gitlab-runner/ docker.io/gitlab/gitlab-runner register \
  --name="docker-non-concurrent-runner" \
  --request-concurrency 1 \
  --url=${GITLAB_URL} \
  --executor "docker" \
  --env='GIT_CLONE_PATH=$CI_BUILDS_DIR/$CI_CONCURRENT_ID/$CI_PROJECT_NAME' \
  --cache-max_uploaded_archive_size 0 \
  --docker-tlsverify="false" \
  --docker-image "docker:23" \
  --docker-volumes="/var/run/docker.sock:/var/run/docker.sock" \
  --docker-volumes="/etc/docker/certs.d:/etc/docker/certs.d" \
  --registration-token=${REGISTRATION_TOKEN} \
  --non-interactive \
  --run-untagged="false" \
  --tag-list="docker-non-concurrent-runner"

docker wait for register

echo "

services:
  dind:
    container_name: dind
    image: docker:23-dind
    restart: always
    privileged: true
    environment:
      DOCKER_TLS_CERTDIR: ''
    command:
      - --storage-driver=overlay2
    networks:
      - gitlab-runner
    volumes:
      - /srv/gitlab-runner/192.168.64.186.crt:/etc/docker/certs.d/192.168.64.186/ca.crt
      - dind_data:/var/lib/docker
  runner:
    user: root
    container_name: runner
    restart: always
    image: docker.io/gitlab/gitlab-runner:v15.8.2
    depends_on:
      - dind
    environment:
      - DOCKER_HOST=tcp://dind:2375
    volumes:
      - /srv/gitlab-runner/config:/etc/gitlab-runner
    networks:
      - gitlab-runner
networks:
  gitlab-runner: {}

volumes:
  dind_data:
" >${DEPLOY_FOLDER}/docker-compose.yml

cd ${DEPLOY_FOLDER}
docker compose up -d --wait
```

```bash
crontab -l
```

```bash
# free disk space every week
0 1 * * 6 sudo docker exec dind docker system prune -f --volumes | sudo tee -a /home/autotoll/crontab.log
```
