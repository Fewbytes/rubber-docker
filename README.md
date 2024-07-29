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
### On AWS
There are currently 3 options to start the workshop by yourself:
 1. We created a public AMI with the required configuration and utilities
    already installed:
    | Region | AMI |
    |--------|-----|
    | eu-central-1 | `ami-041c4af571b01d0f8` |
    | il-central-1 | `ami-036406540dcc4a690` |
    | us-east-1 | `ami-0cb446a6fd2678063` |
    | us-west-1 | `ami-0defd345b84194d79` |
 1. We provide a [packer template](https://www.packer.io/) so you can create
    your own AMI.
 1. We have a [Vagrantfile](https://www.vagrantup.com/) for you to run using
    your favorite virtual machine hypervisor (NOTE: not yet fully tested).

### On Azure
We have a [packer template](https://www.packer.io/) so you can create your own
VM on Azure with the following procedure:

1. Build the image with Packer:
    ```bash
    $ packer build packer/rubber-docker-azure.json
    ```
1. Create the VM based on the new image:
   ```bash
   az vm create \
	--resource-group PackerImages \
	--name rubber-docker \
	--location westus2 \
	--image rubberDocker \
	--admin-user ubuntu \
	--generate-ssh-keys
    ```
1. Once the VM is built, you can connect to it with SSH with the username `ubuntu` and 
   newly created private key: 

    ```bash
    $ ssh ubuntu@<myPublicIP> -i ~/.ssh/ubuntu
    ```
The workshop material is checked out at `/workshop` on the instance:
- `/workshop/rubber-docker` - this repository, where you do all the work
- `/workshop/images` - images for containers, already populated with ubuntu and busybox images

Before starting the workshop, go over the prep docs in the `docs` folder.

Start the workshop at `/workshop/rubber-docker/levels/00_fork_exec`.

## Dev environment
If you need to build and install the `linux` module:

```sh
make install 
```

If you want a distributable wheel package:
```sh
make build
```


# PR stuff
This workshop has been publicly given in many places starting February 2016.

- Opstalk meetup, Tel-Aviv, February 2016
- DevOps Sydney meetup, Sydney, June 2016
- DevOpsDays Amsterdam, Amsterdam, June 2016
- SRECon EU, Dublin, July 2016
- Sela Developer Practice, Tel-Aviv, June 2016
- SRECon US, Santa Clara, March 2018
- DevOpsDays Kiel, Kiel, May 2018

# FAQ
### Why did you create this?
Because we feel the only way to truly understand something to build it from scratch - and Linux containers are a very hyped and poorly understood technology

### Can I use this repository to conduct my own public/private workshop?
Of course! If you do, please consider letting us know on Twitter (@nukemberg and @nocoot) and of course send feedback.

### This workshop doesn't cover seccomp/user containers/whatever
Yes, no way we can cover the entire featureset of a real container engine. We tried to concentrate on thing we believe are important for understanding how containers work

### I found a bug!
See contributions below


# Contributions
Contributions are welcome! If you found a bug or something to improve feel free to open an issue or a pull request. Please note that the entire repository is under MIT license and your contribution will be under that license.

# Sponsors
We'd like to thank our friends at [Strigo.io](http://strigo.io/) for kindly providing their platform, and allowing us to deliver this and other workshops without worrying about infrastructure.
If you plan to deliver this workshop yourself, we highly encourage you to [contact them](contact@strigo.io).
