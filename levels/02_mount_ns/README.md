# Level 02: mount namespace

Let's add a mount namespace using the `unshare()` call.

Also, it's time to create device nodes in our container root using `mknod()`:

```python
os.mknod(os.path.join(dev_path, device), 0666 | S_IFCHR, os.makedev(major, minor))
```
