# Level 08: CPU CGroup

In this Level we add our first cgroup:
- First, we create a top cgroup for all containers and a subgroup for every container, something like `/sys/fs/cgroup/cpu/rubber-docker/<container_id>`.
- Then we move the contained process to the group by writing its pid to the `tasks` file of the group.
- Finally, we set the limits of the group by writing the number of allocated shares to `cpu.shares`.

## Relevant Documentation
- [Kernel docs, scheduler design](https://www.kernel.org/doc/Documentation/scheduler/sched-design-CFS.txt) - section 7
- [Kernel docs, CPU accounting controller](https://www.kernel.org/doc/Documentation/cgroup-v1/cpuacct.txt)


## Exercises
- Run a container with 200 cpu shares and then generate cpu load inside the container (using the `stress` tool). How much cpu usage does the host show? Why?
- Run two containers with different shares allocations, generate cpu load in both and observe cpu usage using top on the host.
- What is the interaction between cgroup limits and `nice` priorities and priority classes (e.g. RT scheduler)?

## How to check your work
Look at the content of `/proc/self/cgroup` from within a container to verify it is in a new cpu cgroup:
```
$ sudo python rd.py run -i ubuntu /bin/bash
Created a new root fs for our container: /workshop/containers/57f02a16-4515-4068-b097-b241b66e4987/rootfs
root@57f02a16-4515-4068-b097-b241b66e4987:/# cat /proc/self/cgroup
10:hugetlb:/user.slice/user-1000.slice/session-2.scope
9:blkio:/user.slice/user-1000.slice/session-2.scope
8:net_cls,net_prio:/user.slice/user-1000.slice/session-2.scope
7:cpu,cpuacct:/rubber_docker/57f02a16-4515-4068-b097-b241b66e4987
6:perf_event:/user.slice/user-1000.slice/session-2.scope
5:devices:/user.slice/user-1000.slice/session-2.scope
4:cpuset:/user.slice/user-1000.slice/session-2.scope
3:memory:/user.slice/user-1000.slice/session-2.scope
2:freezer:/user.slice/user-1000.slice/session-2.scope
1:name=systemd:/user.slice/user-1000.slice/session-2.scope

root@57f02a16-4515-4068-b097-b241b66e4987:/# grep 57f02a16-4515-4068-b097-b241b66e4987 /proc/self/cgroup
7:cpu,cpuacct:/rubber_docker/57f02a16-4515-4068-b097-b241b66e4987
```

Alternatively, you can take a look from the host at `/sys/fs/cgroup/cpu`:
```
$ cat /sys/fs/cgroup/cpu/rubber_docker/57f02a16-4515-4068-b097-b241b66e4987/tasks
5386
```
