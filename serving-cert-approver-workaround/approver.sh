echo "Logged-in as: `oc whoami`"

csrcount=`oc get csr | grep -i Pending |wc -l`
pendingcsr=`oc get csr | grep -i Pending  | awk '{print $1}'`

if [ $csrcount -gt 0 ]
then
  echo "Listing all Pending CSRs..."
  oc get csr | grep Pending
  echo "Approving only Node Serving Certificate CSR, please approve node-bootstrapper manually..."

  for csr in $pendingcsr; do
    if [[ `oc get csr  -o  custom-columns=:.spec.username $csr` == *"node-bootstrapper"* ]]; then
  	  echo "Detected $csr as bootstrap request, skipping, please approve manually ..."
    else
	  oc adm certificate approve $csr
    fi
  done  
else
  echo "No Node Serving Certificate CSR in pending approval state..."
fi
