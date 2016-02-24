# Level 03: pivot_root

After succesfully jailing a process with *chroot()*, let's escape from this jail: copy the breakout.py script into the chroot and run it!

Ok, obviously *chroot()* isn't good enough. Let's try using *pivot_root()* - remember that *pivot_root()* works on **all** processes - luckily we are using mount namespaces.