#
# Conditional build:
%bcond_with	sc	# softCAM support
%bcond_with	xine	# xine support, requires patched xine-lib-devel
#
%define		_sc_ver		0.9.3
%define		_xine_ver	0.9.4
Summary:	Video Disk Recorder
Summary(pl.UTF-8):	Video Disk Recorder - narzędzie do nagrywania filmów
Name:		vdr
Version:	1.7.22
Release:	1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.tvdr.de/vdr/Developer/%{name}-%{version}.tar.bz2
# Source0-md5:	b9c0fe1aac8e653c0d0234bc72c2bb2c
Source1:	http://207.44.152.197/%{name}-sc-%{_sc_ver}.tar.gz
# Source1-md5:	d02d88213fcfb9b6c3f8c819eab4be68
Source2:	http://home.vrweb.de/~rnissl/%{name}-xine-%{_xine_ver}.tgz
# Source2-md5:	0374123d6991f55d91122b020361d8f6
URL:		http://www.tvdr.de/
BuildRequires:	fontconfig-devel
BuildRequires:	fribidi-devel
BuildRequires:	libjpeg-devel
%{?with_xine:BuildRequires:	xine-lib-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# plugins use symbols provided by the binary
%define		skip_post_check_so	.*%{_libdir}/vdr/libvdr-.*\.so\..*

%description
Video Disk Recorder.

%description -l pl.UTF-8
Video Disk Recorder - narzędzie do nagrywania filmów.

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
%{__mv} svdrpsend.pl svdrpsend

{ cd PLUGINS/src
for plugin in * ; do
	%{__mv} $plugin/HISTORY ../../HISTORY-$plugin
	%{__mv} $plugin/README ../../README-$plugin
done
}

%if %{with sc}
cd PLUGINS/src
gzip -dc %{SOURCE1} | tar -xf -
mv sc-%{_sc_ver} sc
cd ../..
patch -p1 < PLUGINS/src/sc/patches/vdr-1.4.x-sc7.diff
%endif

%if %{with xine}
cd PLUGINS/src
gzip -dc %{SOURCE2} | tar -xf -
mv xine-%{_xine_ver} xine
cd ../..
%endif

%build
%{__make} \
	CXXFLAGS="%{rpmcflags}" \
	PREFIX="%{_prefix}" \
	LOCDIR="%{_localedir}" \
	CONFDIR="%{_sysconfdir}/%{name}" \
	VIDEODIR=/var/lib/vdr \
	PLUGINLIBDIR="%{_libdir}/%{name}" \
	BIDI=1 \
	REMOTE=LIRC

%{__make} plugins \
	CXXFLAGS="%{rpmcflags} -fPIC" \
	INCLUDES="-I../../../include -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/themes

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	LOCDIR="%{_localedir}" \
	VIDEODIR=/var/lib/vdr \
	PLUGINLIBDIR="%{_libdir}/%{name}"

cp -p *.conf{,.*} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CONTRIBUTORS HISTORY* INSTALL MANUAL PLUGINS.html README README-* UPDATE-* epg2html summary2info
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/themes
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf*
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/svdrpsend
%attr(755,root,root) %{_libdir}/vdr/libvdr-dvbhddevice.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-dvbsddevice.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-hello.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-osddemo.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-pictures.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-skincurses.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-status.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-svccli.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-svcsvr.so.*
%attr(755,root,root) %{_libdir}/vdr/libvdr-svdrpdemo.so.*
%attr(770,root,video) /var/lib/%{name}
%{_mandir}/man*/%{name}.*

%if %{with sc}
%files sc
%defattr(644,root,root,755)
%doc PLUGINS/src/sc/{HISTORY,README}
%attr(755,root,root) %{_libdir}/libsc*
%attr(755,root,root) %{_libdir}/vdr/libvdr-sc.so.*
%endif

%if %{with xine}
%files xine
%defattr(644,root,root,755)
%doc PLUGINS/src/xine/{HISTORY,MANUAL,INSTALL,README}
%attr(755,root,root) %{_libdir}/vdr/libvdr-xine.so.*
%endif
