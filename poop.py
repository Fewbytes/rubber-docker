#!/usr/bin/env python

import linux
import tarfile
import os
import uuid


def recover():
    try:
        for mount in ['proc', 'sys', 'dev']:
            linux.umount('/mnt/cowfs/' + mount)
        linux.umount('/mnt/cowfs')
        if os.path.exists('/mnt/cowfs_rw/old_root'):
            os.rmdir('/mnt/cowfs_rw/old_root')
    except Exception:
        pass


def prepare_rootfs():
    for directory in ['/mnt/rootfs', '/mnt/cowfs', '/mnt/cowfs_rw', '/mnt/cowfs_workdir']:
        if not os.path.exists(directory):
            os.makedirs(directory)

    with tarfile.open('/vagrant/busybox.tar.gz') as t:
        t.extractall('/mnt/rootfs')

    linux.mount('overlay', '/mnt/cowfs', 'overlay',
                linux.MS_NODEV, "lowerdir=/mnt/rootfs,upperdir=/mnt/cowfs_rw,workdir=/mnt/cowfs_workdir")


def mount_sysfs(new_root):
    for mount in ['/proc', '/sys', '/dev']:
        linux.mount(mount, new_root + mount, 'none', linux.MS_BIND, '')


def contain():
    linux.unshare(linux.CLONE_NEWNS)

    os.mkdir('/mnt/cowfs/old_root')
    try:
        linux.pivot_root("/mnt/cowfs", "/mnt/cowfs/old_root")
        linux.umount('/mnt/cowfs/old_root')
        os.rmdir('/mnt/cowfs/old_root')
        # os.chroot('/mnt/cowfs')
        os.chdir('/')
        linux.unshare(linux.CLONE_NEWIPC)
        linux.unshare(linux.CLONE_NEWUTS)
        linux.unshare(linux.CLONE_NEWNET)
        linux.sethostname(str(uuid.uuid1()))
        os.execv("/bin/sh", ['/bin/sh'])
    except Exception:
        raise


prepare_rootfs()
mount_sysfs('/mnt/cowfs')

pid = os.fork()
if pid == 0:
    contain()
else:
    os.waitpid(pid, 0)
    recover()
