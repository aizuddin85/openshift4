# FIO Storage Benchmarking for RHOCP/RHOCS.

This deployment is to help to run FIO benchmarking for OCS PV.

## High Level Steps
* Create PVC - For CephFS use cephfs-pvc.yaml and change the PVC volume mount name in the fio-tool.yaml, same goes to cephrbd.
```
# oc create -f cephfs-pvc.yaml -n fio-lab
```

* Create FIO configmap - Change FIO settings accordingly as per your own if necessary.
```
# oc create -f fio-configmap.yaml -n fio-lab
```

* Create fio tool pod deployment. This wills start the benchmarking.
```
# oc create -f fio-tool.yaml -n fio-lab
```


* Expose route for result webserver
```
# oc create -f fio-svc-route.yaml -n fio-lab
```


## Result

* Navigate to your route "http://fio-tools-fio-lab.apps.ocp4.example.com/server/plots/"

* Read IOPS Latency result example
![Read IOPS](https://github.com/aizuddin85/openshift4/blob/master/fio-lab/assets/readiops.png)

* Write IOPS Latency result example
![Write IOPS](https://github.com/aizuddin85/openshift4/blob/master/fio-lab/assets/writeiops.png)