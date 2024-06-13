# compare image version

1. connect vpn
2. open ssh tunnel
   ```
   ssh user00@172.24.150.130 -N -L 8083:172.24.150.130:8083
   ```
3. execute script `./scripts/list_harbor_build_time.py`, you will get csv file like this:

   | repo_name      | build_time                     | size      | tag_name |
   | -------------- | ------------------------------ | --------- | -------- |
   | bes/accmgt-api | 2023-04-13T02:40:34.582888533Z | 105175796 | nonprod  |
   | bes/auth-api   | 2023-03-22T03:14:04.170682888Z | 99566871  | nonprod  |

4. get csv file from p1 and p2, then compare build time
