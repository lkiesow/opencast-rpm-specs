#%lib_package mpeg2 0
#%lib_package mpeg2convert 0
%define real_name libmpeg2

Summary: A free MPEG-2 video stream decoder
Name: mpeg2dec
Version: 0.5.1
Release: 6%{?dist}
License: GPLv2
Group: System Environment/Libraries
URL: http://libmpeg2.sourceforge.net/
Source0: http://libmpeg2.sourceforge.net/files/%{real_name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc-c++
BuildRequires: SDL-devel, alsa-lib-devel

%description
libmpeg2 is a free library for decoding mpeg-2 and mpeg-1 video
streams. It is released under the terms of the GPL license.

mpeg2dec is a test program for libmpeg2. It decodes mpeg-1 and mpeg-2
video streams, and also includes a demultiplexer for mpeg-1 and mpeg-2
program streams.

The libmpeg2 source code is always distributed in the mpeg2dec package,
to make it easier for people to test it.

%package devel
Summary: Development files for building against the mpeg2dec package
Provides: libmpeg2-devel = %{evr}

%description devel
This package provides the files necessary for development against
mpeg2dec. Use this package if you need to build a package
depending on mpeg2dec at build time, or if you want to do your own
development against mpeg2dec.

%package -n libmpeg2_0
Summary: Shared libraries for package mpeg2dec

%description -n libmpeg2_0
This package provides the shared libraries libmpeg2.so.0* for the
package mpeg2dec. Shared libraries are required at runtime for
software built against mpeg2dec. Keeping shared libraries in a
separate package enables their use as forward/backward
compatibility packages.

%package -n libmpeg2convert0
Summary: Shared libraries for package mpeg2dec

%description -n libmpeg2convert0
This package provides the shared libraries libmpeg2convert.so.0*
for the package mpeg2dec. Shared libraries are required at runtime
for software built against mpeg2dec. Keeping shared libraries in a
separate package enables their use as forward/backward
compatibility packages.

%prep
%setup -q -n %{real_name}-%{version}
perl -pi -e's,LIBMPEG2_CFLAGS -prefer-non-pic,LIBMPEG2_CFLAGS,' configure
# Avoid standard rpaths on lib64 archs:
perl -pi -e 's|"/lib /usr/lib\b|"/%{_lib} %{_libdir}|' configure

iconv -f iso8859-1 -t utf-8 AUTHORS -o AUTHORS.txt
touch -r AUTHORS AUTHORS.txt
mv AUTHORS.txt AUTHORS

%build
%configure --enable-shared \
%ifnarch %{ix86}
    --disable-accel-detect \
%endif

make

%install
rm -rf %{buildroot}
%makeinstall
rm %{buildroot}%{_libdir}/*.a
rm %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc ChangeLog AUTHORS COPYING NEWS README TODO
%{_bindir}/corrupt_mpeg2
%{_bindir}/extract_mpeg2
%{_bindir}/mpeg2dec
%{_mandir}/man1/extract_mpeg2.1*
%{_mandir}/man1/mpeg2dec.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/mpeg2dec/
%{_libdir}/pkgconfig/*.pc

%files -n libmpeg2_0
%defattr(-,root,root,-)
%{_libdir}/libmpeg2.so*

%files -n libmpeg2convert0
%defattr(-,root,root,-)
%{_libdir}/libmpeg2convert*so*


%changelog
* Wed Oct 24 2012 Lars Kiesow <lkiesow@uos.de> - 0.5.1-5
- Port for Matterhorn repository

* Sat Nov 15 2008 Paulo Roma <roma@lcg.ufrj.br> - 0.5.1-4
- Update to 0.5.1.
- Changed license.
- Using real_name.
- Converted AUTHORS to utf8.
- Removed rpath from binary.

* Sun Mar 11 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.1-3
- Update to 0.4.1.

* Tue Jul 12 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.
