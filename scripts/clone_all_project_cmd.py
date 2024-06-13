from operator import truediv
import requests
import yaml

# disable insecure request warning
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


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


def get_all_project() -> dict:
    url = f"{GITLAB_API_BASE_URL}/groups/bes/projects"
    data = {
        'simple': True,
        'include_subgroups': True,
        'page': 1,
        'per_page': 100
    }

    response = requests.request("GET", url, headers=AUTH_HEADER, data=data, verify=False)
    response_dict = response.json()
    return response_dict


def get_all_package(page) -> dict:
    url = f"{GITLAB_API_BASE_URL}/groups/bes/packages"
    data = {
        # 'simple': True,
        # 'include_subgroups': True,
        'page': page,
        'per_page': 100
    }

    response = requests.request("GET", url, headers=AUTH_HEADER, data=data, verify=False)
    response_dict = response.json()
    return response_dict


def get_all_dll_project_path():
    all_package_list = []
    for i in range(20):
        page = i
        package_list = get_all_package(page)
        all_package_list.extend(package_list)

    # extract project path list    
    project_path_map = map(lambda p: p['project_path'], all_package_list)
    project_path_list = list(project_path_map)

    # remove duplicated value
    project_path_list = list(dict.fromkeys(list(project_path_list)))

    return project_path_list


GITLAB_API_BASE_URL = "https://192.168.64.188/api/v4"
AUTH_HEADER = {'Authorization': 'Bearer N-F4KT4v5rcffJTz6qks'}

project_id_list = read_yaml_file("scripts/gitlab_project_id_list.yaml")
# project_id_list = url_encode_list(project_id_list)

# project_list = get_all_project()

# loop project id list
for project_id in project_id_list:
    project_name = project_id.split('/')[-1]
    git_url = f"https://192.168.64.188/{project_id}.git"
    # print(f'git clone {git_url}')
    # print(f'git -C ./{project_name} checkout master')
    # print(f'git -C ./{project_name} checkout dev')
    # print(f'git -C ./{project_name} checkout stg')
    print(f'git -C ./{project_name} pull')
    # print(f'git -C ./{project_name} reset --hard HEAD')

    # print(f'dotnet clean .\{project_name}\{project_name}.csproj')
    # print(f'dotnet build .\{project_name}\{project_name}.csproj --force')
    # print(f'dotnet.exe build ./{project_name}/{project_name}.csproj --force | grep Error')

    # print(f'git -C ./{project_name} pull')
    # print(f'git -C ./{project_name} add --all')
    # print(f'git -C ./{project_name} commit -m "remove non used https appsettings"')
    # print(f'git -C ./{project_name} push')

# project_path_list = get_all_dll_project_path()
# print(project_path_list)
