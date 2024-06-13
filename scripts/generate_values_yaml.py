from asyncore import loop
import re
import os

import yaml
import my_util_func as uf


def get_folder_list(folder: str) -> list[str]:
    folder_list = []
    for f in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, f)):
            folder_list.append(f)
    return folder_list


def format_str_with_dict(str_template: str, dict_data: dict) -> str:
    # flatten dict
    dict_data_flat = {}
    for k, v in dict_data.items():
        if isinstance(v, dict):
            for k1, v1 in v.items():
                dict_data_flat[k + '.' + k1] = v1
        else:
            dict_data_flat[k] = v

    for key, value in dict_data_flat.items():
        value_str = str(value)
        str_template = str_template.replace('{{' + key + '}}', value_str)
    return str_template


def get_yaml_dict(zone_path, app_folder, yaml_file) -> dict:
    # delete file values-allow-client-cert.yaml
    app_values_path = os.path.join(zone_path, app_folder, yaml_file)
    # read yaml to dict
    with open(app_values_path, 'r') as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


def gen_values_yaml(zone_path: str, template_file_path: str, output_file_name: str):
    app_folder_list = get_folder_list(zone_path)

    # loop all app folder in zone_dir
    for app_folder_name in app_folder_list:
        if uf.is_app_skip(env, app_folder_name):
            continue

        # get vars from values.yaml
        vars = get_yaml_dict(zone_path, app_folder_name, 'values.yaml')

        # read template file
        with open(template_path, 'r') as f:
            template_yaml = f.read()

        # fill var into template
        result_yaml = format_str_with_dict(template_yaml, vars)

        # save path
        save_path = os.path.join(zone_path, app_folder_name, output_file_name)

        # ensure save folder existed
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        # save file
        with open(save_path, 'w') as output_file:
            output_file.write(result_yaml)


def get_folder_list_in_k8s_yaml():
    folder_list = []
    for f in os.listdir(K8S_YAML_FOLDER_PATH):
        if os.path.isdir(os.path.join(K8S_YAML_FOLDER_PATH, f)):
            folder_list.append(f)
    return folder_list


def gen_values_yaml_in_all_zone(template_path: str, output_file_name: str):
    zone_folder_list = get_folder_list_in_k8s_yaml()

    # loop all zone folder in k8s_yaml
    for zone_folder in zone_folder_list:
        zone_folder_path = os.path.join(K8S_YAML_FOLDER_PATH, zone_folder)
        gen_values_yaml(zone_folder_path, template_path, output_file_name)


K8S_YAML_FOLDER_PATH = './k8s_yaml'

# env = 'dev'
# template_path = 'scripts/template_value_dev_common.yaml'
# output_file_name = 'values-dev-common.yaml'
# gen_values_yaml_in_all_zone(template_path, output_file_name)

# env = 'stg'
# template_path = 'scripts/template_value_stg_common.yaml'
# output_file_name = 'values-stg-common.yaml'
# gen_values_yaml_in_all_zone(template_path, output_file_name)

# env = 'nonprod'
# template_path = 'scripts/template_value_nonprod_common.yaml'
# output_file_name = 'values-nonprod-common.yaml'
# gen_values_yaml_in_all_zone(template_path, output_file_name)

# env = 'p1'
# template_path = 'scripts/template_value_p1_common.yaml'
# output_file_name = 'values-p1-common.yaml'
# gen_values_yaml_in_all_zone(template_path, output_file_name)

# env = 'p2'
# template_path = 'scripts/template_value_p2_common.yaml'
# output_file_name = 'values-p2-common.yaml'
# gen_values_yaml_in_all_zone(template_path, output_file_name)

# template_path = 'scripts/template_value_nonprod_image_tag.yaml'
# output_file_name = 'values-nonprod-image-tag.yaml'
# gen_values_yaml_in_all_zone(template_path, output_file_name)
