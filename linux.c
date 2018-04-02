#define _GNU_SOURCE
#include <Python.h>
#include <sys/syscall.h>
#include <sys/mount.h>
#include <sched.h>
#include <sys/wait.h>
#include <unistd.h>

#define STACK_SIZE 32768

#define LINUX_MODULE_DOC "linux\n"\
                         "=====\n"\
                         "The linux module is a simple Python c extension, containing syscall wrappers "\
                         "missing from the Python os module. You will need to use these system calls "\
                         "to implement different aspect of process containment during the workshop."

#define PIVOT_ROOT_DOC  ".. py:function:: pivot_root(new_root, put_old)\n"\
                        "\n"\
                        "change the root filesystem\n"\
                        "\n"\
                        ":param str new_root: New root file system\n"\
                        ":param str put_old: Directory to move the current process root file system to\n"\
                        ":return: None\n"\
                        ":raises RuntimeError: if pivot_root fails\n"\
                        "\n"\
                        "**NOTE:** The following restrictions apply to `new_root` and `put_old`:\n"\
                        "\n"\
                        "* They must be directories.\n"\
                        "* `new_root` and put_old must not be on the same filesystem as the current root.\n"\
                        "* `new_root` must be a mountpoint.\n"\
                        "* `put_old` must  be  underneath `new_root`, that is, adding a nonzero number\n"\
                        "  of /.. to the string pointed to by `put_old` must yield the same directory as\n"\
                        "  `new_root`.\n"\
                        "* No other filesystem may be mounted on `put_old`.\n"

static PyObject *
pivot_root(PyObject *self, PyObject *args) {
	const char *put_old, *new_root;

	if (!PyArg_ParseTuple(args, "ss", &new_root, &put_old))
		return NULL;

	if (syscall(SYS_pivot_root, new_root, put_old) == -1) {
		PyErr_SetFromErrno(PyExc_RuntimeError);
		return NULL;
	} else {
		Py_INCREF(Py_None);
		return Py_None;
	}
}

#define MOUNT_DOC   ".. py:function:: mount(source, target, filesystemtype, mountflags, mountopts)\n"\
                    "\n"\
                    "mount filesystem\n"\
                    "\n"\
                    ":param str source: filesystem to attach (can be ``None``)\n"\
                    ":param str target: directory being attached to, or manipulated (in case of flag change)\n"\
                    ":param str filesystemtype: filesystem supported by the kernel (can be ``None``)\n"\
                    ":param int mountflags: any combination (using ``|``) of mount flags supported by mount(2).\n"\
                    "                       For the workshop you are most likely to use ``0`` (i.e. no flags), \n"\
                    "                       or a combination of: ``linux.MS_REC``, ``linux.MS_PRIVATE``\n"\
                    ":param str mountopts: options passed to the specified filesystem (can be ``None``)\n"\
                    ":return: None\n"\
                    ":raises RuntimeError: if mount fails\n"\
                    "\n"

static PyObject *
_mount(PyObject *self, PyObject *args) {
	const char *source, *target, *filesystemtype, *mountopts;
	unsigned long mountflags;

	if (!PyArg_ParseTuple(args, "zszkz", &source, &target, &filesystemtype, &mountflags, &mountopts)) {
		return NULL;
	}

	if (mount(source, target, filesystemtype, mountflags, mountopts) == -1) {
		PyErr_SetFromErrno(PyExc_RuntimeError);
		return NULL;
	} else {
		Py_INCREF(Py_None);
		return Py_None;
	}
}

#define UMOUNT_DOC  ".. py:function:: umount(target)\n"\
                    "\n"\
                    "unmount filesystem\n"\
                    "\n"\
                    ":param str target: the (topmost) filesystem this directory is mounted on will be removed\n"\
                    ":return: None\n"\
                    ":raises RuntimeError: if umount fails\n"\
                    "\n"

