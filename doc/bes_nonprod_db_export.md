# select small, non-backup table

```sql
SELECT table_name, round((data_length / 1024 / 1024 ), 2) AS table_size_mb
FROM information_schema.tables
WHERE table_schema = 'bes_core'
AND NOT (TABLE_NAME LIKE '%2022%' OR TABLE_NAME LIKE '%2023%' OR TABLE_NAME LIKE '%_bak%')
AND data_length < (1 * 1024 * 1024 * 1024)
ORDER BY data_length DESC

SELECT GROUP_CONCAT(TABLE_NAME SEPARATOR ' ') AS all_small_table_names
FROM information_schema.tables
WHERE table_schema = 'bes_core'
AND NOT (TABLE_NAME LIKE '%2022%' OR TABLE_NAME LIKE '%2023%' OR TABLE_NAME LIKE '%_bak%')
AND data_length < (1 * 1024 * 1024 * 1024)
ORDER BY data_length
```

## select big, non-backup table

```sql
SELECT table_name, 
  round((data_length / 1024 / 1024 ), 2) AS table_data_size_mb, 
  round((data_length / 1024 / 1024 / 1024), 2) AS table_data_size_gb,
  round((index_length / 1024 / 1024 ), 2) AS table_index_size_mb, 
  round((index_length / 1024 / 1024 / 1024), 2) AS table_index_size_gb
FROM information_schema.tables
WHERE table_schema = 'bes_core'
AND NOT (TABLE_NAME LIKE '%2022%' OR TABLE_NAME LIKE '%2023%' OR TABLE_NAME LIKE '%_bak%')
AND data_length > (1 * 1024 * 1024 * 1024)
ORDER BY data_length DESC
```

## export all small table to one gzip file

