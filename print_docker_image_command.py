from ast import For
from operator import truediv
import re
import os
import shutil
import requests
import yaml
import datetime
import subprocess
import my_util_func as uf
# --------------------------------------------------
# until function
# --------------------------------------------------

from colorama import Fore, Back, Style


def print_warn(message):
    print(f"{Back.MAGENTA}{Fore.WHITE} Warning {Style.RESET_ALL}: {message}")


def print_error(message):
    print(f"{Back.RED}{Fore.WHITE} Warning {Style.RESET_ALL}: {message}")


def get_yaml_dict(zone_path, app_folder, yaml_file) -> dict:
    # delete file values-allow-client-cert.yaml
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
        str_template = str_template.replace('{{' + key + '}}', value)
    return str_template


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# --------------------------------------------------
# end until function
# --------------------------------------------------


def loop_all_app(action_func, deploy_env):
    all_app_data_list = []
    zone_folder_list = get_folder_list("k8s_yaml")
    # loop all zone folder
    for zone_folder in zone_folder_list:
        app_data_list = loop_app_folder_in_zone(action_func, zone_folder, deploy_env)
        all_app_data_list.append(app_data_list)
    return all_app_data_list


def loop_app_folder_in_zone(action_func, zone_folder: str, deploy_env: str):
    zone_path = os.path.join('k8s_yaml', zone_folder)
    app_folder_list = get_folder_list(zone_path)
    app_data_list = []

    # sort app_folder by alphabet
    app_folder_list.sort()

    # loop all app folder in zone_dir
    for app_folder in app_folder_list:
        app_folder_path = os.path.join(zone_path, app_folder)

        if skip_app_list != None and len(skip_app_list) > 0:
            if app_folder in skip_app_list:
                continue

        if uf.is_app_skip(deploy_env, app_folder):
            continue

        # my_app_list is not none and length greater than 1
        if my_app_list != None and len(my_app_list) > 0:
            if app_folder not in my_app_list:
                continue

        value_file_path = os.path.join(app_folder_path, f'values-{deploy_env}-common.yaml')
        if not os.path.exists(value_file_path):
            print_warn(f"{app_folder} don't have a value file, skiped, {value_file_path}.")
            continue

        data = get_data_from_app_folder(app_folder_path, zone_folder, deploy_env)
        action_func(data)
        app_data_list.append(data)
    return app_data_list


def get_data_from_app_folder(app_folder_path, zone_folder, deploy_env):
    # try:
    #   dev_registry = get_yaml_dict(app_folder_path, 'values-tspdev-common.yaml')['image']['registry']
    # except:
    #   dev_registry = get_yaml_dict(app_folder_path, 'values.yaml')['image']['registryf']

    # stg_registry = get_yaml_dict(app_folder_path, 'values-stg-common.yaml')['image']['registry']
    # stg_tag = get_yaml_dict(app_folder_path, 'values-stg-image-tag.yaml')['image']['tag']

    dev_tag = get_yaml_dict(app_folder_path, 'values.yaml')['image']['tag']
    deploy_registry = get_yaml_dict(app_folder_path, f'values-{deploy_env}-common.yaml')['image']['registry']

    if deploy_env == 'nonprod':
        deploy_tag = 'nonprod'
    else:
        deploy_tag = get_yaml_dict(app_folder_path, f'values-{deploy_env}-image-tag.yaml')['image']['tag']

    repo = get_yaml_dict(app_folder_path, 'values.yaml')['image']['repository']
    app_name = get_yaml_dict(app_folder_path, 'values.yaml')['fullnameOverride']

    # split by / and get last one
    image_name = repo.split('/')[-1]

    other_app_names = []

    other_app_folder_path = os.path.join(app_folder_path, 'values-others')
    if uf.is_file_existed(other_app_folder_path):
        other_app_value_paths = os.listdir(other_app_folder_path)
        for value_path in other_app_value_paths:
            if value_path.startswith(f'values-{deploy_env}-'):
                other_app_name = get_yaml_dict(other_app_folder_path, value_path)['fullnameOverride']
                other_app_names.append(other_app_name)

    data = {
        # "source_registry": stg_registry,
        # "source_tag": stg_tag,

        # "source_registry": "172.24.150.130:8083",
        # "source_tag": "nonprod",

        "source_registry": "192.168.64.186",
        "source_tag": dev_tag,

        "deploy_registry": deploy_registry,
        "deploy_tag": deploy_tag,
        "repo": repo,
        "zone_folder": zone_folder,
        "app_name": app_name,
        "image_name": image_name,
        "other_app_names": other_app_names
    }

    return data


