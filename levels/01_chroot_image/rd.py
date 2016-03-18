#!/usr/bin/env python2.7
#
# Docker From Scratch Workshop
# Level 1 - chrooting into an image
#
# Goal: Let's get some filesystem isolation with good ol' chroot
#       i.e. running:
#                rd.py run -i ubuntu /bin/sh
#            will:
#               fork a new process
#                   The child will:
#                       - unpack an ubuntu image into a new directory
#                       - chroot() into that directory
#                       - exec '/bin/sh'
#                   The parent waits for it to finish.
#

from __future__ import print_function

import os
import tarfile
import uuid

import click

import linux


def _get_image_path(image_name, image_dir, image_suffix='tar'):
    return os.path.join(image_dir, os.extsep.join([image_name, image_suffix]))


def _get_container_path(container_id, container_dir, *subdir_names):
    return os.path.join(container_dir, container_id, *subdir_names)


def create_container_root(image_name, image_dir, container_id, container_dir):
    """
    Create a container root by extracting an image into a new directory
    Usage:
    new_root = create_container_root(image_name, image_dir, container_id, container_dir)

    @param image_name: the image name to extract
    @param image_dir: the directory to lookup image tarballs in
    @param container_id: the unique container id
    @param container_dir: the base directory of newly generated container directories
    @retrun: new container root directory
    @rtype: str
    """
    image_path = _get_image_path(image_name, image_dir)
    container_root = _get_container_path(container_id, container_dir, 'rootfs')

    assert os.path.exists(image_path), "unable to locate image %s" % image_name

    if not os.path.exists(container_root):
        os.makedirs(container_root)

    with tarfile.open(image_path) as t:
        # Fun fact: tar files may contain *nix devices! *facepalm*
        t.extractall(container_root, members=[m for m in t.getmembers() if m.type not in (tarfile.CHRTYPE, tarfile.BLKTYPE)])

    return container_root


@click.group()
def cli():
    pass


def contain(command, image_name, image_dir, container_id, container_dir):
    # TODO: would you like to do something before chrooting?
    # print('Created a new root fs for our container: {}'.format(new_root))

    # TODO: chroot into new_root
    # TODO: something after chrooting?

    os.execvp(command[0], command)


@cli.command()
@click.option('--image-name', '-i', help='Image name', default='ubuntu')
@click.option('--image-dir', help='Images directory', default='/workshop/images')
@click.option('--container-dir', help='Containers directory', default='/workshop/containers')
@click.argument('Command', required=True, nargs=-1)
def run(image_name, image_dir, container_dir, command):
    container_id = str(uuid.uuid4())
    pid = os.fork()
    if pid == 0:
        # This is the child, we need to exec the command
        contain(command, image_name, image_dir, container_id, container_dir)
    else:
        # This is the parent, pid contains the PID of the forked process
        _, status = os.waitpid(pid, 0)  # wait for the forked child, fetch the exit status
        print('{} exited with status {}'.format(pid, status))


if __name__ == '__main__':
    cli()
