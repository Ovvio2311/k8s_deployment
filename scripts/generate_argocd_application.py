#!/usr/bin/python
import argparse
import os

import yaml
import my_util_func as uf


def get_yaml_dict(path) -> dict:
    # delete file values-allow-client-cert.yaml
    # read yaml to dict
    with open(path, 'r') as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


def get_folder_list(folder: str) -> list:
    folder_list = []
    for file_name in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file_name)):
            folder_list.append(file_name)
    return folder_list


def get_file_list(folder: str) -> list:
    folder_list = []
    for file_name in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file_name)) == False:
            folder_list.append(file_name)
    return folder_list


def format_str_with_dict(str_template: str, dict_data: dict) -> str:
    for key, value in dict_data.items():
        str_template = str_template.replace('{{' + key + '}}', value)
    return str_template


def gen_argocd_application_yaml(env: str, zone: str):

    zone_path = f"k8s_yaml/{zone}"
    output_path = f"k8s_argocd_yaml/{env}/{zone}/"
    template_path = f"scripts/template_argocd_application_{env}.yaml"

    app_folder_list = get_folder_list(zone_path)
    for app_folder_name in app_folder_list:
        if uf.is_app_skip(env, app_folder_name):
            continue

        if uf.is_file_existed(f"{zone_path}/{app_folder_name}/values.yaml") == False:
            continue

        app_name = app_folder_name

        # prepare vars
        vars = {'app_name': app_name, 'app_folder_name': app_folder_name, 'namespace': NAMESPACE, 'env': env, 'zone_path': zone_path}

        # read template file
        with open(template_path, 'r') as f:
            template_yaml = f.read()

        # fill var into template
        result_yaml = format_str_with_dict(template_yaml, vars)

        # save path
        save_path = os.path.join(output_path, f'argo-{app_name}.yaml')

        # ensure save folder existed
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        # save file
        with open(save_path, 'w') as output_file:
            output_file.write(result_yaml)


def gen_all_zone_argocd_application_yaml(all_env, all_zone):
    # loop env and zone
    for env in all_env:
        for zone in all_zone:

            if zone == 'toms' and env not in ('dev', 'stg'):
                continue

            gen_argocd_application_yaml(env, zone)
            gen_argocd_app_yaml_from_other_values(env, zone)


def gen_argocd_app_yaml_from_other_values(env, zone):
    zone_path = f"k8s_yaml/{zone}"
    output_path = f"k8s_argocd_yaml/{env}/{zone}/"
    template_path = f"scripts/template_argocd_application_{env}.yaml"

    app_folder_list = get_folder_list(zone_path)
    for app_folder_name in app_folder_list:

        if uf.is_file_existed(f"{zone_path}/{app_folder_name}/values-others") == False:
            continue

        others_app_values_files = get_file_list(f"{zone_path}/{app_folder_name}/values-others")

        for app_values_file in others_app_values_files:

            if app_values_file.startswith(f'values-{env}-') == False:
                continue

            with open(f"{zone_path}/{app_folder_name}/values-others/{app_values_file}", 'r') as f:
                app_values_dict = yaml.safe_load(f)

            app_name = app_values_dict['nameOverride']

            # prepare vars
            vars = {'app_name': app_name, 'app_folder_name': app_folder_name, 'namespace': NAMESPACE, 'env': env, 'zone_path': zone_path}

            # read template file
            with open(template_path, 'r') as f:
                template_yaml = f.read()

            # fill var into template
            result_yaml = format_str_with_dict(template_yaml, vars)

            result_yaml_dict = yaml.safe_load(result_yaml)
            result_yaml_dict['spec']['source']['helm']['valueFiles'].append(f"values-others/{app_values_file}")

            # save path
            save_path = os.path.join(output_path, f'argo-{app_name}.yaml')

            # ensure save folder existed
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))

            # save file
            with open(save_path, 'w') as output_file:
                yaml.safe_dump(result_yaml_dict, output_file)
                # output_file.write(result_yaml)


print('start')
NAMESPACE = "bes"

ALLOWED_ENV = ['dev', 'stg', 'nonprod', 'p1', 'p2']
ALLOWED_ZONE = ["bes", 'bes-job', "toms", "dmz-bes"]

gen_all_zone_argocd_application_yaml(ALLOWED_ENV, ALLOWED_ZONE)
