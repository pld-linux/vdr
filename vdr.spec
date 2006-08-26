%bcond_with	sc	# softCAM support
%bcond_without	xine	# xine support

%define		_sc_ver		0.5.9
%define		_xine_ver	0.7.9
Summary:	Video Disk Recorder
Summary(pl):	Video Disk Recorder
Name:		vdr
Version:	1.4.1
Release:	0.1
License:	- (enter GPL/GPL v2/LGPL/BSD/BSD-like/other license name here)
Group:		Applications
Source0:	ftp://ftp.cadsoft.de/vdr/%{name}-%{version}.tar.bz2
# Source0-md5:	f17ab7d185f3c5426cc713c2ad4cc708
Source1:	http://207.44.152.197/%{name}-sc-%{_sc_ver}.tar.gz
# Source1-md5:	cbd648dd4b7e9f8d08d86fc75a6681b0
Source2:	http://home.vrweb.de/~rnissl/%{name}-xine-%{_xine_ver}.tgz
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.cadsoft.de/vdr/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Video Disk Recorder

%description -l pl
Video Disk Recorder

%package sc
Summary:	SoftCAM plugin for VDR
Summary(pl):	Wtyczka SoftCAM dla VDR
Group:		Applications

%description sc
It's not legal to use this software in most countries of the world. SC
means softcam, which means a software CAM emulation.

%description sc -l pl
U¿ywanie tego oprogramowania jest nielegalne we wiêkszo¶ci krajów
¶wiata. SC znaczy softcam, co oznacza programowa emulacje CAM.

%package xine
Summary:	xine plugin for VDR
Summary(pl):	Wtyczka xine dla VDR
Group:		Libraries

%description xine
xine plugin for VDR

%description xine -l pl
Wtyczka xine dla VDR

%prep
%setup -q
%patch0 -p1
%if %{with sc}
cd PLUGINS/src/
/bin/gzip -dc %{SOURCE1} | tar -xf -
mv sc* sc
cd ../../
patch -p1 <PLUGINS/src/sc/patches/vdr-1.4.0-sc.diff
%endif

%if %{with xine}
cd PLUGINS/src/
/bin/gzip -dc %{SOURCE2} | tar -xf -
mv xine* xine
cd ../../
%endif

%build
%{__make} \
	BINDIR="%{_bindir}" \
	MANDIR="%{_mandir}" \
	VIDEODIR=/var/lib/vdr \
	PLUGINLIBDIR="%{_libdir}" \
	REMOTE=LIRC

%{__make} plugins \
	BINDIR="%{_bindir}" \
	MANDIR="%{_mandir}" \
	VIDEODIR=/var/lib/vdr \
	PLUGINLIBDIR="%{_libdir}" \
	INCLUDES="-I../../../include -I/usr/include/ncurses" \
	REMOTE=LIRC

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/vdr
install -d $RPM_BUILD_ROOT%{_sysconfdir}/vdr/plugins

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR="%{_bindir}" \
	MANDIR="%{_mandir}" \
	VIDEODIR=/var/lib/vdr \
	PLUGINLIBDIR="%{_libdir}"

mv $RPM_BUILD_ROOT/var/lib/vdr/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/vdr
cd $RPM_BUILD_ROOT
ln -s %{_sysconfdir}/vdr/channels.conf var/lib/vdr/
ln -s %{_sysconfdir}/vdr/diseqc.conf var/lib/vdr/
ln -s %{_sysconfdir}/vdr/keymacros.conf var/lib/vdr/
ln -s %{_sysconfdir}/vdr/sources.conf var/lib/vdr/
ln -s %{_sysconfdir}/vdr/svdrphosts.conf var/lib/vdr/
ln -s %{_sysconfdir}/vdr/plugins var/lib/vdr/

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc epg2html.pl HISTORY INSTALL MANUAL PLUGINS.html README summary2info.pl svdrpsend.pl UPDATE-*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libvdr-hello.so*
%attr(755,root,root) %{_libdir}/libvdr-osddemo.so*
%attr(755,root,root) %{_libdir}/libvdr-skincurses.so*
%attr(755,root,root) %{_libdir}/libvdr-sky.so*
%attr(755,root,root) %{_libdir}/libvdr-status.so*
%attr(755,root,root) %{_libdir}/libvdr-svccli.so*
%attr(755,root,root) %{_libdir}/libvdr-svcsvr.so*
%attr(755,root,root) %{_libdir}/libvdr-svdrpdemo.so*
%attr(755,video,video) /var/lib/%{name}
%{_mandir}/*/*

%if %{with sc}
%files sc
%defattr(644,root,root,755)
%doc PLUGINS/src/sc/HISTORY PLUGINS/src/sc/README
%attr(755,root,root) %{_libdir}/libsc*
%attr(755,root,root) %{_libdir}/libvdr-sc.so*
%endif

%if %{with xine}
%files xine
%defattr(644,root,root,755)
%doc PLUGINS/src/xine/HISTORY PLUGINS/src/xine/MANUAL PLUGINS/src/xine/INSTALL PLUGINS/src/xine/README
%attr(755,root,root) %{_libdir}/libvdr-xine.so*
%endif
