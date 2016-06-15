# Level 02: mount namespace

Let's add a mount namespace using the `unshare()` call.
Mount namespaces essentially work like bind mounts - operations in mount namespaces will be propagated to other namespaces *unless* we make the parent mount (/ in our case) a *private* mount (or similar).
For this reason, we need to change / to a private mount. This is done using the *mount()* syscall with `MS_PRIVATE` and `MS_REC` flags (why do we need `MS_REC`?)

Python doesn't have the mount syscall exposed. Use `linux` module provided in this repo instead.

Also, it's time to create device nodes in our container root using `mknod()`:

```python
os.mknod(os.path.join(dev_path, device), 0666 | S_IFCHR, os.makedev(major, minor))
```

## Relevant Documentation

- [man 2 mount](http://linux.die.net/man/2/mount)
- [Kernel docs - shared mounts](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)
- [man 7 namespaces](http://man7.org/linux/man-pages/man7/namespaces.7.html)

## How to check your work:
Verify your new forked process is in a different mount namespace
```bash
$ ls -lh /proc/self/ns/mnt
lrwxrwxrwx 1 root root 0 Mar 18 04:13 /proc/self/ns/mnt -> mnt:[4026531840]
$ python rd.py run -i ubuntu-trusty /bin/bash
$ ls -lh /proc/self/ns/mnt
lrwxrwxrwx 1 root root 0 Mar 18 04:13 /proc/self/ns/mnt -> mnt:[4026532139]
```
