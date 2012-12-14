Summary: Freeware Advanced Audio Coder
Name: faac
Version: 1.28
Release: 7%{?dist}
License: LGPL
Group: Applications/Multimedia
URL: http://www.audiocoding.com/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0: faac-1.28-excessivedefines.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf, automake, libtool
BuildRequires: gcc-c++
BuildRequires: dos2unix

Obsoletes: libmp4v2_0

%description
The ISO/MPEG 2/4 AAC Encoder Library provides a high-level interface
for encodin g MPEG2 and MPEG4 ISO AAC files.


%package devel
Summary: Development files for faac
Group: Development/Libraries

%description devel
The ISO/MPEG 2/4 AAC Encoder Library provides a high-level interface
for encodin g MPEG2 and MPEG4 ISO AAC files.

This package contains libraries, header files and developer documentation.


%package libs
Provides: libfaac0 = %{version}-%{release}
Summary: Shared libraries for package faac

%description libs
This package provides the shared libraries libfaac.so.0* for the
package faac. Shared libraries are required at runtime for
software built against faac. Keeping shared libraries in a
separate package enables their use as forward/backward
compatibility packages.


%prep
%setup -q
%patch0 -p1 -b .excessivedefines
dos2unix bootstrap configure.in

%build
sh -x ./bootstrap
%configure --disable-static --with-mp4v2
make


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm $RPM_BUILD_ROOT%{_libdir}/libfaac.la
rm $RPM_BUILD_ROOT%{_libdir}/libfaac.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO docs/*
%{_bindir}/faac
%{_mandir}/man1/faac.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/faac.h
%{_includedir}/faaccfg.h

%files libs
%defattr(-,root,root,-)
%{_libdir}/libfaac.*

%changelog
* Mon Oct 22 2012 Lars Kiesow <lkiesow@uos.de - 1.28-7
- Port for Matterhorn repo

* Sun Mar  1 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.28-4
- Update to 1.28.

* Sun Feb 17 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.26-3
- Update to 1.26.

* Fri Feb 23 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.25-2
- Get package-w-o-upstream out of the way.

* Sun Mar 12 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.
