csrcount=`oc get csr | grep -i Pending |wc -l`

if [ $csrcount -gt 0 ]
then
  oc adm certificate approve `oc get csr -o name`
else
  echo "No CSR in pending approval state..."
fi
