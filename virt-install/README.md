

## virt-install (Tested on 4.7.16)

1. Create a working direction on the virt-install client node.
```bash
[root@bastion ~]# mkdir rhcosbin
```

2. Download live-initramfs and live-kernel into virt-install client node.
```bash
[root@bastion ~]# cd rhcosbin
[root@bastion ~]# wget https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.7/latest/rhcos-4.7.13-x86_64-live-kernel-x86_64
[root@bastion ~]# wget https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.7/latest/rhcos-4.7.13-x86_64-live-initramfs.x86_64.img
```

3. Create a treeinfo file with below content.
```bash
[root@bastion ~]# cat .treeinfo
[general]
family = Fedora
version = 29
arch = x86_64
platforms = x86_64
[images-x86_64]
initrd = rhcos-4.7.13-x86_64-live-initramfs.x86_64.img
kernel = rhcos-4.7.13-x86_64-live-kernel-x86_64
```

4. Now we need a live rootfs downloaded into webserver.
```bash
[root@bastion ~]# cd /var/www/html/openshift4
[root@bastion ~]# wget https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.7/latest/rhcos-live-rootfs.x86_64.img
[root@bastion ~]# chown www-data. * 
```

5. Assuming ignition configs already created and placed in the webserver, we now create the virtual machine.
* Bootstrap

```bash
[root@bastion ~]# cd rhcosbin
[root@bastion ~]# virt-install --connect=qemu+ssh://root@hypervisor/system --name="bootstrap.c01" --vcpus=4 --ram=8192 \
--disk path=/var/lib/libvirt/images/bootstrap.qcow2,bus=virtio,size=60 \
--os-variant rhel8.0 --network type=direct,source=enp10s0,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/bootstrap.ign ip=192.168.254.60::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole
```

* Master
```bash
[root@bastion ~]# virt-install --connect=qemu+ssh://root@hypervisor/system --name="master01.c01" --vcpus=6 --ram=10240 \
--disk path=/var/lib/libvirt/images/master01.qcow2,bus=virtio,size=80 \
--os-variant rhel8.0 --network type=direct,source=enp10s0,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/master.ign ip=192.168.254.61::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole

[root@bastion ~]# virt-install --connect=qemu+ssh://root@hypervisor/system --name="master02.c01" --vcpus=6 --ram=10240 \
--disk path=/var/lib/libvirt/images/master02.qcow2,bus=virtio,size=80 \
--os-variant rhel8.0 --network type=direct,source=enp10s0,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/master.ign ip=192.168.254.62::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole

[root@bastion ~]# virt-install --connect=qemu+ssh://root@hypervisor/system --name="master03.c01" --vcpus=6 --ram=10240 \
--disk path=/var/lib/libvirt/images/master03.qcow2,bus=virtio,size=80 \
--os-variant rhel8.0 --network type=direct,source=enp10s0,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/master.ign ip=192.168.254.63::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole
```

* Worker
```bash
[root@bastion ~]# virt-install --connect=qemu:///system --name="worker01.c01" --vcpus=8 --ram=24576 \
--disk path=/var/lib/libvirt/images/worker01.qcow2,bus=virtio,size=80 \
--os-variant rhel8.0 --network type=direct,source=enp0s31f6,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/worker.ign ip=192.168.254.64::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole

[root@bastion ~]# virt-install --connect=qemu:///system --name="worker02.c01" --vcpus=8 --ram=24576 \
--disk path=/var/lib/libvirt/images/worker02.qcow2,bus=virtio,size=80 \
--os-variant rhel8.0 --network type=direct,source=enp0s31f6,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/worker.ign ip=192.168.254.65::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole

[root@bastion ~]# virt-install --connect=qemu:///system --name="worker03.c01" --vcpus=8 --ram=24576 \
--disk path=/var/lib/libvirt/images/worker03.qcow2,bus=virtio,size=80 \
--os-variant rhel8.0 --network type=direct,source=enp0s31f6,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/worker.ign ip=192.168.254.66::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole
```

* Router
```bash
[root@bastion ~]# virt-install --connect=qemu:///system --name="router01.c01" --vcpus=6 --ram=8096 \
--disk path=/var/lib/libvirt/images/router01.qcow2,bus=virtio,size=80 \
--os-variant rhel8.0 --network type=direct,source=enp0s31f6,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/worker.ign ip=192.168.254.67::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole

[root@bastion ~]# virt-install --connect=qemu:///system --name="router02.c01" --vcpus=6 --ram=8096 \
--disk path=/var/lib/libvirt/images/router01.qcow2,bus=virtio,size=80 \
--os-variant rhel8.0 --network type=direct,source=enp0s31f6,source_mode=bridge,model=virtio \
--boot menu=on --location ./ --extra-args "rd.neednet=1 coreos.inst=yes coreos.inst.install_dev=/dev/vda coreos.live.rootfs_url=http://192.168.254.254:9090/openshift4/rhcos-live-rootfs.x86_64.img coreos.inst.ignition_url=http://192.168.254.254:9090/openshift4/worker.ign ip=192.168.254.68::192.168.254.1:255.255.255.0::enp1s0:none nameserver=192.168.254.254 " --noautoconsole
```