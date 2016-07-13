#!/usr/bin/env python2.7
"""Docker From Scratch Workshop - Level 4: Add overlay FS.

Goal: Instead of re-extracting the image, use it as a read-only layer
      (lowerdir), and create a copy-on-write layer for changes (upperdir).

HINT: Don't forget that overlay fs also requires a workdir.

Read more on overlay FS here:
https://www.kernel.org/doc/Documentation/filesystems/overlayfs.txt
"""

from __future__ import print_function

import linux
import tarfile
import uuid

import click
import os
import stat
import traceback


def _get_image_path(image_name, image_dir, image_suffix='tar'):
    return os.path.join(image_dir, os.extsep.join([image_name, image_suffix]))


def _get_container_path(container_id, container_dir, *subdir_names):
    return os.path.join(container_dir, container_id, *subdir_names)


def create_container_root(image_name, image_dir, container_id, container_dir):
    image_path = _get_image_path(image_name, image_dir)
    assert os.path.exists(image_path), "unable to locate image %s" % image_name

    # TODO: Instead of creating the container_root and extracting to it,
    #       create an images_root.
    # keep only one rootfs per image and re-use it
    container_root = _get_container_path(container_id, container_dir, 'rootfs')

    if not os.path.exists(container_root):
        os.makedirs(container_root)
        with tarfile.open(image_path) as t:
            # Fun fact: tar files may contain *nix devices! *facepalm*
            members = [m for m in t.getmembers()
                       if m.type not in (tarfile.CHRTYPE, tarfile.BLKTYPE)]
            t.extractall(container_root, members=members)

    # TODO: create directories for copy-on-write (uppperdir), overlay workdir,
    #       and a mount point

    # TODO: mount the overlay (HINT: use the MS_NODEV flag to mount)

    return container_root  # return the mountpoint for the mounted overlayfs


@click.group()
def cli():
    pass


def makedev(dev_path):
    for i, dev in enumerate(['stdin', 'stdout', 'stderr']):
        os.symlink('/proc/self/fd/%d' % i, os.path.join(dev_path, dev))
    os.symlink('/proc/self/fd', os.path.join(dev_path, 'fd'))
    # Add extra devices
    DEVICES = {'null': (stat.S_IFCHR, 1, 3), 'zero': (stat.S_IFCHR, 1, 5),
               'random': (stat.S_IFCHR, 1, 8), 'urandom': (stat.S_IFCHR, 1, 9),
               'console': (stat.S_IFCHR, 136, 1), 'tty': (stat.S_IFCHR, 5, 0),
               'full': (stat.S_IFCHR, 1, 7)}
    for device, (dev_type, major, minor) in DEVICES.iteritems():
        os.mknod(os.path.join(dev_path, device),
                 0666 | dev_type, os.makedev(major, minor))


def _create_mounts(new_root):
    # Create mounts (/proc, /sys, /dev) under new_root
    linux.mount('proc', os.path.join(new_root, 'proc'), 'proc', 0, '')
    linux.mount('sysfs', os.path.join(new_root, 'sys'), 'sysfs', 0, '')
    linux.mount('tmpfs', os.path.join(new_root, 'dev'), 'tmpfs',
                linux.MS_NOSUID | linux.MS_STRICTATIME, 'mode=755')

    # Add some basic devices
    devpts_path = os.path.join(new_root, 'dev', 'pts')
    if not os.path.exists(devpts_path):
        os.makedirs(devpts_path)
        linux.mount('devpts', devpts_path, 'devpts', 0, '')

    makedev(os.path.join(new_root, 'dev'))


def contain(command, image_name, image_dir, container_id, container_dir):
    linux.unshare(linux.CLONE_NEWNS)  # create a new mount namespace

    linux.mount(None, '/', None, linux.MS_PRIVATE | linux.MS_REC, None)

    new_root = create_container_root(
        image_name, image_dir, container_id, container_dir)
    print('Created a new root fs for our container: {}'.format(new_root))

    _create_mounts(new_root)

    old_root = os.path.join(new_root, 'old_root')
    os.makedirs(old_root)
    linux.pivot_root(new_root, old_root)

    os.chdir('/')

    linux.umount2('/old_root', linux.MNT_DETACH)  # umount old root
    os.rmdir('/old_root') # rmdir the old_root dir
    os.execvp(command[0], command)


@cli.command()
@click.option('--image-name', '-i', help='Image name', default='ubuntu')
@click.option('--image-dir', help='Images directory',
              default='/workshop/images')
@click.option('--container-dir', help='Containers directory',
              default='/workshop/containers')
@click.argument('Command', required=True, nargs=-1)
def run(image_name, image_dir, container_dir, command):
    container_id = str(uuid.uuid4())

    pid = os.fork()
    if pid == 0:
        # This is the child, we'll try to do some containment here
        try:
            contain(command, image_name, image_dir, container_id,
                    container_dir)
        except Exception:
            traceback.print_exc()
            os._exit(1)  # something went wrong in contain()

    # This is the parent, pid contains the PID of the forked process
    # wait for the forked child, fetch the exit status
    _, status = os.waitpid(pid, 0)
    print('{} exited with status {}'.format(pid, status))


if __name__ == '__main__':
    cli()
