# level 04: overlay CoW filesystem

So far, unpacking the image every time was slow and we want fast startup times for our containers. In addition, it would be nice if every container won't take so much space (~ 180MB in ubuntu minimal's case).

In this level, we will add overlayfs. A secondary win is that now we can make *pivot_root()* work since our new root will be a mountpoint!

After implementing this step, try a few things to see how overlayfs behaves:
- write a file using `dd` inside the container and see if you can fill the host drive
- write a large file (say 1GB) to the image directory, then open it for (non-truncating) writing in the container, perhaps using this python code: `open('big_file', 'r+')`. How much time does the open operation take? why?
- Do some file operations (write files, move files, delete files) in the container then have a look at the `upperdir` (using `ls -la`)