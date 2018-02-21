# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"
  end

  config.vm.provision "shell", inline: <<-SHELL
    grep -q `hostname` /etc/hosts || echo 127.0.0.1 `hostname` |sudo tee -a /etc/hosts
    sudo bash /vagrant/packer/bootstrap.sh
    sudo bash /etc/rc.local
  SHELL
end
