#!/usr/bin/python

import os
from distutils.dir_util import copy_tree


def get_zone_path(zone):
    return f'k8s_yaml/{zone}/'


def get_folder_list(folder):
    folder_list = []
    for f in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, f)):
            folder_list.append(f)
    return folder_list


def copy_web_api_helm_template_to_apps_in_zone(zone, chart):

    template_path = f'helm_charts_example/{chart}/templates'
    zone_path = get_zone_path(zone)
    app_folder_list = get_folder_list(zone_path)

    for app_folder in app_folder_list:
        # if app_folder existed in skip_list
        if app_folder in skip_list:
            continue
        app_path = os.path.join(zone_path, app_folder)
        copy_tree(template_path, app_path + '/templates')


# skip not dotnet (web-api or worker-service)
# secondocr-webapi is python
skip_list = ['secondocr-webapi', 'daily-renew-rsa-cert', 'health-check-api', 'sim-trxn-upload-worker']

# only for web api
# chart='dotnet_web_api'
# copy_web_api_helm_template_to_apps_in_zone('dmz-bes', chart)
# copy_web_api_helm_template_to_apps_in_zone('bes',chart)
# copy_web_api_helm_template_to_apps_in_zone('toms',chart)

# job do not use web api template
# chart='dotnet_cron_job'
# copy_web_api_helm_template_to_apps_in_zone('bes-job',chart)