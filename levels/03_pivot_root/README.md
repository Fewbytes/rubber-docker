# Level 03: pivot_root

After successfully jailing a process with [chroot()](https://docs.python.org/2/library/os.html#os.chroot), let's escape from this jail: copy the [breakout.py](breakout.py) script into the chroot and run it!

```bash
sudo python rd.py run -i ubuntu /bin/bash

# Check that you are inside chroot
ls /

# Escape!
python breakout.py

# Aaaaand we're out :)
ls /
```


Ok, obviously [chroot()](https://docs.python.org/2/library/os.html#os.chroot) isn't good enough. Let's try using [pivot_root()](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html#linux.pivot_root).
Remember that [pivot_root()](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html#linux.pivot_root) works on **all** processes - luckily we are using mount namespaces.

Because we are using mount namespace which internally uses the mount bind mechanism, by default our (sub)mounts will be visible by the parent mount (and mount namespace).
To avoid that, we need to mount private the root mount immediately after moving to the new mount namespace - also, this needs to be done *recursively* for all submounts, otherwise we will end up unmounting important things like `/dev/pts` :)

After using [pivot_root()](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html#linux.pivot_root), we need to [umount2()](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html#linux.umount2) the `old_root`.
We need to use umount2 and not umount because we need to pass certain flags to the call; specifically, we need to detach. See `man 2 umount` for details.

## Relevant Documentation

- [man 2 pivot_root](http://man7.org/linux/man-pages/man2/pivot_root.2.html)
- [man 2 umount2](http://man7.org/linux/man-pages/man2/umount2.2.html)

## How to check your work

Within the container, you should see a new *rootfs* device; However, this step will actually fail:

```
$ sudo python rd.py run -i ubuntu /bin/bash
Created a new root fs for our container: /workshop/containers/f793960b-64bd-4c21-9a7f-da1b0fbe9aad/rootfs
Traceback (most recent call last):
  File "rd.py", line 126, in <module>
    cli()
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 700, in __call__
    return self.main(*args, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 680, in main
    rv = self.invoke(ctx)
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 1027, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 873, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/usr/local/lib/python2.7/dist-packages/click/core.py", line 508, in invoke
    return callback(*args, **kwargs)
  File "rd.py", line 118, in run
    contain(command, image_name, image_dir, container_id, container_dir)
  File "rd.py", line 98, in contain
    linux.pivot_root(new_root, old_root)
RuntimeError: (16, 'Device or resource busy')
10766 exited with status 256
```

The reason this step will fail is that [pivot_root(new_root, put_old)](https://rawgit.com/Fewbytes/rubber-docker/master/docs/linux/index.html#linux.pivot_root) requires *new_root* to be a different filesystem then the old root.
This will be resolved in step 04 when we mount an overlay filesystem as *new_root*.

To circumvent that, we can copy the image files to a [tmpfs](https://en.wikipedia.org/wiki/Tmpfs) mount.
```python
# ...
# TODO: uncomment (why?)
linux.mount('tmpfs', container_root, 'tmpfs', 0, None)
# ...
```

Repeat the `breakout.py` exercise and see if you can still escape :)
