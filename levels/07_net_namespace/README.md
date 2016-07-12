# Level 07: network namespace

Move to a new network namespace so that the container doesn't have access to the host NICs.
After implementing this, you can check with `ip link` or `ifconfig` that you don't see the host NICs anymore.

Bonus: The iproute2 toolchain also allows fiddling with network namespaces.
Have a look at the `ip netns` commands.
To make it work with the namespaces we generate using syscalls, we need to link a file in `/var/run/netns` to the network namespace file descriptor from `/proc/<pid>/ns/`.

## Relevant Documentation

- [Namespaces in operation - network namespace](https://lwn.net/Articles/580893/)
- [man ip-netns](http://man7.org/linux/man-pages/man8/ip-netns.8.html)

## How to check your work
Run the container and use `ip link` or `ifconfig` to browse the available NICs.
You should see only `lo` (if using `ip link`) or no NICs (if using `ifconfig`).
```
$ sudo python rd.py run -i ubuntu /bin/bash
Created a new root fs for our container: /workshop/containers/9feb3d2d-725b-4c36-8c4d-0c586766f6f6/rootfs
root@9feb3d2d-725b-4c36-8c4d-0c586766f6f6:/# ip a
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
root@9feb3d2d-725b-4c36-8c4d-0c586766f6f6:/# ifconfig
```

## Bonus round
The `ip netns` command allows you to manipulate network namespaces, e.g. to create a `veth` pair and assign one of the pair to your new network namespace.
The `veth` pair is somewhat like a patch cable - packets sent on one `veth` NIC will appear on the other member of the pair.
You can use the `veth` to connect your container to a bridge/vswitch (like Docker does) or routing table.
`ip netns` uses the `netlink` kernel API and you can use it directly with the `pyroute2` module.
Alternatively, it may be easier to start by running `ip netns` commands.
Note that `ip netns` requires a network namespace file descriptor to reside in `/var/run/netns`, you can symlink `/proc/<pid>/ns/net` to get `ip netns` to work.
