Summary: 	Library for MPEG TS and DVB PSI tables decoding and generation
Name: 		libdvbpsi
Version: 	0.2.2
Release: 	2%{?dist}
License: 	LGPLv2+
Group: 		System Environment/Libraries
URL: 		http://www.videolan.org/developers/libdvbpsi.html
Source0: 	http://download.videolan.org/pub/libdvbpsi/%{version}/%{name}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	graphviz doxygen

%package devel
Summary: 	Development package for %{name}
Group: 		Development/Libraries
Requires: 	%{name} = %{version}-%{release}

# -----------------------------------------------------------------------------

%description
libdvbpsi is a very simple and fully portable library designed for
MPEG TS and DVB PSI table decoding and generation.

%description devel
libdvbpsi is a very simple and fully portable library designed for
MPEG TS and DVB PSI table decoding and generation.
This package contains development files for %{name}

# -----------------------------------------------------------------------------

%prep
%setup -q



# -----------------------------------------------------------------------------

%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags}
make doc

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html
%{_includedir}/dvbpsi/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libdvbpsi.pc

# -----------------------------------------------------------------------------

%changelog
* Wed Jan 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.2.2-2
- Rebuilt for target i686

* Sat Nov 05 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.2.2-1
- Update to 0.2.2

* Tue May 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.2.0-1
- Update to 0.2.0
- Switch to LGPLv2+

* Sat Apr 24 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.1.7-1
- Update to 0.1.7

* Sat Oct 17 2009 kwizart < kwizart at gmail.com > - 0.1.6-6
- Rebuild

* Sun Apr  5 2009 kwizart < kwizart at gmail.com > - 0.1.6-5
- Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.1.6-4
- rebuild for new F11 features

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.1.6-3
- rebuild

* Tue Feb 26 2008 kwizart < kwizart at gmail.com > - 0.1.6-2
- Rebuild for gcc43

* Mon Oct 22 2007 kwizart < kwizart at gmail.com > - 0.1.6-1
- Update to 0.1.6

* Sun Oct 14 2007 kwizart < kwizart at gmail.com > - 0.1.5-3
- Rpmfusion Merge Review

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0.1.5-2
- Drop Epoch completely

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Jul 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1.5-0.lvn.1
- 0.1.5.
- Build with dependency tracking disabled.
- Miscellaneous specfile cleanups.

* Mon May 17 2004 Dams <anvil[AT]livna.org> - 0:0.1.3-0.lvn.4
- Added url in Source0

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.3
- Removed comment after scriptlets

* Mon Aug 18 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.2
- Moved some doc to devel package

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 0:0.1.3-0.fdr.1
- Added post/postun scriptlets
- Using RPM_OPT_FLAGS
- Updated to 0.1.3

* Sun Jun 29 2003 Dams <anvil[AT]livna.org> 
- Initial build.
