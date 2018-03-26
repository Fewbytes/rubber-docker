# level 04: overlay CoW filesystem

So far, unpacking the image every time was slow and we want fast startup times for our containers.
Also, it would be nice if every container won't take so much space (~ 180MB in ubuntu minimal's case).

In this level, we will add overlayfs.
A secondary win is that now we can make `pivot_root()` work since our new root will be a mountpoint!

What we want to do is extract the image to an *image_root* directory (if it's not extracted already), and then create the following:
- a *container_dir* with a mount directory for overlayfs
- a directory for the writable branch (*upperdir*)
- a directory for the *workdir*

## Exercises

After implementing this step, try a few things to see how overlayfs behaves:
- write a file using `dd` inside the container and see if you can fill the host drive.
- write a large file (say 1GB) to the image directory, then open it for (non-truncating) writing in the container, perhaps using this python code: `open('big_file', 'r+')`. How much time does the open operation take? why?
- Do some file operations (write files, move files, delete files) in the container, then have a look at the `upperdir` (using `ls -la`).

## Relevant Documentation

- [OverlayFS - Kernel archives](https://www.kernel.org/doc/Documentation/filesystems/overlayfs.txt)

## How to check your work

```
$ time sudo python rd.py run -i ubuntu /bin/bash -- -c true
Created a new root fs for our container: /workshop/containers/7a3393a1-df94-4c44-a935-700ec52c2607/rootfs
11191 exited with status 0

real	0m3.475s
user	0m1.492s
sys	0m1.260s

$ time sudo python rd.py run -i ubuntu /bin/bash -- -c true
Created a new root fs for our container: /workshop/containers/98282744-82bd-4c70-bbf9-028e8c92f995/rootfs
11196 exited with status 0

real	0m0.162s
user	0m0.088s
sys	0m0.032s
```
Observe that second launch of a container using the same image takes almost no time, because we don't need to extract the image again.
