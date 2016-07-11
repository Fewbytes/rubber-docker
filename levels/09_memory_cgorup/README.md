# Level 09: Memory CGroup

In this level we limit the memory usage of the container.
Create a directory inside the memory cgroup fs (like we did in the cpu cgroup) per container.
Move the process to the cgroup by writing the pid to the `tasks` file and then setup the limits by writing to the following files:
- `memory.limit_in_bytes` - either number of bytes or units e.g. 1g
- `memory.memsw.limit_in_bytes` - either number of bytes or units e.g. 1g

## Exercises

After setting the limits, run a container with the stress tool and observe what happens when your container goes over the allotted limit.
Explore the behavior of the container:
- Watch when the container goes over `memory.limit_in_bytes`.
- Watch when the container goes over `memory.memsw.limit_in_bytes.`
- Watch `memory.kmem.usage_in_bytes`, is all kernel memory used accounted for?
- Try the infamous `while true; do mkdir t; cd t; done` DOS attack from within the container. Does it succeed in DOSing the host?
- Where is `tcp` socket buffers memory accounted? where is `udp` memory accounted?
- Explore the behavior of memory cgroup with different OOM control options. (`memory.oom_control` file).

## Relevant Documentation
- [Kernel docs, memory cgroup](https://www.kernel.org/doc/Documentation/cgroup-v1/memory.txt)


## How to check your work
From the container:
```
$ sudo python rd.py run -i ubuntu --memory 128m --memory-swap 150m /bin/bash
Created a new root fs for our container: /workshop/containers/1e9b16b3-3ea3-4cad-84e1-f623ba4deada/rootfs
root@1e9b16b3-3ea3-4cad-84e1-f623ba4deada:/# cat /proc/self/cgroup
10:hugetlb:/user.slice/user-1000.slice/session-2.scope
9:blkio:/user.slice/user-1000.slice/session-2.scope
8:net_cls,net_prio:/user.slice/user-1000.slice/session-2.scope
7:cpu,cpuacct:/rubber_docker/1e9b16b3-3ea3-4cad-84e1-f623ba4deada
6:perf_event:/user.slice/user-1000.slice/session-2.scope
5:devices:/user.slice/user-1000.slice/session-2.scope
4:cpuset:/user.slice/user-1000.slice/session-2.scope
3:memory:/rubber_docker/1e9b16b3-3ea3-4cad-84e1-f623ba4deada
2:freezer:/user.slice/user-1000.slice/session-2.scope
1:name=systemd:/user.slice/user-1000.slice/session-2.scope
```

From the host:
```
$ cat /sys/fs/cgroup/memory/rubber_docker/1e9b16b3-3ea3-4cad-84e1-f623ba4deada/memory.limit_in_bytes
134217728
$ cat /sys/fs/cgroup/memory/rubber_docker/1e9b16b3-3ea3-4cad-84e1-f623ba4deada/memory.memsw.limit_in_bytes
157286400
```

## Bonus round
read about and use the following control files:
- `memory.oom_control`
- `memory.swappiness`
- `memory.kmem.limit_in_bytes`
- `memory.kmem.tcp.limit_in_bytes`
- `memory.soft_limit_in_bytes`
