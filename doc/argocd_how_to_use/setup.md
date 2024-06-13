[TOC]

## Installation

[Getting Started - Argo CD - Declarative GitOps CD for Kubernetes (argoproj.github.io)](https://argoproj.github.io/argo-cd/getting_started/)

## Create An Application From A Git Repository

### Prepare GitLab repo
![image-20210423170847761](setup_image/image-20210423170847761.png)

### Connection Repo
![image-20210423163133759](setup_image/image-20210423163133759.png)
![image-20210423164438377](setup_image/image-20210423164438377.png)
![image-20210423164641648](setup_image/image-20210423164641648.png)
![image-20210423164719423](setup_image/image-20210423164719423.png)

### Deploy an app from GitLab repo
![image-20210423165110573](setup_image/image-20210423165110573.png)
![image-20210423165704626](setup_image/image-20210423165704626.png)
![image-20210423170357429](setup_image/image-20210423170357429.png)
![image-20210423170022775](setup_image/image-20210423170022775.png)
![image-20210423170506819](setup_image/image-20210423170506819.png)

### Upgrade image from Nginx 1.14.2 to 1.9
1. Modify deployment.yaml file on GitLab and commit.
   ![image-20210423171607025](setup_image/image-20210423171607025.png)

2. Go to ArgoCD and you will see OutOfSync, click `MORE` will show the commit message we just wrote.
   ![image-20210423171943363](setup_image/image-20210423171943363.png)

3. Click `SYNC` button to sync the app
   ![image-20210423172502947](setup_image/image-20210423172502947.png)

4. SYNC Status will show the latest commit message.
   ![image-20210423174421992](setup_image/image-20210423174421992.png)

   

### Rollback
![image-20210423174323756](setup_image/image-20210423174323756.png)
![image-20210423174606412](setup_image/image-20210423174606412.png)



