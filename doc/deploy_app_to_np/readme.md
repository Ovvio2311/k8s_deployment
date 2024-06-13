# deploy app to nonprod

1. open scripts file `print_docker_image_command.py`, uncomment apps you want to deploy
   ![](print_docker_image_command_py.png)
2. execute script in folder `k8s_deployment`, select env you want to deploy
   ![](print_docker_image_command_py_2.png)
3. it should create some files in folder `k8s_deployment/deploy_image_cmd_file`
   ![](print_docker_image_command_py_3.png)
4. connect Forti VPN 
5. double click batch script `__xx_deploy.bat`
   ![](deploy_bat.png)