def print_cmd(cmd='', end_with_new_line=True):
    # print(cmd)
    if (cmd != ''):
        # get dir from file path
        dir = os.path.dirname(cmd_file_path)
        # ensure dir exists
        if not os.path.exists(dir):
            os.makedirs(dir)

        # append to file with linux new line
        with open(cmd_file_path, 'a', newline='\n') as f:
            if end_with_new_line:
                f.write(cmd + '\n')
            else:
                f.write(cmd)


def get_yaml_dict(app_folder_path, yaml_file) -> dict:
    app_values_path = os.path.join(app_folder_path, yaml_file)
    # read yaml to dict
    with open(app_values_path, 'r') as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


def print_docker_untag_command(data) -> str:
    deploy_repo = f'{data["source_registry"]}/{data["repo"]}:{data["source_tag"]}'
    cmd = f'docker image rm {deploy_repo}'
    print_cmd(cmd)
    return cmd


def print_docker_pull_command(data) -> str:
    deploy_repo = f'{data["source_registry"]}/{data["repo"]}:{data["source_tag"]}'
    cmd = f'docker pull {deploy_repo}'
    print_cmd(cmd)
    return cmd


def print_docker_tag_rm_registry_command(data) -> str:
    # remove registry
    deploy_repo = f'{data["source_registry"]}/{data["repo"]}:{data["source_tag"]}'
    deploy_repo_with_no_reg = f'{data["repo"]}:{data["source_tag"]}'
    cmd = f'docker tag {deploy_repo} {deploy_repo_with_no_reg}'
    print_cmd(cmd)
    return cmd


def print_docker_save_command(data) -> str:
    deploy_repo_with_no_reg = f'{data["repo"]}:{data["source_tag"]}'
    deploy_tag = data["source_tag"]
    image_name = data['image_name']

    # if save multi image, use this new command can make file smeller
    # docker save $(docker images --filter=reference='bes/*:nonprod-*' --format '{{.Repository}}:{{.Tag}}') -o all_bes_nonprod_images_20220626.tar
    # cmd = f'docker save -o "{image_name}_{deploy_tag}.tar" "{deploy_repo_with_no_reg}"'
    cmd = f' "{deploy_repo_with_no_reg}" '
    print_cmd(cmd, end_with_new_line=False)
    return cmd


def print_zip_command(data) -> str:
    deploy_tag = data["source_tag"]
    image_name = data['image_name']

    cmd = f'zip "{image_name}_{deploy_tag}.zip" "{image_name}_{deploy_tag}.tar"'
    # cmd = f'Compress-Archive "{OUTPUT_FOLDER}/{image_name}_{deploy_tag}.tar" "{OUTPUT_FOLDER}\{image_name}_{deploy_tag}.zip"'
    print_cmd(cmd)
    return cmd


def print_unzip_command(data) -> str:
    deploy_tag = data["source_tag"]
    image_name = data['image_name']

    # unzip -o means overwrite
    # cmd = f'unzip -o "{image_name}_{deploy_tag}.zip"'

    # unzip -n means never overwrite
    cmd = f'unzip -n "{image_name}_{deploy_tag}.zip"'
    print_cmd(cmd)
    return cmd


def print_docker_load_command(data) -> str:
    deploy_tag = data["source_tag"]
    image_name = data['image_name']
    cmd = f'docker load --input "{image_name}_{deploy_tag}.tar"'
    print_cmd(cmd)
    return cmd


def print_docker_tag_command(data) -> str:
    source_tag = f'{data["source_tag"]}'
    deploy_tag = f'{data["deploy_tag"]}'
    repo = data["repo"]
    registry = data["deploy_registry"]

    cmd = f'docker tag "{repo}:{source_tag}" "{repo}:{deploy_tag}"'
    print_cmd(cmd)

    cmd = f'docker tag "{repo}:{source_tag}" "{registry}/{repo}:{deploy_tag}"'
    print_cmd(cmd)

    source_registry = data["source_registry"]
    source_tag = data["source_tag"]
    harbor_project_name = data["repo"].split('/')[0]
    image_name = data["image_name"]
    tag_list = get_all_source_tag_list_from_harbor(source_registry, source_tag, harbor_project_name, image_name)
    for tag_name in tag_list:
        cmd = f'docker tag "{repo}:{source_tag}" "{registry}/{repo}:{tag_name}"'
        print_cmd(cmd)
    return cmd


def get_all_source_tag_list_from_harbor(source_registry, source_tag, harbor_project_name, image_name):
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    verify_ssl = False

    url = f"https://{source_registry}/api/v2.0/projects/{harbor_project_name}/repositories/{image_name}/artifacts/{source_tag}/tags?page=1&page_size=10"

    response = requests.get(url, verify=False)
    if response.status_code != 200:
        return [source_tag]

    tag_detail_list = response.json()
    tag_name_list = map(lambda x:  x.get("name"), tag_detail_list)
    tag_name_list = filter(lambda name: name != 'latest', tag_name_list)

    return tag_name_list


