Name:		rtmpdump
Version:	2.3
Release:	3%{?dist}
Summary:	Toolkit for RTMP streams

Group:		Applications/Internet
License:	GPLv2+
# Note that librtmp is actually LGPLv2, so if you package that separately
# (for which you'd probably want to make it a dynamic library) you should
# label its licence correctly. But the _tools_ are GPLv2.
URL:		http://rtmpdump.mplayerhq.hu/
Source0:	http://rtmpdump.mplayerhq.hu/download/rtmpdump-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gnutls-devel zlib-devel

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://. 

%package -n librtmp
Summary:	Support library for RTMP streams
Group:		Applications/Internet
License:	LGPLv2+

%description -n librtmp
librtmp is a suport library for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://. 

%package -n librtmp-devel
Summary:	Files for librtmp development
Group:		Applications/Internet
License:	LGPLv2+
Requires:	librtmp = %{version}-%{release}

%description -n librtmp-devel
librtmp is a suport library for RTMP streams. The librtmp-devel package
contains include files needed to develop applications using librtmp.

%prep
%setup -q

%build
# The fact that we have to add -ldl for gnutls is Fedora bug #611318
make CRYPTO=GNUTLS SHARED=yes OPT="$RPM_OPT_FLAGS" LIB_GNUTLS="-lgnutls -lgcrypt -ldl" LIBRTMP=librtmp/librtmp.so LIBS=


%install
rm -rf $RPM_BUILD_ROOT
make CRYPTO=GNUTLS SHARED=yes DESTDIR=$RPM_BUILD_ROOT prefix=/usr mandir=%{_mandir} libdir=%{_libdir} install
rm -f $RPM_BUILD_ROOT/%{_libdir}/librtmp.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -n librtmp -p /sbin/ldconfig

%postun -n librtmp -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/rtmpdump
%{_sbindir}/rtmpsrv
%{_sbindir}/rtmpgw
%{_sbindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*
%doc COPYING README

%files -n librtmp
%defattr(-,root,root,-)
%{_libdir}/librtmp.so.0
%doc librtmp/COPYING

%files -n librtmp-devel
%defattr(-,root,root,-)
/usr/include/librtmp
%{_libdir}/librtmp.so
%{_libdir}/pkgconfig/librtmp.pc
%{_mandir}/man3/librtmp.3*
%doc ChangeLog

%changelog
* Wed Jan 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3-3
- Rebuilt for target i686

* Sun Jul 04 2010 Dominik Mierzejewski <rpm@greysector.net> 2.3-2
- call ldconfig in post(un) scripts for the shared library
- add strict dependency on the library to -devel

* Sun Jul 04 2010 David Woodhouse <dwmw2@infradead.org> 2.3-1
- Update to 2.3; build shared library

* Fri Apr 30 2010 David Woodhouse <dwmw2@infradead.org> 2.2d-1
- Update to 2.2d

* Tue Apr 20 2010 David Woodhouse <dwmw2@infradead.org> 2.2c-2
- Link with libgcrypt explicitly since we call it directly

* Mon Apr 19 2010 David Woodhouse <dwmw2@infradead.org> 2.2c-1
- Initial package
