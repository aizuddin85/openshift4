1. Edit configMap of fluentd as per fluentd-cm.yaml  
2. Delete all fluentd pods:
```
oc delete pod -l component=fluentd -n openshift-logging
```
3. Create new index based on the 'index_name .audit' from store directive.
Management -> Index Patterns -> Create Index Pattern -> Enter ".audit" in the Index Pattern. 
