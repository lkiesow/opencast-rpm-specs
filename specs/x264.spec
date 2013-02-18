
Summary:       A free h264/avc encoder
Name:          x264
Version:       0.129
%define        pkgversion 20130127-2245
Release:       1_20130127.2245%{?dist}
License:       GPLv2
Group:         Applications/Multimedia
URL:           http://www.videolan.org/developers/x264.html
Source0:       ftp://ftp.videolan.org/pub/videolan/x264/snapshots/%{name}-snapshot-%{pkgversion}-stable.tar.bz2
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libX11-devel
BuildRequires: gpac-devel
BuildRequires: nasm, yasm
BuildRequires: gettext


%package libs
Summary:        Library for encoding H264/AVC video streams
Group:          System Environment/Libraries
Requires:       %{name}-libs = %{version}-%{release}


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}


%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch. This package contains the executable.

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch. This package contains the libraries.

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch. This package contains the development files.

%prep
%setup -q -n %{name}-snapshot-%{pkgversion}-stable
perl -pi -e's, -lintl,,' gtk/Makefile
#grep -rl /usr/X11R6/lib . | xargs perl -pi -e's,/usr/X11R6/lib,%{_x_libraries},'

%build
%configure \
  %{?with_gpac:--enable-mp4-output} \
  --enable-pthread \
  --enable-visualize \
  --enable-pic \
  --enable-shared \
  --extra-cflags="%{optflags}"
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir} %{buildroot}%{_libdir}/pkgconfig \
  %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS doc/*.txt
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%doc COPYING AUTHORS doc/*.txt
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libx264.so

%files libs
%defattr(-,root,root,-)
%doc COPYING AUTHORS doc/*.txt
%defattr(-,root,root,-)
%{_libdir}/libx264.so.*

%changelog
* Fri Mar  2 2012 Lars Kiesow <lkiesow@uos.de> - 0.129-1_20130127.2245
- Updated to new version

* Fri Mar  2 2012 Lars Kiesow <lkiesow@uos.de> - 0.118-19_20111111.2245
- Corrected some minor packaging issues.

* Thu Feb 16 2012 Lars Kiesow <lkiesow@uos.de> - 0.118-18_20111111.2245
- Fixed issues with CentOS
- Build devel and libs package

* Sat Nov 12 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.118-17_20111111.2245
- Update to latest stable snapshot.

* Sat Jun 11 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.115-16_20110610.2245
- Update to latest stable snapshot.

* Wed Mar  9 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.114-15_20110308.2245
- Update to latest stable snapshot.

* Sat Oct  2 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.106-13_20101001.2245
- Update to latest git.

* Tue Jun 22 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.98-12_20100621.2245
- Update to latest git.

* Thu Apr  1 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.92-12_20100401.2245
- Update to latest git.

* Fri Nov 20 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.79-11_20091119.2245
- Update to latest git.

* Mon Jul 20 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.68-10_20090719.2245
- Update to latest git.

* Sun Nov 16 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.65-8_20081108.2245
- x264-libs from a 3rd party repo generates conflicts.

* Sun Nov  9 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.65-6_20081108.2245
- Update to latest git.

* Fri Jun 27 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20080626_2245-5
- Update to latest git.

* Tue Feb 26 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20080225_2245-5
- Update to latest svn.

* Sun Apr 15 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20070414_2245-4
- Update to latest svn.

* Wed Feb  7 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20070206_2245-3
- Update to latest svn.

* Wed Jan  3 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20070102_2245-2
- Update to latest svn.

* Wed Sep 13 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - svn20060912_2245-1
- Initial build.

