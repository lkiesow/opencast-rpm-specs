Summary: A free DTS Coherent Acoustics decoder
Name: libdca
Version: 0.0.5
Release: 5%{?dist}
License: GPLv2
Group: System Environment/Libraries
URL: http://www.videolan.org/developers/libdca.html
Source0: http://download.videolan.org/pub/videolan/%{name}/%{version}/%{name}-%{version}.tar.bz2
Patch0: libdca-0.0.5-relsymlinks.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: pkgconfig

%description
libdca is a free library for decoding DTS Coherent Acoustics streams.

%package devel
Summary: Development files for building against the libdca package
Obsoletes: libdts-devel < %{evr}
Provides: libdts-devel = %{evr}

%description devel
This package provides the files necessary for development against
libdca. Use this package if you need to build a package depending
on libdca at build time, or if you want to do your own development
against libdca.

%package -n libdca0
Summary: Shared libraries for package libdca

%description -n libdca0
This package provides the shared libraries libdca.so.0* for the
package libdca. Shared libraries are required at runtime for
software built against libdca. Keeping shared libraries in a
separate package enables their use as forward/backward
compatibility packages.

%prep
%setup -q
%patch0 -p1 -b .relsymlinks
iconv -f iso8859-1 -t utf8 -o AUTHORS2 AUTHORS
mv AUTHORS2 AUTHORS

%build
%ifarch x86_64
CFLAGS="%{optflags} -fPIC"
%endif
%configure

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/*.a
rm %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING README TODO AUTHORS NEWS ChangeLog
%{_bindir}/dcadec
%{_bindir}/dtsdec
%{_bindir}/extract_dca
%{_bindir}/extract_dts
%{_mandir}/man1/dcadec.1*
%{_mandir}/man1/dtsdec.1*
%{_mandir}/man1/extract_dca.1*
%{_mandir}/man1/extract_dts.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/dts.h
%{_includedir}/dca.h
%{_libdir}/pkgconfig/libdts.pc
%{_libdir}/pkgconfig/libdca.pc

%files -n libdca0
%defattr(-,root,root,-)
%{_libdir}/libdca.so*

%changelog
* Wed Oct 24 2012 Lars Kiesow <lkiesow@uos.de> 0.0.5-5
- Ported to matterhorn repository

* Mon Jan 14 2008 Paulo Roma <roma@lcg.ufrj.br> 0.0.5-4
- Updated to 0.0.5
- Created devel package.
- Patched for using relative symbolic links (Mathias Saou).
- Converted AUTHORS to UTF8.
- Added post and postun sections.

* Sun Mar 12 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.
