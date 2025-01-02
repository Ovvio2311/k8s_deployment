# deploy toms-api to nonprod

## detail procedure

1. download image from dev harbor as zip file
   use **`Git Bash`** to execute below command

   ```bash
   IMAGE_NAME="toms-portal" # "auth-api" # "toms-api" # "toms-middleware" # "toms-portal"
   docker image rm -f --no-prune $(docker images --filter=reference=*/bes/${IMAGE_NAME}:master* --filter=reference=bes/${IMAGE_NAME}:master* --format "{{.Repository}}:{{.Tag}}")
   docker pull 192.168.64.186/bes/${IMAGE_NAME}:master
   docker tag 192.168.64.186/bes/${IMAGE_NAME}:master bes/${IMAGE_NAME}:master
   IMAGE_V_TAG=$(curl -k "https://192.168.64.186/api/v2.0/projects/bes/repositories/${IMAGE_NAME}/artifacts/master/tags?page_size=1&q=name%3D~master-v" | grep -o -P '(?<="name":")[^"]*')
   docker tag bes/${IMAGE_NAME}:master bes/${IMAGE_NAME}:${IMAGE_V_TAG}
   docker tag bes/${IMAGE_NAME}:master bes/${IMAGE_NAME}:latest

   docker save -o ${IMAGE_NAME}-${IMAGE_V_TAG}.tar "bes/${IMAGE_NAME}:master" "bes/${IMAGE_NAME}:${IMAGE_V_TAG}" "bes/${IMAGE_NAME}:latest"
   zip ${IMAGE_NAME}-${IMAGE_V_TAG}.zip ${IMAGE_NAME}-${IMAGE_V_TAG}.tar
   echo done
   ```

2. upload zip file to remote desktop  
   172.24.150.4:39833 ( C:\autotoll_workspace\deploy_folder\tmp\ )

3. upload zip file to linux `/mnt/data/toms/tmp/`

4. unzip and load image in linux

   ```bash
   su

   ENV_NAME=nonprod # nonprod # p1 # p2

   cd /mnt/data/toms/tmp/
   unzip *.zip -n
   docker load -i *.tar
   sleep 1
   IMAGE_REPO="bes/$(ls *.tar | sed 's/.tar//g' | sed 's/-master/:master/g')"
   IMAGE_NEW_REPO="$(echo ${IMAGE_REPO} | sed 's/[:].*//g'):${ENV_NAME}"
   docker tag ${IMAGE_REPO} ${IMAGE_NEW_REPO}

   # restart container
   sleep 1
   cd /mnt/data/toms
   docker-compose up -d
   ```

5. clearup
   ```bash
   mkdir -p /mnt/data/toms/images/
   mv /mnt/data/toms/tmp/* /mnt/data/toms/images/ -f
   ```
