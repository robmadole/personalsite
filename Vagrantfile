# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"

  # Flask in development mode
  config.vm.network :forwarded_port, guest: 5000, host: 5000, auto_correct: false
  # Sphinx docs
  config.vm.network :forwarded_port, guest: 5001, host: 5001, auto_correct: false
  # Karma test runner
  config.vm.network :forwarded_port, guest: 9876, host: 9876, auto_correct: false

  # For Salt
  config.vm.synced_folder "salt/roots", "/srv"

  config.vm.provision :salt do |salt|
    salt.run_highstate = true
    salt.minion_config = "salt/minion"
    salt.install_type = "git"
    salt.install_args = "v2014.1.1"
    salt.install_master = false
    salt.bootstrap_script = "salt/bootstrap.sh"
    salt.verbose = false
  end
end
