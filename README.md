# Docker From Scratch Workshop


## Preparatory Talk
[The preparatory talk](https://docs.google.com/presentation/d/10vFQfEUvpf7qYyksNqiy-bAxcy-bvF0OnUElCOtTTRc/edit?usp=sharing)
covers all the basics you'll need for this workshop, including:
- Linux syscalls and glibc wrappers
- chroot vs pivot_root
- namespaces
- cgroups
- capabilities
- and more

## The Workshop
Use [the provided slides](https://github.com/Fewbytes/rubber-docker/tree/master/slides) while advancing through the levels, adding more features to your container.
Remember to go over each level's readme, and if things get rough -
you can always find the solution for level N in the level N+1 skeleton.

## The linux python module
Not all the necessary system calls are exposed in python's standard library.
In addition, we want to preserve the semantics of the system calls and use them as if we were writing C.
We therefore wrote a python module called *linux* (take a look at [linux.c](linux.c)) which exposes the relevant system calls. 
Have a look at the [module documentation](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html) for more info.

## Quickstart
There are currently 3 options to start the workshop by yourself:
 1. We created a public AMI with the required configuration and utilities
    already installed: ami-8faab0e3 (eu-central-1).
 1. We provide a [packer template](https://www.packer.io/) so you can create
    your own AMI.
 1. We have a [Vagrantfile](https://www.vagrantup.com/) for you to run using
    your favorite virtual machine hypervisor (NOTE: not yet fully tested).

The workshop material in checked in `/workshop` on the instance:
- `/workshop/rubber-docker` - this repository, where you do all the work
- `/workshop/images` - images for containers, already populated with ubuntu and busybox images

Before starting the workshop, go over the prep docs in the `docs` folder.

Start the workshop at `/workshop/rubber-docker/levels/00_fork_exec`.