def print_docker_push_command(data) -> str:
    repo = data["repo"]
    registry = data["deploy_registry"]
    cmd = f'docker push {registry}/{repo} --all-tags'
    print_cmd(cmd)
    return cmd


def print_restart_trust_app(data) -> str:
    zone_folder = data["zone_folder"]
    app_name = data["app_name"]
    if zone_folder == "bes":
        # f"argocd app actions run {app_name} restart --kind Deployment"
        print_cmd(f"kubectl rollout restart deploy -n bes {app_name}")

        for other_app_name in data['other_app_names']:
            print_cmd(f"kubectl rollout restart deploy -n bes {other_app_name}")


def print_restart_dmz_app(data) -> str:
    zone_folder = data["zone_folder"]
    app_name = data["app_name"]
    if zone_folder == "dmz-bes":
        # f"argocd app actions run {app_name} restart --kind Deployment"
        print_cmd(f"kubectl rollout restart deploy -n bes {app_name}")
        for other_app_name in data['other_app_names']:
            print_cmd(f"kubectl rollout restart deploy -n bes {other_app_name}")


def print_echo_done():
    print_cmd('echo done')


# if not specify my_app_list, loop all app in zone_dir
my_app_list = [
    # "accmgt-api",
    # "auth-api",
    # "auto-payment-scheduler",
    # "bes-acc-im001-fft-account-registration",
    # "bes-acc-im002-fft-vehicle-management",
    # "bes-acc-im003-fft-vehicle-group-management",
    # "bes-acc-im004-fft-account-search",
    # "bes-acc-im005-fft-driver-approval",
    # "bes-acc-im006-fft-account-management",
    # "bes-acc-im007-fft-vehicle-pairing",
    # "bes-acc-im008-fft-tag-management",
    # "bes-acc-im009-fft-payment-and-billing",
    # "bes-acc-im010-fft-transaction",
    # "bes-acc-im011-ffts-toll-and-surcharge",
    # "bes-acc-im012-ffts-account-history",
    # "bes-acc-im013-ffts-performance-monitoring",
    # "bes-cre-im001-tokenization",
    # "bes-cre-im002-otp",
    # "bes-cre-im007-notification-template-management",
    # "bes-cre-im008-notification-message-management",
    # "bes-cre-im009-notification-processor",
    # "bes-cre-im010-shortlink",
    # "bes-notification-pulsar-consumer-services",
    # "bes-notification-push-app-services",
    # "bes-notification-push-email-services",
    # "bes-notification-push-sms-services",
    # "bes-notification-push-app-services-2",
    # "bes-notification-push-email-services-2",
    # "bes-notification-push-sms-services-2",
    # "bes-send-schedule-notification-services",
    # "ccms-api",
    # "ccs-api",
    # "central-db-services-accmgt",
    # "central-db-services-ccms",
    # "central-db-services-core"
    # "central-db-services-ecms",
    # "centraldbservices-das",
    # "das-evid-api",
    # "das-evidence-record-consumer",
    # "das-imageobj-consumer",
    # "das-raw-evid-consumer",
    # "das-raw-trxn-consumer",
    # "das-transaction-record-consumer",
    # "ecms-api",
    # "health-check-api",
    # "mariadb-data-collector",
    # "mariadb-metric-collector",
    # "notification-api",
    # "s3-api",
    # "secondocr-webapi",
    # "sim-trxn-upload-worker",
    # "tx-validation",
    # "txv-process-consumer",
    # "txv-stat-consumer",
    # "validv-api"
    # ---------------------------------------------
    # ------------------bes-job--------------------
    # ---------------------------------------------
    # "auto-issue-suspend-fsn",
    # "bes-s3objectstorage-archive-bucket",
    # "bes-schedule-account-idle",
    # "bes-schedule-ftoken-phone-whitelist",
    # "bes-schedule-account-idle-reminder",
    # "bes-schedule-driver-approval-pairing-expiry",
    # "bes-schedule-monthly-statement-notice",
    # "bes-schedule-payment-reminder",
    # "bes-schedule-remove-vehicle-data-for-tt-trxn",
    # "bes-schedule-autopay-dsva-outstanding-trxn"
    # "das-missing-data-schedule",
    # "das-pairing-data-purger",
    # "ecms-surcharge-notice-generation",
    # "generate-issued-surcharge",
    # "restart-app-multi-cronjobs",
    # "pair-das-data-schedule",
    # "repost-mir"
    # "sim-trxn-upload-worker",
    # "trigger-das-mid-idaa11-bes-status-upload",
    # "bes-schedule-email-trxn-csv",
    # "trigger-tx-valid-ia007-repost-unpaired",
    # ---------------------------------------------
    # ------------------dmz-bes--------------------
    # ---------------------------------------------
    # "bes-ccs",
    # "bes-psp"
    # "bes-signalr-server",
    # "bes-tsp",
    # "bes-ttis",
    # "bes-wmm",
    # "bes-wmm2",
    # "bescore-portal",
    # "ccms-portal",
    # "ccs-middleware",
    # "ccs-scheduler",
    # "das-middleware",
     "ecms-portal"
    # "ffts-web",
    # "mongo-house-keeping",
    # "notification-result",
    # "notification-result2",
    # "validv-middleware",
    #  "tids-scheduler"
    # ---------------------------------------------
    # ------------------toms----------------------
    # ---------------------------------------------
]


