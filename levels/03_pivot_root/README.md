# Level 03: pivot_root

After succesfully jailing a process with `chroot()`, let's escape from this jail: copy the breakout.py script into the chroot and run it!

Ok, obviously `chroot()` isn't good enough. Let's try using `pivot_root()` - remember that *pivot_root()* works on **all** processes - luckily we are using mount namespaces.

Because we are using mount namespace which internally uses mount bind mechanism, by default our (sub)mounts will be seen by the parent mount (and mount namespace). To avoid that we need to mount private the root mount immediately after moving to the new mount namespace - also, this needs to be done *recursively* for all submounts, otherwise we will end up unmounting important things like `/dev/pts` :)

After using `pivot_root()` we need to `umount2()` the `old_root`. We need to use umount2 and not umount because we need to pass certain flags to the call, specifically we need to detach. See `man 2 umount` for details.
 