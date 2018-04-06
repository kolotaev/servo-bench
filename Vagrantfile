# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/jessie64"
  config.ssh.insert_key = false

  config.vm.provider :virtualbox do |v|
    v.name = "test-machine"
    v.memory = 512
    v.cpus = 1
    v.customize ["modifyvm", :id, "--ioapic", "on"]
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  config.vm.provision "shell", path: "provision.sh", privileged: true

  config.vm.hostname = "test-machine"
  config.vm.network :forwarded_port, guest: 8080, host: 8088

  config.vm.synced_folder ".", "/shared"
end
