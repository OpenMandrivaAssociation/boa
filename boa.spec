%define name boa
%define version 0.94.14
%define rcver	rc21
%define release %mkrel 0.%{rcver}.1
%define webrootdir /var/www/html


Summary:	Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.boa.org/%{name}-%{version}%{rcver}.tar.gz
Source1:	boa.init
Source2:	boa.sysconfig
Patch:		boa-default-config.patch
URL:		http://www.boa.org/
License:	GPL+
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-%{version}buildroot
BuildRequires:	flex
BuildRequires:	bison

Requires(post):		rpm-helper
Requires(postun):	rpm-helper

Provides: webserver

%description
A high speed, lightweight web server (HTTP protocol).
Based on direct use of the select(2) system call, it
internally multiplexes all connections without forking,
for maximum speed and minimum system resource use.

%prep
%setup -q -n %{name}-%{version}%{rcver}
%patch -p1

%build
%serverbuild
%configure
%make CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
cd src
mkdir -p %{buildroot}%{_sbindir}
install boa %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}/boa
install boa_indexer %{buildroot}%{_libdir}/boa/

mkdir -p %{buildroot}/%{webrootdir}

cd ..
mkdir -p %{buildroot}%{_mandir}/man8
install -m 644 docs/boa.8 %{buildroot}%{_mandir}/man8/

cd examples
mkdir -p %{buildroot}/%{_sysconfdir}/{boa,logrotate.d}
install -m 644 boa.conf %{buildroot}/%{_sysconfdir}/boa/
cd ../contrib
install -m 644 rpm/boa.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/boa

cd ..
mkdir -p %{buildroot}/%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}/%{_initrddir}/boa
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/boa

mkdir -p %{buildroot}/var/log/boa
%clean
rm -rf %{buildroot}

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


