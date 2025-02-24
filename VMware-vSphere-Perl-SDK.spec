# ERROR: No build ID note found in .../opt/VMware-vSphere-Perl-SDK/lib/perl5/VMware/pyexe/datetime.so
%define debug_package %{nil}

%global release_tag 17698549

Summary:   vSphere Perl SDK for vSphere
Name:      VMware-vSphere-Perl-SDK
Version:   7.0.0
Release:   %{release_tag}.2%{?dist}
License:   VMware
Source:    %{name}-%{version}-%{release_tag}.x86_64.tar.gz
Patch0:    makefile.patch
Patch1:    uuid-module.patch
URL:       https://developercenter.vmware.com/web/sdk/60/vsphere-perl

# avoid circular dependencies of VMware-vSphere-Perl-SDK on itself
Autoreq:   0

%global prefix /opt/%{name}


BuildRequires: perl
BuildRequires: perl-ExtUtils-MakeMaker

Requires: perl-Monitoring-Plugin
%if 0%{?el7}
Requires: perl-Data-Dumper
%endif
# check_vmware_api.pl fails with if the package below is missing:
# VMWARE_API UNKNOWN - Missing perl module VMware::VIRuntime
Requires: perl-XML-LibXML
# check_vmware_api.pl fails with if the package below is missing:
# CHECK_VMWARE_API.PL CRITICAL - Server version unavailable at
Requires: perl-libwww-perl
%if 0%{?el7}
Requires: perl-HTTP-Date
Requires: perl-LWP-Protocol-https
Requires: perl-Net-HTTP
%endif
# uuid-perl replaces UUID thanks to uuid-module.patch
Requires: perl(Data::UUID)

Requires: perl-Devel-StackTrace perl-Class-Data-Inheritable perl-Convert-ASN1 perl-Crypt-OpenSSL-RSA
Requires: perl-Crypt-OpenSSL-X509
Requires: perl-Exception-Class-TryCatch perl-Archive-Zip perl-Path-Class perl-Class-MethodMaker perl-Data-Dump perl-SOAP-Lite perl-Socket6 perl-IO-Socket-INET6 perl-Net-INET6Glue
Requires: perl-Text-Template
%if 0%{?el6}
Requires: perl-Class-Accessor perl-Config-Tiny
%endif

%description
The vSphere SDK for Perl provides an easy-to-use Perl scripting interface to the vSphere API. Administrators and
developers can work with vSphere API objects using vSphere SDK for Perl. vSphere SDK for Perl 4.0 and later is
bundled with the vSphere Command-Line Interface (vSphere CLI). When you install vSphere SDK for Perl, both
vSphere CLI and vSphere SDK for Perl are installed.


%prep
%setup -q -n vmware-vsphere-cli-distrib
%patch0 -p0
%patch1 -p0

# remove unused modules
%{__rm} -rf lib/5.10/Crypt-X509-* lib/5.10/Crypt-SSLeay-* lib/5.10/Crypt-OpenSSL-RSA-*
%{__sed} -i '/X509/d' vmware-install.pl
%{__rm} -rf lib/UUID-Random-* lib/5.10/UUID-Random-*
%{__sed} -i '/UUID::Random/d' vmware-install.pl

# How to force installation of modules from CPAN during
#yum -y install perl-Devel-CheckLib libuuid-devel openssl-devel perl-CPAN perl-Module-Build
#%%{__sed} -i 's/install_rhel55_local = 1/install_rhel55_local = 0/' vmware-install.pl
#%%{__sed} -i "s/'yesno', ''/'yesno', 'yes'/" vmware-install.pl
#%%{__perl} vmware-install.pl --default --prefix=%%{prefix} EULA_AGREED=yes


%build
%{__perl} Makefile.PL INSTALL_BASE=$RPM_BUILD_ROOT%{prefix}
make

cat <<EOF > %{name}.sh
# NOTE: This is an automatically-generated file!  (generated by the
# %%{name} RPM).  Any changes made here will be lost if the RPM is
# uninstalled or upgraded.

