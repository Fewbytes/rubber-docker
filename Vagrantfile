# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/wily64"
  # config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "512"
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    # echo deb https://apt.dockerproject.org/repo ubuntu-trusty main | sudo tee /etc/apt/sources.list.d/docker.list
    echo deb https://apt.dockerproject.org/repo ubuntu-wily main | sudo tee /etc/apt/sources.list.d/docker.list
    sudo apt-get update
    sudo apt-get install -y python-dev python-pip build-essential docker-engine

    sudo pip install ipython
  SHELL
end