static PyObject *
_umount(PyObject *self, PyObject *args) {
	const char *target;

	if (!PyArg_ParseTuple(args, "s", &target)) {
		return NULL;
	}

	if (umount(target) == -1) {
		PyErr_SetFromErrno(PyExc_RuntimeError);
		return NULL;
	} else {
		Py_INCREF(Py_None);
		return Py_None;
	}
}

#define UMOUNT2_DOC  ".. py:function:: umount2(target, flags)\n"\
                    "\n"\
                    "unmount filesystem but allows additional `flags` controlling the behavior of the operation\n"\
                    "\n"\
                    ":param str target: the (topmost) filesystem this directory is mounted on will be removed\n"\
                    ":param int flags: control the behavior of the operation. You can combine multiple flags\n"\
                    "                  using ``|``. For the workshop you are most likely to use\n"\
                    "                  ``linux.MNT_DETACH``\n"\
                    ":return: None\n"\
                    ":raises RuntimeError: if umount2 fails\n"\
                    "\n"

static PyObject *
_umount2(PyObject *self, PyObject *args) {
	const char *target;
	int flags;

	if (!PyArg_ParseTuple(args, "si", &target, &flags)) {
		return NULL;
	}

	if (umount2(target, flags) == -1) {
		PyErr_SetFromErrno(PyExc_RuntimeError);
		return NULL;
	} else {
		Py_INCREF(Py_None);
		return Py_None;
	}
}

#define UNSHARE_DOC ".. py:function:: unshare(flags)\n"\
                    "\n"\
                    "disassociate parts of the process execution context\n"\
                    "\n"\
                    ":param int flags: which parts of the execution context should be unshared. You can\n"\
                    "                  combine multiple flags using ``|``. See below for flags you might want\n"\
                    "                  to use in this workshop\n"\
                    ":return: None\n"\
                    ":raises RuntimeError: if unshare fails\n"\
                    "\n"\
                    "Useful flags:\n"\
                    "\n"\
                    "* ``linux.CLONE_NEWNS`` - Unshare the mount namespace\n"\
                    "* ``linux.CLONE_NEWUTS`` - Unshare the UTS namespace (hostname, domainname, etc)\n"\
                    "* ``linux.CLONE_NEWNET`` - Unshare the network namespace\n"\
                    "* ``linux.CLONE_NEWPID`` - Unshare the PID namespace\n"\

static PyObject *
_unshare(PyObject *self, PyObject *args) {
	int clone_flags;

	if (!PyArg_ParseTuple(args, "i", &clone_flags))
		return NULL;

	if (unshare(clone_flags) == -1) {
		PyErr_SetFromErrno(PyExc_RuntimeError);
		return NULL;
	} else {
		Py_INCREF(Py_None);
		return Py_None;
	}
}

#define SETNS_DOC   ".. py:function:: setns(fd, nstype)\n"\
                    "\n"\
                    "reassociate process with a namespace\n"\
                    "\n"\
                    ":param int fd: file descriptor referring to a namespace to associate with\n"\
                    ":param int nstype: one of the following: ``0`` (Allow any type of namespace to be joined),\n"\
                    "                   ``CLONE_NEWIPC`` (join IPC namespace), ``CLONE_NEWNET`` (join network \n"\
                    "                   namespace), or ``CLONE_NEWUTS`` (join UTS namespace)\n"\
                    ":return: None\n"\
                    ":raises RuntimeError: if setns fails\n"\
                    "\n"\

static PyObject *
_setns(PyObject *self, PyObject *args) {
	int fd, nstype;

	if (!PyArg_ParseTuple(args, "ii", &fd, &nstype))
		return NULL;

	if (setns(fd, nstype) == -1) {
		PyErr_SetFromErrno(PyExc_RuntimeError);
		return NULL;
	} else {
		Py_INCREF(Py_None);
		return Py_None;
	}
}

struct py_clone_args {
	PyObject *callback;
	PyObject *callback_args;
};

