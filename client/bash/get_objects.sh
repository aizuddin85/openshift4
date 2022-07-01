#!/bin/bash

nameSpace=()
k8sObject=("project" "deployment" "deploymentconfig" "statefulset"  
           "persistentvolumeclaim" "secrets" "serviceaccount" 
           "role" "rolebinding" "imagestream" "imagestreamtag"
           "configmap" "daemonset" "cronjob" "job" "replicaset" "replicationcontroller"
           "horizontalpodautoscaler" "pods" )

filePrefix=$(date +%Y%m%d%s)

for i in `oc get projects | egrep -v "^NAME|^default|^kube|^openshift" | cut -d " " -f 1`;
  do
    ns+=($i)
done
mkdir openshift-$filePrefix

[ ! -d "openshift-$filePrefix" ] && echo "Unable to create folder!" && exit 1

oc get pv -o yaml > openshift-$filePrefix/pv.yaml

for namespace in ${ns[@]};
  do
    mkdir openshift-$filePrefix/$namespace
    [ ! -d "openshift-$filePrefix/$namespace" ] && echo "Unable to create folder!" && exit 1

    for object in ${k8sObject[@]};
      do
        mkdir openshift-$filePrefix/$namespace/$object
        [ ! -d "openshift-$filePrefix/$namespace/$object" ] && echo "Unable to create folder!" && exit
        echo "Collecting for $object in $namespace..."
        oc get $object -o yaml -n $namespace >  openshift-$filePrefix/$namespace/$object/$object.yaml
    done
done 

echo "Please tar.gz openshift-$filePrefix and send this to us..."