#!/bin/bash
set -e

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
    exec sudo -H -n bash $0 $@
fi

# Wait for cloud-init
sleep 10

# Install packages
export DEBIAN_FRONTEND=noninteractive
export DEBIAN_PRIORITY=critical
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt update
apt install -y docker-ce stress python3-dev build-essential cmake htop ipython3 python3-pip python3-click git

# Include the memory and memsw cgroups for cgroups v1 on old images; not needed for ubuntu 24.04 cgroups v2
# sed -i.bak 's|^kernel.*$|\0 cgroup_enable=memory swapaccount=1|' /boot/grub/menu.lst
# sed -i -r 's|GRUB_CMDLINE_LINUX="(.*)"|GRUB_CMDLINE_LINUX="\1 cgroup_enable=memory swapaccount=1"|' /etc/default/grub
# update-grub

# Configure Docker to use overlayfs
cat - > /etc/docker/daemon.json <<'EOF'
{
  "storage-driver": "overlay2"
}
EOF
# restart docker (to use overlay)
systemctl restart docker

usermod -G docker -a ubuntu

# Clone git repo
mkdir /workshop
git clone https://github.com/Fewbytes/rubber-docker.git /workshop/rubber-docker

# Fetch images
mkdir -p /workshop/images
pushd /workshop/images
export_image ubuntu:noble ubuntu-export /bin/bash -c 'apt get update && apt get install -y python stress'
export_image busybox busybox /bin/true
cp /workshop/rubber-docker/levels/03_pivot_root/breakout.py ./
chmod +x breakout.py
tar cf ubuntu.tar breakout.py
tar Af ubuntu.tar ubuntu-export.tar
rm breakout.py ubuntu-export.tar
popd

# On boot, pull the repo and build the C extension
cat > /etc/rc.local <<'EOF'
#!/bin/bash

# Pull latest version of rubber-docker, install requirements & build the C extension
if [[ -d /workshop/rubber-docker ]]; then
    pushd /workshop/rubber-docker
    git pull && pip install --break-system-packages .
    # [[ -f requirements.txt ]] && pip install -r requirements.txt
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
sudo -H -u ubuntu bash -e <<'EOS'
cd ~
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
cp /tmp/vimrc ~/.vimrc
echo "Installing plugins using Vundle"
echo | echo | vim +PluginInstall +qall &>/dev/null
echo "Vundle done"
python3 ~/.vim/bundle/YouCompleteMe/install.py 
EOS