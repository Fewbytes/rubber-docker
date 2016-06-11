# Docker From Scratch Workshop


## Preparatory Talk
[The preparatory talk](https://docs.google.com/presentation/d/10vFQfEUvpf7qYyksNqiy-bAxcy-bvF0OnUElCOtTTRc/edit?usp=sharing) covers all the basics you'll need for this workshop, including: Linux syscalls and glibc wrappers, chroot vs pivot_root, namespaces, cgroups, capabilities and more.

## The Workshop
Use [the provided slides](https://github.com/Fewbytes/rubber-docker/tree/master/slides) while advancing through the levels, adding more features to your container. Remember to go over each level's readme, and if things get rough- you can always find the solution for level N in level N+1 skeleton.

## Quickstart
There are currently 3 options to start the workshop by yourself:

 1. We created a public AMI with the required configuration and utilities already installed: ami-8faab0e3 (eu-west-1)
 2. We provide a [packer template](https://www.packer.io/) so you can create your own AMI
 3. We have a [Vagrantfile](https://www.vagrantup.com/) for you to run using your favorite virtual machine hypervisor (NOTE: still not fully tested)
