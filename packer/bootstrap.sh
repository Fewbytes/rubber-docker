#!/bin/bash

if [ $(id -u) -ne 0 ]; then
    echo "You must run this script as root. Attempting to sudo" 1>&2
    exec sudo -n bash $0 $@
fi

# Wait for cloud-init
sleep 10

# Install packages
apt-get update

apt-get -y install docker.io stress python-dev build-essential htop ipython

# Include the memory and memsw cgroups
sed -i.bak 's|^kernel.*$|\0 cgroup_enable=memory swapaccount=1|' /boot/grub/menu.lst

# Configure Docker to use overlayfs
[[ -d /etc/systemd/system/docker.service.d ]] || mkdir /etc/systemd/system/docker.service.d
cat - >/etc/systemd/system/docker.service.d/overlay.conf <<EOF
[Service]
ExecStart=
ExecStart=/usr/bin/docker daemon -H fd:// --storage-driver overlay
EOF

# restart docker
systemctl daemon-reload
systemctl restart docker

# Fetch images
mkdir -p /root/images
pushd /root/images
for i in busybox ubuntu:latest; do
    echo Fetching $i image
    docker pull $i && docker save -o $i.tar $i
done
popd

# Clone git repo
pushd /root
git clone https://github.com/Fewbytes/rubber-docker.git
popd

# On boot, pull the repo and build the C extension
cat > /etc/rc.local <<'EOF'
#!/bin/bash

if [[ -d /root/rubber-docker ]]; then
    pushd /root/rubber-docker
    git pull && python setup.py install
    popd
fi
EOF

# Seutp motd
cat > /etc/motd <<'EOF'
Welcome to the "Docker From Scratch" workshop!

Don't forget to have fun and break things :)
EOF
