#  Introduction

Pre-Req:
* rook-ceph installed: https://rook.io/docs/rook/v1.0/ceph-storage.html


# Steps
This guide as an example how we can use CephFS as flexVolume persistent volume that will be use RWX by registry.

1. Create custom restricted SCC that contains registry service account.

``` oc create -f restricted_flexVolume_scc.yaml```

2. Create cephfs CR  

```oc create -f cephfs-object.yaml```

3. Create PV for image registry PVC  

``` oc create -f registry-cephfs-flex-volume-rwx.yaml```

4. Example output:
  
```
mzali@mzali-fedora.redhat.com:~ $ oc get pvc
NAME                     STATUS   VOLUME                 CAPACITY   ACCESS MODES   STORAGECLASS      AGE
image-registry-storage   Bound    registry-flex-volume   100Gi       RWX               16m
mzali@mzali-fedora.redhat.com:~ $ oc get pv
NAME                   CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                             STORAGECLASS   REASON   AGE
registry-flex-volume   100Gi       RWX            Retain           Bound    openshift-image-registry/image-registry-storage                           16m
```
