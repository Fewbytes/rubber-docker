#!/bin/bash -e

function export_image() {
  image_name=$1
  export_name=$2
  shift; shift
  CONTAINER_ID=$(docker run -d $image_name "$@")
  docker wait $CONTAINER_ID
  docker export -o $export_name.tar $CONTAINER_ID
  docker rm $CONTAINER_ID
}

if [ $(id -u) -ne 0 ]; then
    echo "You must run this script as root. Attempting to sudo" 1>&2
    exec sudo -n bash $0 $@
fi

# Wait for cloud-init
sleep 10

# Install packages
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-$(lsb_release -c -s) main" > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get -y install linux-image-extra-$(uname -r)
apt-get -y install docker-engine stress python-dev build-essential htop ipython python-pip
# for vim YouCompleteMe
apt-get -y install vim-youcompleteme

# Include the memory and memsw cgroups
sed -i.bak 's|^kernel.*$|\0 cgroup_enable=memory swapaccount=1|' /boot/grub/menu.lst
sed -i -r 's|GRUB_CMDLINE_LINUX="(.*)"|GRUB_CMDLINE_LINUX="\1 cgroup_enable=memory swapaccount=1"|' /etc/default/grub
update-grub

# Configure Docker to use overlayfs
[[ -d /etc/systemd/system/docker.service.d ]] || mkdir /etc/systemd/system/docker.service.d
cat - >/etc/systemd/system/docker.service.d/overlay.conf <<EOF
[Service]
ExecStart=
ExecStart=/usr/bin/docker daemon -H fd:// --storage-driver overlay
EOF

# restart docker (to use overlay)
systemctl daemon-reload
systemctl restart docker

# Clone git repo
pushd /workshop
git clone https://github.com/Fewbytes/rubber-docker.git
pip install -r rubber-docker/requirements.txt
popd

# Fetch images
mkdir -p /workshop/images
pushd /workshop/images
export_image ubuntu:trusty ubuntu /bin/bash -c 'apt-get update && apt-get install -y python stress'
export_image busybox busybox /bin/true
cp /workshop/rubber-docker/levels/03_pivot_root/breakout.py ./
chmod +x breakout.py
tar rf ubuntu.tar breakout.py
rm breakout.py
popd

# On boot, pull the repo and build the C extension
cat > /etc/rc.local <<'EOF'
#!/bin/bash

# Pull latest version of rubber-docker, install requirements & build the C extension
if [[ -d /workshop/rubber-docker ]]; then
    pushd /workshop/rubber-docker
    git pull && python setup.py install
    [[ -f requirements.txt ]] && pip install -r requirements.txt
    popd
fi

# This will allow us to change rc.local stuff without regenerating the AMI
/workshop/rubber-docker/packer/on_boot.sh

EOF

# Seutp motd
cat > /etc/motd <<'EOF'
Welcome to the "Docker From Scratch" workshop!

Workshop material is in /workshop
Workshop code is checked out in /workshop/rubber-docker

Hint: you probably want to work as root.

Don't forget to have fun and break things :)
EOF

# setup vim
cd ~
vam install youcompleteme
cat > .vimrc <<'EOF'
set bg=dark
syntax on
filetype indent plugin on
EOF
cd -
