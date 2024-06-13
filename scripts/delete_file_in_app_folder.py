from asyncore import loop
import re
import os

def get_folder_list(folder: str) -> list[str]:
    folder_list = []
    for f in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, f)):
            folder_list.append(f)
    return folder_list

def delete_file(zone_path: str, delete_file_name: str):
    app_folder_list = get_folder_list(zone_path)

    # loop all app folder in zone_dir
    for app_folder in app_folder_list:
        # delete file values-allow-client-cert.yaml
        app_values_path = os.path.join(zone_path, app_folder, delete_file_name)
        if os.path.exists(app_values_path):
            os.remove(app_values_path)

def delete_file_in_all_zone(delete_file_name: str):
    delete_file('k8s_yaml/bes', delete_file_name)
    delete_file('k8s_yaml/bes-job', delete_file_name)
    delete_file('k8s_yaml/dmz-bes', delete_file_name)
    delete_file('k8s_yaml/toms', delete_file_name)


# delete_file_in_all_zone('values-nonprod-image-repo.yaml')

