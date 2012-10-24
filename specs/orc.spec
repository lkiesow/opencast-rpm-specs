Name:		orc
Version:	0.4.16
Release:	5%{?dist}
Summary:	The Oil Run-time Compiler

Group:		System Environment/Libraries
License:	BSD
URL:		http://code.entropywave.com/projects/orc/
Source0:	http://code.entropywave.com/download/orc/orc-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gtk-doc, libtool

Patch1:		orc-no-nopl.patch
Patch2:		orc-no-nopw.patch
# Upstream bug: https://bugs.freedesktop.org/show_bug.cgi?id=41446
Patch3:		orc-subdir.patch

%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.

%package doc
Summary:	Documentation for Orc
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for Orc.

%package devel
Summary:	Development files and static libraries for Orc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-compiler
Requires:	pkgconfig

%description devel
This package contains the files needed to build packages that depend
on orc.

%package compiler
Summary:	Orc compiler
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description compiler
The Orc compiler, to produce optimized code.



%prep
%setup -q
%patch1 -p1 -b .nopl
%patch2 -p1 -b .nopw
%patch3 -p1 -b .subdir

autoreconf -vif


%build
%configure --disable-static --enable-gtk-doc --enable-user-codemem

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

# Remove unneeded files.
find %{buildroot}/%{_libdir} -name \*.a -or -name \*.la -delete
rm -rf %{buildroot}/%{_libdir}/orc

touch -r stamp-h1 %{buildroot}%{_includedir}/%{name}-0.4/orc/orc-stdint.h   


%clean
rm -rf %{buildroot}


%check
%ifnarch s390 s390x ppc ppc64 %{arm} i686
make check
%endif


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig



%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/liborc-*.so.*
%{_bindir}/orc-bugreport

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/orc/

%files devel
%defattr(-,root,root,-)
%doc examples/*.c
%{_includedir}/%{name}-0.4/
%{_libdir}/liborc-*.so
%{_libdir}/pkgconfig/orc-0.4.pc
%{_datadir}/aclocal/orc.m4

%files compiler
%defattr(-,root,root,-)
%{_bindir}/orcc



%changelog
* Sat Jan 07 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-5
- Updated subdir patch.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.16-4
- Rebuilt for glibc bug#747377

* Sun Oct 16 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-3
- Add Fedora specific patch for tempfiles in subdirs

* Sun Oct 16 2011 Daniel Drake <dsd@laptop.org> - 0.4.16-2
- Add upstream patches to fix gstreamer crash on Geode (#746185)

* Mon Oct 03 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.16-1
- Update to 0.4.16
- Fixing regression introdcued by 0.4.15 (#742534 and #734911)

* Mon Sep 26 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.15-1
- Update to 0.4.15

* Mon Jun 20 2011 Peter Robinson <pbrobinson@gmail.com> - 0.4.14-3
- Add ARM platforms to the make check exclusion

* Sat May 07 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.14-2
- Add orc-bugreport to the main package (#702727)

* Sat Apr 30 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.14-1
- Update to 0.4.14

* Tue Apr 19 2011 Fabian Deutsch <fabiand@fedorpaproject.org> - 0.4.13-1
- Update to 0.4.13, another bug fixing release

* Fri Apr 15 2011 Fabian Deutsch <fabiand@fedorpaproject.org> - 0.4.12-1
- Update to 0.4.12, a bug fixing release

* Wed Feb 23 2011 Karsten Hopp <karsten@redhat.com> 0.4.11-3
- don't run tests on ppc, ppc64

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.11-1
- Update to 0.4.11.
- More bug fixes for CPUs that do not have backends, mmx and sse.

* Fri Oct 08 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.10-1
- Update to 0.4.10.
- Fixes some bugs related to SELinux.

* Mon Sep 06 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9, a pimarily bug fixing release.

* Thu Aug 19 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.7-1
- Updated to 0.4.7.

* Tue Jul 22 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.6-1
- Updated to 0.4.6.
- New orc-bugreport added.

* Tue Jul 13 2010 Dan Horák <dan[at]danny.cz> - 0.4.5-3
- don't run test on s390(x)

* Sun Jun 13 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.5-2
- Added removed testing libraries to package.

* Sun Jun 13 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.5-1
- Updated to 0.4.5.
- Removed testing libraries from package.

* Mon Apr 05 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.4-2
- Docs as noarch.
- Sanitize timestamps of header files.
- orcc in -compiler subpackage.

* Tue Mar 30 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 0.4.4-1
- Updated to 0.4.4: Includes bugfixes for x86_64.

* Wed Mar 17 2010 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.3-2
- Running autoreconf to prevent building problems.
- Added missing files to docs.
- Added examples to devel docs.

* Thu Mar 04 2010 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.3-1
- Updated to 0.4.3

* Sun Oct 18 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-4
- Removed unused libdir

* Sun Oct 18 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-3
- Specfile cleanup
- Removed tools subpackage
- Added docs subpackage

* Sat Oct 03 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-2
- Use orc as pakage name
- spec-file cleanup
- Added devel requirements
- Removed an rpath issue

* Fri Oct 02 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-1
- Initial release

