# Users

From the kernel’s PoV, a user is an `int` parameter in various structs
A process (*task_struct*) has several uid fields: *ruid*, *suid*, *euid*, *fsuid*

There is no need to “add” or "create" new users - since a "user" is just an int parameter, we can just a assign any value to it. There are only two types of users:
- uid 0, aka _root_
- everyone else

More on that in the _capabilities_ section.

User names are a userspace feature of which the kernel is completely oblivious. Largely implemented in `libnss` and `glibc`, user names are a mapping from a human friendly names to uid numbers, managed in `/etc/passwd` and `/etc/shadow`.
Commands like `useradd` manipulate `/etc/passwd`, `/etc/shadow`.
If there's no matching entry for a uid in `/etc/passwd`, everything still works except we won't have the mapping to human friendly names. E.g., try the following:

```
touch /tmp/test
sudo chown 29311 /tmp/test
ls -lh /tmp/test
```

## User permissions
The kernel uses uid numbers (and gid) to decide if a process is permitted to perform certain actions. For example, if a process is trying to `open()` a file, the *fsuid* of the process is compared with the owner uid of the file (and it's permissions mask).

But how does a process change it's uid fields? When a process is cloned it inherits its uid fields from the parent and can then call `setuid()` or similar to change the uid. A process can only change its *ruid* (real uid) if it is currently uid 0 (root).

No identity checks (NFS i’m looking at you)
