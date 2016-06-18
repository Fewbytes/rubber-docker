# Level 01: chroot

"Jail" a process so it doesn't see the rest of the file system.

First, try to run a process with chroot; If that doesn't work.... perhaps we should extract an image there

If we want tools like `ps` to work properly, we need to mount the special filesystems like `/proc`, `/sys` and `/dev` inside the new root. This can be done using the *linux* python module which exposes the *mount()* syscall:

```python
linux.mount('proc', os.path.join(new_root, 'proc'), 'proc', 0, '')
```
The semantics of the *mount()* syscall have been preserved; to learn more about it read `man 3 mount`.

From within the chroot, have a look at `/proc/mounts`. Does it look different from `/proc/mounts` outside the chroot?
Remember we are not using mount namespace yet!

(*answer*: [linux/fs/proc_namespace.c on Github](https://github.com/torvalds/linux/blob/33caf82acf4dc420bf0f0136b886f7b27ecf90c5/fs/proc_namespace.c#L110))

## Relevant Documentation

[chroot manpage](http://linux.die.net/man/2/chroot)

## How to check your work

Without extracting an image:
```
$ sudo python rd.py run -i ubuntu-trusty /bin/bash
Created a new root fs for our container: /workshop/containers/3cfcd2b8-3f45-4531-af8a-62fc85b36755/rootfs
Traceback (most recent call last):
  File "rd.py", line 90, in <module>
    cli()
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 700, in __call__
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 680, in main
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 1027, in invoke
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 873, in invoke
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 508, in invoke
  File "rd.py", line 82, in run
    contain(command, image_name, image_dir, container_id, container_dir)
  File "rd.py", line 69, in contain
    os.execvp(command[0], command)
  File "/usr/lib/python2.7/os.py", line 346, in execvp
  File "/usr/lib/python2.7/os.py", line 370, in _execvpe
OSError: [Errno 2] No such file or directory
3916 exited with status 256
```

With an extracted image:
```shell
$ sudo python rd.py run -i ubuntu-trusty /bin/bash
$ ls /
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
$ touch /test
$ exit
$ ls /test
ls: cannot access /test: No such file or directory
```
