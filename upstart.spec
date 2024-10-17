Name:           upstart
Version:        0.6.3
Release:        %mkrel 1
Summary:        An event-driven init system

Group:          System/Configuration/Boot and Init
License:        GPLv2+
URL:            https://upstart.ubuntu.com
Source0:        http://upstart.ubuntu.com/download/0.6/upstart-%{version}.tar.bz2
Source1:	ttyX.conf
# (fc) 0.6.3-1mdv fix rc path
Patch0:		upstart-0.6.3-fix-rc-path.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
#Obsoletes: SysVinit < 2.87-2, sysvinit < 2.87-2
#Provides: SysVinit = 2.87-2, sysvinit = 2.87-2
Conflicts:	sysvinit
BuildRequires:  gettext
BuildRequires: 	dbus-devel
BuildRequires:	expat-devel

%description
Upstart is an event-based replacement for the /sbin/init daemon which
handles starting of tasks and services during boot, stopping them
during shutdown and supervising them while the system is running.

%prep
%setup -q
%patch0 -p1 -b .fix-rc-path

%build
%configure2_5x --sbindir=/sbin --libdir=/%{_lib}
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# libupstart and libnih aren't shipped
rm -f %{buildroot}/%{_lib}/libupstart.*
rm -f %{buildroot}/%{_lib}/libnih.*
rm -f %{buildroot}/%{_includedir}/libnih.h
rm -f %{buildroot}/%{_includedir}/libupstart.h
rm -rf %{buildroot}/%{_includedir}/nih
rm -rf %{buildroot}/%{_includedir}/upstart
rm -rf %{buildroot}/%{_datadir}/aclocal/compiler.m4
rm -rf %{buildroot}/%{_datadir}/aclocal/linker.m4
rm -rf %{buildroot}/%{_datadir}/aclocal/misc.m4

for i in 1 2 3 4 5 6 ; do
 cat %{SOURCE1} | sed -e "s,@TTY@,$i,g" > %{buildroot}/%{_sysconfdir}/init/tty$i.conf
 chmod 644 %{buildroot}/%{_sysconfdir}/init/tty$i.conf
done

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS
%doc COPYING
%doc NEWS
%doc README
%doc TODO
%doc HACKING
%{_sysconfdir}/init
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/*
/sbin/halt
/sbin/init
/sbin/initctl
/sbin/poweroff
/sbin/reboot
/sbin/runlevel
/sbin/shutdown
/sbin/start
/sbin/status
/sbin/stop
/sbin/telinit
/sbin/restart
%{_mandir}/*/*


%changelog
* Thu Sep 10 2009 Frederic Crozat <fcrozat@mandriva.com> 0.6.3-1mdv2010.0
+ Revision: 436825
- Fix buildrequires
- import upstart

