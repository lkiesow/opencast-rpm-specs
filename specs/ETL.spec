%define debug_package %{nil}

Name:           ETL
Epoch:		1
Version:        1.2.1
Release:        1%{?dist}
Summary:        Extended Template Library

Group:          Development/Libraries
License:        GPLv2+
URL:            http://synfig.org
Source0:        http://downloads.sourceforge.net/synfig/ETL-%{version}.tar.gz
#git clone, d4e547
#Source0:        ETL.tar.gz
#Patch0:         ETL-0.04.13-gcc47.patch
#Patch1:		ETL-0.04.14-disable-tests.patch
#Patch2:		ETL-0.04.14-gcc47.patch
#Patch3:		ETL-swap-type.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildrequires:  doxygen
#Buildrequires:  autoconf automake
Requires:       pkgconfig

%description
Voria ETL is a multi-platform class and template library designed to add
new datatypes and functions which combine well with the existing
types and functions from the C++ Standard Template Library (STL).


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
#%patch0 -p1
#%patch1 -p0
#%patch2 -p0
#%patch3 -p0

%build
#pushd test
#autoreconf -if
#popd
%configure
make %{?_smp_mflags} all docs


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
#touch -r ChangeLog $RPM_BUILD_ROOT%{_bindir}/ETL-config
#touch -r ChangeLog $RPM_BUILD_ROOT%{_includedir}/ETL/etl_profile.h


%clean
rm -rf $RPM_BUILD_ROOT


%check
make check


%files devel
%defattr(-,root,root,-)
%doc README COPYING AUTHORS NEWS
%{_includedir}/ETL/
%{_bindir}/ETL-config
%{_libdir}/pkgconfig/ETL.pc


%changelog
* Mon Sep 11 2017 Gwyn Ciesla <limburgher@gmail.com> - 1:1.2.1-1
- 1.2.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.04.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.04.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 07 2017 Jon Ciesla <limburgher@gmail.com> - 1:0.04.22-3
- Fix FTBFS.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.04.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Jon Ciesla <limburgher@gmail.com> - 1:0.04.22-1
- 0.4.22, Epoch bump.

* Fri Jun 24 2016 Jon Ciesla <limburgher@gmail.com> - 1.1.10-0.20160624gitd4e547
- Latest upstream.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.04.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 05 2013 Jon Ciesla <limburgher@gmail.com> - 0.04.17-1
- Latest upstream.

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Jon Ciesla <limburgher@gmail.com> - 0.04.16-1

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Jon Ciesla <limburgher@gmail.com> - 0.04.15-1
- New ETL, BZ 814969.
- gcc47 ETL 0.04.13,14 patches upstreamed.

* Wed Mar 21 2012 Jon Ciesla <limburgher@gmail.com> - 0.04.14-3
- Patch for gcc47 builds against ETL.

* Thu Feb 16 2012 Jon Ciesla <limburgher@gmail.com> - 0.04.14-2
- New upstream to support new synfig, BZ 790249.
- Disable spline an value tests, per upstream comments.

* Wed Jan 18 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.04.13-4
- Add ETL-0.04.13-gcc47.patch (Fix mass rebuild FTBFS).

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 14 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.04.13-1
- New upstream release
- Drop our build patch, since upstream fixed necessary bits

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jan 9 2009 Lubomir Rintel <lkundrak@v3.sk> 0.04.12-1
- New upstream release
- Run regression tests
- Build documentation
- Fix BRs

* Tue May 6 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.4.11-4
- Removed some requires and buildrequires to clean stuff up.

* Thu May 1 2008 Marc Wiriadisastra <marc@mwiriadi.id.a> - 0.4.11-3
- Added the lines for timestamp consistency

* Fri Mar 7 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.4.11-2
- Added patch to clean up etl-profile_.in
- renamed package to ETL as requested by ralf

* Thu Mar 6 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.4.11-1
- Removed patches
- New version

* Sun Feb 3 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.04-10-3
- Added backported patch adding <cstring>

* Thu Jan 24 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.04-10-2
- Included Ralfs patch for ETL-config

* Sat Jan 12 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.04.10-1
- new release