```bash
SMALL_TABLES='tb_valid_v tb_das_raw_data_pairing_archive tb_vehicle_hist tb_vehicle tb_das_mon_status tb_billing tb_acct tb_auto_payment_processing_hist tb_txv_notprocess tb_valid_v_owner tb_retention_based_cust_trxn tb_billing_detail tb_vehicle_supp_hist tb_payment tb_acct_login tb_vehicle_supp tb_acct_noti_preference tb_das_raw_evid_json tb_acct_phone tb_acct_email tb_acct_name ttb_acct_email tb_auto_payment_pending_hist tb_acct_pin tb_payment_detail tb_acct_address tb_auto_payment_processing tb_valid_v_action_log tb_payment_failure ttb_acct_phone tb_short_link tb_das_evid_obj_dup_upload ttb_vid tb_valid_v_info_complete tb_bes_trxn_hist_balance tb_tag tb_mir_type_chg_hist tb_tag_application tb_auto_payment_token tb_tag_veh_mapping tb_acct_login_log ttb_acct_first_name tb_monthly_statement_noti tb_mir_process tb_das_raw_data_pairing_12 tb_acct_id_seed tb_das_raw_data_pairing_13 tb_das_raw_data_pairing_18 tb_das_raw_data_pairing_17 tb_acct_history tb_das_raw_data_pairing_15 tb_valid_v_change_request tb_das_raw_data_pairing_08 tb_acct_auto_payment_setting tb_das_raw_data_pairing_19 tb_das_raw_data_pairing_16 tb_das_raw_data_pairing_14 tb_txv_mir_stat tb_das_raw_data_pairing_20 tb_das_raw_data_pairing_21 tb_das_raw_data_pairing_07 tb_das_raw_data_pairing_11 tb_das_op_status tb_das_raw_data_pairing_10 tb_das_raw_data_pairing_09 tb_otp tb_das_raw_data_pairing_22 tb_das_raw_data_pairing_23 tb_auto_payment_pending tb_das_raw_trxn_json tb_das_raw_data_pairing_00 tb_bes_op_status_upload_hist tb_das_raw_data_pairing_06 tb_das_raw_data_pairing_01 tb_das_raw_data_pairing_03 tb_das_tran_evid_summary_upload tb_acct_dsva_acc_bal tb_das_raw_data_pairing_02 tb_das_raw_data_pairing_unsuccess tb_das_raw_data_pairing_05 tb_das_trxn_obj_archive tb_mir_tag tb_valid_v_icp_archive tb_otp2 tb_valid_v_trailers_archive tb_das_raw_data_pairing_04 tb_valid_v_icp tb_payment_notification tb_otp1 tb_word_filter tb_registration_acct_noti_preference tb_txv_vrm_whitelist tb_valid_v_trailers tb_das_trxn_veh_obj_archive tb_valid_v_trade_license tb_valid_v_gov_archive tb_das_hourly_trxn_summary tb_valid_v_trade_license_archive tb_etl_stat_txv_process tb_registration_acct_notification tb_das_config tb_valid_v_other_type_holder_info tb_etl_stat_trxn_post tb_toll_rate_set_detail tb_notification_template_content tb_valid_v_disable_archive tb_das_event tb_valid_v_irn_mapping tb_payment_return_request tb_valid_v_gov tb_etl_process_log tb_valid_v_movement_permit_archive tb_valid_v_download tb_ccms_life_cycle_log tb_veh_associate_rvo_approval tb_ccms tb_valid_v_disable tb_valid_v_movement_permit tb_toll_subschedule tb_veh_associate tb_veh_pairing_hist tb_veh_associate_hist tb_wmm_refresh_token tb_auto_payment_setup tb_toll_subschedule_time ttb_vrm_pending tb_veh_associate_reg tb_ccms_detail tb_bes_approval_request tb_das_daily_event_summary tb_veh_associate_rvo_approval_hist tb_veh_pairing tb_toll_rate_set tb_ccms_action tb_driver_approval_hist tb_daily_rsa_key tb_enf tb_veh_associate_log tb_payment_token_revoke_request tb_driver_approval_detail_hist tb_raw_txv_process_archive tb_driver_approval tb_das_client_cert tb_raw_txv_process tb_enf_detail tb_raw_txv_notprocess tb_txv_exception lut_valid_v_veh_make tb_notification_template tb_veh_class_mapping tb_bes_trxn_dispute tb_middleware_client_cert tb_driver_approval_detail tb_toll_point tb_mom_veh_list tb_message_queue_task tb_acct_password_history tb_auto_payment_token_ins_que tb_toll_point_status_hist tb_das_evid_obj_sim tb_tag_acct_mapping tb_das_trxn_obj_sim tb_das_evid_obj_archive lut_ccms_category_tier tbl_txn_process tb_cert_thumbprint tb_tag_driver_mapping tb_veh_blacklist tb_mir_media_video tb_toll_rate_set_factor lut_bank_code tb_das_trxn_upload tb_das_evid_image_obj_sim tb_das_trxn_tag_obj_archive tb_payment_arrear_method tb_bes_posted_mir_trip tb_auto_payment_method tb_valid_v_process tb_das_trxn_veh_obj_sim tb_veh_group tb_das_evid_image_obj_archive tb_auto_payment_method_refund tb_special_day tb_das_trxn_tag_obj_sim tb_imsmart tb_toll_schedule tb_das_evid_upload tb_ccms_reply_log tb_mir_fingerprint tb_auto_payment_token_ins_hist tb_config_general tb_etl_process_general tb_public_holiday tb_team_members tb_ccms_followup_log lut_veh_class tb_acct_login_deny tb_camera_config tb_enf_video_request tb_config_allowed_email_domain tb_veh_associate_deny tb_sys_noti_msg_mapping tb_message_type tb_ccms_attachment tb_veh_group_mapping tb_surcharge_notice_video_request tb_toll_special_period_list tb_veh_pairing_favourite tb_payment_arrear_method_refund tb_toll_domain tb_sys_noti_acct_type_mapping lut_toll_domain_traffic_bound tb_das_trxn_seq tb_valid_v_veh_gross_weight_class_mapping tb_bes_virtual_account_creation_log tb_auto_payment_method_setup tb_surcharge_notice_media lut_veh_make tb_acct_payment_method tb_manual_payment_token_archive lut_acct_status tb_kpi_management_information tb_das_config_request lut_acct_district tb_auto_payment_token_termin_hist tb_toll_schedule_deleted_arch lut_trxn_type tb_das_op_status_request tb_enf_life_cycle_log tb_bes_op_status pay_tkn_revo_req_seq lut_tag_status noti_msg_seq tb_2pc_acct_priority_config tb_das_toll_point_switch_hist tb_payment_arrear_method_hist lut_special_day_type lut_payment_status tb_das_vssd tb_das_vss_video_upload billing_seq tb_das_status_change tb_auto_payment_method_hist mir_seq lut_ccms_incoming_channel tb_valid_v_keystore lut_veh_status tb_config_txv tb_sub_acct_mapping lut_billing_status lut_das_op_status tb_registration_acct_preference lut_acct_payment_method rpt_report_select_list_item lut_valid_v_veh_body_type tb_acct_govt_dept lut_tag_application_status tb_pm_das_toll_point_switch_request lut_acct_application_channel user_app_seq lut_token_revoke_type tb_acct_biz tb_enf_court_order tb_payment_arrear_method_refund_hist tb_toll_factor_element lut_surcharge_issuing_method rpt_system_reports tb_bes_approval_config tb_object_storage auto_pay_proc_seq tb_tag_veh_class lut_enf_status tb_valid_v_veh_class rpt_3rd_party_performance xtr_reports tb_auto_payment_method_refund_hist tb_das_toll_domain_context_request lut_dispute_receive_channel lut_vid_irn_type tb_das_status_detail tb_acct_saved_payment_method_detail tb_config_valid_v rpt_bes_main_elements tb_surcharge_rate lut_ccms_attach_type lut_veh_country_of_origin tb_toll_subschedule_deleted_arch tb_acct_password tb_config_ecms tb_registration_tag lut_acct_region lut_valid_v_veh_color tb_kpi_fault_management_2 ttb_acct_address_2 tb_phone_number_position tb_manual_payment_token tb_pm_kpi_trxn_prcs_time lut_acct_billing_type tb_toll_schedule_change_hist lut_trxn_status tb_acct_change_acct_type tb_toll_domain_statement tb_enf_evidence pay_return_request_seq tb_toll_factor_template_mapping lut_surcharge_post_delivery_status lut_trip_process_method tb_valid_v_password role_app_seq tb_team lut_payment_method rpt_das_exception_events_report tb_auto_payment_method_setup_hist tb_das_vrs_video_upload lut_driver_approval_options customer_case_seq lut_dispute_status tb_das_toll_point_mon_status tb_das_avc_veh_class lut_ccms_hashtag toll_sch_app_seq lut_veh_pairing_status tb_config_gov_tag_prefix tb_manual_payment_token_task tb_special_period_list lut_acct_type lut_veh_body_type tb_kpi_incorrect_charge_tsp_record tb_vehicle_sub_mapping tb_ccms_hashtag lut_acct_note_type lut_valid_v_id_type tb_acct_franchised_bus tb_das_toll_point_switch_request tb_enf_summon template_app_seq lut_tag_type tb_bes_reason_code isn_seq lut_payment_type tb_aes_key rpt_das_operating_status_report tb_das_op_request tb_driver_acct_veh_class tb_notification_template_para tb_kpi_ivr_availability auto_pay_pndg_seq tb_tag_prefix lut_driver_approval_status tb_das_status_upload_request tb_das_trxn_sum_hr_upload lut_ccms_status lut_das_severity_status tb_valid_v_action_type lut_veh_type tb_das_toll_point_mon tb_acct_preference tb_config_txv_supp_check_rules lut_ccms_action_type team_id_seq lut_veh_color tb_config_billing_and_payment tb_ccs_traffic_volume tb_registration_driver_acct_veh_class lut_acct_preference_type tb_auto_payment_token_termin_que lut_valid_v_veh_class tb_kpi_fault_management_1 ttb_acct_address_1 tb_das_kpi_event_request lut_ccms_main_category tb_pm_kpi_cust_web_app_response lut_acct_billing_preference tb_veh_exemption_list tb_das_kpi tb_toll_factor_template lut_surcharge_notice_status rpt_tsp_manual_review_activity pay_tkn_authz_req_seq lut_payment_channel rpt_das_exceptional_report fsn_seq enf_case_seq tb_sys_noti_preference lut_dispute_request_reason tb_core_doc_no_running tb_pm_das_master_status tb_acct_transfer_ownership tb_core_doc_no '

mariadb-dump -h t2vdbs-tdffsbe-tdb04-rpt.dbaas.gcisdctr.hksarg -P 19307 -u besdb_owner --password='Fpi22!AMZ' --ssl --net-buffer-length=16777216  \
--insert-ignore=TRUE --skip-lock-tables=TRUE --skip-add-locks=TRUE --skip-add-drop-table=TRUE \
--log-error='/mnt/data/tmp_db_backup_2023_05_16/error.log' \
bes_core ${EXPORT_TABLES} | gzip > /mnt/data/tmp_db_backup_2023_05_16/bes_core_small_table_3_20230516.gz
```

