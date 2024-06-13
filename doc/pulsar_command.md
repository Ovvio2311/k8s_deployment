# kubectl command

## stop all consumer and das-middleware

```bash
# change all consumer replicaCount to 0

# executed on trust k8s master
kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd login 127.0.0.1:8080 --insecure --username admin --password 'Atl@2022'
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep consumer | grep -v bes-notification-pulsar-consumer-services);do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app set -p replicaCount=0 $app_name && echo $app_name; done
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep 'tx-validation');do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app set -p replicaCount=0 $app_name && echo $app_name; done

# executed on dmz k8s master, change all das-middleware replicaCount to 0
kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd login 127.0.0.1:8080 --insecure --username admin --password 'Atl@2022'
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep 'das-middleware\|das-video');do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app set -p replicaCount=0 $app_name && echo $app_name; done
```

## restart consumer and das-middleware

```bash
# unset replicaCount=0, use default replicaCount in gitlab yaml file
# executed on trust k8s master
kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd login 127.0.0.1:8080 --insecure --username admin --password 'Atl@2022'
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep consumer | grep -v bes-notification-pulsar-consumer-services);do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app unset -p replicaCount $app_name && echo $app_name; done
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep tx-validation | grep -v bes-notification-pulsar-consumer-services);do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app unset -p replicaCount $app_name && echo $app_name; done

# executed on dmz k8s master
kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd login 127.0.0.1:8080 --insecure --username admin --password 'Atl@2022'
for app_name in $(kubectl get application -n argocd -o name | cut -b 25- | grep 'das-middleware\|das-video');do kubectl exec deploy/argo-cd-argocd-server -n argocd -- argocd app unset -p replicaCount $app_name && echo $app_name; done
```

# pulsar operation command

## create das topic for tunnel

```bash
su
cd /opt/apache-pulsar-2.9.1/

# tsca
bin/pulsar-admin namespaces create das/tsca
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/txv_process_stat_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_txv_process_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_backlog_txv_process_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_idax01_trxn_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_sim_idax01_trxn_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_sim_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_imgobj_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_imgobj_sim_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_raw_trxn_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_raw_evid_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_2_idax01_trxn_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_2_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/tsca/das_middleware_imgobj_2_idax02_evid_upload

# lrt
bin/pulsar-admin namespaces create das/lrt
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/txv_process_stat_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_txv_process_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_backlog_txv_process_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_idax01_trxn_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_sim_idax01_trxn_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_sim_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_imgobj_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_imgobj_sim_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_raw_trxn_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_raw_evid_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_2_idax01_trxn_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_2_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/lrt/das_middleware_imgobj_2_idax02_evid_upload

# smt
bin/pulsar-admin namespaces create das/smt
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/txv_process_stat_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_txv_process_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_backlog_txv_process_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_middleware_idax01_trxn_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_middleware_sim_idax01_trxn_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_middleware_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_middleware_sim_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_middleware_imgobj_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_middleware_imgobj_sim_idax02_evid_upload
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_raw_trxn_queue
bin/pulsar-admin topics create-partitioned-topic -p 6 persistent://das/smt/das_raw_evid_queue
```

## delete das topic for tunnel

