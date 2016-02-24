# Level 06: PID namespace

The PID namespace is a little different from other namespaces: `unshare()` doesn't move the current process to a new namespace, instead only it's future children will be in the new PID namespace. We have 2 options:
1. Use `unshare()` before we fork
2. Use `clone()` instead of `fork()` and pass the `CLONE_NEWPID` flag

Our version of `clone()` exposed by the `linux` module mirror the `libc` API (because it's simpler):
```python
linux.clone(python_callable, flags, callable_args_tuple) # --> returns pid of new process
```


Try using the PID namespace without the `/proc` mount or mount binding the original `/proc` mount. How do tools like `ps` behave in this case?
