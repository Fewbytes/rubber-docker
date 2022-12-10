#!/usr/bin/env python2.7
"""Docker From Scratch Workshop - Level 9: Add Memory Control group.

Goal: prevent your container from eating all the RAM.
"""

from __future__ import print_function

import linux
import tarfile
import uuid

import click
import os
import stat


def _get_image_path(image_name, image_dir, image_suffix='tar'):
    return os.path.join(image_dir, os.extsep.join([image_name, image_suffix]))


def _get_container_path(container_id, base_path, *subdir_names):
    return os.path.join(base_path, container_id, *subdir_names)


def create_container_root(image_name, image_dir, container_id, container_dir):
    image_path = _get_image_path(image_name, image_dir)
    image_root = os.path.join(image_dir, image_name, 'rootfs')

    assert os.path.exists(image_path), "unable to locate image %s" % image_name

    if not os.path.exists(image_root):
        os.makedirs(image_root)
        with tarfile.open(image_path) as t:
            # Fun fact: tar files may contain *nix devices! *facepalm*
            members = [m for m in t.getmembers()
                       if m.type not in (tarfile.CHRTYPE, tarfile.BLKTYPE)]
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(t, image_root, members=members)

    # Create directories for copy-on-write (uppperdir), overlay workdir,
    # and a mount point
    container_cow_rw = _get_container_path(
        container_id, container_dir, 'cow_rw')
    container_cow_workdir = _get_container_path(
        container_id, container_dir, 'cow_workdir')
    container_rootfs = _get_container_path(
        container_id, container_dir, 'rootfs')
    for d in (container_cow_rw, container_cow_workdir, container_rootfs):
        if not os.path.exists(d):
            os.makedirs(d)

    # Mount the overlay (HINT: use the MS_NODEV flag to mount)
    linux.mount(
        'overlay', container_rootfs, 'overlay', linux.MS_NODEV,
        "lowerdir={image_root},upperdir={cow_rw},workdir={cow_workdir}".format(
            image_root=image_root,
            cow_rw=container_cow_rw,
            cow_workdir=container_cow_workdir))

    return container_rootfs  # return the mountpoint for the overlayfs


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
                 0o666 | dev_type, os.makedev(major, minor))


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


def _setup_cpu_cgroup(container_id, cpu_shares):
    CPU_CGROUP_BASEDIR = '/sys/fs/cgroup/cpu'
    container_cpu_cgroup_dir = os.path.join(
        CPU_CGROUP_BASEDIR, 'rubber_docker', container_id)

    # Insert the container to new cpu cgroup named 'rubber_docker/container_id'
    if not os.path.exists(container_cpu_cgroup_dir):
        os.makedirs(container_cpu_cgroup_dir)
    tasks_file = os.path.join(container_cpu_cgroup_dir, 'tasks')
    open(tasks_file, 'w').write(str(os.getpid()))

    # If (cpu_shares != 0)  => set the 'cpu.shares' in our cpu cgroup
    if cpu_shares:
        cpu_shares_file = os.path.join(container_cpu_cgroup_dir, 'cpu.shares')
        open(cpu_shares_file, 'w').write(str(cpu_shares))


def contain(command, image_name, image_dir, container_id, container_dir,
            cpu_shares, memory, memory_swap):
    _setup_cpu_cgroup(container_id, cpu_shares)

    # TODO: similarly to the CPU cgorup, add Memory cgroup support here
    #       setup memory -> memory.limit_in_bytes,
    #       memory_swap -> memory.memsw.limit_in_bytes if they are not None

    linux.sethostname(container_id)  # Change hostname to container_id

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
    os.rmdir('/old_root')  # rmdir the old_root dir

    os.execvp(command[0], command)


@cli.command(context_settings=dict(ignore_unknown_options=True,))
@click.option('--memory',
              help='Memory limit in bytes.'
              ' Use suffixes to represent larger units (k, m, g)',
              default=None)
@click.option('--memory-swap',
              help='A positive integer equal to memory plus swap.'
              ' Specify -1 to enable unlimited swap.',
              default=None)
@click.option('--cpu-shares', help='CPU shares (relative weight)', default=0)
@click.option('--image-name', '-i', help='Image name', default='ubuntu')
@click.option('--image-dir', help='Images directory',
              default='/workshop/images')
@click.option('--container-dir', help='Containers directory',
              default='/workshop/containers')
@click.argument('Command', required=True, nargs=-1)
def run(memory, memory_swap, cpu_shares, image_name, image_dir, container_dir,
        command):
    container_id = str(uuid.uuid4())

    # linux.clone(callback, flags, callback_args) is modeled after the Glibc
    # version. see: "man 2 clone"
    flags = (linux.CLONE_NEWPID | linux.CLONE_NEWNS | linux.CLONE_NEWUTS |
             linux.CLONE_NEWNET)
    callback_args = (command, image_name, image_dir, container_id,
                     container_dir, cpu_shares, memory, memory_swap)
    pid = linux.clone(contain, flags, callback_args)

    # This is the parent, pid contains the PID of the forked process
    # Wait for the forked child, fetch the exit status
    _, status = os.waitpid(pid, 0)
    print('{} exited with status {}'.format(pid, status))


if __name__ == '__main__':
    cli()
