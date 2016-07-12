# Linux processes

A _process_ is an operating system concept describing a task with a separate memory space and resources.
In Linux, _processes_ are created using the `clone()` system call, which clones an existing process to create a new process.
The `clone()` call accepts various flags which tell Linux what resources to share/copy with the original process.
Usually, the `clone()` system call is not used directly; instead we use POSIX calls (like `fork()`) which are implemented in _glibc_ (userspace).
In fact, most of the Linux and POSIX interfaces we use are implemented in _glibc_, not in the kernel.

The `fork()` call we know and love creates a _process_ by calling `clone()` with a bunch of flags. Threads are created using the `pthread_create()` call.

Under the hood, both threads and processes are tasks and are represented by a struct called (surprise surprise) *task_struct*. *task_struct* has about 170 fields, and is around 1k size. Some notable fields are: _*user_, _pid_, _tgid_, _*files_, _*fs_, _*nsproxy_
- *fs_struct* _*fs_ holds information on current root, working directory, umask, etc.
- *pid* struct maps processes to one or more tasks

## Processes - fork & exec

Traditionally \*nixs created new processes by calling the following calls in order:
 1. *fork()* - Duplicate the current process, VM is copy-on-write
 1. *exec()* - Replace text/data/bss/stack with new program image

After calling *exec()*, the new process image starts executing from the entrypoint (main function) and the new command line arguments (argv) are passed to it.

- glibc’s *fork()* and *pthread_create()* both call clone() syscall
- *clone()* creates a new *task_struct* from parent
controls resource sharing by flags (e.g. share VM, share/copy fd)
