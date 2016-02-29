# Level 07: network namespace

Move to a new network namespace so that the container doesn't have access to the host NICs. After implementing this, you can check with `ip a` or `ifconfig` that you don't see the host NICs anymore

Bonus: iproute2 toolchain also allows fiddling with network namespaces. Have a look at the `ip netns` commands, to make it work with namespaces we generate using syscalls we need to link a file in `/var/run/netns` to the network namespace file descriptor from `/proc/<pid>/ns/`
