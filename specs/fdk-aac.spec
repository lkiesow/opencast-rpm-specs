Name: fdk-aac
License: Fraunhofer Cusom License
Group: Applications/Multimedia
Version: 0.1.3
Release: 1%{?dist}
Summary: Modified library of Fraunhofer AAC decoder and encoder.
Source: http://netcologne.dl.sourceforge.net/project/opencore-amr/fdk-aac/%{name}-%{version}.tar.gz
URL: http://sourceforge.net/projects/opencore-amr/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

BuildRequires: gcc-c++
BuildRequires: libtool

%description
fdk-aac is a free software library and application for encoding video
streams into the H.264/MPEG-4 AVC format, and is released under the
terms of the GNU GPL.


%package devel
Summary: Development files for fdk-aac
Group: Development/Libraries

%description devel
fdk-aac is a free software library and application for encoding video
streams into the H.264/MPEG-4 AVC format, and is released under the
terms of the GNU GPL.

This package contains libraries, header files and developer documentation.


%prep
%setup -q


%build
autoreconf -fiv
%configure --enable-shared --disable-static
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_libdir}/libfdk-aac.la


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc NOTICE ChangeLog
%{_libdir}/libfdk-aac.so.*


%files devel
%defattr(-,root,root)
%{_includedir}/fdk-aac/
%{_libdir}/libfdk-aac.so
%{_libdir}/pkgconfig/fdk-aac.pc


%post
/sbin/ldconfig


%postun
/sbin/ldconfig

%changelog
* Mon Jan 27 2014 Lars Kiesow <lkiesow@uos.de> - 0.1.3-1
- Update to 0.1.3

* Sun May 19 2013 Lars Kiesow <lkiesow@uos.de> - 0.1.0-1
- Downgrade to 0.1.0

* Mon Apr 29 2013 Lars Kiesow <lkiesow@uos.de> - 0.1.1-1
- Initial build for libfdk-aac
