@REM log location /opt/jasperreports-server-cp-8.0.0/apache-tomcat/webapps/jasperserver/WEB-INF/logs/jasperserver.log
plink -pw "Atl@2022" user00@172.24.150.156 "echo 'Atl@2022' | su -c 'cp /opt/jasperreports-server-cp-8.0.0/apache-tomcat/webapps/jasperserver/WEB-INF/logs/jasperserver.log /home/user00/ && chown user00 /home/user00/jasperserver.log'"
pscp  -pw "Atl@2022" user00@172.24.150.156:/home/user00/jasperserver.log "%USERPROFILE%/Desktop/jasperserver.log"
plink -pw "Atl@2022" user00@172.24.150.156 "rm /home/user00/jasperserver.log"
set /p=press enter to exit 