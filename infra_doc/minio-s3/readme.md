## Install MinIO
```bash
DATA_PATH=/mnt/minio_s3/data
CONFIG_PATH=/mnt/minio_s3/config
LOGIN_USER=admin
LOGIN_PASSWORD="3Dxxxxxx"

# remove old container
sudo docker container stop minio
sudo docker container rm minio

sudo docker run --restart unless-stopped -it -d \
   -p 9000:9000 \
   -p 9090:9090 \
   --name minio \
   -v $DATA_PATH:/data \
   -v $CONFIG_PATH:/root/.minio \
   -e "MINIO_ROOT_USER=$LOGIN_USER" \
   -e "MINIO_ROOT_PASSWORD=$LOGIN_PASSWORD" \
   quay.io/minio/minio server /data --console-address ":9090"

# clear password in bash history
history -c
```

```bash
# find file older then 200min
find /mnt/minio_s3/data/tsca -mmin +200 -type f -printf "%t %-25p\n"

# show file count
find /mnt/minio_s3/data/tsca -mmin +200 -type f -printf "%t %-25p\n" | wc -l

# find file older then 7day
find /mnt/minio_s3/data/tsca -mtime +7 -type f -printf "%t %-25p\n"
 
# show files total size in GB
echo $[($(find /mnt/minio_s3/data/tsca -mmin +300 -type f -printf %s+)0)/1024/1024/1024]
```