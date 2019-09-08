# rook.io + Ceph 1.1
Actual documentation can be found here: [Rook.io 1.1](https://rook.io/docs/rook/v1.1/ceph-examples.html)  

1. Create common resource
```
#> oc create -f common.yaml
```

2. Create operator
```
#> oc create -f operator-openshift.yaml
```

3. Create Ceph cluster
```
#> oc create -f cluster.yaml
```

4. Create ceph filesystem for later storageclass use
```
#> oc create -f filesystems.yaml
```

5. Create Ceph CSI based storageclass
```
#> oc create -f csi/cephfs/storageclass.yaml

# To test the SC

#> oc create -f csi/cephfs/pvc.yaml
#> oc create -f csi/cephfs/pod.yaml
```

6. Create RBD CSI based storageclass
```
#> oc create -f csi/rbd/storageclass.yaml

# To test the SC

#> oc create -f csi/rbd/pvc.yaml
#> oc create -f csi/rbd/pod.yaml

```
