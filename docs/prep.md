# The basics of Linux containers

# What is a Linux container?

A container, or "O/S virtualization" as it is sometimes known, refers to an isolated group of processes in an O/S. Let's take postgres as an example service.

Suppose we have postgres running in a container.
Postgres spawns a process for every connection it holds so all the process of a postgres instance must have access to the same resources.
But we don't want other processes (e.g. Apache) to have access or even to be able to see the resources postgres (e.g. memory) is using, and we would also like to limit the amount of resources postgres is allowed to consume.

In addition, we would also like to abstract each postgres instance's view of the O/S so it doesn't concern itself with the peculiarities of the specific host it running on.
For example postgres stores its data in `/var/lib/postgres` and we would like to preserve that regardless of how many postgres instances are running on that host.

So to sum up, this is what we want from a container:
- isolation
- abstraction
- resource constraints

Traditionally sysadmins used users and filesystem permissions for isolation.
Abstraction was done using `chroot` and resource constraints were managed using `rlimit`.
This was far from satisfactory, as evident by the growing popularity of virtual machines.
To make things more manageable, we want the kernel to provide a mechanism which will achieve the above.

Unfortunately, such a mechanism does not exist in Linux.
Instead, we have a a few independent mechanisms which we can orchestrate together to achieve various levels of isolation, abstraction and resource constraints.
We have:
- namespaces
- cgroups
- chroot/pivot_root
- seccomp
- appaprmor/SELinux

Thus, a "Linux container" is not a well defined entity.
From the kernel perspective, there is no such thing as a container, just a bunch of processes with namespaces, cgroups and so on.

To understand how these mechanisms work, it's a good idea to revisit how relevant Linux primitives work:
- [Processes](prep-processes.md)
- [Users](prep-users.md)
- [Mounts](prep-mounts.md)
- [chroot/pivot_root](prep-chroot.md)
- [Memory management](prep-memory.md)

After going over the primitives, let's see how the new mechanisms work:
- [Namespaces](prep-namespaces.md)
- [cgroups](prep-cgroups.md)
- [seccomp](prep-seccomp.md)
- [capabilities](prep-capabilities.md)
