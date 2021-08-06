# Using govc to create OpenShift VM


1. Prepare the prereq as per official docs and generate ignitions file.

2. Create base64 version of those ignition files.

```bash
[root@bastion-spodon ocp4]# base64 -w0 bootstrap.ign > bootstrap.b64
[root@bastion-spodon ocp4]# base64 -w0 master.ign > master.b64
[root@bastion-spodon ocp4]# base64 -w0 worker.ign > worker.b64
```

3. Setup govc environment.
```bash
[root@bastion-spodon ocp4]# cat govc.env 
export GOVC_URL=vcenter.example.com
export GOVC_USERNAME=admin
export GOVC_PASSWORD=admin123
export GOVC_INSECURE=true
[root@bastion-spodon ocp4]# source govc.env 
[root@bastion-spodon ocp4]# 

```

3. Create Bootstrap VM using govc client.

a. Create Bootstrap VM from OVA VM Template

```bash

[root@bastion-spodon ocp4]# govc vm.clone -vm ocp4_8 -c=8 -m=24000 -dc="vSAN Datacenter" -ds=vsanDatastore -folder="Din VM" -net="1G DSwitch-Mgmt Network-ephemeral"  -on=false -debug=true bootstrap-ocp4-01

[root@bastion-spodon ocp4]# export IPCFG="ip=172.21.11.156::172.21.11.1:255.255.255.0:::none nameserver=172.21.11.151"

[root@bastion-spodon ocp4]# govc vm.change -vm bootstrap-ocp4-01 -e "guestinfo.afterburn.initrd.network-kargs=${IPCFG}"


[root@bastion-spodon ocp4]# govc vm.change -vm bootstrap-ocp4-01 -e "guestinfo.ignition.config.data.encoding=base64"

[root@bastion-spodon ocp4]# govc vm.change -vm bootstrap-ocp4-01 -e "disk.EnableUUID=true"

[root@bastion-spodon ocp4]# govc vm.disk.change  -vm bootstrap-ocp4-01 -disk.key=0 -size 50G
```


b. Specifically just for the boostrap node, create `guestinfo.ignition.config.data` using console, this is due to base64 content size is too big for govc to handle.

```bash
[root@bastion-spodon ocp4]# bootstrap64=`cat bootstrap.b64`

[root@bastion-spodon ocp4]# govc vm.change -vm bootstrap-ocp4-01 -e "guestinfo.ignition.config.data=${bootstrap64}"
-bash: /usr/bin/govc: Argument list too long
```

 **Edit Settings** > **VM Options** >> **Advanced** >> **Configuration Parameters(EDIT CONFIGURATION...)**, then add `guestinfo.ignition.config.data` with content from bootstrap.b64 file, then **OK**.

c. Power on this bootstrap VM, then continue with master node VM creation.

4. Create Control Plane VM using govc client.

a. Create Control Plane and Worker VM from OVA VM Template

i. Control Plane 01
```bash

[root@bastion-spodon ocp4]# govc vm.clone -vm ocp4_8 -c=8 -m=24000 -dc="vSAN Datacenter" -ds=vsanDatastore -folder="Din VM" -net="1G DSwitch-Mgmt Network-ephemeral"  -on=false -debug=true controlplane-ocp4-01

[root@bastion-spodon ocp4]# export IPCFG="ip=172.21.11.155::172.21.11.1:255.255.255.0:::none nameserver=172.21.11.151"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-01 -e "guestinfo.afterburn.initrd.network-kargs=${IPCFG}"

[root@bastion-spodon ocp4]# controlplane64=`cat master.b64`

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-01 -e "guestinfo.ignition.config.data=${controlplane64}"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-01 -e "guestinfo.ignition.config.data.encoding=base64"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-01 -e "disk.EnableUUID=true"

[root@bastion-spodon ocp4]# govc vm.disk.change  -vm controlplane-ocp4-01 -disk.key=0 -size 100G
``` 


