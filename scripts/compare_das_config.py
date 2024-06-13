import re
import os
import yaml
import my_util_func as uf
from deepdiff import DeepDiff
from prettytable import PrettyTable
import csv
from urllib.parse import parse_qs

all_app_folder_paths = {}


def get_app_folder_path(app):
    if len(all_app_folder_paths.keys()) == 0:
        temp_list = []
        zone_folde_list = ['k8s_yaml/bes', 'k8s_yaml/bes-job', 'k8s_yaml/dmz-bes']
        for zone_folder in zone_folde_list:
            app_folder_list = uf.get_folder_list(zone_folder)
            for app_folder in app_folder_list:
                all_app_folder_paths[app_folder] = os.path.join(zone_folder, app_folder)
    return all_app_folder_paths[app]


def sort_dict_by_key(d):
    return dict(sorted(d.items()))


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def export_diff_csv_2(app, dict_1, dict_2, filename, same_key):
    dict_1 = sort_dict_by_key(flatten_dict(dict_1))
    dict_2 = sort_dict_by_key(flatten_dict(dict_2))
    with open(filename, 'a', newline='') as csvfile:

        fieldnames = ['app', same_key, 'config',  'changed', dict_1['diff_field'] + '_value', dict_2['diff_field'] + '_value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        global header_wrote
        if header_wrote == False:
            writer.writeheader()
            header_wrote = True

        sorted_keys = sorted(set(dict_1.keys()) | set(dict_2.keys()))
        for key in sorted_keys:
            if key in ['env', 'tunnel', 'diff_field', 'fullnameOverride', 'service_enabled', 'service_type', 'service_httpNodePort', 'service_httpsNodePort',
                       'config_Serilog__WriteTo__0__Args__configureLogger__WriteTo__0__Args__indexFormat']:
                continue

            config = key
            v1 = dict_1.get(key, '')
            v2 = dict_2.get(key, '')

            v1_db_server = ''
            v2_db_server = ''
            if key == 'config_MySQL__ConnectionString':
                config = 'Databse'
                if v1 != '':
                    conn_dict = parse_qs(v1.replace(';', '&'))
                    conn_dict = parse_qs(v1.replace(';', '&'))
                    v1 = conn_dict.get('Database', [''])[0]
                    v1_db_server = conn_dict.get('server', [''])[0]
                if v2 != '':
                    conn_dict = parse_qs(v2.replace(';', '&'))
                    v2 = conn_dict.get('Database', [''])[0]
                    v2_db_server = conn_dict.get('server', [''])[0]
                
                changed = v1 != v2
                writer.writerow({
                    fieldnames[0]: app,
                    fieldnames[1]: dict_1.get(same_key, ''),
                    fieldnames[2]: 'Database_server',
                    fieldnames[3]: changed,
                    fieldnames[4]: v1_db_server,
                    fieldnames[5]: v2_db_server
                })

            changed = v1 != v2
            writer.writerow({
                fieldnames[0]: app,
                fieldnames[1]: dict_1.get(same_key, ''),
                fieldnames[2]: config,
                fieldnames[3]: changed,
                fieldnames[4]: v1,
                fieldnames[5]: v2
            })
    print(f"Dictionaries exported to {filename}.")

header_wrote = False
def export_diff_csv(app, dict_1, dict_2, filename):
    diff = DeepDiff(dict_1, dict_2, ignore_order=True, verbose_level=2)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['App', 'Config', 'Added/Changed/Deleted', dict_1['diff_field'], dict_2['diff_field']]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        global header_wrote
        if header_wrote == False:
            writer.writeheader()
            header_wrote = True

        for status, val in diff.items():
            if status == "iterable_item_added":
                for key in val:
                    writer.writerow({'App': app, 'Config': key, 'Added/Changed/Deleted': 'Added', dict_1['diff_field']: '-', dict_2['diff_field']: val[key]['value']})
            elif status == "iterable_item_removed":
                for key in val:
                    writer.writerow({'App': app, 'Config': key, 'Added/Changed/Deleted': 'Deleted', dict_1['diff_field']: val[key]['value'], dict_2['diff_field']: '-'})
            elif status == "values_changed":
                for key in val:
                    if key == "root['diff_field']":
                        break
                    writer.writerow({'App': app, 'Config': key, 'Added/Changed/Deleted': 'Changed',
                                    dict_1['diff_field']: val[key]['old_value'], dict_2['diff_field']: val[key]['new_value']})
    print(f"Differences exported to {filename}.")


def compare_env(tunnel, source_env, dest_env, app):
    app_folder_path = get_app_folder_path(app)
    if app == 'das-middleware':
        source_yaml_file = os.path.join(app_folder_path, 'values-others', f'values-{source_env}-{tunnel}-app-settings.yaml')
        dest_yaml_file = os.path.join(app_folder_path, 'values-others', f'values-{dest_env}-{tunnel}-app-settings.yaml')
    else:
        source_yaml_file = os.path.join(app_folder_path, 'values-others', f'values-{source_env}-{tunnel}.yaml')
        dest_yaml_file = os.path.join(app_folder_path, 'values-others', f'values-{dest_env}-{tunnel}.yaml')

    source_dict = uf.get_dict_from_yaml(source_yaml_file)
    dest_dict = uf.get_dict_from_yaml(dest_yaml_file)

    source_dict['diff_field'] = source_env
    dest_dict['diff_field'] = dest_env

    source_dict['tunnel'] = tunnel
    dest_dict['tunnel'] = tunnel

    source_dict['env'] = source_env
    dest_dict['env'] = dest_env

    # export_diff_csv(app, source_dict, dest_dict, 'env_diff.csv')

    export_diff_csv_2(app,  source_dict, dest_dict, 'env_diff.csv', 'tunnel')


def compare_tunnel(env, source_tunnel, dest_tunnel, app):
    app_folder_path = get_app_folder_path(app)
    if app == 'das-middleware':
        source_yaml_file = os.path.join(app_folder_path, 'values-others', f'values-{env}-{source_tunnel}-app-settings.yaml')
        dest_yaml_file = os.path.join(app_folder_path, 'values-others', f'values-{env}-{dest_tunnel}-app-settings.yaml')
    else:
        source_yaml_file = os.path.join(app_folder_path, 'values-others', f'values-{env}-{source_tunnel}.yaml')
        dest_yaml_file = os.path.join(app_folder_path, 'values-others', f'values-{env}-{dest_tunnel}.yaml')

    source_dict = uf.get_dict_from_yaml(source_yaml_file)
    dest_dict = uf.get_dict_from_yaml(dest_yaml_file)

    source_dict['diff_field'] = source_tunnel
    dest_dict['diff_field'] = dest_tunnel

    source_dict['tunnel'] = source_tunnel
    dest_dict['tunnel'] = dest_tunnel

    source_dict['env'] = env
    dest_dict['env'] = env

    # export_diff_csv(app, source_dict, dest_dict, 'tunnel_diff.csv')

    export_diff_csv_2(app, source_dict, dest_dict, 'tunnel_diff.csv', 'env',)


header_wrote = False
compare_tunnel('p2', 'smt', 'lrt', 'das-middleware')
compare_tunnel('p2', 'smt', 'lrt', 'das-evidence-record-consumer')
compare_tunnel('p2', 'smt', 'lrt', 'das-imageobj-consumer')
compare_tunnel('p2', 'smt', 'lrt', 'das-transaction-record-consumer')
compare_tunnel('p2', 'smt', 'lrt', 'tx-validation')
compare_tunnel('p2', 'smt', 'lrt', 'txv-process-consumer')
compare_tunnel('p2', 'smt', 'lrt', 'txv-stat-consumer')

header_wrote = False
compare_env('lrt', 'p2', 'p1', 'das-middleware')
compare_env('lrt', 'p2', 'p1', 'das-evidence-record-consumer')
compare_env('lrt', 'p2', 'p1', 'das-imageobj-consumer')
compare_env('lrt', 'p2', 'p1', 'das-transaction-record-consumer')
compare_env('lrt', 'p2', 'p1', 'tx-validation')
compare_env('lrt', 'p2', 'p1', 'txv-process-consumer')
compare_env('lrt', 'p2', 'p1', 'txv-stat-consumer')
