%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:      LASH Audio Session Handler
Name:         lash
Version:      0.5.4
Release:      9%{?dist}
License:      GPLv2+
Group:        System Environment/Libraries
URL:          http://www.nongnu.org/lash/
Source0:      http://download.savannah.gnu.org/releases/lash/lash-%{version}.tar.gz
Source1:      %{name}-panel.desktop
Patch0:       lash-0.5.3-no-static-lib.patch
# Fix DSO-linking failure
# Upstream bugtracker is closed for some reason. Sent via email:
Patch1:       lash-linking.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: gtk2-devel 
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: libxml2-devel
BuildRequires: python-devel
BuildRequires: readline-devel
BuildRequires: swig
BuildRequires: texi2html

%if 0%{?fedora} < 12
BuildRequires: e2fsprogs-devel
%endif
#%else
BuildRequires: libuuid-devel
#%endif

%description
LASH is a session management system for JACK and ALSA audio applications on
GNU/Linux. It allows you to save and restore audio sessions consisting of
multiple interconneced applications, restoring program state (i.e. loaded
patches) and the connections between them.

%package devel
Summary:      Development files for LASH
Group:        Development/Libraries
Requires:     %{name} = %{version}-%{release}
Requires:     alsa-lib-devel
Requires:     jack-audio-connection-kit-devel
Requires:     pkgconfig

%if 0%{?fedora} < 12
Requires:     e2fsprogs-devel
%else
Requires:     libuuid-devel
%endif

%description devel
Development files for the LASH library.

%package -n python-lash
Summary:      Python wrapper for LASH
Group:        System Environment/Libraries
Requires:     %{name} = %{version}-%{release}

%description -n python-lash
Contains Python language bindings for developing Python applications that use
LASH.

%prep
%setup -q
%patch0 -p0
%patch1 -p1 -b .linking

%build
export am_cv_python_pythondir=%{python_sitearch}
CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" %configure --disable-static --disable-serv-inst
# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/liblash.la
rm -f %{buildroot}%{python_sitearch}/_lash.la

# Fix permission
chmod -x %{buildroot}%{python_sitearch}/lash.py

# Move icons to the right place
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/96x96/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mv %{buildroot}%{_datadir}/lash/icons/lash_16px.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/lash.png
mv %{buildroot}%{_datadir}/lash/icons/lash_24px.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/lash.png
mv %{buildroot}%{_datadir}/lash/icons/lash_48px.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/lash.png
mv %{buildroot}%{_datadir}/lash/icons/lash_96px.png %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/lash.png
mv %{buildroot}%{_datadir}/lash/icons/lash.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/lash.svg

# Move the dtd file to our Fedora Friendly place
mkdir -p %{buildroot}%{_datadir}/xml/lash/dtds
mv %{buildroot}%{_datadir}/lash/dtds/lash-project-1.0.dtd %{buildroot}%{_datadir}/xml/lash/dtds

# This directory is empty!
rm -rf %{buildroot}%{_datadir}/lash

# install the desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor fedora         \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE1}

