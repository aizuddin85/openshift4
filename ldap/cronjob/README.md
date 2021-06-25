# Enabling LDAP Group Sync & Prune CronJob

## Prepare service account and authorization
1. Create SA to be used by the pod.
```bash
#> oc create -f serviceaccount.yaml
```

2. Create custom CustomRole and its CustomRoleBinding.
```bash
#> oc creage -f customrole.yaml -f customrolebinding.yaml
```

3. Create configmap that contain the LDAPSyncConfig object. This will be mounted by the pod when executing the group syncing or group pruning.
```bash
#> oc create -f configmap.yaml
```

4. Then create a syncing cronjob, to add new/sync object from LDAP.
```bash
#> oc create -f cronjob-syncer.yaml
```

5. Create LDAP bind encrypted secret
```bash
#> oc adm ca encrypt --genkey=bindPassword.key --out=bindPassword.encrypted

#> oc create secret generic bindencrypted --from-file=bindPassword.encrypted

#> oc create secret generic bindkey --from-file=bindPassword.key
```

6. Lastly create a pruner cronjob, to do clean up for object no longer exists in LDAP from the platform.
```bash
#> oc create -f cronjob-pruner.yaml
```