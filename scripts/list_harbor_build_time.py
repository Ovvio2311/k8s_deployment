### open ssh tunnel before run this script
# np: plink user00@172.24.150.131 -pw Atl@2022 -N -L 8083:172.24.150.130:8083 
# p1: plink user00@172.16.150.133 -pw Atl@2022 -N -L 8083:172.16.150.130:8083 
# p2: plink user00@172.20.150.131 -pw Atl@2022 -N -L 8083:172.20.150.130:8083 


# import for rest api call
import os
import requests
import csv
# disable verify ssl
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
verify_ssl = False

app_zone_list = {
    "accmgt-api": "bes",
    "auth-api": "bes",
    "auto-payment-scheduler": "bes",
    "bes-acc-im001-fft-account-registration": "bes",
    "bes-acc-im002-fft-vehicle-management": "bes",
    "bes-acc-im003-fft-vehicle-group-management": "bes",
    "bes-acc-im004-fft-account-search": "bes",
    "bes-acc-im005-fft-driver-approval": "bes",
    "bes-acc-im006-fft-account-management": "bes",
    "bes-acc-im007-fft-vehicle-pairing": "bes",
    "bes-acc-im008-fft-tag-management": "bes",
    "bes-acc-im009-fft-payment-and-billing": "bes",
    "bes-acc-im010-fft-transaction": "bes",
    "bes-acc-im011-ffts-toll-and-surcharge": "bes",
    "bes-acc-im012-ffts-account-history": "bes",
    "bes-acc-im013-ffts-performance-monitoring": "bes",
    "bes-cre-im001-tokenization": "bes",
    "bes-cre-im002-otp": "bes",
    "bes-cre-im007-notification-template-management": "bes",
    "bes-cre-im008-notification-message-management": "bes",
    "bes-cre-im009-notification-processor": "bes",
    "bes-cre-im010-shortlink": "bes",
    "bes-notification-pulsar-consumer-services": "bes",
    "bes-notification-push-app-services-2-high": "bes",
    "bes-notification-push-app-services-2": "bes",
    "bes-notification-push-app-services": "bes",
    "bes-notification-push-email-services-2-high": "bes",
    "bes-notification-push-email-services-2": "bes",
    "bes-notification-push-email-services": "bes",
    "bes-notification-push-sms-services-2-high": "bes",
    "bes-notification-push-sms-services-2": "bes",
    "bes-notification-push-sms-services": "bes",
    "bes-send-schedule-notification-services": "bes",
    "ccms-api": "bes",
    "ccs-api": "bes",
    "central-db-services-accmgt": "bes",
    "central-db-services-ccms": "bes",
    "central-db-services-core": "bes",
    "central-db-services-ecms": "bes",
    "centraldbservices-das": "bes",
    "das-evid-api": "bes",
    "das-evidence-record-consumer-backlog": "bes",
    "das-evidence-record-consumer-lrt-backlog": "bes",
    "das-evidence-record-consumer-lrt": "bes",
    "das-evidence-record-consumer-smt-backlog": "bes",
    "das-evidence-record-consumer-smt": "bes",
    "das-evidence-record-consumer": "bes",
    "das-imageobj-consumer-backlog": "bes",
    "das-imageobj-consumer-lrt-backlog": "bes",
    "das-imageobj-consumer-lrt": "bes",
    "das-imageobj-consumer-smt-backlog": "bes",
    "das-imageobj-consumer-smt": "bes",
    "das-imageobj-consumer": "bes",
    "das-transaction-record-consumer-backlog": "bes",
    "das-transaction-record-consumer-lrt-backlog": "bes",
    "das-transaction-record-consumer-lrt": "bes",
    "das-transaction-record-consumer-smt-backlog": "bes",
    "das-transaction-record-consumer-smt": "bes",
    "das-transaction-record-consumer": "bes",
    "ecms-api": "bes",
    "mariadb-metric-collector": "bes",
    "notification-api": "bes",
    "s3-api": "bes",
    "secondocr-webapi": "bes",
    "tx-validation-backlog": "bes",
    "tx-validation-lrt-backlog": "bes",
    "tx-validation-lrt": "bes",
    "tx-validation-smt-backlog": "bes",
    "tx-validation-smt": "bes",
    "tx-validation": "bes",
    "txv-process-consumer-backlog": "bes",
    "txv-process-consumer-lrt-backlog": "bes",
    "txv-process-consumer-lrt": "bes",
    "txv-process-consumer-smt-backlog": "bes",
    "txv-process-consumer-smt": "bes",
    "txv-process-consumer": "bes",
    "txv-stat-consumer-lrt": "bes",
    "txv-stat-consumer-smt": "bes",
    "txv-stat-consumer": "bes",
    "validv-api": "bes",
    "auto-issue-suspend-fsn": "bes-job",
    "bes-s3objectstorage-archive-bucket": "bes-job",
    "bes-schedule-account-idle-reminder": "bes-job",
    "bes-schedule-account-idle": "bes-job",
    "bes-schedule-driver-approval-pairing-expiry": "bes-job",
    "bes-schedule-monthly-statement-notice": "bes-job",
    "bes-schedule-payment-reminder": "bes-job",
    "bes-schedule-remove-vehicle-data-for-tt-trxn": "bes-job",
    "das-missing-data-schedule": "bes-job",
    "das-pairing-data-purger": "bes-job",
    "ecms-surcharge-notice-generation": "bes-job",
    "generate-issued-surcharge": "bes-job",
    "pair-das-data-schedule": "bes-job",
    "trigger-das-mid-idaa11-bes-status-upload": "bes-job",
    "bes-ccs": "dmz-bes",
    "bes-psp": "dmz-bes",
    "bes-signalr-server": "dmz-bes",
    "bes-tsp": "dmz-bes",
    "bes-ttis": "dmz-bes",
    "bes-wmm": "dmz-bes",
    "bes-wmm2": "dmz-bes",
    "bescore-portal": "dmz-bes",
    "ccms-portal": "dmz-bes",
    "ccs-middleware": "dmz-bes",
    "ccs-scheduler": "dmz-bes",
    "das-middleware-lrt-video": "dmz-bes",
    "das-middleware-lrt": "dmz-bes",
    "das-middleware-smt-video": "dmz-bes",
    "das-middleware-smt": "dmz-bes",
    "das-middleware-video": "dmz-bes",
    "das-middleware": "dmz-bes",
    "ecms-portal": "dmz-bes",
    "ffts-web": "dmz-bes",
    "notification-result": "dmz-bes",
    "validv-middleware": "dmz-bes",
}


