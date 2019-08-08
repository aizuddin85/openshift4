# OCP 4 UPI Baremetal
## Node Serving Certificate CSR Approver CronJob

**NOTE:** This is community effort, and provided as-is without any support for such.

## 1. Create project to host this cronjob
```
#> oc create-project serving-cert-approver-workaround
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
#> buildah tag 8ff88db8565b default-route-openshift-image-registry.<ocp4_route_domain>/openshift/oclientubi8:latest
#> buildah push default-route-openshift-image-registry.<ocp4_route_domain>/openshift/oclientubi8:latest
```

## 3. Prepare secret and configMaps

In this case, I`m using kubeconfig generated during the installation and script to execute the command. This will be mounted on the pod running the job later.

**NOTE:** The better practise is to use serviceaccount with proper RBAC just for approving CSR instead of kubeadmin superuser.

Create kubeconfig secret,
```
#> oc create secret generic kubeadmin --from-file=kubeconfig -n serving-cert-approver-workaround
```

Create script configMap,
```
#> cd serving-cert-approver-workaround
#> oc create configmap script --from-file=approver.sh -n serving-cert-approver-workaround
```

## 4. Create a OpenShift cronjob

At this stage where we have:
* Image
* Secret
* ConfigMap

We now can defined the cronjob, this YAML defined a job that will run once per hour:

```
#> oc create -f cronjob.yaml -n serving-cert-approver-workaround
```
