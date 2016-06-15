# The basics of Linux containers

# What is a Linux container?

A container, or "O/S virtualization" as it is sometimes known, refers to an isolated group of process in an O/S. For example, suppose we have postgres running in a container. Postgres spawns a process for every connection it holds so all the process of a postgres instance must have access to the same resources, but we don't want other processes (e.g. Apache) to have access or even to be able to see the resources postgres is using. Additionally, we would like to limit the amount of resources (e.g. memory) postgres is allowed to consume. We would also like to abstract postgres view of the O/S so it doesn't concern itself with the peculiarities of the specific host it running on - for example postgres stores its data in `/var/lib/postgres` and we would like to preserve that regardless of how many postgres instances are running on that host.

So to sum up, this is what we want from a container:
- isolation
- abstraction
- resource constraints

Traditionally we used users and filesystem permissions for isolation. Abstraction was done using `chroot` and resource constraints was managed using `rlimit`. This was far from satisfactory as evident by the growing popularity of virtual machines. To solve this, we want the kernel to provide a mechanism which will achieve the above.

Unfortunately, such a mechanism does not exist in Linux. Instead, we have a a few independent mechanisms which we can orchestrate together to achieve various levels of isolation, abstraction and resource constraints. We have:
- namespaces
- cgroups
- chroot/pivot_root
- seccomp
- appaprmor/SELinux

Thus, a "Linux container" is not a well defined entity. From the kernel perspective there is no such thing as a container, just a bunch of processes with namespaces, cgroups and so on.

To understand how these mechanisms work, it's a good idea to revisit how relevant Linux primitives works.

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
