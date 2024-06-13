# bulk delete object

## Install aws cli tools

<https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>

## Reference doc:

- [high-level commands](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html)
- [API-level command](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-apicommands.html)
- non-official online command builder
  - https://awsclibuilder.com/home/services/s3
  - https://awsclibuilder.com/home/services/s3api

## Command

```bash
# worked on powershell or bash
aws configure set ca_bundle "C:\autotoll_workspace\gov_object_storage_root_ca.cer"

# set access key
aws configure set aws_access_key_id dGRmZnxxxxxxxxxxxxxxxxxxx
aws configure set aws_secret_access_key 417baxxxxxxxxxxxxxxxxxxxxxxxxxxx
cat "~\.aws\credentials"

# delete all jpg files in folder and subfolder, s3 url = s3://<bucket>/<path>
aws s3 rm s3://tsca/Evidence/9/41/20220707/ --no-verify-ssl --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*.jpg"

# with dryrun and debug option
aws s3 rm s3://tsca/Evidence/9/41/20220707/ --no-verify-ssl --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*.jpg" --dryrun --debug
```

```bash
# run container
docker run -it -d --entrypoint bash --name aws-cli 172.20.148.130:8083/tools/aws-cli:latest

# add trusted certificate
openssl s_client -showcerts -verify 5 -connect tdffsbe-o1.obj001.gcis.hksarg:443 < /dev/null | awk '/BEGIN CERTIFICATE/,/END CERTIFICATE/{ if(/BEGIN CERTIFICATE/){a++}; out="cert_chain.pem"; print >out}'
docker cp ./cert_chain.pem aws-cli:/aws/
docker exec aws-cli aws configure set ca_bundle "/aws/cert_chain.pem"

# set access key
docker exec aws-cli aws configure set aws_access_key_id dGRmZnNiZS1vMV9hZG1pbg==
docker exec aws-cli aws configure set aws_secret_access_key 417ba0e872d21eb816aacfc2fd23e1f7
docker exec aws-cli cat ~/.aws/credentials

# go into container bash
docker exec -it aws-cli bash

# delete
docker exec aws-cli-aug aws s3 rm s3://tsca/Evidence/9/41/20220801/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" > log.txt
```

```bash
docker run -it -d --entrypoint bash --name aws-cli-sep 172.20.148.130:8083/tools/aws-cli:latest


docker cp ./cert_chain.pem aws-cli-sep:/aws/
docker exec aws-cli-sep aws configure set ca_bundle "/aws/cert_chain.pem"
docker exec aws-cli-sep aws configure set aws_access_key_id dGRmZnNiZS1vMV9hZG1pbg==
docker exec aws-cli-sep aws configure set aws_secret_access_key 417ba0e872d21eb816aacfc2fd23e1f7
docker exec aws-cli-sep cat ~/.aws/credentials
docker cp ./s3_bulk_delete_sep.sh aws-cli-sep:/aws/
docker exec -d aws-cli-sep sh /aws/s3_bulk_delete_sep.sh
```

```bash
docker cp ./s3_bulk_delete.sh aws-cli:/aws/
docker exec -d aws-cli sh /aws/s3_bulk_delete.sh
docker exec -t aws-cli tail -n 50 -f /aws/log.txt
docker exec -t aws-cli-aug tail -n 50 -f /aws/log.txt
docker exec -t aws-cli-sep tail -n 50 -f /aws/log.txt
```

```bash
plink -no-antispoof -pw "Atl@2022" user00@172.20.150.130 "echo 'Atl@2022' | su -c 'docker exec -t aws-cli tail -n 50 -f /aws/log.txt'"
plink -no-antispoof -pw "Atl@2022" user00@172.20.150.130 "echo 'Atl@2022' | su -c 'docker exec -t aws-cli-aug tail -n 50 -f /aws/log.txt'"
plink -no-antispoof -pw "Atl@2022" user00@172.20.150.130 "echo 'Atl@2022' | su -c 'docker exec -t aws-cli-sep tail -n 50 -f /aws/log.txt'"
```

```bash
#!/bin/bash
my_date_array=("20220707"  "20220708"  "20220709"  "20220710"  "20220711"  "20220712"  "20220713"  "20220714"  "20220715"  "20220716"  "20220717"  "20220718"  "20220719"  "20220720"  "20220721"  "20220722"  "20220723"  "20220724"  "20220725"  "20220726"  "20220727"  "20220728"  "20220729"  "20220730"  "20220731"  "20220801"  "20220802"  "20220803"  "20220804"  "20220805"  "20220806"  "20220807"  "20220808"  "20220809"  "20220810"  "20220811"  "20220812"  "20220813"  "20220814"  "20220815"  "20220816"  "20220817"  "20220818"  "20220819"  "20220820"  "20220821"  "20220822"  "20220823"  "20220824"  "20220825"  "20220826"  "20220827"  "20220828"  "20220829"  "20220830"  "20220831"  "20220901"  "20220902"  "20220903"  "20220904"  "20220905"  "20220906"  "20220907"  "20220908"  "20220909"  "20220910"  "20220911"  "20220912"  "20220913"  "20220914")
for my_date in ${my_date_array[*]}; do
    for i in {1..6}; do
        aws s3 rm s3://tsca/video/VRS/MAINSTREAM/9/41/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm s3://tsca/video/VRS/MAINSTREAM/9/42/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm s3://tsca/video/VRS/MAINSTREAM/9/43/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm s3://tsca/video/VRS/MAINSTREAM/9/44/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm  s3://tsca/video/VRS/SUBSTREAM/9/41/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm  s3://tsca/video/VRS/SUBSTREAM/9/42/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm  s3://tsca/video/VRS/SUBSTREAM/9/43/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm  s3://tsca/video/VRS/SUBSTREAM/9/44/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm             s3://tsca/Evidence/9/41/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm             s3://tsca/Evidence/9/42/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm             s3://tsca/Evidence/9/43/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
        aws s3 rm             s3://tsca/Evidence/9/44/$my_date/ --endpoint-url https://tdffsbe-o1.obj001.gcis.hksarg --recursive --exclude "*" --include "*" >> log.txt
    done
done
```