```bash
cd /opt/apache-pulsar-2.9.1/

bin/pulsar-admin topics delete --force                   persistent://das/tsca/das_middleware_backlog_idax01_trxn_upload
bin/pulsar-admin topics delete --force                   persistent://das/tsca/das_middleware_backlog_sim_idax01_trxn_upload
bin/pulsar-admin topics delete --force                   persistent://das/tsca/das_middleware_backlog_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/tsca/das_middleware_backlog_sim_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/tsca/das_middleware_imgobj_backlog_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/tsca/das_middleware_imgobj_backlog_sim_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/tsca/das_backlog_txv_process_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_middleware_idax01_trxn_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_middleware_sim_idax01_trxn_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_middleware_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_middleware_sim_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_middleware_imgobj_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_middleware_imgobj_sim_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_txv_process_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_raw_trxn_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/das_raw_evid_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/tsca/txv_process_stat_queue


bin/pulsar-admin topics delete --force                   persistent://das/lrt/das_middleware_backlog_idax01_trxn_upload
bin/pulsar-admin topics delete --force                   persistent://das/lrt/das_middleware_backlog_sim_idax01_trxn_upload
bin/pulsar-admin topics delete --force                   persistent://das/lrt/das_middleware_backlog_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/lrt/das_middleware_backlog_sim_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/lrt/das_middleware_imgobj_backlog_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/lrt/das_middleware_imgobj_backlog_sim_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/lrt/das_backlog_txv_process_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_middleware_idax01_trxn_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_middleware_sim_idax01_trxn_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_middleware_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_middleware_sim_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_middleware_imgobj_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_middleware_imgobj_sim_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_txv_process_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_raw_trxn_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/das_raw_evid_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/lrt/txv_process_stat_queue


bin/pulsar-admin topics delete --force                   persistent://das/smt/das_middleware_backlog_idax01_trxn_upload
bin/pulsar-admin topics delete --force                   persistent://das/smt/das_middleware_backlog_sim_idax01_trxn_upload
bin/pulsar-admin topics delete --force                   persistent://das/smt/das_middleware_backlog_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/smt/das_middleware_backlog_sim_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/smt/das_middleware_imgobj_backlog_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/smt/das_middleware_imgobj_backlog_sim_idax02_evid_upload
bin/pulsar-admin topics delete --force                   persistent://das/smt/das_backlog_txv_process_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_middleware_idax01_trxn_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_middleware_sim_idax01_trxn_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_middleware_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_middleware_sim_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_middleware_imgobj_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_middleware_imgobj_sim_idax02_evid_upload
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_txv_process_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_raw_trxn_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/das_raw_evid_queue
bin/pulsar-admin topics delete-partitioned-topic --force persistent://das/smt/txv_process_stat_queue

bin/pulsar-admin namespaces delete "das/tsca"
bin/pulsar-admin namespaces delete "das/lrt"
bin/pulsar-admin namespaces delete "das/smt"

```

## clear das backlog

```bash
# clear-backlog in namespace "das/lrt"
bin/pulsar-admin namespaces clear-backlog "das/lrt" --force -s "DAS_TxnRecordConsumer"
bin/pulsar-admin topics clear-backlog persistent://das/lrt/das_middleware_idax01_trxn_upload --subscription "DAS_TxnRecordConsumer";
bin/pulsar-admin topics clear-backlog persistent://das/lrt/das_middleware_backlog_idax01_trxn_upload --subscription "DAS_TxnRecordConsumer";
bin/pulsar-admin topics clear-backlog persistent://das/lrt/das_middleware_idax02_evid_upload --subscription "DAS_EvidRecordConsumer";
bin/pulsar-admin topics clear-backlog persistent://das/lrt/das_middleware_backlog_idax02_evid_upload --subscription "DAS_EvidRecordConsumer";
bin/pulsar-admin topics clear-backlog persistent://das/lrt/das_backlog_txv_process_queue --subscription "TxnProcessConsumer";
```

## create tsp pulsar message topic

```bash
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-sms-msg-high
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/receive-msg-low
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/receive-msg-high
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-app-msg-high
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-sms-msg-low
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-email-msg-medium
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/receive-msg-medium
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-app-msg-low
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-app-msg-medium
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-email-msg-low
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-email-msg-high
bin/pulsar-admin topics delete-partitioned-topic --force persistent://tsp/notification-service/send-sms-msg-medium

bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-sms-msg-high
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/receive-msg-low
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/receive-msg-high
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-app-msg-high
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-sms-msg-low
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-email-msg-medium
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/receive-msg-medium
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-app-msg-low
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-app-msg-medium
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-email-msg-low
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-email-msg-high
bin/pulsar-admin topics create-partitioned-topic -p 1 persistent://tsp/notification-service/send-sms-msg-medium
```

## other useful pulsar command

