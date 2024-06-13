REM Set environment variables for remote servers and login credentials
set tkubw2_ip=172.16.150.132
set ik8s_ip=172.16.148.106
set tk8s_ip=172.16.150.138
set pass=Atl@2022

REM Copy deployment files to the remote server and execute shell scripts
plink -P 22 -no-antispoof -pw "%pass%" user00@%tkubw2_ip% mkdir /mnt/data/tmp_upload_images/tmp_deploy_folder
pscp  -P 22 -pw "%pass%" "*.zip" user00@%tkubw2_ip%:/mnt/data/tmp_upload_images/tmp_deploy_folder/
pscp  -P 22 -pw "%pass%" "*.sh" user00@%tkubw2_ip%:/mnt/data/tmp_upload_images/tmp_deploy_folder/
plink -P 22 -no-antispoof -pw "%pass%" user00@%tkubw2_ip% "cd /mnt/data/tmp_upload_images/tmp_deploy_folder && echo 'Atl@2022' | su -c 'sh _unpack_deploy_images_cmd.sh'"

@REM actually deploy 
plink -P 22 -no-antispoof -pw "%pass%" user00@%tkubw2_ip% "cd /mnt/data/tmp_upload_images/tmp_deploy_folder && echo 'Atl@2022' | su -c 'sh _tag_and_push_image.sh'"

REM Get the current date and time and format it as `today`
for /f "skip=1" %%x in ('wmic os get localdatetime') do if not defined MyDate set MyDate=%%x
for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set fmonth=00%Month%
set fday=00%Day%
set today=%Year%-%fmonth:~-2%-%fday:~-2%

REM Move deployed files to a `trash_can` folder on the remote server
set folder_suffix=%fmonth:~-2%%fday:~-2%_%time:~0,2%%time:~3,2%
echo folder_suffix: %folder_suffix%
plink -P 22 -no-antispoof -pw "%pass%" user00@%tkubw2_ip% "cd /mnt/data/tmp_upload_images/ && mv tmp_deploy_folder trash_can/bes_images_%folder_suffix%"

REM Copy a shell script to another remote server and restart the application
pscp  -P 22 -pw "%pass%" "_restart_dmz_app.sh" user00@%ik8s_ip%:/home/user00/
plink -P 22 -no-antispoof -pw "%pass%" user00@%ik8s_ip% "sh /home/user00/_restart_dmz_app.sh"
plink -P 22 -no-antispoof -pw "%pass%" user00@%ik8s_ip% "rm -f /home/user00/_restart_dmz_app.sh"

REM Copy a shell script to a third remote server and restart the application
pscp  -P 22 -pw "%pass%" "_restart_trust_app.sh" user00@%tk8s_ip%:/home/user00/
plink -P 22 -no-antispoof -pw "%pass%" user00@%tk8s_ip% "sh /home/user00/_restart_trust_app.sh"
plink -P 22 -no-antispoof -pw "%pass%" user00@%tk8s_ip% "rm -f /home/user00/_restart_trust_app.sh"

REM Create a folder on the user's desktop and move the deployed files to it
mkdir "%USERPROFILE%\Desktop\trash_can\bes_images_%folder_suffix%"
move "*.zip" "%USERPROFILE%\Desktop\trash_can\bes_images_%folder_suffix%\"
move "*.sh" "%USERPROFILE%\Desktop\trash_can\bes_images_%folder_suffix%\"
move "*.tar" "%USERPROFILE%\Desktop\trash_can\bes_images_%folder_suffix%\"

echo deploy finished, press echo to exit
set /p=
