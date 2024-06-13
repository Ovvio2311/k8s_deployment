## create docker compose file

```bash
tee /home/autotoll/pulsar/docker-compose.yml << EOF
version: "3.7"
services:
  pulsar:
    container_name: "pulsar"
    image: apachepulsar/pulsar:2.6.0
    command: bin/pulsar standalone
    hostname: pulsar
    ports:
      - "8080:8080"
      - "6650:6650"
    restart: unless-stopped
    volumes:
      - "/home/autotoll/pulsar/data/:/pulsar/data/"
  pulsar-manager:
    container_name: "pulsar-manager"
    image: apachepulsar/pulsar-manager:v0.2.0
    ports:
      - "9527:9527"
      - "7750:7750"
    restart: unless-stopped
    volumes:
      - "/home/autotoll/pulsar-manager/data/:/data/"
    depends_on:
      - pulsar
    links:
      - pulsar
    environment:
      SPRING_CONFIGURATION_FILE: /pulsar-manager/pulsar-manager/application.properties
EOF
```

## start containers

```bash
cd /home/autotoll/pulsar/
sudo docker compose up -d
```

## create login user

```bash
pulsar_broker_url=http://192.168.64.107:7750
CSRF_TOKEN=$(curl $pulsar_broker_url/pulsar-manager/csrf-token)

curl \
    -H "X-XSRF-TOKEN: $CSRF_TOKEN" \
    -H "Cookie: XSRF-TOKEN=$CSRF_TOKEN;" \
 -H 'Content-Type: application/json' \
 -X PUT $pulsar_broker_url/pulsar-manager/users/superuser \
 -d '{"name": "pulsar", "password": "pulsar", "description": "pulsar", "email": "username@test.org"}'
```

## create env in ui

1. open browser http://192.168.64.107:9527/
2. click "+New Environment"
3. Environment Name: dev  
   Service URL: http://192.168.64.107:8080/


