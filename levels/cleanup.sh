#!/usr/bin/env bash
#
# The dirtiest cleanup script
#

# don't interfere with umount
pushd /

# umount stuff
while $(grep -q workshop /proc/mounts); do 
    sudo umount $(grep workshop /proc/mounts | shuf | head -n1 | cut -f2 -d' ') 2>/dev/null
done

# remove stuff
sudo rm -rf /workshop/containers/*

popd