# Work around the newer texi2html which is behaving somehow else
if [ ! -d docs/lash-manual-html-split/lash-manual/ ]; then
  mkdir -p docs/lash-manual-html-split/lash-manual/
  cp -p docs/lash-manual-html-split/*.html docs/lash-manual-html-split/lash-manual/
fi

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
# update icon themes
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
# update icon themes
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README docs/lash-manual-html-split/lash-manual icons/lash.xcf
%{_bindir}/lash*
%{_libdir}/liblash.so.1
%{_libdir}/liblash.so.1.*
%{_datadir}/icons/hicolor/16x16/apps/lash.png
%{_datadir}/icons/hicolor/24x24/apps/lash.png
%{_datadir}/icons/hicolor/48x48/apps/lash.png
%{_datadir}/icons/hicolor/96x96/apps/lash.png
%{_datadir}/icons/hicolor/scalable/apps/lash.svg
%{_datadir}/xml/lash
%{_datadir}/applications/*lash-panel.desktop

%files devel
%defattr(-,root,root,-)
%{_libdir}/liblash.so
%{_includedir}/lash-1.0
%{_libdir}/pkgconfig/lash*

%files -n python-lash
%defattr(-,root,root,-)
%{python_sitearch}/_lash.so
%{python_sitearch}/lash.py*

%changelog
* Wed Feb 10 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.5.4-9
- Fix DSO-linking failure

* Wed Aug 05 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.5.4-8
- Update .desktop file

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.5.4-6
- Build against libuuid on F-12 (e2fsprogs got split up)

* Sat Jun 13 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.5.4-5
- Re-enable python package
- Some macro consistency cleanup
- Update scriptlets according to new guidelines
- Make the .desktop file nicer
- Update description
- Remove rpath
- Clear some rpmlints

* Sun Mar 22 2009 Robert Scheck <robert@fedoraproject.org> - 0.5.4-4
- Work around the newer texi2html which is behaving somehow else

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 28 2008 Anthony Green <green@redhat.com> 0.5.4-2
- Force build with _GNU_SOURCE, not _POSIX_SOURCE..

* Thu Feb 28 2008 Anthony Green <green@redhat.com> 0.5.4-1
- Upgrade to 0.5.4.  Force build with _POSIX_SOURCE.

* Mon Oct 08 2007 Anthony Green <green@redhat.com> 0.5.3-3
- Disable pylash until we can figure out how to install it properly.

* Mon Oct 08 2007 Anthony Green <green@redhat.com> 0.5.3-2
- Fixed python installation for 64-bit systems.

* Sun Oct 07 2007 Anthony Green <green@redhat.com> 0.5.3-1
- Upgrade sources.
- Don't install info files (no longer built).
- Add python package.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.5.1-15
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 Florian La Roche <laroche@redhat.com> 0.5.1-14
- info files are gzipped, add info dir entry

* Thu Feb 01 2007 Anthony Green <green@redhat.com> 0.5.1-11
- Rebuild to drop libtermcap dependency as per bugzilla #226761.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.5.1-10
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Anthony Green <green@redhat.com> 0.5.1-9
- Update -texi-dir patch.

* Tue Sep 19 2006 Anthony Green <green@redhat.com> 0.5.1-8
- Fix release tag.

* Mon Sep 18 2006 Anthony Green <green@redhat.com> 0.5.1-7.1
- Rebuild.

* Mon Sep  4 2006 Anthony Green <green@redhat.com> 0.5.1-7
- The devel package must Require pkgconfig.

* Fri Jul 14 2006 Anthony Green <green@redhat.com> 0.5.1-6
- The devel package must Require e2fsprogs-devel.

* Sun Jun 26 2006 Anthony Green <green@redhat.com> 0.5.1-5
- Use || : is %%post(un) scripts.

* Sun Jun 26 2006 Anthony Green <green@redhat.com> 0.5.1-4
- Fix files reference to %%{_datadir}/xml/lash.
- Don't use update-desktop-database.
- Use %%{version} in Source0.

* Mon Jun 19 2006 Anthony Green <green@redhat.com> 0.5.1-3
- Fix changelog entries.
- Move pkgconfig file to devel package.
- Run ldconfig is post and postun.
- Clean up BuildRequires.
- Fix docs install.
- Move icons to correct directory.
- Move dtds to correct directory.
- Don't install INSTALL or TODO.
- Install desktop file.

* Tue May 30 2006 Anthony Green <green@redhat.com> 0.5.1-2
- Fix URL.
- Add lash-0.5.1-service.patch.
- Fix some BuildRequires.
- The devel package Requires things now.
- Use %%{_infodir}.
- Delete the texinfo dir file.
- Add -texi-dir patch.
- Install info files properly.
- Add Fernando Lopez-Lazcano's -service.patch.
- Delete .la file after installation.
- Configure with --disable-serv-inst.

* Tue Apr 18 2006 Anthony Green <green@redhat.com> 0.5.1-1
- Build for Fedora Extras.

* Mon May 30 2005 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>
- remove references to deprecated function jack_set_server_dir in
  jack (patch4), fc4 test build, no release bump yet
* Sun Dec 19 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>
- spec file cleanup
* Thu May 20 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>
- aded tetex buildrequires
* Sat May  8 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>
- added buildrequires
- add patch to not add service to /etc/services
* Tue Feb 24 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.4.0-2
- added patch (thanks to Guenter Geiger) to not require a service number
  entry in /etc/services
* Fri Nov 14 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.4.0-1
- spec file tweaks
* Thu Nov  6 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.4.0-1
- updated to 0.4.0
- patched to build under gcc2.96 (patch1)
* Wed Feb 11 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.3.0-1
- updated to 0.3.0
- added 7.2 workaround for gtk2 configuration problem
* Mon Jan 13 2003  Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2-1
- Initial build.
