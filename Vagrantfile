# -*- mode: ruby -*-
# vi: set ft=ruby :

CENTOSVER=ENV.fetch('CENTOSVER', '7.2')

Vagrant.configure(2) do |config|
  config.vm.define "centos" do |machine|
    machine.vm.box = 'puppetlabs/centos-' + CENTOSVER + '-64-puppet'
    machine.vm.box_url = 'puppetlabs/centos-' + CENTOSVER + '-64-puppet'
    machine.vm.provider "virtualbox" do |v|
      v.memory = 256
      v.cpus = 1
    end
  end
  config.vm.define "centos" do |machine|
    machine.vm.provision :shell, :inline => "hostname localhost", run: "always"
    machine.vm.provision :shell, :inline => 'yum clean all'
    machine.vm.provision :shell, :inline => 'yum -y install git rpm-build'
    machine.vm.provision :shell, :inline => 'yum -y install rpm-build perl-ExtUtils-MakeMaker'
    machine.vm.provision :shell, :inline => "sudo su - vagrant -c \"rpmbuild -bb --define '_sourcedir /vagrant' /vagrant/VMware-vSphere-Perl-SDK.spec\""
    machine.vm.provision :shell, :inline => "if `cat /etc/redhat-release | grep -qi 'release 6'` && ! rpm -q epel-release; then yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm; fi"
    machine.vm.provision :shell, :inline => "if `cat /etc/redhat-release | grep -qi 'release 7'` && ! rpm -q epel-release; then yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm; fi"
    machine.vm.provision :shell, :inline => "if `cat /etc/redhat-release | grep -qi 'release 8'` && ! rpm -q epel-release; then yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; fi"
    machine.vm.provision :shell, :inline => "yum -y install /home/vagrant/rpmbuild/RPMS/*/*.rpm"
    machine.vm.provision :shell, :inline => "source /opt/VMware-vSphere-Perl-SDK/bin/VMware-vSphere-Perl-SDK.sh&& vmware-cmd --help"
    machine.vm.provision :shell, :inline => "mkdir -p /vagrant/" + CENTOSVER
    machine.vm.provision :shell, :inline => "cp -rpf /home/vagrant/rpmbuild/RPMS /vagrant/" + CENTOSVER
  end
end

