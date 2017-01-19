# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.provision 'shell', path: 'install-python'
  config.vm.synced_folder "../client-server-app/", "/home/vagrant", create: true
end
