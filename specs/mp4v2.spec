Name:           mp4v2
Version:        1.9.1
Release:        3%{?dist}
Summary:        Library:which provides functions to read, create, and modify mp4 files

Group:          System Environment/Libraries
License:        MPLv1.1
URL:            http://code.google.com/p/mp4v2
Source0:        http://mp4v2.googlecode.com/files/mp4v2-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
    
%{?fedora:Conflicts: libmp4v2}

%description
The MP4v2 library provides an API to create and modify mp4 files as defined by
ISO-IEC:14496-1:2001 MPEG-4 Systems. This file format is derived from Apple's
QuickTime file format that has been used as a multimedia file format in a
variety of platforms and applications. It is a very powerful and extensible
format that can accommodate practically any type of media.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --enable-static=no --enable-shared=yes
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT LIBDIR=%{_libdir}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README doc/ReleaseNotes.txt
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%doc COPYING README doc/ReleaseNotes.txt
%{_includedir}/%{name}
%{_libdir}/*.so

%changelog
* Fri Aug 24 2012 Lars Kiesow <lkiesow@uos.de> - 1.9.1-3
- Marked conflict with libmp4v2 from Fedora repository

* Fri Mar  2 2012 Lars Kiesow <lkiesow@uos.de> - 1.9.1-2
- Corrected some minor packaging issues.

* Thu Mar  1 2012 Lars Kiesow <lkiesow@uos.de> - 1.9.1-1
- Created package
