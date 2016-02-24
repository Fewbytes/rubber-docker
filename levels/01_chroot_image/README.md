# Level 01: chroot

"Jail" a process so it doesn't see the rest of the file system.

First, try to run a process with chroot; If that doesn't work.... perhaps we should extract an image there

From within the chroot, have a look at `/proc/mounts`. Does it look different from `/proc/mounts` outside the chroot?
Remember we are not using mount namespace yet!

(*answer*: [linux/fs/proc_namespace.c on Github](https://github.com/torvalds/linux/blob/33caf82acf4dc420bf0f0136b886f7b27ecf90c5/fs/proc_namespace.c#L110))
