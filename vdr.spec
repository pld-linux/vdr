#
# Conditional build:
%bcond_with	sc	# softCAM support (outdated code)
%bcond_with	xine	# xine support (outdated code)
#
%define		sc_ver		0.9.3
%define		xine_ver	0.9.4
Summary:	Video Disk Recorder
Summary(pl.UTF-8):	Video Disk Recorder - narzędzie do nagrywania filmów
Name:		vdr
Version:	2.0.0
Release:	1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.tvdr.de/vdr/%{name}-%{version}.tar.bz2
# Source0-md5:	fd7f481b996e03fae3c00e80b6b0d301
Source1:	http://207.44.152.197/%{name}-sc-%{sc_ver}.tar.gz
# Source1-md5:	d02d88213fcfb9b6c3f8c819eab4be68
Source2:	http://home.vrweb.de/~rnissl/%{name}-xine-%{xine_ver}.tgz
# Source2-md5:	0374123d6991f55d91122b020361d8f6
URL:		http://www.tvdr.de/
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	fribidi-devel
BuildRequires:	libcap-devel
BuildRequires:	libjpeg-devel
BuildRequires:	ncurses-devel >= 5
%{?with_xine:BuildRequires:	xine-lib-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# plugins use symbols provided by the binary
%define		skip_post_check_so	.*%{_libdir}/vdr/libvdr-.*\.so\..*

%description
Video Disk Recorder.

%description -l pl.UTF-8
Video Disk Recorder - narzędzie do nagrywania filmów.

%package devel
Summary:	Header files for %{name}
Summary(pl.UTF-8):	Pliki nagłówkowe %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name}.

%description devel -l pl.UTF-8
Pliki nagłówkowe %{name}.

%package sc
Summary:	SoftCAM plugin for VDR
Summary(pl.UTF-8):	Wtyczka SoftCAM dla VDR
Group:		Applications

%description sc
It's not legal to use this software in most countries of the world. SC
means softcam, which means a software CAM emulation.

%description sc -l pl.UTF-8
Używanie tego oprogramowania jest nielegalne w większości krajów
świata. SC znaczy softcam, co oznacza programową emulację CAM.

%package xine
Summary:	xine plugin for VDR
Summary(pl.UTF-8):	Wtyczka xine dla VDR
Group:		Libraries

%description xine
xine plugin for VDR.

%description xine -l pl.UTF-8
Wtyczka xine dla VDR.

%prep
%setup -q

cd PLUGINS/src
for plugin in *; do
	%{__mv} $plugin/HISTORY ../../HISTORY-$plugin
	%{__mv} $plugin/README ../../README-$plugin
done
cd ../..

%if %{with sc}
cd PLUGINS/src
gzip -dc %{SOURCE1} | tar -xf -
mv sc-%{sc_ver} sc
cd ../..
%{__patch} -p1 < PLUGINS/src/sc/patches/vdr-1.4.x-sc7.diff
%endif

%if %{with xine}
cd PLUGINS/src
gzip -dc %{SOURCE2} | tar -xf -
mv xine-%{xine_ver} xine
cd ../..
%endif

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} -I/usr/include/ncurses" \
	PREFIX="%{_prefix}" \
	LOCDIR="%{_localedir}" \
	CONFDIR="%{_sysconfdir}/%{name}" \
	VIDEODIR=/var/lib/vdr \
	PLUGINLIBDIR="%{_libdir}/%{name}" \
	BIDI=1 \
	REMOTE=LIRC

%{__make} plugins \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} -fPIC" \
	INCLUDES="-I../../../include -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{plugins,themes}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	LOCDIR="%{_localedir}" \
	VIDEODIR=/var/lib/vdr \
	PLUGINLIBDIR="%{_libdir}/%{name}"

cp -p *.conf{,.*} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# hack
for langdir in $RPM_BUILD_ROOT%{_datadir}/locale/*_*; do
	lang=$(basename $langdir)
	[ $lang = "zh_CN" ] && continue
	newlang=$(echo "$lang" | sed -e 's#_.*##g')
	mv $RPM_BUILD_ROOT%{_datadir}/locale/{$lang,$newlang}
done

# vdr, vdr-dvbhddevice, vdr-hello, vdr-pictures, vdr-skincurses domains
%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CONTRIBUTORS HISTORY* INSTALL MANUAL PLUGINS.html README README-* UPDATE-* epg2html summary2info
%attr(2775,root,video) %dir %{_sysconfdir}/%{name}
%attr(2775,root,video) %dir %{_sysconfdir}/%{name}/plugins
%attr(2775,root,video) %dir %{_sysconfdir}/%{name}/themes
%attr(664,root,video) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/channels.conf
%attr(664,root,video) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/channels.conf.cable
%attr(664,root,video) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/channels.conf.terr
%attr(664,root,video) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/diseqc.conf
%attr(664,root,video) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/keymacros.conf
%attr(664,root,video) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/scr.conf
%attr(664,root,video) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/sources.conf
%attr(664,root,video) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/svdrphosts.conf
%attr(755,root,root) %{_bindir}/vdr
%attr(755,root,root) %{_bindir}/svdrpsend
%dir %{_libdir}/vdr
%attr(755,root,root) %{_libdir}/vdr/libvdr-dvbhddevice.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-dvbsddevice.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-epgtableid0.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-hello.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-osddemo.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-pictures.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-rcu.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-skincurses.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-status.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-svccli.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-svcsvr.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-svdrpdemo.so.*
%attr(2775,root,video) %dir /var/lib/%{name}
# XXX: %ghost or %config?
%attr(664,root,video) /var/lib/%{name}/*.conf
%{_mandir}/man1/svdrpsend.1*
%{_mandir}/man1/vdr.1*
%{_mandir}/man5/vdr.5*

%files devel
%defattr(644,root,root,755)
%doc README.i18n
%{_includedir}/libsi
%{_includedir}/vdr
%{_pkgconfigdir}/vdr.pc

%if %{with sc}
%files sc
%defattr(644,root,root,755)
%doc PLUGINS/src/sc/{HISTORY,README}
%attr(755,root,root) %{_libdir}/libsc-*.so*
%attr(755,root,root) %{_libdir}/vdr/libvdr-sc.so.*
%endif

%if %{with xine}
%files xine
%defattr(644,root,root,755)
%doc PLUGINS/src/xine/{HISTORY,MANUAL,INSTALL,README}
%attr(755,root,root) %{_libdir}/vdr/libvdr-xine.so.*
%endif
