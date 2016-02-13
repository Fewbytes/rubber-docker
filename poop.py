#!/usr/bin/env python

import linux
import tarfile
import os
import uuid
import shutil


def recover():
    for mount in ['proc', 'sys', 'dev/pts']:
        try:
            linux.umount('/mnt/cowfs/' + mount)
        except Exception as e:
            print "Exception: %r" % e

    try:
        linux.umount('/mnt/cowfs')
    except Exception as e:
        print "Exception: %r" % e


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
    linux.mount('tmpfs', os.path.join(new_root, 'dev'), 'tmpfs',
                linux.MS_NOSUID | linux.MS_STRICTATIME, 'mode=755')
    pts_dir = os.path.join(new_root, 'dev', 'pts')
    if not os.path.exists(pts_dir):
        os.makedirs(pts_dir)
    linux.mount('devpts', pts_dir, 'devpts', 0, '')
    for i, dev in enumerate(['stdin', 'stdout', 'stderr']):
        os.symlink('/proc/self/fd/%d' % i, os.path.join(new_root, 'dev', dev))


def contain():
    linux.mount(None, '/', None, linux.MS_PRIVATE, None)
    new_root = prepare_rootfs()
    old_root = os.path.join(new_root, 'old_root')
    os.mkdir(old_root)
    try:
        mount_sysfs(new_root)
        linux.pivot_root(new_root, old_root)
        os.chdir('/')
        linux.mount(None, '/old_root', None, linux.MS_PRIVATE | linux.MS_REC, None)
        linux.umount2('/old_root', linux.MNT_DETACH)
        os.rmdir('/old_root')
        linux.unshare(linux.CLONE_NEWIPC)
        linux.unshare(linux.CLONE_NEWUTS)
        linux.unshare(linux.CLONE_NEWNET)
        linux.sethostname(str(uuid.uuid1()))
    except Exception:
        raise

    os.execv("/bin/sh", ['/bin/sh'])

linux.unshare(linux.CLONE_NEWPID)  # forks will be in a new PID namespace
linux.unshare(linux.CLONE_NEWNS)  # new mount namespace

pid = os.fork()
if pid == 0:
    contain()
else:
    pid, status = os.waitpid(pid, 0)
    print status
    #recover()
