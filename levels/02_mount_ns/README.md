# Level 02: mount namespace

Let's add a mount namespace using the [unshare()](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html#linux.unshare) call.
Mount namespaces essentially work like bind mounts - operations in mount namespaces will be propagated to other namespaces *unless* we make the parent mount (/ in our case) a *private* mount (or similar).
For this reason, we need to change / to a private mount.
This is done using the [mount()](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html#linux.mount) syscall with `MS_PRIVATE` and `MS_REC` flags (why do we need `MS_REC`?)

Python doesn't have the mount syscall exposed; use the `linux` module provided in this repo instead.

**Fun Fact**: The Linux kernel documentation says private mounts are the default, but are they?

Also, it's time to create device nodes in our container root using [mknod()](https://docs.python.org/2/library/os.html#os.mknod):

```python
os.mknod(os.path.join(dev_path, device), 0666 | stat.S_IFCHR, os.makedev(major, minor))
```

Look at the host's `/dev` and think which devices you might need, note their minor/major (using ls -l), and create them inside the container.

## Relevant Documentation

- [man 2 mount](http://man7.org/linux/man-pages/man2/mount.2.html)
- [Kernel docs - shared mounts](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)
- [man 7 namespaces](http://man7.org/linux/man-pages/man7/namespaces.7.html)

## How to check your work:

### Mount namespace
Verify your new forked process is in a different mount namespace
```bash
$ ls -lh /proc/self/ns/mnt
lrwxrwxrwx 1 root root 0 Mar 18 04:13 /proc/self/ns/mnt -> mnt:[4026531840]
$ sudo python rd.py run -i ubuntu /bin/bash
root@ip-172-31-31-83:/# ls -lh /proc/self/ns/mnt
lrwxrwxrwx 1 root root 0 Mar 18 04:13 /proc/self/ns/mnt -> mnt:[4026532139]
```

Create a new mount inside the container, and make sure it's invisible from the outside
```bash
$ sudo python rd.py run -i ubuntu /bin/bash
root@ip-172-31-31-83:/# mkdir /mnt/moo
root@ip-172-31-31-83:/# mount -t tmpfs tmpfs /mnt/moo

# Keep that contained process running, and open another terminal
$ grep moo /proc/mounts
$
```

### Device nodes
We love throwing stuff to /dev/null, what if it was a regular file?
```bash
# Without a null device node
$ sudo python rd.py run -i ubuntu /bin/bash
root@ip-172-31-31-83:/# find / > /dev/null
root@ip-172-31-31-83:/# ls -lh /dev/null
-rw-r--r-- 1 root root 2.2M Jun 21 16:40 /dev/null

# With a null device node
$ sudo python rd.py run -i ubuntu /bin/bash
Created a new root fs for our container: /workshop/containers/6aeb472a-94da-42f3-a004-f5809367327b/rootfs
root@ip-172-31-31-83:/# find / > /dev/null
root@ip-172-31-31-83:/# ls -lh /dev/null
crw-r--r-- 1 root root 1, 3 Jun 21 16:44 /dev/null
```

## Cleanup
Don't forget to remove the containers and mounts using [cleanup.sh](../cleanup.sh)
