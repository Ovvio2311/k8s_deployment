## mongodb
```shell
# export from 
mongodump --uri="mongodb://atdbuser:Autotoll2345!@192.168.64.183:27017/?authSource=admin" --db=bes_web_config --out=bes_web_config/

mongorestore --uri="mongodb://user00:Atl%402022@localhost:27017/?authSource=admin" --db=bes_web_config bes_web_config/

mongodump --uri="mongodb://atdbuser:Autotoll2345!@192.168.64.183:27017/?authSource=admin" --db=token_service --out=token_service/

mongorestore --uri="mongodb://user00:Atl%402022@localhost:27017/?authSource=admin" --db=token_service token_service/
```


## mariadb
```
# can used on jasper report 
jdbc:mariadb://t1vdbs-tdffsbe-tdb04-ha1.dbaas.gcisdctr.hksarg:19307/bes_core?useSSL=true&trustServerCertificate=true
```

gov ref doc [here](./GCIS_DBaaS_Self_Service_Admin_Procedure_v1.5.pdf)
```sql
-- procedure provided by gov doc

call GCIS_SCHEMA.CREATE_DB_SCHEMA('bes_core');
ALTER DATABASE bes_core COLLATE = 'utf8mb4_unicode_ci';
SET collation_server = 'utf8mb4_unicode_ci';

call GCIS_SCHEMA.DROP_DB_USER('besdb_owner');
call GCIS_SCHEMA.DROP_DB_USER('besdb_user');
call GCIS_SCHEMA.DROP_DB_USER('besdb_readonly');

call GCIS_SCHEMA.CREATE_DB_USER('besdb_owner', 'bes_core', 'objectowner','XXXXXX');
call GCIS_SCHEMA.CREATE_DB_USER('besdb_user', 'bes_core', 'app_readwrite','XXXXXX');
call GCIS_SCHEMA.CREATE_DB_USER('besdb_readonly', 'bes_core', 'readonly','XXXXXX');
call GCIS_SCHEMA.CHANGE_DB_USER_PASSWORD('besdb_owner', 'XXXXXX');

call GCIS_SCHEMA.CREATE_DB_SCHEMA('testdb1');
call GCIS_SCHEMA.LIST_DB_SCHEMA();
call GCIS_SCHEMA.DROP_DB_SCHEMA('[Schema Name]');
call GCIS_SCHEMA.LIST_DB_SESSION();
call GCIS_SCHEMA.KILL_DB_SESSION(28632);
call GCIS_SCHEMA.SHOW_DB_LOCK()
call GCIS_SCHEMA.SHOW_DB_BLOCK()
call GCIS_SCHEMA.FLUSH_DB_PRIV();
call GCIS_SCHEMA.FLUSH_DB_HOST();
```
