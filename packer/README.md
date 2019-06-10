# Building Rubber-Docker Workshop VMs

## Overview

This directory has two packer.json files that you can use to construct
VMs for the lab.  You'll need to [download
packer](https://www.packer.io/downloads.html) or [build it from
source](https://www.packer.io/docs/install/index.html#compiling-from-source).

Login using ubuntu/ubuntu for both VMs.

## AWS AMI

Set your AWS credentials as environmental variables and fill in a valid 
subnet ID from your VPC in rubber-docker-aws.json, then execute: 
```
packer build rubber-docker-aws.json 
```
Note that the source AMI is not accessible outside the region given
in the packer build file.

## VMware OVA 

Build on Mac OS X.  In addition to packer you'll need VMware Fusion
and ovftool. Execute the following:

```
packer build rubber-docker-vmware.json
ovftool packer-rubber-docker-ubuntu-16.04-vmware/rubber-docker-ubuntu-16.04.vmx rubber-docker-ubuntu-16.04.ova
```
The OVA is optional. You can also just start the VM directly in
VMware Fusion.

Note: The external network interface name on the VM may switch from
ens33 to ens32 when you export to ovftool and boot.  If this occurs
edit /etc/network/interfaces and switch the interface name to the
correct value.

## Licensing

VMware packer file rubber-docker-vmware.json and preseed.cfg are derived
from similar files published at 
https://github.com/geerlingguy/packer-ubuntu-1604 under the [MIT license](https://opensource.org/licenses/MIT). 
