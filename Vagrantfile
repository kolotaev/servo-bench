# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/jessie64"

  config.vm.provider :virtualbox do |v|
    v.name = "test-machine"
    v.memory = 512
    v.cpus = 1
    v.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.hostname = "test-machine"
  config.vm.network "private_network", ip: "192.168.33.33"

  config.vm.synced_folder ".", "/shared"
end
