%define name boa
%define version 0.94.14
%define rcver	rc17
%define release 0.rc17.3mdk
%define webrootdir /var/www/html


Summary: The boa web server
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.boa.org/%{name}-%{version}%{rcver}.tar.bz2
Source1: boa.init
Source2: boa.sysconfig
Patch: boa-default-config.patch
URL: http://www.boa.org/
License: GPL
Group: System/Servers
BuildRoot: %{_tmppath}/%{name}-%{version}buildroot
BuildRequires: flex bison
Requires: /etc/mime.types
Prereq: rpm-helper
Provides: webserver

%description
a high speed, lightweight web server (HTTP protocol).
based on direct use of the select(2) system call, it
internally multiplexes all connections without forking,
for maximum speed and minimum system resource use.

%prep
%setup -q -n %{name}-%{version}%{rcver}
%patch -p 1

%build
%serverbuild
%configure
%make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
cd src
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install boa $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/boa
install boa_indexer $RPM_BUILD_ROOT%{_libdir}/boa/

mkdir -p $RPM_BUILD_ROOT/%{webrootdir}

cd ..
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m 644 docs/boa.8 $RPM_BUILD_ROOT%{_mandir}/man8/

cd examples
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/{boa,logrotate.d}
install -m 644 boa.conf $RPM_BUILD_ROOT/%{_sysconfdir}/boa/
cd ../contrib
install -m 644 redhat/boa.logrotate $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/boa

cd ..
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/boa
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/boa

mkdir -p $RPM_BUILD_ROOT/var/log/boa
%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service boa

%preun
%_preun_service boa

%files
%defattr(-,root,root)
%doc docs/*.{texi,png} contrib/*
%{_sbindir}/boa
%{_libdir}/boa/boa_indexer
%dir %{_libdir}/boa/
%dir %{_sysconfdir}/boa
%config(noreplace) %{_initrddir}/boa
%config(noreplace) %{_sysconfdir}/boa/boa.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/boa
%config(noreplace) %{_sysconfdir}/sysconfig/boa
%dir %{webrootdir}
%dir /var/log/boa
%{_mandir}/man8/*


