#!/bin/bash
select result in auth-api toms-api toms-middleware toms-portal; do
    echo "Selected image: ${result}"
    echo "Start Download Image"

    IMAGE_NAME=$result
    docker image rm -f --no-prune $(docker images --filter=reference=*/bes/${IMAGE_NAME}:master* --filter=reference=bes/${IMAGE_NAME}:master* --format "{{.Repository}}:{{.Tag}}")
    docker pull 192.168.64.186/bes/${IMAGE_NAME}:master
    docker tag 192.168.64.186/bes/${IMAGE_NAME}:master bes/${IMAGE_NAME}:master
    IMAGE_V_TAG=$(curl -k "https://192.168.64.186/api/v2.0/projects/bes/repositories/${IMAGE_NAME}/artifacts/master/tags?page_size=1&q=name%3D~master-v" | grep -o -P '(?<="name":")[^"]*')
    docker tag bes/${IMAGE_NAME}:master bes/${IMAGE_NAME}:${IMAGE_V_TAG}
    docker tag bes/${IMAGE_NAME}:master bes/${IMAGE_NAME}:latest
    
    echo "start save to file"
    docker save -o ${IMAGE_NAME}-${IMAGE_V_TAG}.tar "bes/${IMAGE_NAME}:master" "bes/${IMAGE_NAME}:${IMAGE_V_TAG}" "bes/${IMAGE_NAME}:latest"

    echo "start zip file"
    zip ${IMAGE_NAME}-${IMAGE_V_TAG}.zip ${IMAGE_NAME}-${IMAGE_V_TAG}.tar

    echo "Download Completed"
    read -p "Press enter to exit..."
    exit
done
