# gitlab backup

## application backup

gitlab config file: /etc/gitlab/gitlab.rb

```rb
# ref docs: https://docs.gitlab.com/13.12/omnibus/settings/backups.html
# backup related config
gitlab_rails['manage_backup_path'] = true
gitlab_rails['backup_path'] = "/mnt/minio-gitlab-backup"
gitlab_rails['backup_keep_time'] = 259200
# 259200 = 3 days = 60 * 60 * 24 * 3
```

reload config after modify

```bash
gitlab-ctl reconfigure
```

onetime gitlab data backup

```bash
gitlab-backup create
```

## config & secret backup

onetime config backup

```bash
gitlab-ctl backup-etc
ls /etc/gitlab/config_backup
```

## minio client configuration

Create minio client config file

```
mkdir -p /root/.mc/
tee /root/.mc/config.json <<EOF
{
        "version": "10",
        "aliases": {
                "myminio": {
                        "url": "http://192.168.64.131:9000",
                        "accessKey": "gXFJMGgZN9g2AL3D",
                        "secretKey": "KbODvGjeemQT6eeOrvBEEZLwlTk09oju",
                        "api": "s3v4",
                        "path": "auto"
                }
        }
}
EOF
```

## crontab

```
# backup gitlab data
0 2 * * *  gitlab-backup create CRON=1
# backup gitlab config
0 3 * * *  gitlab-ctl backup-etc && cd /etc/gitlab/config_backup && cp $(ls -t | head -n1) /mnt/minio-gitlab-backup/
# upload backup file to minio
30 3 * * * docker run --rm -it -v /mnt/minio-gitlab-backup/:/backup/ -v /root/.mc/config.json:/root/.mc/config.json --entrypoint='' minio/mc:RELEASE.2023-04-06T16-51-10Z sh -c 'mc cp --newer-than 0d12h0s /backup/* myminio/gitlab-backup'
# remove file in minio that older than 7 days
0 4 * * * docker run --rm -it -v /root/.mc/config.json:/root/.mc/config.json --entrypoint='' minio/mc:RELEASE.2023-04-06T16-51-10Z sh -c "mc find myminio/gitlab-backup --older-than 7d --exec 'mc rm {}'"
```
