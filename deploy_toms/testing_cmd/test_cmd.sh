curl https://172.24.151.119:32002/TrustObject/idat02_trust_obj_req \
-d '{"client_id":"DASTSC1","app_id":"APP00211","req_id":"test1202_01"}' \
-H 'Content-Type: application/json-patch+json' \
-k --key ./client-cert-to-toms-mw.key --cert ./client-cert-to-toms-mw.crt && echo

 curl https://172.24.151.119:32002/TrustObject/idat00_asymmetric_key \
-H 'accept: text/plain' \
-k --key ./client-cert-to-toms-mw.key --cert ./client-cert-to-toms-mw.crt && echo