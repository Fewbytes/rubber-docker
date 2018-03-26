# Level 10: setuid

In this level we implement functionality similar to `docker run -u UID` - the ability to run processes as a non-root user.
In order to run the contained process as a different user, use the _setuid_ and _setgid_ system calls.
These system calls must be called before we _exec_, but after we do all the tasks that require root privileges.

## Exercises
- Use a uid of an existing username (e.g. 1000) and play around with the container's _/etc/passwd_ file.
- Create some files inside the container and observe the owner uid outside the container. How does that affect shared volumes between containers?

## Relevant Documentation

- [man 2 setuid](hhttp://man7.org/linux/man-pages/man2/setuid.2.html)

## How to check your work
```
$ sudo python rd.py run -i ubuntu --user 2014:222 /bin/bash
Created a new root fs for our container: /workshop/containers/1e9b16b3-3ea3-4cad-84e1-f623ba4deada/rootfs
root@1e9b16b3-3ea3-4cad-84e1-f623ba4deada:/# id

```
