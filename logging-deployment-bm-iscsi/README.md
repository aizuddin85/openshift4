## Configuring openshift-logging.

1. Create required namespace namespace.yaml
2. Install required operator from operator hub:
* Elasticsearch operator
* Logging operator

3. Once operator installer, create CR for clusterlogging.
4. Edit PV to claimRef to created PVC by operator.
5. create PV from yaml.
6. Label node with proper selector.
7. Edit each ES deployment to met this nodeSelector.eg. elastic-01 to node-01.
