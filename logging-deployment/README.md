## Prepare Logging namespace
* oc new-project cluster-logging

## Install Operator from OperatorHub.
* logging operator - in the cluster-logging namespace
* Elasticsearch operator

## Create logging stack
* oc create -f logging-cr.yaml
