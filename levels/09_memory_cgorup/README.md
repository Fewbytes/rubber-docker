# Level 09: Memory CGroup

In this level we limit memory usage of the container. Create a directory inside the memory cgroup fs (like we did in the cpu cgroup) per container. Move the process to the cgroup by writing the pid to the `tasks` file then setup the limits by writing to the following files:
- `memory.limit_in_bytes` - either number of bytes or units e.g. 1g
- `memory.memsw.limit_in_bytes` - either number of bytes or units e.g. 1g

After setting the limits, run a container with the stress tool and observe what happens when your container goes over the allotted limit.

## Bonus round
read about and use the following control files
- `memory.oom_control`
- `memory.swappiness`
- `memory.kmem.limit_in_bytes`
- `memory.soft_limit_in_bytes`
