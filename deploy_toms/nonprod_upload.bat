REM example of upload.bat
set linux_ip=172.24.150.2
set ENV_NAME=nonprod

REM upload image to linux
pscp -pw "Atl@2022" -r "C:\autotoll_workspace\deploy_folder\tmp\*.zip" user00@%linux_ip%:/mnt/data/toms/tmp/

REM load image from zip file
plink -no-antispoof -pw "Atl@2022" user00@%linux_ip% "cd /mnt/data/toms/tmp/ && echo 'Atl@2022' | su -c 'unzip *.zip'"
plink -no-antispoof -pw "Atl@2022" user00@%linux_ip% "cd /mnt/data/toms/tmp/ && echo 'Atl@2022' | su -c 'docker load -i *.tar'"
plink -no-antispoof -pw "Atl@2022" user00@%linux_ip% "cd /mnt/data/toms/tmp/ && echo 'Atl@2022' | su -c 'IMAGE_REPO=bes/$(ls *.tar | sed s/.tar//g | sed s/-master/:master/g) && IMAGE_NEW_REPO=$(echo ${IMAGE_REPO} | sed s/[:].*//g):%ENV_NAME% && docker tag ${IMAGE_REPO} ${IMAGE_NEW_REPO}'"

REM restart container
plink -no-antispoof -pw "Atl@2022" user00@%linux_ip% "cd /mnt/data/toms/ && echo 'Atl@2022' | su -c 'docker-compose up -d'" 

echo press enter to continue
set /p=

REM clearup
plink -no-antispoof -pw "Atl@2022" user00@%linux_ip% "mkdir -p /mnt/data/toms/images/ && mv /mnt/data/toms/tmp/* /mnt/data/toms/images/ -f" 

move "C:\autotoll_workspace\deploy_folder\tmp\*.zip" "C:\autotoll_workspace\deploy_folder\trash_can\"