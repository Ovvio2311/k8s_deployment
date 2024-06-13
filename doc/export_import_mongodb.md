# export import mongodb

## export

```bash
mongodump --uri="mongodb://root:Atl%402022@192.168.64.103:27017/?authSource=admin" --db=bes_web_config --out=mongodump/bes_web_config
mongodump --uri="mongodb://root:Atl%402022@192.168.64.103:27017/?authSource=admin" --db=token_service --out=mongodump/token_service
```

## import

```bash
mongorestore --uri="mongodb://root:Atl%402022@172.20.150.3:27017/?authSource=admin" --db=bes_web_config mongodump/bes_web_config/
mongorestore --uri="mongodb://root:Atl%402022@172.20.150.3:27017/?authSource=admin" --db=token_service mongodump/token_service/
```
