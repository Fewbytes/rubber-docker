# Level 00: fork & exec

In this level we will get to know `rd.py` - the skeleton of our rubber-docker. `rd.py` already implements one CLI command - *run* using the *click* python module. It should be used like this:

```
$ python rd.py run /path/to/executable
```

Right now the skeleton doesn't actually do much, so at a bare minimum we need to make it run our executable. This can be achieved using Linux' *fork-exec* mechanism.

## Fork-exec
In \*nix family of operating systems, new processes are spawned using *fork-exec* -
the *fork* call and the *exec* call work together to create the new process.

*fork()* is the name of the system call (actually a *libc* call in Linux) that the parent process uses to "divide" itself ("fork" into two identical processes). After calling fork(), the created child process is an exact copy of the parent except for the return value and execution will proceed from the same point in the program - the return of the *fork()* call. In some cases the two processes continue to run the same binary, but often one (usually the child) switches to running another binary executable using the *exec()* system call (actually a family of calls).

When a process forks, a complete copy of the executing program is made into the new process. This new process (which is a child of the parent) has a new PID. The *fork()* function returns the child's PID to the parent, while it returns 0 to the child, in order to allow the two identical processes to distinguish one another.

When the child process calls exec(), all data in the original program is lost, and it is replaced with a running copy of the new program.

### Example

```python
pid = os.fork()
if pid == 0:
    # this is the child
    os.execv('/bin/bash', ['/bin/bash', '-c', 'echo test'])
else:
    # this is the parent
    os.waitpid(pid, 0) # wait for the child to finish
```

## Further reading
- [Wikipedia - Fork-exec](https://en.wikipedia.org/wiki/Fork%E2%80%93exec)

## How to check your work

```
$ python rd.py run -- /bin/bash -c "echo test"
test
10722 exited with status 0
```
