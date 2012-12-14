Name: libsidplay
Summary: SID chip music module playing library
Version: 1.36.57
Release: 21%{?dist}
Source: http://home.arcor.de/ms2002sep/bak/%{name}-%{version}.tgz
Patch0: libsidplay-post57fixes.patch
Patch1: libsidplay-post59fixes.patch
Patch2: libsidplay-1.36.57-opts.patch
Patch3: libsidplay-1.36.57-gcc43.patch
Group: System Environment/Libraries
URL: http://home.arcor.de/ms2002sep/bak/
License: GPLv2+
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
# Package is relocatable.
Prefix: %{_prefix}

%description
This library provides support for playing SID music modules originally
created on Commodore 64 and compatibles. It contains a processing engine
for MOS 6510 machine code and MOS 6581 Sound Interface Device (SID)
chip output. It is used by music player programs like SIDPLAY and
several plug-ins for versatile audio players.

Developers should consider switching to libsidplay version 2 or newer.


%package devel
Summary: Files needed for compiling programs that use libsidplay
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
These are the files needed for compiling programs that use libsidplay.
Developers should consider switching to libsidplay version 2 or newer.


%prep
%setup -q
%patch0 -p1 -b .post57fixes
%patch1 -p1 -b .post59fixes
%patch2 -p1 -b .opts
%patch3 -p1 -b .gcc43

%build
CXXFLAGS="$RPM_OPT_FLAGS" %configure \
  --disable-static
make %{_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libsidplay.so.*
%exclude %{_libdir}/*.la

%files devel
%defattr(-,root,root,-)
%doc AUTHORS DEVELOPER src/*.txt
%{_libdir}/libsidplay.so
#%{_libdir}/libsidplay.a
%{_includedir}/sidplay/

%changelog
* Thu Dec 17 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.36.57-21
- apply minor patch to avoid uninitialised values

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36.57-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36.57-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-18
- only a few spec file adjustments (including new summaries and
  descriptions)

* Fri Feb 08 2008 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering

* Thu Jan  3 2008 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-16
- Patch ios::binary check for GCC 4.3.0 C++.

* Sat Oct 20 2007 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-15
- Move the i386-specific configure options into a __i386__ patch.
  This shall fix the multiarch conflict in libsidplay-devel (#342371).

* Tue Aug 21 2007 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Thu Aug  2 2007 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-13
- Clarify licence (GPLv2+).
- Use backup urls as a substitute for vanished web home.

* Thu Jan 04 2007 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Mon Aug 28 2006 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Thu Feb 16 2006 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-10
- rebuilt for FC5

* Sat Sep 17 2005 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-9
- don't build/include static library

* Thu May 12 2005 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-8
- rebuilt

* Sun Mar  6 2005 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-7
- Remove "Icon:". This was the only package in Fedora Extras, which
  used such an icon, and it breaks --specfile queries.

* Thu Dec 16 2004 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-6
- Use %%configure macro, so %%_libdir and friends get set for x86_64.

* Wed Nov 10 2004 Michael Schwendt <mschwendt@fedoraproject.org> 1.36.57-5
- Fix build for FC3/GCC 3.4 with patch from newer upstream release
  (I'm still upstream for this, afaik).
- Bump release.

* Fri Apr 25 2003 Panu Matilainen <pmatilai@welho.com> 1.36.57-0.fdr.4
- strict dependency in -devel package
- simpler arch detection

* Fri Apr 25 2003 Panu Matilainen <pmatilai@welho.com> 1.36.57-0.fdr.3
- clean buildroot in install
- -devel requires the actual package as well
- use version-release for BuildRoot

* Fri Apr 25 2003 Panu Matilainen <pmatilai@welho.com> 1.36.57-0.fdr.2
- ldconfig in %%post,%%postun

* Sat Apr 05 2003 Panu Matilainen <pmatilai@welho.com> 1.36.57-0.fdr.1
- Initial Fedora packaging
