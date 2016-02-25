# Level 08: CPU CGroup

In this Level we add our first cgroup. First, we create a top cgroup for all containers then a subgroup for every container, something like `/sys/fs/cgroup/cpu/rubber-docker/<container_id>`

We then move the contained process to the group by writing its pid to the `tasks` file of the group. Finally we set the limits of the group by writing the number of alloted shares to `cpu.allowed_shares`

Excersices:
- Run a container with 200 cpu shares then generate cpu load inside the container (using the `stress` tool). How much cpu usage does the host show? Why?
- Run two containers with different shares allocations, generate cpu load in both and observe cpu usage using top on the host
- How does cgroup limits effect/work with `nice` priorities?