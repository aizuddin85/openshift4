# OCP 4 UPI Baremetal
## Node Serving Certificate CSR Approver CronJob

**THIS CRON SCRIPT WILL SKIP "NODE-BOOTSTRAPPER" CSR APPROVAL REQUEST**


**NOTE:** This is community effort, and provided as-is without any support for such.

## 1. Create project to host this cronjob
```
#> oc new-project serving-cert-approver-workaround
```

## 2. Build & Push Image

Pre-Req:
* Buildah 
* Podman

Building base UBI8 image with OC client downloaded. 

```
#> git clone https://github.com/aizuddin85/openshift4.git
#> cd serving-cert-approver-workaround
#> buildah build-using-dockerfile  .
```

Tag image to the OCP 4 registry:
```
#> HOST=$(oc get route default-route -n openshift-image-registry --template='{{ .spec.host }}')
#> podman login -u $(oc whoami) -p $(oc whoami -t) --tls-verify=false $HOST 
#> buildah tag <BUILT IMAGE TAG> default-route-openshift-image-registry.<ocp4_route_domain>/openshift/oclientubi8:latest
#> buildah push default-route-openshift-image-registry.<ocp4_route_domain>/openshift/oclientubi8:latest
```
## 3. Prepare RBAC and ServiceAccount

Create clusterrole and clusterrolebinding just to allow CSR list and approval.
```
#> cd serving-cert-approver-workaround
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

## 4. Prepare configMaps that contains the script


Create script configMap,
```
#> cd serving-cert-approver-workaround
#> oc create configmap script --from-file=approver.sh -n serving-cert-approver-workaround
```

## 5. Create a OpenShift cronjob

At this stage where we have:
* Image
* Secret
* ConfigMap

We now can defined the cronjob, this YAML defined a job that will run once per hour:

```
#> oc create -f cronjob.yaml -n serving-cert-approver-workaround
```

Example of succesful run:

![alt text](https://github.com/aizuddin85/openshift4/blob/master/serving-cert-approver-workaround/Assets/example1.png)

