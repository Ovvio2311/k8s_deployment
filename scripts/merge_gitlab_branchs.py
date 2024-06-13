import argparse
from dataclasses import dataclass
import sys
import time
import requests
import yaml

# disable insecure request warning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from_branch', metavar='', help='from branch', required=False)
    parser.add_argument('-t', '--to_branch', metavar='', help='to branch', required=False)
    parser.add_argument('-p', '--project_id', metavar='', help='project id, "all" or "227" or "bes/notification/bes_cre_im011_notification_result"', required=False)

    args = parser.parse_args()

    if args.project_id is None:
        print(f'project id cloud be')
        args.project_id = input('Enter project id:')
        if args.project_id is None or args.project_id == '':
            print('project_id cannot be empty')
            sys.exit(1)

    if args.from_branch is None or args.to_branch is None:
        print(f'branch option: [{ALLOWED_BRANCH}]')

    # if args.from_branch is empty, ask user to input from_branch
    if args.from_branch is None:
        args.from_branch = input('Enter from branch: ')

    if args.from_branch not in ALLOWED_BRANCH:
        print('invalid from branch')
        sys.exit(1)

    if args.to_branch is None:
        args.to_branch = input('Enter to branch: ')

    if args.to_branch not in ALLOWED_BRANCH:
        print('invalid to branch')
        sys.exit(1)

    return args


def append_to_file(file_path, content):
    with open(file_path, 'a') as f:
        f.write(content)


def ensure_dir_exists(path):
    import os
    import os.path
    # get dir
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def log(text=''):
    import json
    try:
        pretty_text = json.dumps(text, indent=4, sort_keys=False)
    except:
        pretty_text = text

    print(pretty_text)
    ensure_dir_exists(LOG_PATH)
    append_to_file(LOG_PATH, pretty_text + '\n')


def url_encode_list(project_id_list):
    # loop project id list with index
    for index, project_id in enumerate(project_id_list):
        project_id_list[index] = url_encode(project_id)
    return project_id_list


def url_encode(text: str):
    import urllib.parse
    return urllib.parse.quote_plus(text)


def create_merge_request(project_id, source_branch, target_branch) -> dict:
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests"
    data = {
        'assignee_id': ASSIGN_USER_ID,
        'source_branch': source_branch,
        'target_branch': target_branch,
        'title': f"merge branch from {source_branch} to {target_branch}"
    }

    response = requests.request("POST", url, headers=AUTH_HEADER, data=data, verify=False)
    response_dict = response.json()
    return response_dict


def get_merge_request(project_id, merge_request_iid):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}"
    response = requests.request("GET", url, headers=AUTH_HEADER, verify=False)
    return response.json()


def merge_merge_request(project_id, merge_request_iid, check_count=0):
    merge_status = get_merge_request(project_id, merge_request_iid)['merge_status']

    if check_count > 10:
        log('merge request check count exceeded')
        return close_merge_request(project_id, merge_request_iid)

    if merge_status == 'checking':
        time.sleep(3)
        return merge_merge_request(project_id, merge_request_iid, check_count + 1)

    if merge_status == 'can_be_merged':
        url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/merge"
        data = {
            # 'merge_commit_message': 'merge to stg'
            'squash': False,
            'should_remove_source_branch': False,
            # 'merge_when_pipeline_succeeds': True,
        }
        response = requests.request("PUT", url, headers=AUTH_HEADER, data=data, verify=False)

        # if success, return response.json
        if response.status_code == 200:
            return response.json()

    return close_merge_request(project_id, merge_request_iid)


def close_merge_request(project_id, merge_request_iid):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}"
    data = {'state_event': 'close'}
    response = requests.request("PUT", url, headers=AUTH_HEADER, data=data, verify=False)
    return response.json()


def delete_merge_request(project_id, merge_request_iid):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}"
    response = requests.request("DELETE", url, headers=AUTH_HEADER, verify=False)
    return response.json()


def read_yaml_file(file_path):
    # read yaml file
    with open(file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None


ALLOWED_BRANCH = ['main', 'master', 'dev', 'stg', 'nonprod', 'prod']
LOG_PATH = 'E:\Projects\gitlab_repo\k8s_deployment\logs\log.txt'

GITLAB_URL = 'https://192.168.64.188'
AUTH_HEADER = {'Authorization': 'Bearer N-F4KT4v5rcffJTz6qks'}

ISAAC_USER_ID = 14
ASSIGN_USER_ID = ISAAC_USER_ID


def main():
    args = get_args()
    if args.project_id == 'all':
        project_id_list = read_yaml_file("./scripts/gitlab_project_id_list.yaml")

    if(args.project_id != 'all'):
        project_id_list = [args.project_id]

    project_id_list = url_encode_list(project_id_list)

    for project_id in project_id_list:
        # project_id = urlencode(project_id)

        log('__________________________________________________________')
        merge_request = create_merge_request(project_id, args.from_branch, args.to_branch)
        log(merge_request)

        merge_request_iid = merge_request['iid']

        result = merge_merge_request(project_id, merge_request_iid)
        log('')
        log(result)
        log('__________________________________________________________')


main()
