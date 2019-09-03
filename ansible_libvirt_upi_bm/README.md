[![techbeatly](https://www.techbeatly.com/wp-content/uploads/2018/05/techbeatly-logo-v1.png)](https://www.techbeatly.com/)

## Introduction

#Pre-Req
* Ansible Core 2.8
* python-ldap (or python3-ldap depends on your setup)
* Update VM template corresponding to your host capabilities. (02-provision_ocp_nodes/roles/deploy_ocpvms/templates/machine-template.xml.j2)
* Pull secret 
* Core user ssh public key
* DNS Configured (i`m using IdM as DNS server under 01-setup_idm_dns)

There are four main parts in this playbook.

  * 1. Prepare & Configure Helper Node (DNS is out of scope).  
      * In this repo I`m using IdM as DNS server, so there is IdM related DNS configuration playbook.      
  * 2. Preparation, Configuring and Deploying VM.
  * 3. Clean up and deprovisioning VM.

All variables are stored in `group_vars` directory as much as possible with vaulted data for sensitive piece.

### 1. Inventory

An inventory file should look like this with groups:
```
[ocp4_nodes] # All OCP4 Nodes
bootstrap.ocp4.local.bytewise.my
master01.ocp4.local.bytewise.my
master02.ocp4.local.bytewise.my
master03.ocp4.local.bytewise.my
worker01.ocp4.local.bytewise.my
worker02.ocp4.local.bytewise.my
worker03.ocp4.local.bytewise.my

[ocp4_bootstrap_vm] # OCP4 Bootstrap Node
bootstrap.ocp4.local.bytewise.my

[ocp4_master_vm] # OCP4 Master Node
bootstrap.ocp4.local.bytewise.my
master01.ocp4.local.bytewise.my
master02.ocp4.local.bytewise.my
master03.ocp4.local.bytewise.my

[ocp4_worker_vm] # OCP4 Worker Node 
worker01.ocp4.local.bytewise.my
worker02.ocp4.local.bytewise.my
worker03.ocp4.local.bytewise.my

[helper_vm] # Helper Node, not OCP4 node.
bastion4.bytewise.my # Should only be stated here, not everywhere else!
```

### 2. Variables

#### Group Variables
There are vault protected variable exists in:

* group_vars/all/vars.yml
* group_vars/helper_vm/vars.yml

Use ansible-vault to encrypt (or dont!) your data:

```
ansible-vault encrypt_string 'ssh-rsa AAAA REDACTED'
```

#### Host Variable
All host variable should be place in `host_vars` directory, with their content in this repo are all required hostvars for each node group.



### 3. Setup Helper Node

A. This node already installed (RHEL 7 or RHEL 8, I`m using RHEL 8) and basic OS configured. We are just running playbook against this node.

B. To execute this playbook (with become sudo):
```
#> cd 00-setup_helper_node
#> ansible-playbook -i ../inventory  site.yml  -u root -K  -b
BECOME password: 
```

What this will do:
* Install all packages required.
* Configure firewall rules and selinux.
* Initial configuration for:
  * OCP CLI Client & Installer Binary
  * PXE 



### 4. Provision OCP Node

This playbook will configure above helper node initial config with all OCP nodes information including:

* DHCP.
* LB (a HAProxy software LB).
* PXE (with mac-address based pxelinux.cfg, so it will autoboot with correct menu).
* Configure Ignition Files.
* Create storage for VM (there are storage profiling involved in my env).
* Defined VM into Libvirt from machine template yaml.


To execute this playbook (as localhost on Libvirt host):

```
#> cd 02-provision_ocp_nodes
#> ansible-playbook  -i ../inventory  site.yml  -u root -K -b
BECOME password: 
Pull secret from cloud.redhat.com: {"auths":{"cloud.openshift.com":......redhat.com"}}}
Core SSH Public key: ssh-rsa ......redhat.com

```


### 5. Deprovisioning OCP Node

This playbook do below clean up:
* Stop and remove all OCP node (not Helper node).
* Clean up storage from provisioned play above.

To execute VM clean up:

```
#> cd zz-delete_ocpvm
#> ansible-playbook  -i ../inventory  site.yml  -u root -K -b
BECOME password: 
```
