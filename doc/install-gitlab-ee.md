# GitLab Server Setup

Install docker
<https://docs.docker.com/engine/install/ubuntu/>
install docker-compose
<https://docs.docker.com/compose/install/>

Perpare TLS Cert

```shell
mkdir ~/tmp
cd ~/tmp
MY_GITLAB_IP=10.13.0.55
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $MY_GITLAB_IP.key -out $MY_GITLAB_IP.crt -subj "/CN=$MY_GITLAB_IP" -addext subjectAltName=DNS:localhost,IP:$MY_GITLAB_IP

sudo mkdir -p /srv/gitlab/config/ssl
sudo mv $MY_GITLAB_IP.crt /srv/gitlab/config/ssl
sudo mv $MY_GITLAB_IP.key /srv/gitlab/config/ssl
```

Create docker-compose file

```shell
cat << 'EOF' > docker-compose.yml
web:
  image: 'gitlab/gitlab-ce:latest'
  restart: always
  hostname: '10.13.0.55'
  environment:
    GITLAB_OMNIBUS_CONFIG: |
      external_url 'https://10.13.0.55'
      gitlab_rails['initial_root_password'] = "i_am_password"
      gitlab_rails['gitlab_shell_ssh_port'] = 2224
      gitlab_rails['gitlab_email_from'] = "etc.gitlab@autotoll.com.hk"
      gitlab_rails['gitlab_email_reply_to'] = "noreply@autotoll.com.hk"
      gitlab_rails['smtp_enable'] = true
      gitlab_rails['smtp_address'] = "192.168.11.211"
      gitlab_rails['smtp_port'] = 25
      gitlab_rails['smtp_enable_starttls_auto'] = false
      gitlab_rails['smtp_tls'] = false
      gitlab_rails['smtp_force_ssl'] = false
      gitlab_rails['smtp_openssl_verify_mode'] = "none"
      nginx['ssl_certificate'] = "/etc/gitlab/ssl/10.13.0.55.crt"
      nginx['ssl_certificate_key'] = "/etc/gitlab/ssl/10.13.0.55.key"
  ports:
    - '80:80'
    - '443:443'
    - '2224:22'
  volumes:
    - '/srv/gitlab/config:/etc/gitlab'
    - '/srv/gitlab/logs:/var/log/gitlab'
    - '/srv/gitlab/data:/var/opt/gitlab'

EOF
```

```shell
sudo docker-compose up -d
sudo docker ps
sudo docker logs  <container_id> --follow
## wait for gitlab setup
```
