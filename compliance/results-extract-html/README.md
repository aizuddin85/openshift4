# Enabling extractor job and html report generation.

PREREQ: We need a host with a NFS running. In my case, using a bastion node.

1. Prepare bastion for NFS export and permission.
```bash
[root@bastion ~]# cat /etc/exports
/reports/compliance_result *(rw,root_squash)
```

2. Now create necessary directory and set permission on this the export path:
```bash
[root@bastion ~]# ls -lrt /reports/compliance_result
total 4
drwxr-xr-x. 7 1000660000 1000660000   60 Aug  4 00:45 ocp4-cis
drwxr-xr-x. 7 1000660000 1000660000   60 Aug  4 00:45 rhcos-master
drwxr-xr-x. 7 1000660000 1000660000   60 Aug  4 00:45 rhcos-router
drwxr-xr-x. 7 1000660000 1000660000   60 Aug  4 00:45 rhcos-worker

[root@bastion ~]# 
```
**NOTE**: The UID/GID are coming from openshift-compliance `openshift.io/sa.scc.uid-range` and `openshift.io/sa.scc.supplemental-groups`. The other option perhaps using supplementalGroups under securityContext spec.

3. Now create the PV and PVC for the report consolidation.
```bash
[root@bastion ~]# oc create -f compliance-hosting-pv.yaml

[root@bastion ~]# oc create -f compliance-hosting-pvc.yaml
```

4. Build the Dockerfile to include oscap binary or you can use other built image that has oscap binary in it.
```bash
[root@bastion ~]# buildah bud -t quay.io/mzali/oscap:latest

[root@bastion ~]# podman push quay.io/mzali/oscap:latest
```

5. Deploy cronjob(suspend: true, so we can create job from this as template).

**NOTE**: Ensure volume details are per result server(RS) PVC name(and any other details as per your env).
```bash
[root@bastion ~]# oc create -f extractor-job.yaml
```

6. Now run the compliance report.

7. Once the ComplianceScan status is **DONE**, create the extractor job. This job will consolidate all RS PVC data and push into the NFS shared earlier.
```bash
[root@bastion ~]# oc create job extractor-job --from=cronjob/extractor-custom-job
```

This will copy all result, generate html report that is available on the NFS export earlier.

8. The NFS path content:
```
[root@bastion compliance_result]# tree /root/compliance_result/ocp4-cis/
/reports/compliance_result/ocp4-cis/
|-- 0
|   |-- ocp4-cis-api-checks-pod.xml.bzip2
|   `-- ocp4-cis-api-checks-pod.xml.bzip2.html
|-- 1
|   |-- ocp4-cis-api-checks-pod.xml.bzip2
|   `-- ocp4-cis-api-checks-pod.xml.bzip2.html
|-- 2
|   |-- ocp4-cis-api-checks-pod.xml.bzip2
|   `-- ocp4-cis-api-checks-pod.xml.bzip2.html
|-- 3
|   |-- ocp4-cis-api-checks-pod.xml.bzip2
|   `-- ocp4-cis-api-checks-pod.xml.bzip2.html
`-- lost+found

5 directories, 8 files
```

9. We can start a quick python http server and serve this content via http webserver.
```
[root@bastion compliance_result]# pwd
/reports/compliance_result
[root@bastion compliance_result]# python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
192.168.254.21 - - [04/Aug/2021 20:14:45] "GET / HTTP/1.1" 200 -
192.168.254.21 - - [04/Aug/2021 20:14:45] code 404, message File not found
192.168.254.21 - - [04/Aug/2021 20:14:45] "GET /favicon.ico HTTP/1.1" 404 -
192.168.254.21 - - [04/Aug/2021 20:14:47] "GET /rhcos-master/ HTTP/1.1" 200 -
192.168.254.21 - - [04/Aug/2021 20:14:49] "GET /ocp4-cis/ HTTP/1.1" 200 -
192.168.254.21 - - [04/Aug/2021 20:14:50] "GET /ocp4-cis/3/ HTTP/1.1" 200 -
192.168.254.21 - - [04/Aug/2021 20:14:51] "GET /ocp4-cis/3/ocp4-cis-api-checks-pod.xml.bzip2.html HTTP/1.1" 200 -
```