import argparse
from dataclasses import dataclass
import json
import sys
import time
import requests
import yaml

# disable insecure request warning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def get_all_project() -> dict:
    url = f"{GITLAB_URL}/api/v4/groups/{GITLAB_GROUP}/projects"
    data = {
        'simple': 'true',
        'include_subgroups': 'true'
    }

    response = requests.request("GET", url, headers=AUTH_HEADER, data=data, verify=False)
    response_dict = response.json()
    return response_dict


def get_project_pipelines(project_id, status) -> dict:
    url = f"{GITLAB_URL}/api/v4//projects/{project_id}/pipelines"
    data = {
        # created, waiting_for_resource, preparing, pending, running, success, failed, canceled, skipped, manual, scheduled
        'status': status
    }
    response = requests.request("GET", url, headers=AUTH_HEADER, data=data, verify=False)
    pipeline_list = response.json()
    return pipeline_list


def get_non_finished_pipelines() -> dict:
    project_list = get_all_project()
    non_finished_pipelines_list = []
    # loop project id list
    for project in project_list:
        project_id = project['id']

        non_finished_pipelines_list.extend(get_project_pipelines(project_id, 'created'))
        non_finished_pipelines_list.extend(get_project_pipelines(project_id, 'waiting_for_resource'))
        non_finished_pipelines_list.extend(get_project_pipelines(project_id, 'preparing'))
        non_finished_pipelines_list.extend(get_project_pipelines(project_id, 'pending'))
        non_finished_pipelines_list.extend(get_project_pipelines(project_id, 'running'))

    return non_finished_pipelines_list


GITLAB_URL = 'https://192.168.64.188'
GITLAB_GROUP = 'bes'
AUTH_HEADER = {'Authorization': 'Bearer N-F4KT4v5rcffJTz6qks'}

non_finished_pipelines = get_non_finished_pipelines()
print(json.dumps(non_finished_pipelines, indent=4, sort_keys=True))
