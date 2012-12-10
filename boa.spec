%define name boa
%define version 0.94.14
%define rcver	rc21
%define release %mkrel 0.%{rcver}.3
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
%configure2_5x
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




%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.94.14-0.rc21.3mdv2011.0
+ Revision: 610081
- rebuild

* Tue Feb 16 2010 Funda Wang <fwang@mandriva.org> 0.94.14-0.rc21.2mdv2010.1
+ Revision: 506702
- use configuer2_5x
- rediff config patch

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sat Feb 02 2008 Adam Williamson <awilliamson@mandriva.org> 0.94.14-0.rc21.1mdv2008.1
+ Revision: 161359
- rebuild for new era
- 'new' pre-release rc21
- spec clean

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel
    - convert prereq


* Wed Feb 23 2005 Michael Scherer <misc@mandrake.org> 0.94.14-0.rc17.3mdk
- provides webserver
- fix some rpmlint warning

* Mon Oct 25 2004 Michael Scherer <misc@mandrake.org> 0.94.14-0.rc17.2mdk
- Rebuild

* Wed Sep 17 2003 Michael Scherer <scherer.michael@free.fr> 0.94.14-0.rc17.1mdk
- use macro
- [DIRM]
- 0.94.14rc17

* Wed Oct 30 2002 Philippe Libat <philippe@mandrakesoft.com> 0.94.14-0.rc1.3mdk
- fix CGI/POST problem (TMP)
- add /etc/sysconfig/boa external startup file

* Tue Oct 29 2002 Philippe Libat <philippe@mandrakesoft.com> 0.94.14-0.rc1.2mdk
- fix Alias in default config
- add logrotate

* Fri Oct 25 2002 Amaury Amblard-Ladurantie <amaury@mandrakesoft.com> 0.94.14-0.rc1.1mdk
- new release
- changed default config file to match Apache settings

* Thu Apr 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.94.12-0.1rc7mdk
- new release

* Tue Oct 09 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.94.8.3-5mdk
- sanitize for lord rpmlint

* Wed Jul 11 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.94.8.3-4mdk
- build release
- a few spec cleaning

* Thu Mar 29 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.94.8.3-3mdk
- remove doubl chkconfig

* Thu Mar 29 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.94.8.3-2mdk
- fredification (aka rebuild 4 libsafe& co)

* Tue Oct 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.94.8.3-1mdk
- Some noreplace.
- 0.94.8.3 security fix.

* Sun Aug 06 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.94.8.2-1mdk
- rebuild for new shiny version

* Wed Jul 19 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.94.8.1-2mdk
- BM
- use new man macros

* Fri Jul 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.94.8.1-1mdk
- first mandrake version