skip_app_list = [
    "secondocr-webapi",
]
print_warn(f"skiped app: {skip_app_list}")

ALLOWED_ENV = ['nonprod', 'p1', 'p2']
deploy_env = input('Enter deploy_env id (np | p1 | p2):')
if deploy_env == 'np':
    deploy_env = 'nonprod'

CMD_OUTPUT_FOLDER = './deploy_image_cmd_file'
# create dir if not existed
if not os.path.exists(CMD_OUTPUT_FOLDER):
    os.makedirs(CMD_OUTPUT_FOLDER)

# delete old files
for f in os.listdir(CMD_OUTPUT_FOLDER):
    if (f in ['_pack_deploy_images_cmd.bat', '_restart_dmz_app.sh', '_restart_trust_app.sh', '_tag_and_push_image.sh', '_unpack_deploy_images_cmd.sh']):
        os.remove(os.path.join(CMD_OUTPUT_FOLDER, f))
    if (f.endswith('.zip')):
        os.remove(os.path.join(CMD_OUTPUT_FOLDER, f))
    # if f.endswith('.bat') or f.endswith('.sh'):
    #     os.remove(os.path.join(CMD_OUTPUT_FOLDER, f))


# generate command batch file
file_suffix = f'{deploy_env}_{datetime.datetime.now().strftime("%m%d_%H%M")}'

cmd_file_path = os.path.join(CMD_OUTPUT_FOLDER, '_pack_deploy_images_cmd.bat')
# print_cmd(f'\n')
# print_cmd('for /f %i IN (\'curl -X GET --insecure -s --write-out %{http_code} "https://' + SOURCE_REGISTRY + '/api/v2.0/health" --output "output.txt"\') DO set http_code=%i')
# print_cmd('if not %http_code%==200 exit')

print_cmd("if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )")
loop_all_app(print_docker_untag_command, deploy_env)
loop_all_app(print_docker_pull_command, deploy_env)
loop_all_app(print_docker_tag_rm_registry_command, deploy_env)

print_cmd(f'docker save -o "deploy_images_{file_suffix}.tar" ', end_with_new_line=False)
loop_all_app(print_docker_save_command, deploy_env)

print_cmd(f'\n')
print_cmd(f'timeout /t 2')
print_cmd(f'zip "deploy_images_{file_suffix}.zip" "deploy_images_{file_suffix}.tar" ')
print_cmd(f'recycle "deploy_images_{file_suffix}.tar" ')
# loop_all_app(print_zip_command, deploy_env)
print_echo_done()

cmd_file_path = os.path.join(CMD_OUTPUT_FOLDER, '_unpack_deploy_images_cmd.sh')
print_cmd(f'unzip -n "deploy_images_{file_suffix}.zip"')
print_cmd(f'docker load --input "deploy_images_{file_suffix}.tar"')
# loop_all_app(print_unzip_command, deploy_env)
# loop_all_app(print_docker_load_command, deploy_env)
print_echo_done()

cmd_file_path = os.path.join(CMD_OUTPUT_FOLDER, f'_tag_and_push_image.sh')
loop_all_app(print_docker_tag_command, deploy_env)
loop_all_app(print_docker_push_command, deploy_env)
print_echo_done()

cmd_file_path = os.path.join(CMD_OUTPUT_FOLDER, f'_restart_trust_app.sh')
loop_all_app(print_restart_trust_app, deploy_env)
print_echo_done()

cmd_file_path = os.path.join(CMD_OUTPUT_FOLDER, f'_restart_dmz_app.sh')
loop_all_app(print_restart_dmz_app, deploy_env)
print_echo_done()

os.chdir("deploy_image_cmd_file")
os.startfile("_pack_deploy_images_cmd.bat")

# delete_file(f'deploy_images_{file_suffix}.tar')
