# Level 01: chroot

"Jail" a process so it doesn't see the rest of the file system.

To exec a process in a chroot we need a few things:
 1. Choose a new root directory for the process
   1. with our target binary
   1. with any other dependency (proc? sys? dev?)
 1. Chroot into it using Python's [os.chroot](https://docs.python.org/2/library/os.html#os.chroot)

To help you get there quickly, we implemented *create_container_root()* which extracts pre-downloaded images (ubuntu OR busybox), and returns a path.

If we want tools like `ps` to work properly, we need to mount the special filesystems like `/proc`, `/sys` and `/dev` inside the new root.
This can be done using the [linux python module](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html) which exposes the [mount()](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html#linux.mount) syscall:

```python
linux.mount('proc', os.path.join(new_root, 'proc'), 'proc', 0, '')
```
The semantics of the *mount()* syscall have been preserved; to learn more about it read `man 2 mount`.

From within the chroot, have a look at `/proc/mounts`. Does it look different from `/proc/mounts` outside the chroot?
Remember we are not using mount namespace yet!

(*answer*: [linux/fs/proc_namespace.c on Github](https://github.com/torvalds/linux/blob/33caf82acf4dc420bf0f0136b886f7b27ecf90c5/fs/proc_namespace.c#L110))

## Cleaning up

You might notice upon completing this level that you have many unused entries in */proc/mounts* and many unused extracted images in */workshop/containers*. You can use [our cleanup script](../cleanup.sh) to remove them quickly.

## Relevant Documentation

[chroot manpage](http://linux.die.net/man/2/chroot)

## How to check your work

Without extracting an image:
```shell
$ sudo python rd.py run -i ubuntu -- /bin/ls -l /workshop/rubber-docker/levels/
total 44
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 00_fork_exec
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 01_chroot_image
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 02_mount_ns
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 03_pivot_root
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 04_overlay
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 05_uts_namespace
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 06_pid_namespace
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 07_net_namespace
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 08_cpu_cgroup
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 09_memory_cgorup
drwxr-xr-x 2 ubuntu ubuntu 4096 Jun 20 21:37 10_setuid
1620 exited with status 0
```

With an extracted image:
```shell
$ sudo python rd.py run -i ubuntu -- /bin/ls -l /workshop/rubber-docker/levels/
Created a new root fs for our container: /workshop/containers/1739af4b-3849-4e88-ae65-dc98264a0e69/rootfs
/bin/ls: cannot access /workshop/rubber-docker/levels/: No such file or directory
1656 exited with status 512
```