```bash
cd /opt/apache-pulsar-2.9.1/

# clear-backlog in all partitioned-topics
for one_topic in $(bin/pulsar-admin topics list-partitioned-topics "my-tenant/my-namespace");
    do (
        for one_sub in $(bin/pulsar-admin topics subscriptions "$one_topic");
            do bin/pulsar-admin topics clear-backlog $one_topic --subscription $one_sub; echo "$one_topic : $one_sub"
        done);
done

# test send messages
bin/pulsar-client produce my-tenant/my-namespace/my-topic  -m "---------hello apache pulsar-------"
# list partitioned topics
bin/pulsar-admin topics list-partitioned-topics "my-tenant/my-namespace"
# list topics
bin/pulsar-admin topics list "my-tenant/my-namespace"
# delete namespace
bin/pulsar-admin namespaces delete "my-tenant/my-namespace"
# create namespace
bin/pulsar-admin namespaces create "my-tenant/my-namespace"
# skip messages
bin/pulsar-admin topics skip --count 1 --subscription XXXX "persistent://my-tenant/my-namespace/my-topic"

# delete all topic
for one_topic in $(bin/pulsar-admin topics list "my-tenant/my-namespace"); do bin/pulsar-admin topics delete "$one_topic" --force; done

# delete all partitioned topic
for one_topic in $(bin/pulsar-admin topics list-partitioned-topics "my-tenant/my-namespace"); do bin/pulsar-admin topics delete-partitioned-topics "$one_topic" --force; done

# loop all sub in all topic
for one_topic in $(bin/pulsar-admin topics list "my-tenant/my-namespace"); do (for one_sub in $(bin/pulsar-admin topics subscriptions "$one_topic"); do echo $one_sub; done); done
# unsubscribe for all topic all sub in namespace
for one_topic in $(bin/pulsar-admin topics list "my-tenant/my-namespace"); do (for one_sub in $(my-tenant/my-namespace "$one_topic"); do bin/pulsar-admin topics unsubscribe "$one_topic" --force -s "$one_sub"; done); done

# skip for all message for all sub, all topic in namespace
for one_topic in $(bin/pulsar-admin topics list "my-tenant/my-namespace"); do (for one_sub in $(my-tenant/my-namespace "$one_topic"); do bin/pulsar-admin topics skip --count 99999 --subscription "$one_sub" "$one_topic"; done); done

# remove-auto-topic-creation
bin/pulsar-admin namespaces remove-auto-topic-creation "public/default"

# set-auto-topic-creation
bin/pulsar-admin namespaces set-auto-topic-creation "public/default" --disable true

# check broker
bin/pulsar-admin brokers get-runtime-config
bin/pulsar-admin brokers healthcheck
bin/pulsar-admin broker-stats monitoring-metrics -i
bin/pulsar-admin broker-stats topics -i

# check bookie
curl http://localhost:8000/metrics | grep bookie_SERVER_STATUS

# check topic
bin/pulsar admin persistent stats-internal $TOPIC
```

## disable auto-topic-creation

```bash
su
cd /opt/apache-pulsar-2.9.1/
# backup
cp conf/broker.conf conf/broker.conf.$(date +%Y%m%d.%H%M%S)
# modify config file
sed -i 's/allowAutoTopicCreation=true/allowAutoTopicCreation=false/g' conf/broker.conf
# check config file after replace
cat conf/broker.conf | grep allowAutoTopicCreation
# restart broker
systemctl restart pulsar-broker
# display to confirm
bin/pulsar-admin brokers get-runtime-config | grep allowAutoTopicCreation
```

# delpoy pulsar manager UI

```bash
pulsar_broker_url=http://10.14.0.103:7750
docker pull apachepulsar/pulsar-manager:v0.3.0
docker run -it -d \
 -p 9527:9527 -p 7750:7750 \
 -e SPRING_CONFIGURATION_FILE=/home/esso/pulsar-manager/application.properties \
 apachepulsar/pulsar-manager:v0.3.0

CSRF_TOKEN=$(curl $pulsar_broker_url/pulsar-manager/csrf-token)
curl \
    -H "X-XSRF-TOKEN: $CSRF_TOKEN" \
    -H "Cookie: XSRF-TOKEN=$CSRF_TOKEN;" \
 -H 'Content-Type: application/json' \
 -X PUT $pulsar_broker_url/pulsar-manager/users/superuser \
 -d '{"name": "pulsar", "password": "pulsar", "description": "test", "email": "username@test.org"}'
```

# bookkeeper shell

```bash
bin/bookkeeper shell bookieformat -d -n -f
bin/bookkeeper shell deleteledger -force -ledgerid 97
bin/bookkeeper shell readledger 97
bin/bookkeeper shell bookieinfo
bin/bookkeeper shell listledgers
bin/bookkeeper shell simpletest
bin/bookkeeper shell
```

# kubectl go in pulsar

```bash
kubectl exec -i -t -n pulsar pulsar-broker-0 -c pulsar-broker -- sh -c "clear; (bash || ash || sh)"
```