def ask_harbor_tag():
    print('Enter tag (nonprod | p1 | p2):')
    tag = input()
    if tag not in ['nonprod', 'p1', 'p2']:
        print('tag only allow nonprod or p1 or p2')
        exit()
    return tag


def get_harbor_project_id() -> int:
    response = requests.get(f"{harbor_api_base_uri}/projects?name=bes",
                            auth=(harbor_user, harbor_password), verify=False)
    project_list = response.json()  # type: list
    project_id = project_list[0]['project_id']
    return project_id


def get_harbor_repo_list(harbor_api_base_uri, harbor_user, harbor_password) -> list:
    repo_list = []
    page = 1
    harbor_project_id = get_harbor_project_id()

    # loop_max just for prevent infinite loop
    loop_max = 10
    done = False
    while done == False and page < loop_max:
        response = requests.get(f"{harbor_api_base_uri}/repositories?project_id={harbor_project_id}&page={page}&page_size=100",
                                auth=(harbor_user, harbor_password), verify=False)

        request_repo_list = response.json()
        repo_list.extend(request_repo_list)

        if len(request_repo_list) < 100:
            done = True

        page += 1
    return repo_list


def get_harbor_repo_tag_detail(repo_name: str, tag: str) -> dict:
    repo_name = repo_name.replace("/", "%2F")
    response = requests.get(f"{harbor_api_base_uri}/repositories/{repo_name}/tags/{tag}", auth=(harbor_user, harbor_password), verify=False)
    tag_detail = response.json()
    return tag_detail


# def get_harbor_repo_artifacts_detail(repo_name: str, tag: str) -> dict:
#     repo_name = repo_name.replace('harbor_project_name/', '')
#     repo_name = repo_name.replace("/", "%2F")
#     response = requests.get(f"{harbor_api_base_uri}/projects/{harbor_project_name}/repositories/{repo_name}/artifacts/{tag}", auth=(harbor_user, harbor_password), verify=False)
#     tag_detail = response.json()
#     return tag_detail


def ensure_dir_existe(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


def save_to_file(file_path, content):
    ensure_dir_existe(file_path)
    with open(file_path, 'w') as f:
        f.write(content)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def save_result_list_to_csv(file_name, result_list) -> None:
    delete_file(file_name)
    with open(file_name, 'w', newline='\n') as csvfile:
        fieldnames = ['repo_name', 'build_time', 'size', 'tag_name', 'hostname']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in result_list:
            writer.writerow(result)


def get_harbor_app_list(repo_list):
    result_list = []
    print(f'{"build_time".ljust(30)} , {"tag_name".ljust(8)} , repo_name ')
    print(f'------------------------------------------------------------------')
    for repo in repo_list:
        repo_name = repo['name']
        tag_detail = get_harbor_repo_tag_detail(repo_name, harbor_tag)
        build_time = tag_detail['created']
        size = tag_detail['size']
        tag_name = tag_detail['name']

        app_name = repo_name.split('/')[1]
        if app_zone_list[app_name] == "bes-job" or app_zone_list[app_name] == "bes":
            hostname = "tkubw1 | tkubw2 | tkubw3 | tkubw4 | tkubw5 | tkubw6"
        elif app_zone_list[app_name] == "dmz-bes":
            hostname = "ikubw1 | ikubw2 | ikubw3"
        else:
            hostname = ""

        result_list.append(dict(repo_name=repo_name, build_time=build_time, size=size, tag_name=tag_name, hostname=hostname))
        print(f'{build_time.ljust(30)} , {tag_name.ljust(8)}, {repo_name}')
    return result_list


def main(harbor_tag):
    repo_list = get_harbor_repo_list(harbor_api_base_uri, harbor_user, harbor_password)
    result_list = get_harbor_app_list(repo_list)
    file_name = f'app_version_{harbor_tag}.csv'
    save_result_list_to_csv(file_name, result_list)
    print(f'saved to csv file: {file_name}')
    print('press enter to exit')
    input()


try:
    harbor_project_name = "bes"
    harbor_api_base_uri = "http://localhost:8083/api"
    harbor_user = 'admin'
    harbor_password = 'Atl@2022'
    harbor_tag = ask_harbor_tag()
    main(harbor_tag)
except Exception as err:
    print('error: %s' % err)
    print('------------------------------')
    print('Press enter to exit')
    input()
