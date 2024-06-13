
import os
import re
import requests
import yaml

# disable verify ssl
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
verify_ssl = False


def is_file_existed(file_path):
    return os.path.exists(file_path)


def ensure_dir_existe(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


def save_to_file(file_path, content):
    ensure_dir_existe(file_path)
    with open(file_path, 'w') as f:
        f.write(content)


def append_to_file(file_path, content):
    with open(file_path, 'a') as f:
        f.write(content)


def get_dict_from_yaml(path: str) -> dict:
    with open(path, 'r') as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


def get_dict_from_app_yaml(zone_path, app_folder, yaml_file) -> dict:
    app_values_path = os.path.join(zone_path, app_folder, yaml_file)
    # read yaml to dict
    with open(app_values_path, 'r') as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


def get_folder_list(folder: str) -> list:
    folder_list = []
    for file_name in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file_name)):
            folder_list.append(file_name)
    return folder_list


def format_str_with_dict(str_template: str, dict_data: dict) -> str:
    for key, value in dict_data.items():
        str_template = str_template.replace('{{' + key + '}}', str(value))
    return str_template


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def read_file_as_string(file_path):
    # read template file
    with open(file_path, 'r') as f:
        template_yaml = f.read()
        return template_yaml


def is_app_skip(env, app_name):    

    if env in ('p1', 'p2'):
        p1_p2_skip_list = [
            'sim-trxn-upload-worker',
            'health-check-api',
            'das-raw-trxn-consumer',
            'das-raw-evid-consumer',
            # 'txv-stat-consumer',
            'notification-result2',
            'toms-middleware',
            'toms-api',
            'toms-auth-api',
            'toms-portal',
            'daily-renew-rsa-cert',
        ]
        return app_name in p1_p2_skip_list

    if env in ('np', 'nonprod'):
        np_skip_list = [
            'health-check-api',
            'toms-middleware',
            'toms-api',
            'toms-auth-api',
            'toms-portal',
            'daily-renew-rsa-cert',
        ]
        return app_name in np_skip_list

    if env == 'stg':
        stg_skip_list = [
            'sim-trxn-upload-worker',
            'das-raw-trxn-consumer',
            'das-raw-evid-consumer',
            'txv-stat-consumer',
            'health-check-api',
            'notification-result2',
            'ccs-scheduler',
        ]
        return app_name in stg_skip_list

    if env == 'dev':
        dev_skip_list = [
            'sim-trxn-upload-worker',
            'notification-result2',
        ]
        return app_name in dev_skip_list
    
    return False
