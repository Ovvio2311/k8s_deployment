# rollback image version

1. go to nonprod/p1/p2 harbor, pick the image you want to rollback base on "Creation Time", click "RETAG"
   ![](./rollback_image_version_1.png)
2. retag the image as nonprod | p1 | p2
   ![](./rollback_image_version_2.png)
3. restart app in argocd
   ![](./restart_app_in_argocd.png)
