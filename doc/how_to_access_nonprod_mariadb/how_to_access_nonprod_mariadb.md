# how_to_access_nonprod_mariadb

## connect nonprod VPN

For bes nonprod

```
FortiClient VPN
Remote Gateway: 202.128.227.2
Customize port: 443
```

## install and use HeidiSQL

### network type must be `SSH tunnel`

![](heidisql_connection.png)

### SSH host should be one of trust zone k8s worker ip
![](heidisql_connection_2.png)

### SSL must on
![](heidisql_connection_3.png)
