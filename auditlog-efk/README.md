1. Edit configMap of fluentd as per fluentd-cm.yaml  
2. Delete all fluentd pods:
```
oc delete pod -l component=fluentd -n openshift-logging
```
3. Create new index based on the 'index_name .audit' from store directive.  
`Management -> Index Patterns -> Create Index Pattern -> Enter ".audit" in the Index Pattern. `


References:
[1]: https://github.com/rbo/openshift-examples/tree/master/efk-auditlog
[2]: https://austindewey.com/2018/10/17/integrating-advanced-audit-with-aggregated-logging-in-openshift-3-11/
