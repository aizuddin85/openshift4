## Introduction

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
bootstrap.ocp4.bytewise.com.my
master01.ocp4.bytewise.com.my
master02.ocp4.bytewise.com.my
master03.ocp4.bytewise.com.my
worker01.ocp4.bytewise.com.my
worker02.ocp4.bytewise.com.my
worker03.ocp4.bytewise.com.my

[ocp4_bootstrap_vm] # OCP4 Bootstrap Node
bootstrap.ocp4.bytewise.com.my

[ocp4_master_vm] # OCP4 Master Node
bootstrap.ocp4.bytewise.com.my
master01.ocp4.bytewise.com.my
master02.ocp4.bytewise.com.my
master03.ocp4.bytewise.com.my

[ocp4_worker_vm] # OCP4 Worker Node 
worker01.ocp4.bytewise.com.my
worker02.ocp4.bytewise.com.my
worker03.ocp4.bytewise.com.my

[helper_vm] # Helper Node, not OCP4 node.
bastion4.bytewise.com.my # Should only be stated here, not everywhere else!
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
#> ansible-playbook -i ../inventory  site.yml  -K --ask-vault-pass   -b
BECOME password: 
Vault password: 
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
#> ansible-playbook -i ../inventory  site.yml  -K --ask-vault-pass
```


### 5. Deprovisioning OCP Node

This playbook do below clean up:
* Stop and remove all OCP node (not Helper node).
* Clean up storage from provisioned play above.

To execute VM clean up:

```
#> cd zz-delete_ocpvm
#> ansible-playbook -i ../inventory  site.yml  -K --ask-vault-pass   -b
BECOME password: 
Vault password: 
```
