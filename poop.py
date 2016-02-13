#!/usr/bin/env python

import linux
import tarfile
import os
import uuid
import resource
import shutil


def recover():
    try:
        for mount in ['proc', 'sys', 'dev']:
            linux.umount('/mnt/cowfs/' + mount)
        linux.umount('/mnt/cowfs')
    except Exception:
        pass


def prepare_rootfs():
    shutil.rmtree("/mnt/cowfs_rw")
    for directory in ['/mnt/rootfs', '/mnt/cowfs', '/mnt/cowfs_rw', '/mnt/cowfs_workdir']:
        if not os.path.exists(directory):
            os.makedirs(directory)

    with tarfile.open('/vagrant/busybox.tar.gz') as t:
        t.extractall('/mnt/rootfs')

    linux.mount('overlay', '/mnt/cowfs', 'overlay',
                linux.MS_NODEV,
                "lowerdir=/mnt/rootfs,upperdir=/mnt/cowfs_rw,workdir=/mnt/cowfs_workdir")

    # linux.mount('aufs', '/mnt/cowfs', 'aufs', linux.MS_NODEV, 'br:/mnt/cowfs_rw:/mnt/rootfs')
    return '/mnt/cowfs'


def mount_sysfs(new_root):
    linux.mount('proc', os.path.join(new_root, 'proc'), 'proc', 0, '')
    linux.mount('sysfs', os.path.join(new_root, 'sys'), 'sysfs', 0, '')
    pts_dir = os.path.join(new_root, 'dev', 'pts')
    if not os.path.exists(pts_dir):
        os.makedirs(pts_dir)
    linux.mount('devpts', pts_dir, 'devpts', 0, '')
    for i, dev in enumerate(['stdin', 'stdout', 'stderr']):
        os.symlink('/proc/self/fd/%d' % i, os.path.join(new_root, 'dev', dev))


def close_fds():
    for fd in range(0, resource.getrlimit(resource.RLIMIT_NOFILE)[1]):
        try:
            os.close(fd)
        except Exception:
            pass


def contain():
    linux.unshare(linux.CLONE_NEWNS)
    new_root = prepare_rootfs()
    os.mkdir(os.path.join(new_root, 'old_root'))
    try:
        mount_sysfs(new_root)
        linux.pivot_root("/mnt/cowfs", "/mnt/cowfs/old_root")
        os.chdir('/')
        linux.unshare(linux.CLONE_NEWIPC)
        linux.unshare(linux.CLONE_NEWUTS)
        linux.unshare(linux.CLONE_NEWNET)
        linux.sethostname(str(uuid.uuid1()))
        linux.umount2('/old_root', linux.MNT_DETACH)
        os.rmdir('/old_root')
        os.execv("/bin/sh", ['/bin/sh'])
    except Exception:
        raise


linux.unshare(linux.CLONE_NEWPID)

pid = os.fork()
if pid == 0:
    # close_fds()
    contain()
else:
    os.waitpid(pid, 0)
    recover()