static int clone_callback(void *args) {
	PyObject *result;
	struct py_clone_args *call_args = (struct py_clone_args *)args;

	if ((result = PyObject_CallObject(call_args->callback, call_args->callback_args)) == NULL) {
		PyErr_Print();
		return -1;
	} else {
		Py_DECREF(result);
	}
	return 0;
}

#define CLONE_DOC   ".. py:function:: clone(callback, flags, callback_args)\n"\
                    "\n"\
                    "create a child process\n"\
                    "\n"\
                    ":param Callable callback: python function to be executed by the forked child\n"\
                    ":param int flags: combination (using ``|``) of flags specifying what should be shared\n"\
                    "                  between the calling process and the child process. See below.\n"\
                    ":param tuple callback_args: tuple of arguments for the callback function\n"\
                    ":return: On success, the thread ID of the child process\n"\
                    ":raises RuntimeError: if clone fails\n"\
                    "\n"\
                    "\n"\
                    "Useful flags:\n"\
                    "\n"\
                    "* ``linux.CLONE_NEWNS`` - Unshare the mount namespace\n"\
                    "* ``linux.CLONE_NEWUTS`` - Unshare the UTS namespace (hostname, domainname, etc)\n"\
                    "* ``linux.CLONE_NEWNET`` - Unshare the network namespace\n"\
                    "* ``linux.CLONE_NEWPID`` - Unshare the PID namespace\n"\

static PyObject *
_clone(PyObject *self, PyObject *args) {
	PyObject *callback, *callback_args;
	void *child_stack;
	int flags;
	pid_t child_pid;

	child_stack = malloc(STACK_SIZE);

	if (!PyArg_ParseTuple(args, "OiO", &callback, &flags, &callback_args))
		return NULL;

	if (!PyCallable_Check(callback)) {
		PyErr_SetString(PyExc_TypeError, "parameter must be callable");
        return NULL;
    }

    struct py_clone_args call_args;
    call_args.callback = callback;
    call_args.callback_args = callback_args;

	if ((child_pid = clone(&clone_callback, child_stack + STACK_SIZE, flags | SIGCHLD, &call_args)) == -1) {
			PyErr_SetFromErrno(PyExc_RuntimeError);
			return Py_BuildValue("i", -1);
	} else {
		return Py_BuildValue("i", child_pid);
	}
}

#define SETHOSTNAME_DOC ".. py:function:: sethostname(hostname)\n"\
                        "\n"\
                        "set the system hostname\n"\
                        "\n"\
                        ":param str hostname: new hostname value\n"\
                        ":return: None\n"\
                        ":raises RuntimeError: if sethostname fails\n"\
                        "\n"\

