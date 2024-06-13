import argparse
import json
import sys
import requests
import yaml

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project_id', help='project id, "all" or "227" or "bes/notification/bes_cre_im011_notification_result"', required=False)

    args = parser.parse_args()

    if args.project_id is None:
        print(f'project id cloud be "all" or "227" or "bes/notification/bes_cre_im011_notification_result"')
        args.project_id = input('Enter project id:')
        if args.project_id is None or args.project_id == '':
            print('project_id cannot be empty')
            sys.exit(1)

    return args


def is_branch_existed(project_id, branch_name):
    """
    判断分支是否存在
    :return:
    """
    url = f'{GITLAB_API_BASE_URL}/projects/{project_id}/repository/branches/{branch_name}'

    # call url with auth token and get response skip tls verify
    response = requests.get(url, headers=http_headers, verify=False)
    if response.status_code == 200:
        # print(f'Branch {branch_name} existed')
        return True
    elif response.status_code == 404:
        return False
    else:
        # throw exception unexpected response
        raise Exception(f'Unexpected response: {response.status_code}')


def create_branch(project_id, new_branch_name, base_branch_name):
    """
    创建分支
    :return:
    """

    url = f'{GITLAB_API_BASE_URL}/projects/{project_id}/repository/branches'
    # post data to create branch
    data = {
        'id': project_id,
        'branch': new_branch_name,
        'ref': base_branch_name
    }
    # call url with auth token and get response
    response = requests.post(url, headers=http_headers, json=data, verify=False)
    if response.status_code == 201:
        decoded_project_id = project_id.replace('%2F', '/')
        print(f'{decoded_project_id} Create branch {new_branch_name} success')
        return True
    elif response.status_code == 400:
        return False
    else:
        # throw exception unexpected response
        raise Exception(f'url: {url}, Unexpected response: {response.status_code}')


def create_stg_branch_if_not_existed(project_id_list):
    # loop project id list
    for project_id in project_id_list:
        # if branch not existed, create it
        if not is_branch_existed(project_id=project_id, branch_name='stg'):
            is_success = create_branch(project_id=project_id, new_branch_name='stg', base_branch_name='dev')
            if not is_success:
                create_branch(project_id=project_id, new_branch_name='stg', base_branch_name='master')


def create_nonprod_branch_if_not_existed(project_id_list):
    # loop project id list
    for project_id in project_id_list:
        # if branch not existed, create it
        if not is_branch_existed(project_id=project_id, branch_name='nonprod'):
            is_success = create_branch(project_id=project_id, new_branch_name='nonprod', base_branch_name='stg')


def create_branch_if_not_existed(project_id_list, new_branch_name, base_branch_name):
    # loop project id list
    for project_id in project_id_list:
        # if branch not existed, create it
        if not is_branch_existed(project_id, new_branch_name):
            is_success = create_branch(project_id, new_branch_name, base_branch_name)


def unprotect_branch_for_all_project(project_id_list, branch_name):
    # loop project id list
    for project_id in project_id_list:
        unprotect_branch_for_project(project_id, branch_name)


def unprotect_branch_for_project(project_id, branch_name):
    url = f'{GITLAB_API_BASE_URL}/projects/{project_id}/protected_branches/{branch_name}'

    response = requests.delete(url, headers=http_headers, verify=False)
    if response.status_code == 204:
        return
        # print(f'Unprotect {project_id} branch {branch_name} success')
    else:
        return
        # print(f'Unprotect {project_id} branch {branch_name} response code: {response.status_code}, response: {response.text}')


def protect_branch_for_all_project(project_id_list, branch_name, push_access_level=40, merge_access_level=40):
    """
    Access Levels: 
    - MAINTAINERS_ONLY = 40
    - MAINTAINERS_AND_DEVELOPERS = 30
    - NO_ONE = 0
    """

    # loop project id list
    for project_id in project_id_list:
        if not is_branch_existed(project_id=project_id, branch_name=branch_name):
            continue

        unprotect_branch_for_project(project_id, branch_name)

        url = f'{GITLAB_API_BASE_URL}/projects/{project_id}/protected_branches'
        data = {
            'id': project_id,
            'name': branch_name,
            'push_access_level': push_access_level,
            'merge_access_level': merge_access_level
        }
        response = requests.post(url, headers=http_headers, json=data, verify=False)
        if response.status_code == 201:
            print(f'{project_id} Protect branch {branch_name} success, push_access_level: {push_access_level}, merge_access_level: {merge_access_level}')
        elif response.status_code == 409:
            print(f'{project_id} Protect branch {branch_name} already exist')
        else:
            print(f'{project_id} Protect branch {branch_name} Unexpected response: {response.status_code}, response: {response.text}')


def change_branch_protect_level(project_id_list, branch_name, push_access_level=40, merge_access_level=40):
    """
    Access Levels: 
    - MAINTAINERS_ONLY = 40
    - MAINTAINERS_AND_DEVELOPERS = 30
    - NO_ONE = 0
    """
    unprotect_branch_for_all_project(project_id_list, branch_name)
    protect_branch_for_all_project(project_id_list, branch_name, push_access_level, merge_access_level)


def url_encode_list(project_id_list):
    # loop project id list with index
    for index, project_id in enumerate(project_id_list):
        project_id_list[index] = url_encode(project_id)
    return project_id_list


def url_encode(text: str):
    import urllib.parse
    return urllib.parse.quote_plus(text)


def read_yaml_file(file_path):
    # read yaml file
    with open(file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None


GITLAB_TOKEN = 'N-F4KT4v5rcffJTz6qks'
GITLAB_API_BASE_URL = "https://192.168.64.188/api/v4"

http_headers = {}
http_headers['Authorization'] = 'Bearer ' + GITLAB_TOKEN


def main():
    print('start')
    args = get_args()
    if args.project_id == 'all':
        project_id_list = read_yaml_file("./scripts/gitlab_project_id_list.yaml")

    if(args.project_id != 'all'):
        project_id_list = [args.project_id]

    project_id_list = url_encode_list(project_id_list)

##########################################################
    create_stg_branch_if_not_existed(project_id_list)
    # create_nonprod_branch_if_not_existed(project_id_list)

    # create_branch_if_not_existed(project_id_list, 'p1', 'nonprod')
    # create_branch_if_not_existed(project_id_list, 'p2', 'nonprod')
##########################################################
    MAINTAINERS_ONLY = 40
    MAINTAINERS_AND_DEVELOPERS = 30
    NO_ONE = 0
    # protect_branch_for_all_project(project_id_list, 'p1', NO_ONE, MAINTAINERS_ONLY)
    # protect_branch_for_all_project(project_id_list, 'p2', NO_ONE, MAINTAINERS_ONLY)
    # protect_branch_for_all_project(project_id_list, 'nonprod', NO_ONE, MAINTAINERS_ONLY)
    protect_branch_for_all_project(project_id_list, 'stg', MAINTAINERS_ONLY, MAINTAINERS_ONLY)
    # protect_branch_for_all_project(project_id_list, 'dev', MAINTAINERS_AND_DEVELOPERS, MAINTAINERS_AND_DEVELOPERS)
##########################################################


main()