## export big table

```bash
## export tb_registration_acct
mariadb-dump -h t2vdbs-tdffsbe-tdb04-rpt.dbaas.gcisdctr.hksarg -P 19307 -u besdb_owner --password='Fpi22!AMZ' --ssl --net-buffer-length=16777216  \
--insert-ignore=TRUE --skip-lock-tables=TRUE --skip-add-locks=TRUE --skip-add-drop-table=TRUE \
--log-error='/mnt/data/tmp_db_backup_2023_05_09/error.log' \
--where 'bi_acct_reg_id > 7500000' \
bes_core tb_registration_acct | gzip > /mnt/data/tmp_db_backup_2023_05_09/bes_core_table_20230509-tb_registration_acct.gz

## export tb_das_trxn_tag_obj
mariadb-dump -h t2vdbs-tdffsbe-tdb04-rpt.dbaas.gcisdctr.hksarg -P 19307 -u besdb_owner --password='Fpi22!AMZ' --ssl --net-buffer-length=16777216  \
--insert-ignore=TRUE --skip-lock-tables=TRUE --skip-add-locks=TRUE --skip-add-drop-table=TRUE \
--log-error='/mnt/data/tmp_db_backup_2023_05_09/error.log' \
--where "bi_das_trxn_tag_obj_id  > 11000000" \
bes_core tb_das_trxn_tag_obj | gzip > /mnt/data/tmp_db_backup_2023_05_09/bes_core_table_20230509-tb_das_trxn_tag_obj.gz
```

## other notes

nohup ./export_small_tables.sh > export_small_tables.log 2>&1 &
nohup ./export_big_tables.sh > export_big_tables.log 2>&1 &

mariadb-dump -h t1vdbs-dept1-testdb1-ha1.dbaas.gcisdctr.hksarg -P 19307 -u app_owner -p --ssl --databases testdb1 --skip-add-locks --net-buffer-length=16777216 > dump.sql
mysqldump.exe --ssl --host="localhost" --port=3307 --user="besdb_owner" --password --insert-ignore --databases bes_core



```sql
SELECT table_name, round((data_length / 1024 / 1024 ), 2) AS table_data_size_mb, round((index_length / 1024 / 1024 ), 2) AS table_index_size_mb
FROM information_schema.tables
WHERE table_schema = 'bes_core'
AND NOT (TABLE_NAME LIKE '%2022%' OR TABLE_NAME LIKE '%2023%' OR TABLE_NAME LIKE '%_bak%')
#AND data_length < (1 * 1024 * 1024 * 1024)
ORDER BY data_length DESC
```