PA=%{prefix}/bin

case \$PATH in
*\${PA}*);;
*?*) PATH=\${PA}:\${PATH};;
*) PATH=\${PA};;
esac
export PATH

PA=%{prefix}/lib/perl5

case \$PERL5LIB in
*\${PA}*);;
*?*) PERL5LIB=\${PA}:\${PERL5LIB};;
*) PERL5LIB=\${PA};;
esac
export PERL5LIB

PA=%{prefix}/man

case \$MANPATH in
  *\${PA}*)      ;;
  *?*)  MANPATH=\${PA}:\${MANPATH} ;;
  *)    MANPATH=\${PA}: ;;
esac
export MANPATH
EOF

cat <<EOF > %{name}.csh
# NOTE: This is an automatically-generated file!  (generated by the
# %%{name} RPM).  Any changes made here will be lost if the RPM is
# uninstalled or upgraded.

set PA=%{prefix}/bin

if (\$?PATH) then
if ("\$PATH" !~ *\${PA}*) then
	setenv PATH \${PA}:\${PATH}
endif
else
setenv PATH \${PA}
endif

unset PA

set PA=%{prefix}/lib/perl5

if (\$?PERL5LIB) then
if ("\$PERL5LIB" !~ *\${PA}*) then
	setenv PERL5LIB \${PA}:\${PERL5LIB}
endif
else
setenv PERL5LIB \${PA}
endif

unset PA

set PA=%{prefix}/man

if (\$?MANPATH) then
    if ("\$MANPATH" !~ *\${PA}*) then
        setenv MANPATH \${PA}:\${MANPATH}
    endif
else
    setenv MANPATH \${PA}:
endif

unset PA
EOF


%install
make install
%{__sed} -i "s|$RPM_BUILD_ROOT||" $RPM_BUILD_ROOT%{prefix}/lib/perl5/x86_64-linux-thread-multi/perllocal.pod

# remove bundled libraries
%{__rm} -rf $RPM_BUILD_ROOT%{prefix}/lib/perl5/VMware/pyexe/

# must use old lib/libwww-perl-5.805 in 6.0.0-3561779 otherwise check_vmware_api.pl hangs
# check_vmware_api.pl hangs with and perl-libwww-perl-6.05-2.el7.noarch perl-LWP-Protocol-https-6.04 
#%{__cp} -rp lib/libwww-perl-*/lib/LWP $RPM_BUILD_ROOT%{prefix}/lib/perl5/LWP
# check_vmware_api.pl hangs with perl-Net-HTTP-6.06-2.el7.noarch
#%{__cp} -rp lib/libwww-perl-*/lib/Net $RPM_BUILD_ROOT%{prefix}/lib/perl5/Net

# copy executables
%{__cp} -rp bin/* $RPM_BUILD_ROOT%{prefix}/bin

# remove uninstall scripts
%{__rm} -rf $RPM_BUILD_ROOT%{prefix}/bin/vmware-uninstall-vSphere-CLI.pl*

# install /etc/profile.d scripts (into bin)
%{__cp} -p %{name}*.*sh $RPM_BUILD_ROOT%{prefix}/bin


%files
%{prefix}


%changelog
* Thu Oct 21 2021 Frank Fenor <red@ct.ed> 7.0.0 17698549
- update to 7.0.0
- add EL8 support

* Wed Jul 13 2016 Marcin Dulak <Marcin.Dulak@gmail.com> 6.0.0 3561779-2
- update and package as a single RPM

* Fri Feb 22 2013 Schlomo Schapiro <schlomo.schapiro@immobilienscout24.de> 5.1.0 780721
- SDK 5.1.0 780721

* Sun Oct 23 2011 Vaughan Whitteron <rpmbuild@firetooth.net> 5.0.0 522456.1
- Split package into Perl SDK and CLI packages
- Include RCLI scripts in the CLI package

* Mon Aug 29 2011 Vaughan Whitteron <rpmbuild@firetooth.net> 5.0.0 522456
- SDK 5.0.0 522456