ii. Control Plane 02
```bash

[root@bastion-spodon ocp4]# govc vm.clone -vm ocp4_8 -c=8 -m=24000 -dc="vSAN Datacenter" -ds=vsanDatastore -folder="Din VM" -net="1G DSwitch-Mgmt Network-ephemeral"  -on=false -debug=true controlplane-ocp4-02

[root@bastion-spodon ocp4]# export IPCFG="ip=172.21.11.154::172.21.11.1:255.255.255.0:::none nameserver=172.21.11.151"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-02 -e "guestinfo.afterburn.initrd.network-kargs=${IPCFG}"

[root@bastion-spodon ocp4]# controlplane64=`cat master.b64`

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-02 -e "guestinfo.ignition.config.data=${controlplane64}"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-02 -e "guestinfo.ignition.config.data.encoding=base64"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-02 -e "disk.EnableUUID=true"

[root@bastion-spodon ocp4]# govc vm.disk.change  -vm controlplane-ocp4-02 -disk.key=0 -size 100G
``` 

iii. Control Plane 03
```bash

[root@bastion-spodon ocp4]# govc vm.clone -vm ocp4_8 -c=8 -m=24000 -dc="vSAN Datacenter" -ds=vsanDatastore -folder="Din VM" -net="1G DSwitch-Mgmt Network-ephemeral"  -on=false -debug=true controlplane-ocp4-03

[root@bastion-spodon ocp4]# export IPCFG="ip=172.21.11.153::172.21.11.1:255.255.255.0:::none nameserver=172.21.11.151"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-03 -e "guestinfo.afterburn.initrd.network-kargs=${IPCFG}"

[root@bastion-spodon ocp4]# controlplane64=`cat master.b64`

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-03 -e "guestinfo.ignition.config.data=${controlplane64}"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-03 -e "guestinfo.ignition.config.data.encoding=base64"

[root@bastion-spodon ocp4]# govc vm.change -vm controlplane-ocp4-03 -e "disk.EnableUUID=true"

[root@bastion-spodon ocp4]# govc vm.disk.change  -vm controlplane-ocp4-03 -disk.key=0 -size 100G
``` 


iv. Worker Node 01
```bash

[root@bastion-spodon ocp4]# govc vm.clone -vm ocp4_8 -c=8 -m=24000 -dc="vSAN Datacenter" -ds=vsanDatastore -folder="Din VM" -net="1G DSwitch-Mgmt Network-ephemeral"  -on=false -debug=true workernode-ocp4-01

[root@bastion-spodon ocp4]# export IPCFG="ip=172.21.11.160::172.21.11.1:255.255.255.0:::none nameserver=172.21.11.151"

[root@bastion-spodon ocp4]# govc vm.change -vm workernode-ocp4-01 -e "guestinfo.afterburn.initrd.network-kargs=${IPCFG}"

[root@bastion-spodon ocp4]# workernode64=`cat worker.b64`

[root@bastion-spodon ocp4]# govc vm.change -vm workernode-ocp4-01 -e "guestinfo.ignition.config.data=${workernode64}"

[root@bastion-spodon ocp4]# govc vm.change -vm workernode-ocp4-01 -e "guestinfo.ignition.config.data.encoding=base64"

[root@bastion-spodon ocp4]# govc vm.change -vm workernode-ocp4-01 -e "disk.EnableUUID=true"

[root@bastion-spodon ocp4]# govc vm.disk.change  -vm workernode-ocp4-01 -disk.key=0 -size 100G
``` 

v. Worker Node 02
```bash

[root@bastion-spodon ocp4]# govc vm.clone -vm ocp4_8 -c=8 -m=24000 -dc="vSAN Datacenter" -ds=vsanDatastore -folder="Din VM" -net="1G DSwitch-Mgmt Network-ephemeral"  -on=false -debug=true workernode-ocp4-02

[root@bastion-spodon ocp4]# export IPCFG="ip=172.21.11.161::172.21.11.1:255.255.255.0:::none nameserver=172.21.11.151"

[root@bastion-spodon ocp4]# govc vm.change -vm workernode-ocp4-02 -e "guestinfo.afterburn.initrd.network-kargs=${IPCFG}"

[root@bastion-spodon ocp4]# workernode64=`cat worker.b64`

[root@bastion-spodon ocp4]# govc vm.change -vm workernode-ocp4-02 -e "guestinfo.ignition.config.data=${workernode64}"

[root@bastion-spodon ocp4]# govc vm.change -vm workernode-ocp4-02 -e "guestinfo.ignition.config.data.encoding=base64"

[root@bastion-spodon ocp4]# govc vm.change -vm workernode-ocp4-02 -e "disk.EnableUUID=true"

[root@bastion-spodon ocp4]# govc vm.disk.change  -vm workernode-ocp4-02 -disk.key=0 -size 100G
``` 

5. Now, switch on all the VM and let the installation begin and completed.