static PyObject *
_sethostname(PyObject *self, PyObject *args) {
	const char *hostname;

	if (!PyArg_ParseTuple(args, "s", &hostname))
		return NULL;

	if (sethostname(hostname, strlen(hostname)) == -1) {
		PyErr_SetFromErrno(PyExc_RuntimeError);
		return NULL;
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef LinuxMethods[] = {
	{"pivot_root", pivot_root, METH_VARARGS, PIVOT_ROOT_DOC},
	{"unshare", _unshare, METH_VARARGS, UNSHARE_DOC},
	{"setns", _setns, METH_VARARGS, SETNS_DOC},
	{"clone", _clone, METH_VARARGS, CLONE_DOC},
	{"sethostname", _sethostname, METH_VARARGS, SETHOSTNAME_DOC},
	{"mount", _mount, METH_VARARGS, MOUNT_DOC},
	{"umount", _umount, METH_VARARGS, UMOUNT_DOC},
	{"umount2", _umount2, METH_VARARGS, UMOUNT2_DOC},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initlinux(void)
{
	PyObject *module = Py_InitModule3("linux", LinuxMethods, LINUX_MODULE_DOC);

	// clone constants
	PyModule_AddIntConstant(module, "CLONE_NEWNS", CLONE_NEWNS);     // mount namespace
	PyModule_AddIntConstant(module, "CLONE_NEWUTS", CLONE_NEWUTS);   // UTS (hostname) namespace
	PyModule_AddIntConstant(module, "CLONE_NEWPID", CLONE_NEWPID);   // PID namespace
	PyModule_AddIntConstant(module, "CLONE_NEWUSER", CLONE_NEWUSER); // users namespace
	PyModule_AddIntConstant(module, "CLONE_NEWIPC", CLONE_NEWIPC);   // IPC namespace
	PyModule_AddIntConstant(module, "CLONE_NEWNET", CLONE_NEWNET);   // network namespace
	PyModule_AddIntConstant(module, "CLONE_THREAD", CLONE_THREAD);

	// mount constants
	PyModule_AddIntConstant(module, "MS_RDONLY", MS_RDONLY);               /* Mount read-only.  */
	PyModule_AddIntConstant(module, "MS_NOSUID", MS_NOSUID);               /* Ignore suid and sgid bits.  */
	PyModule_AddIntConstant(module, "MS_NODEV", MS_NODEV);                 /* Disallow access to device special files.  */
	PyModule_AddIntConstant(module, "MS_NOEXEC", MS_NOEXEC);               /* Disallow program execution.  */
	PyModule_AddIntConstant(module, "MS_SYNCHRONOUS", MS_SYNCHRONOUS);     /* Writes are synced at once.  */
	PyModule_AddIntConstant(module, "MS_REMOUNT", MS_REMOUNT);             /* Alter flags of a mounted FS.  */
	PyModule_AddIntConstant(module, "MS_MANDLOCK", MS_MANDLOCK);           /* Allow mandatory locks on an FS.  */
	PyModule_AddIntConstant(module, "MS_DIRSYNC", MS_DIRSYNC);             /* Directory modifications are synchronous.  */
	PyModule_AddIntConstant(module, "MS_NOATIME", MS_NOATIME);             /* Do not update access times.  */
	PyModule_AddIntConstant(module, "MS_NODIRATIME", MS_NODIRATIME);       /* Do not update directory access times.  */
	PyModule_AddIntConstant(module, "MS_BIND", MS_BIND);                   /* Bind directory at different place.  */
	PyModule_AddIntConstant(module, "MS_MOVE", MS_MOVE);
	PyModule_AddIntConstant(module, "MS_REC", MS_REC);                     /* Recursive loopback */
	PyModule_AddIntConstant(module, "MS_SILENT", MS_SILENT);
	PyModule_AddIntConstant(module, "MS_POSIXACL", MS_POSIXACL);           /* VFS does not apply the umask.  */
	PyModule_AddIntConstant(module, "MS_UNBINDABLE", MS_UNBINDABLE);       /* Change to unbindable.  */
	PyModule_AddIntConstant(module, "MS_PRIVATE", MS_PRIVATE);             /* Change to private.  */
	PyModule_AddIntConstant(module, "MS_SLAVE", MS_SLAVE);                 /* Change to slave.  */
	PyModule_AddIntConstant(module, "MS_SHARED", MS_SHARED);               /* Change to shared.  */
	PyModule_AddIntConstant(module, "MS_RELATIME", MS_RELATIME);           /* Update atime relative to mtime/ctime.  */
	PyModule_AddIntConstant(module, "MS_KERNMOUNT", MS_KERNMOUNT);         /* This is a kern_mount call.  */
	PyModule_AddIntConstant(module, "MS_I_VERSION", MS_I_VERSION);         /* Update inode I_version field.  */
	PyModule_AddIntConstant(module, "MS_STRICTATIME", MS_STRICTATIME);     /* Always perform atime updates.  */
	PyModule_AddIntConstant(module, "MS_ACTIVE", MS_ACTIVE);
	PyModule_AddIntConstant(module, "MS_NOUSER", MS_NOUSER);
	PyModule_AddIntConstant(module, "MNT_DETACH", MNT_DETACH);             /* Just detach from the tree.  */
	PyModule_AddIntConstant(module, "MS_MGC_VAL", MS_MGC_VAL);
}
