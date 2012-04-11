Name:           leptonica
Version:        1.68
Release:        2%{?dist}
License:        ASL 2.0
Summary:        C library for efficient image processing and image analysis operations
Url:            http://code.google.com/p/leptonica/
Group:          System Environment/Libraries
Source0:        http://leptonica.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:  giflib-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%package devel
Summary:        Leptonica Development Files
Group:          Development/Libraries
Requires:       %{name} = %{version}

%package tools
Summary:        Leptonica tools
Group:          Development/Tools


%description
Library for efficient image processing and image analysis operations.

%description devel
Development files for %{name} library.

%description tools
Regression tests and example programs for %{name}.


%prep
%setup -q

%build
./configure --prefix=%{_prefix}  --libdir=%{_libdir} \
            --mandir=%{_mandir}  --bindir=%{_bindir} \
            --enable-static=no   --includedir=%{_includedir} \
            --enable-shared=yes  --with-gnu-ld=yes
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.html version-notes.html leptonica-license.txt 
%{_libdir}/liblept.so.*

%files devel
%defattr(-,root,root,-)
%doc README.html version-notes.html leptonica-license.txt 
%{_includedir}/%{name}
%{_libdir}/liblept.so

%files tools
%defattr(-,root,root,-)
%doc README.html version-notes.html leptonica-license.txt 
%{_bindir}/*

%changelog
* Sat Mar  3 2012 Lars Kiesow <lkiesow@uos.de> - 1.68-2
- Fixed some packaging issues.

* Fri Feb 24 2012 Lars Kiesow <lkiesow@uos.de> - 1.68-1
- Updated to leptonica 1.68

* Wed Feb  8 2012 Lars Kiesow <lkiesow@uos.de> - 1.66-1
- Initial package leptonlib 1.66
