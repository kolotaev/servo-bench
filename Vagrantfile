# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/bullseye64"
  config.ssh.insert_key = false

  vm_name = "servobench"

  config.vm.provider :virtualbox do |v|
    v.name = vm_name
    v.memory = 1024
    v.cpus = 1
    v.customize ["modifyvm", :id, "--ioapic", "on"]
    # v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    # v.customize ["modifyvm", :id, "--cpuexecutioncap", "10"]
  end

  config.vm.provision "shell", path: "provision.sh", privileged: true

  config.vm.hostname = vm_name
  config.vm.network "private_network", ip: '192.80.80.80'
  # config.vm.network "public_network", type: "dhcp", :bridge => 'en0' # rarely it's needed when docker can't pull images
  config.vm.network :forwarded_port, guest: 8080, host: 8080
  config.vm.network :forwarded_port, guest: 8081, host: 8081
  config.vm.network :forwarded_port, guest: 5432, host: 54320

  config.vm.synced_folder ".", "/shared"
end
