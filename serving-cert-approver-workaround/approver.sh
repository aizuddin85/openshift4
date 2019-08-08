echo "Logged-in as: `oc whoami`"

csrcount=`oc get csr | grep -i Pending |wc -l`

if [ $csrcount -gt 0 ]
then
  echo "Listing all Pending CSRs..."
  oc get csr | grep Pending

  echo "Approving CSR unconditionally..."
  oc adm certificate approve `oc get csr -o name`
else
  echo "No CSR in pending approval state..."
fi