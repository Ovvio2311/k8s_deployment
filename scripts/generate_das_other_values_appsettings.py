
import os
import my_util_func as uf

tunnels = {
    # 'abt': '1' ,
    # 'cht': '2' ,
    # 'eht': '3' ,
    'lrt': '4',
    'smt': '5',
    # 'tct': '6' ,
    # 'wht': '7' ,
    # 'tlt': '8' ,
    # 'tko': '10',

    # tsc handle manually
    # 'tsc': '9',
}

env_configs = {
    'nonprod': {
        'mysql_connection_string': 'server=t1vdbs-tdffsbe-tdb04-ha1.dbaas.gcisdctr.hksarg,t1vdbs-tdffsbe-tdb04-ha2.dbaas.gcisdctr.hksarg,t2vdbs-tdffsbe-tdb04-ha1.dbaas.gcisdctr.hksarg,t2vdbs-tdffsbe-tdb04-ha2.dbaas.gcisdctr.hksarg;Port=19307;Database=bes_core;uid=besdb_user;pwd=Autotoll5678!;Pooling=true;MaximumPoolsize=3500;CharSet=utf8;default command timeout=10;Allow User Variables=True;ConnectionTimeout=10;LoadBalance=LeastConnections;',
        'das_api_base_url': {
            'abt': '',
            'cht': '',
            'eht': '',
            'lrt': 'https://172.24.152.10:50443/',
            'smt': 'https://172.24.152.18:50443/',
            'tct': '',
            'wht': '',
            'tlt': '',
            'tko': '',
            'tsc': 'https://172.24.152.2:50443/',
        },
    },
    'p2': {
        'mysql_connection_string': 'server=p2vdbs-tdffsbe-ptdb01-ha1.dbaas.gcis.hksarg,p2vdbs-tdffsbe-ptdb01-ha2.dbaas.gcis.hksarg;Port=19307;Database=das;uid=besdb_user;pwd=Autotoll5678!;Pooling=true;MaximumPoolsize=100;CharSet=utf8;default command timeout=600;Allow User Variables=True;',
        'das_api_base_url': {
            'abt': '',
            'cht': '',
            'eht': '',
            'lrt': 'https://172.20.152.10:50443/',
            'smt': 'https://172.20.152.18:50443/',
            'tct': '',
            'wht': '',
            'tlt': '',
            'tko': '',
            'tsc': 'https://172.20.152.2:50443/',
        },
    },
    'p1': {
        'mysql_connection_string': 'server=p1vdbs-tdffsbe-ptdb01-ha1.dbaas.gcis.hksarg,p1vdbs-tdffsbe-ptdb01-ha2.dbaas.gcis.hksarg;Port=19307;Database=das;uid=besdb_user;pwd=Autotoll5678!;Pooling=true;MaximumPoolsize=100;CharSet=utf8;default command timeout=600;Allow User Variables=True;',
        'das_api_base_url': {
            'abt': '',
            'cht': '',
            'eht': '',
            'lrt': 'https://172.16.152.10:50443/',
            'smt': 'https://172.16.152.18:50443/',
            'tct': '',
            'wht': '',
            'tlt': '',
            'tko': '',
            'tsc': 'https://172.16.152.2:50443/',
        },
    },
}

tempalte_path = 'scripts/das_tunnel_values_templates'


def main():
    for toll_domain_abb, toll_domain_id in tunnels.items():
        for env, env_config in env_configs.items():
            gen_das_middleware_app_settings(toll_domain_abb, toll_domain_id, env, env_config)
            # gen_tx_validation_app_settings(tunnel, env)


def gen_das_middleware_app_settings(toll_domain_abb, toll_domain_id, env, env_config: dict):
    zone_folder = 'dmz-bes'
    app_name = 'das-middleware'
    template_string = uf.read_file_as_string(f'{tempalte_path}/{app_name}-values-template.yaml')

    config = env_config.copy()
    config .update({
        'toll_domain_id': toll_domain_id,
        'toll_domain_abb': toll_domain_abb,
        'video_suffix': '',
        'http_node_port': '',
        'https_node_port': '',
        'das_api_base_url': env_config['das_api_base_url'][toll_domain_abb],
    })

    # ====================normal====================
    config['video_suffix'] = ''
    config['http_node_port'] = f'3111{toll_domain_id}'
    config['https_node_port'] = f'3211{toll_domain_id}'

    config_file_name = f'values-{env}-{toll_domain_abb}-app-settings.yaml'
    config_file_content = uf.format_str_with_dict(template_string, config)
    uf.save_to_file(f'k8s_yaml_das_values/{zone_folder}/{app_name}/values-others/{config_file_name}', config_file_content)

    # ====================video====================
    config['video_suffix'] = '-video'
    config['http_node_port'] = f'3112{toll_domain_id}'
    config['https_node_port'] = f'3212{toll_domain_id}'

    config_file_name = f'values-{env}-{toll_domain_abb}-video-app-settings.yaml'
    config_file_content = uf.format_str_with_dict(template_string, config)
    uf.save_to_file(f'k8s_yaml_das_values/{zone_folder}/{app_name}/values-others/{config_file_name}', config_file_content)


# def gen_tx_validation_app_settings(tunnel, tunnel_config, env):
#     zone_folder = 'bes'
#     app_name = 'tx-validation'
#     template_string = uf.read_file_as_string('scripts/das_tunnel_values_templates/tx-validation-values-template.yaml')
#     final_config = get_final_config(tunnel_config, env, app_name)

#     # ====================normal====================
#     final_config['name_suffix'] = ''
#     final_config['topic_backlog_suffix'] = ''
#     config_file_name = f'values-{env}-{tunnel}.yaml'
#     config_file_content = uf.format_str_with_dict(template_string, final_config)
#     uf.save_to_file(f'k8s_yaml_das_values/{zone_folder}/{app_name}/values-others/{config_file_name}', config_file_content)

#     # ====================backlog====================
#     final_config['name_suffix'] = '-backlog'
#     final_config['topic_backlog_suffix'] = '_backlog'
#     config_file_name = f'values-{env}-{tunnel}-backlog.yaml'
#     config_file_content = uf.format_str_with_dict(template_string, final_config)
#     uf.save_to_file(f'k8s_yaml_das_values/{zone_folder}/{app_name}/values-others/{config_file_name}', config_file_content)


# def get_final_config(tunnel_config, env, app_name, topic_type='normal'):
#     # default_config = tunnel_config.get('default')
#     app_config = tunnel_config.get(app_name)

#     # env_default_config = app_config.get('env_default')
#     env_config = app_config.get(env)

#     final_config = app_config
#     final_config.update(app_config)
#     # final_config.update(env_default_config)
#     if env_config is not None:
#         final_config.update(env_config)

#     return final_config

# def gen_das_middleware_app_settings():
main()
