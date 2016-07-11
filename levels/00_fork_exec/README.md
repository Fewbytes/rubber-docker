# Level 00: fork & exec

In this level we will get to know `rd.py` - the skeleton of our rubber-docker.
`rd.py` already implements one CLI command - *run* using the *click* python module. It should be used like this:

```
$ python rd.py run /bin/echo "Hello Docker"
```

Right now, the skeleton doesn't actually do much, so at a bare minimum we need to make it run our executable.
This can be achieved using Linux's *fork-exec* mechanism.

## fork-exec
In the \*nix family of operating systems, new processes are spawned using *fork-exec* -
the *fork()* call and the *exec()* call work together to create the new process.

*fork()* is the name of the system call (actually a *libc* call in Linux) that the parent process uses to "divide" itself ("fork" into two identical processes).
After calling *fork()*, a complete copy of the executing program is made into the new process.
This new process (which is a "child" of the "parent") has a new PID.
The *fork()* function returns the child's PID to the parent, while it returns 0 to the child, in order to allow the two identical processes to distinguish one another.
Following return from the *fork()* call, execution will proceed from the same point in the program and then (usually) diverge based on the return value.

In some cases the two processes are made to continue running the same binary, but often one (usually the child) switches to running another binary executable using the *exec()* system call (actually a family of calls).
When the child process calls *exec()*, all data in the original program is lost, and it is replaced with a running copy of the new program.

Finally, the parent must invoke the *wait()* call (or any of it's variants), in order to collect the child's exit status and allow the system to release the resources associated with the child. If a wait is not performed, then the terminated child remains in a defunct (AKA "zombie") state.

### Example

```python
pid = os.fork()
if pid == 0:
    # This is the child
    os.execv('/bin/echo', ['/bin/echo', 'Hello Docker'])
    # Unreachable area, since we change the binary executable
else:
    # This is the parent
    waited_pid, status = os.waitpid(pid, 0) # wait for the child to finish
```

## Further reading
- [os.fork()](https://docs.python.org/2/library/os.html#os.fork)
- [os.execv()](https://docs.python.org/2/library/os.html#os.execv)
- [os.waitpid()](https://docs.python.org/2/library/os.html#os.waitpid)
- Python [Lists](https://docs.python.org/2/tutorial/introduction.html#lists)
- [Wikipedia - Fork-exec](https://en.wikipedia.org/wiki/Fork%E2%80%93exec)

## How to check your work

```
$ python rd.py run /bin/echo "Hello Docker"
Hello Docker

3620 exited with status 0
```

## Bonus

Can you use another exec variant to manipulate your child process environment variables (similar to [docker run -e](https://docs.docker.com/engine/reference/run/#env-environment-variables))?
