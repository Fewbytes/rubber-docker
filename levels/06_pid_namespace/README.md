# Level 06: PID namespace

The PID namespace is a little different from other namespaces: `unshare()` doesn't move the current process to a new namespace, instead only its future children will be in the new PID namespace.
We have 2 options:
 1. Use `unshare()` before we fork
 1. Use `clone()` instead of `fork()` and pass the `CLONE_NEWPID` flag

Our version of `clone()` that is exposed by the `linux` module mirrors the `libc` API (because it's simpler):
```python
linux.clone(python_callable, flags, callable_args_tuple) # --> returns pid of new process
```

## Exercises
- Try using the PID namespace without the `/proc` mount or mount binding the original `/proc` mount. How do tools like `ps` behave in this case?
- Try `kill -9 $$` from within the container with and without PID namespace ($$ is evaluated to the current PID). Is there a difference? why?
- Try generating zombies within the container.

## Relevant Documentation

- [man 7 pid_namespaces](http://man7.org/linux/man-pages/man7/pid_namespaces.7.html)
- [Namespaces in operation part 3](https://lwn.net/Articles/531419/)

## How to check your work

Various process listing commands and the */proc* filesystem should show only container processes:
```
$ sudo python rd.py run -i ubuntu /bin/bash
Created a new root fs for our container: /workshop/containers/a4725e53-b164-4b60-ab6f-8ee527258f71/rootfs
root@a4725e53-b164-4b60-ab6f-8ee527258f71:/# ps
  PID TTY          TIME CMD
    1 pts/0    00:00:00 bash
   11 pts/0    00:00:00 ps
root@a4725e53-b164-4b60-ab6f-8ee527258f71:/# ls /proc | grep '[0-9]'
1
12
13
```
