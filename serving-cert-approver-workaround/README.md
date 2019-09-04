# OCP 4 UPI Baremetal
## Node Serving Certificate CSR Approver CronJob

**THIS CRON SCRIPT WILL SKIP "NODE-BOOTSTRAPPER" CSR APPROVAL REQUEST**


**NOTE:** This is community effort, and provided as-is without any support for such.

## 1. Create project to host this cronjob
```
#> oc new-project serving-cert-approver-workaround
```

## 2. Setup a build config, this will create:
* imagestream mirror to registry.redhat.io/ubi8/ubi:latest in openshift namespace
* imagestream for build output in serving-cert-approver-workaround namespace
* create dockerStrategy build for oc + ubi8 apps image.

NOTE: Please change the "OC_VERSION" environment to suite your version.

```
#>  oc apply -f build_setup.yaml
```


## 3. Build Image

```
#> oc start-build docker-build --follow -n serving-cert-approver-workaround
build.build.openshift.io/docker-build-11 started
Cloning "https://github.com/aizuddin85/openshift4.git" ...
	Commit:	857a4146f5eb8cde0c208a03215fdd6406f0810c (use version instead of latest)
	Author:	Muhammad Aizuddin Zali <mzali@mzali-fedora.redhat.com>
	Date:	Wed Sep 4 15:37:53 2019 +0800
Caching blobs under "/var/cache/blobs".

Pulling image image-registry.openshift-image-registry.svc:5000/openshift/ubi:latest ...
Getting image source signatures
Copying blob sha256:e61d8721e62e50814b162c8341bb235d3453b9c95bd26439bf9100fcf88338c7
Copying blob sha256:c585fd5093c62ee42a56af6c09813ac8384d8145c4285bc62c357b41224b1970
Copying config sha256:c7a62535df3cebd7cb714574c04fb3aa71b92551c11a164cef461855360d3970
Writing manifest to image destination
Storing signatures
STEP 1: FROM image-registry.openshift-image-registry.svc:5000/openshift/ubi:latest
STEP 2: ENV "OC_VERSION"="4.1.13"
STEP 3: MAINTAINER "Muhammad Aizuddin Zali" <mzali@redhat.com>
STEP 4: ADD https://mirror.openshift.com/pub/openshift-v4/clients/ocp/$OC_VERSION/openshift-client-linux-$OC_VERSION.tar.gz /usr/bin/openshift-client-linux-$OC_VERSION.tar.gz
STEP 5: RUN tar -xzvf  /usr/bin/openshift-client-linux-$OC_VERSION.tar.gz  -C /usr/bin &&     chmod +x /usr/bin/oc

<<<TRUNCATED>>>
```


## 4. Prepare RBAC and ServiceAccount

Create clusterrole and clusterrolebinding just to allow CSR list and approval.
```
#> cd openshift4/serving-cert-approver-workaround
#> oc create -f rbac.yaml
clusterrole.rbac.authorization.k8s.io/signer-workaround created
clusterrolebinding.rbac.authorization.k8s.io/signer-workaround created
```

Assign cluster role to service account.
```
#> oc create serviceaccount signer -n serving-cert-approver-workaround
#> oc adm  policy  add-cluster-role-to-user  signer-workaround -z signer
clusterrole.rbac.authorization.k8s.io/signer-workaround added: "signer"
```

## 5. Prepare configMaps that contains the script
NOTE: This can be baked in the image itself, purpose of putting as configMap, is to be able dynamically change the script. 

Create script configMap,
```
#> cd openshift4/serving-cert-approver-workaround
#> oc create configmap script --from-file=approver.sh -n serving-cert-approver-workaround
```

## 6. Create a OpenShift cronjob

At this stage where we have:
* Image
* Secret
* ConfigMap

We now can defined the cronjob, this YAML defined a job that will run once per hour:

```
#> cd openshift4/serving-cert-approver-workaround
#> oc create -f cronjob.yaml -n serving-cert-approver-workaround
```

Example of node-bootstrap skipped for approval:

![alt text](https://github.com/aizuddin85/openshift4/blob/master/serving-cert-approver-workaround/Assets/bootstrapreq.png)


Example of Node serving certificate CSR being approved:
![alt text](https://github.com/aizuddin85/openshift4/blob/master/serving-cert-approver-workaround/Assets/nodecsr.png)
