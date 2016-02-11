#define _GNU_SOURCE
#include <Python.h>
#include <sys/syscall.h>

static PyObject *
pivot_root(PyObject *self, PyObject *args) {
	const char *put_old, *new_root;
	int ret;

	if (!PyArg_ParseTuple(args, "s", &new_root))
        return NULL;
    if (!PyArg_ParseTuple(args, "s", &put_old))
    	return NULL;

    ret = syscall(SYS_pivot_root, &new_root, &pivot_root);

    if (ret == -1) {
    	PyErr_SetFromErrno(PyEx_RuntimeError)
    	return NULL;
    }
    
    return NULL;
}

static PyMethodDef LinuxMethods[] = {
    {"pivot_root",  pivot_root, METH_VARARGS,
     "pivot_root system call"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initlinux(void)
{
    (void) Py_InitModule("linux", LinuxMethods);
}