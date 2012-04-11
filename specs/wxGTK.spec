Name:           wxGTK
Version:        2.8.12
Release:        1%{?dist}
Summary:        GTK2 port of the wxWidgets GUI library
License:        wxWidgets
Group:          System Environment/Libraries
URL:            http://www.wxwidgets.org/
Source0:        http://downloads.sourceforge.net/wxwindows/%{name}-%{version}.tar.bz2
Source1:        wx-config
Patch0:         %{name}-2.8.12-test.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel, zlib-devel >= 1.1.4
BuildRequires:  libpng-devel, libjpeg-devel, libtiff-devel
BuildRequires:  expat-devel, SDL-devel, libgnomeprintui22-devel
BuildRequires:  libGL-devel, libGLU-devel
BuildRequires:  libSM-devel
BuildRequires:  gstreamer-devel >= 0.10, gstreamer-plugins-base-devel >= 0.10
BuildRequires:  GConf2-devel
BuildRequires:  autoconf, gettext
BuildRequires:  cppunit-devel

Requires:       wxBase = %{version}-%{release}

%description
wxWidgets/GTK2 is the GTK2 port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        devel
Group:          Development/Libraries
Summary:        Development files for the wxGTK2 library
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-gl = %{version}-%{release}
Requires:       %{name}-media = %{version}-%{release}
Requires:       wxBase = %{version}-%{release}
Requires:       gtk2-devel
Requires:       libGL-devel, libGLU-devel
Requires:       bakefile

%description devel
This package include files needed to link with the wxGTK2 library.


%package        gl
Summary:        OpenGL add-on for the wxWidgets library
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description gl
OpenGL (a 3D graphics API) add-on for the wxWidgets library.


%package        media
Summary:        Multimedia add-on for the wxWidgets library
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description media
Multimedia add-on for the wxWidgets library.


%package -n     wxBase
Summary:        Non-GUI support classes from the wxWidgets library
Group:          System Environment/Libraries

%description -n wxBase
Every wxWidgets application must link against this library. It contains
mandatory classes that any wxWidgets code depends on (like wxString) and
portability classes that abstract differences between platforms. wxBase can
be used to develop console mode applications -- it does not require any GUI
libraries or the X Window System.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .test

sed -i -e 's|/usr/lib\b|%{_libdir}|' wx-config.in configure

# fix plugin dir for 64-bit
sed -i -e 's|/lib|/%{_lib}|' src/unix/stdpaths.cpp

# fix permissions for sources
chmod a-x include/wx/{msgout.h,dcgraph.h,graphics.h}
chmod a-x src/common/msgout.cpp


%build

export GDK_USE_XFT=1

# this code dereferences type-punned pointers like there's no tomorrow.
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
CXXFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"

# --disable-optimise prevents our $RPM_OPT_FLAGS being overridden
# (see OPTIMISE in configure).
%configure \
  --with-opengl \
  --with-sdl \
  --with-gnomeprint \
  --enable-shared \
  --enable-soname \
  --disable-optimise \
  --enable-debug_info \
  --enable-intl \
  --enable-unicode \
  --enable-no_deps \
  --disable-rpath \
  --enable-geometry \
  --enable-graphics_ctx \
  --enable-sound \
  --enable-mediactrl \
  --enable-display \
  --enable-timer \
  --enable-compat24 \
  --disable-catch_segvs

make %{?_smp_mflags}
make %{?_smp_mflags} -C contrib/src/stc
make %{?_smp_mflags} -C contrib/src/ogl
make %{?_smp_mflags} -C contrib/src/gizmos
make %{?_smp_mflags} -C contrib/src/svg

# Why isn't this this part of the main build? Need to investigate.
make %{?_smp_mflags} -C locale allmo

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

%makeinstall -C contrib/src/stc
%makeinstall -C contrib/src/ogl
%makeinstall -C contrib/src/gizmos
%makeinstall -C contrib/src/svg


# install our multilib-aware wrapper
rm $RPM_BUILD_ROOT%{_bindir}/wx-config
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/wx-config

%find_lang wxstd
%find_lang wxmsw
cat wxmsw.lang >> wxstd.lang

%clean
rm -rf $RPM_BUILD_ROOT

%check
pushd tests
make test
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gl -p /sbin/ldconfig
%postun gl -p /sbin/ldconfig

%post media -p /sbin/ldconfig
%postun media -p /sbin/ldconfig

%post -n wxBase -p /sbin/ldconfig
%postun -n wxBase -p /sbin/ldconfig


%files -f wxstd.lang
%defattr(-,root,root,-)
%doc docs/changes.txt docs/gpl.txt docs/lgpl.txt docs/licence.txt
%doc docs/licendoc.txt docs/preamble.txt docs/readme.txt
%{_libdir}/libwx_gtk2u_adv-*.so.*
%{_libdir}/libwx_gtk2u_aui-*.so.*
%{_libdir}/libwx_gtk2u_core-*.so.*
%{_libdir}/libwx_gtk2u_gizmos-*.so.*
%{_libdir}/libwx_gtk2u_gizmos_xrc*.so.*
%{_libdir}/libwx_gtk2u_html-*.so.*
%{_libdir}/libwx_gtk2u_ogl-*.so.*
%{_libdir}/libwx_gtk2u_qa-*.so.*
%{_libdir}/libwx_gtk2u_richtext-*.so.*
%{_libdir}/libwx_gtk2u_stc-*.so.*
%{_libdir}/libwx_gtk2u_svg-*.so.*
%{_libdir}/libwx_gtk2u_xrc-*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/wx-config
%{_bindir}/wxrc*
%{_includedir}/wx-2.8
%{_libdir}/libwx_*.so
%dir %{_libdir}/wx
%dir %{_libdir}/wx/include
%{_libdir}/wx/include/gtk2*
%dir %{_libdir}/wx/config
%{_libdir}/wx/config/gtk2*
%{_datadir}/aclocal/*
%{_datadir}/bakefile/presets/*

%files gl
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk2u_gl-*.so.*

%files media
%defattr(-,root,root,-)
%{_libdir}/libwx_gtk2u_media-*.so.*

%files -n wxBase
%defattr(-,root,root,-)
%doc docs/changes.txt docs/gpl.txt docs/lgpl.txt docs/licence.txt
%doc docs/licendoc.txt docs/preamble.txt docs/readme.txt
%{_libdir}/libwx_baseu-*.so.*
%{_libdir}/libwx_baseu_net-*.so.*
%{_libdir}/libwx_baseu_xml-*.so.*


%changelog
* Thu Apr 14 2011 Dan Horák <dan[at]danny.cz> - 2.8.12-1
- updated to 2.8.12

* Mon Nov 29 2010 Dan Horák <dan[at]danny.cz> - 2.8.11-3
- added fix for crashes during DnD (#626012)
- bakefiles are included in devel subpackage (#626314)

* Thu Jul  1 2010 Dan Horák <dan[at]danny.cz> - 2.8.11-2
- rebuilt without the internal crash handler

* Thu Apr 15 2010 Dan Horák <dan[at]danny.cz> - 2.8.11-1
- updated to 2.8.11

* Wed Nov 25 2009 Dan Horák <dan[at]danny.cz> - 2.8.10-9
- updated the wrapper script (#541087)

* Fri Nov 20 2009 Dan Horák <dan[at]danny.cz> - 2.8.10-8
- added multilib-aware wrapper for wx-config

* Tue Nov 10 2009 Dan Horák <dan[at]danny.cz> - 2.8.10-7
- added fix for html tables rendering (#534030)
- removed the long time disabled odbc subpackage

* Sun Oct 25 2009 Dan Horák <dan[at]danny.cz> - 2.8.10-6
- add fix for wrong menubar height when using larger system font (#528376)

* Fri Oct 16 2009 Dan Horák <dan[at]danny.cz> - 2.8.10-5
- add fix for excessive CPU usage (#494425)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Dan Horák <dan[at]danny.cz> - 2.8.10-3
- add fix for CVE-2009-2369 (#511279)

* Thu Jun 11 2009 Dan Horák <dan[at]danny.cz> - 2.8.10-2
- fix build with glib >= 2.21

* Sat Mar 21 2009 Dan Horák <dan[at]danny.cz> - 2.8.10-1
- update to 2.8.10
- fix default plugin path for 64 bit arches

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Dan Horák <dan[at]danny.cz> - 2.8.9-3
- remove support for bakefiles, fixes directory ownership (#474594)

* Thu Dec  4 2008 Dan Horak <dan[at]danny.cz> - 2.8.9-2
- drop all the Obsoletes/Provides used for upgrading from the wxGTK 2.6 era
- drop using of x11libdir pointing to X11R6
- create media subpackage for more precise package dependencies

* Mon Sep 22 2008 Dan Horak <dan[at]danny.cz> - 2.8.9-1
- update to 2.8.9

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.8-2
- fix license tag

* Thu Jul 31 2008 Dan Horak <dan[at]danny.cz> - 2.8.8-1
- update to 2.8.8 (rh bug #457406)

* Tue Apr  1 2008 Dan Horak <dan[at]danny.cz> - 2.8.7-2
- added fix for a race condition (rh bug #440011)

* Wed Feb 20 2008 Matthew Miller <mattdm@mattdm.org> - 2.8.7-1
- update to 2.8.7 (rh bug #369621, etc.)
- split base libs into separate wxBase package (rh bug #357961)
- okay, so, wxPython 2.8.7.1 seems to work fine against this version of the
  library, so I'm dropping the kludgy-patch-to-2.8.7.1 thing. Please report
  any compatibility problems with wxPython 2.8.7.1 and I'll fix them as they
  come up.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.8.4-7
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.8.4-6
- Rebuild for new expat 2.0

* Fri Aug  3 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.4-5
- obsolete all compat-wxGTK subpackages properly (bug #250687)

* Mon Jul 16 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.4-4
- patch from svn to fix rh bug #247414

* Thu Jul 12 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.4-3
- include libwx_gtk2u_media, since I'm now listing the
  buildreqs properly.

* Thu Jul 12 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.4-2
- buildrequires for libSM-devel, gstreamer-plugins-base-devel,
  and GConf2-devel

* Wed Jul 11 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.4-1
- update to 2.8.4
- obsolete compat-wxGTK
- add -fno-strict-aliasing

* Sun Apr 15 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.3-2
- gratuitously bump release number.

* Sun Apr 15 2007 Matthew Miller <mattdm@mattdm.org> - 2.8.3-1
- update to 2.8.3.

* Sun Dec 17 2006 Matthew Miller <mattdm@mattdm.org> - 2.8.0-2.8.0.1.3
- add --enable-timer to build wxTimer class for XaraLX.
- NOTE: if anyone else needs any non-default classes or features enabled,
  let me know. Thanks!

* Fri Dec 15 2006 Matthew Miller <mattdm@mattdm.org> - 2.8.0-2.8.0.1.2
- buildrequires gettext

* Thu Dec 14 2006 Matthew Miller <mattdm@mattdm.org> - 2.8.0-2.8.0.1.1
- patch to 2.8.0.1 wxPython subrelease (following upstream wxPython)
  from wxWidgets CVS

* Thu Dec 14 2006 Matthew Miller <mattdm@mattdm.org> - 2.8.0-2.8.0.0.1
- update to 2.8.0 release
- gtk2 is now the default (and gtk1.2 gone -- about time!)
- compatibility with wxWidgets 2.2 is now gone; add flag to build 2.4 with
  compatibility, though (now off by default)
- added "--enable-no_deps" for faster builds
- added "--enable-intl", because that seems like a good idea
- added disable-rpath, enable-geometry, enable-graphics_ctx, enable-sound,
  enable-mediactrl, and enable-display to better match upstream wxPython
  package.
- buildrequires: gstreamer-devel
- "animate" contributed module no longer exists.
- enable the svg contributed module
- build the .mo files explicitly -- not sure why that's not happening
  automatically.
- minor -- location of doc files in src tarball has changed

* Mon Aug 28 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3-2.6.3.2.3
- bump release for FC6 rebuild

* Mon Jul  3 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3-2.6.3.2.2
- add libGL-devel and libGLU-devel requires to wxGTK-devel package
  (see bug #197501).

* Thu Apr 13 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3-2.6.3.2.1
- oops -- forgot to change mesa-libGL*-devel -> libGL*-devel

* Thu Apr 13 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3-2.6.3.2.0
- patch to cvs subrelease 2.6.3.2 (matches wxPython)

* Sat Mar 25 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3-1    
- 2.6.3 final
- remove the locale_install thing -- that was just an issue with using the
  release candidate.

* Tue Mar 21 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.3-0.rc2
- update to 2.6.3-rc2 package
- all patches now upstream -- removing 'em.
- use complete 'wxWidgets' source tarball instead of the wxGTK-subset one,
  since that's all there is for the release candidate. I'm operating under
  the assumption that we'll have a wxGTK source tarball in the future --
  otherwise, I'm going to eventually have to change the name of this
  package again. :)
- add ODBC support via unixODBC as subpackage (see bug #176950)
- wait, no; comment out ODBC support as it doesn't build...
- add explicit make locale_install; apparently not done as part of
  the general 'make install' anymore.

* Mon Feb 13 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.2-5
- rebuild in preparation for FC5

* Mon Feb 06 2006 Matthew Miller <mattdm@mattdm.org> - 2.6.2-4
- add wxGTK-2.6.2-socketclosefix.patch to fix aMule crashes. see
  bugzilla bug #178184
- add wxGTK-2.6.2-gcc41stringh.patch (pulled from CVS) to make build on 
  FC5 devel w/ gcc-4.1.
  
* Wed Nov 30 2005 Matthew Miller <mattdm@mattdm.org> - 2.6.2-3
- add wxGTK-2.6.2-intl_cpp.patch to deal with amule and probably other
  issues (see bug #154618 comment #47)
- obsolete wxGTK2 < 2.6.2-1 specifically, at Matthias Saou's suggestion

* Mon Nov 28 2005 Matthew Miller <mattdm@mattdm.org> - 2.6.2-2
- implemented some suggestions from Matthias Saou:
-   removed extraneous / from last line of ./configure 
-   removed -n from setup macro, since we're now actually using the
    standard name
-   don't use summary macro in opengl subpackage, as it's not clear which
    summary should get used
-   don't bother setting CC, CXX, etc., as configure script does that
-   move libdir/wx to devel subpackage

* Thu Nov 24 2005 Matthew Miller <mattdm@mattdm.org> - 2.6.2-1
- ready for actually putting into Extras
- update mesa buildreqs for new split-up xorg packaging
- libgnomeprint22-devel -> libgnomeprintui22-devel

* Tue Oct 04 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 2.6.2-0.1
- Update to 2.6.2.
- Include the sample wx bakefiles.
- Include new .mo files.
- From Paul Johnson:
  Change license to wxWidgets due to concerns over trademark infringement.
  Add dist tag.
- From Tom Callaway: Build and include libwx_gtk2u_animate-2.6.

* Thu Apr 28 2005 Matthew Miller <mattdm@mattdm.org> 2.6.1-0.1
- update to 2.6.1
- from Michael Schwendt in 2.4.2-11 package: build-require
  xorg-x11-Mesa-libGL and xorg-x11-Mesa-libGLU (the libGL and libGLU
  deps aren't provided in FC3, so not using that).
- from Thorsten Leemhuis in 2.4.2-12 package: sed -i -e
  's|/usr/lib\b|%%{_libdir}|' in configure also to fix x86_64
- properly include older 2.4.x changelog

* Wed Apr 27 2005 Matthew Miller <mattdm@mattdm.org> - 2.6.0-0.1
- include libwx_gtk2u_gizmos_xrc in file listing

* Wed Apr 27 2005 Matthew Miller <mattdm@mattdm.org> - 2.6.0-0.0
- update to 2.6.0 final release
- configure now wants "--with-gtk=2" instead of "--enable-gtk2".

* Wed Apr 13 2005 Matthew Miller <mattdm@mattdm.org> - 2.5.5-0.2
- removed provides: wxWidgets/wxWidgets devel -- handy for compatibility
  with unmodified generic source packages, but not so good for 
  repeatable builds.

* Wed Apr 13 2005 Matthew Miller <mattdm@mattdm.org> - 2.5.5-0.1
- whoops -- forgot to remove a reference to the "common" package
- version-release for obsoletes/provides

* Tue Apr 12 2005 Matthew Miller <mattdm@mattdm.org> - 2.5.5-0
- remove BU-specific oddities for fedora an idea for a simplied future....

* Tue Apr 12 2005 Matthew Miller <mattdm@bu.edu> - 2.5.5-bu45.2
- whoops -- forgot "Provides: wxGTK2-devel".

* Tue Apr 12 2005 Matthew Miller <mattdm@bu.edu> - 2.5.5-bu45.1
- update to 2.5.5

* Sat Mar  5 2005 Matthew Miller <mattdm@bu.edu> - 2.5.4-bu45.3
- Obsolete & provide GTK-xrc, wxGTK-stc, to provide clean upgrade path

* Tue Mar  1 2005 Matthew Miller <mattdm@bu.edu> - 2.5.4-bu45.2
- enable wxWindows 2.2 compatibility (for compatibility with 2.4 rpm,
  ironically).

* Tue Mar  1 2005 Matthew Miller <mattdm@bu.edu> - 2.5.4-bu45.1
- update to 2.5.4 -- the devel version is where all the fun is.
- rebase to updated FE 2.4.2 package
- license isn't "BSD" -- it's "wxWindows Library Licence".
- make gtk2-only -- gtk 1.0.x is no longer supported, and 1.2.x is
  being phased out. 2.x is the way to go.
- all current patches no longer necessary (upstream)
- roll "common" subpackage in to main package -- no longer makes sense
  to split it out with gtk+ gone
- use SDL, which will make this use Alsa for sound. I believe.
- add gnomeprint support
- add enable-debug_info for debuginfo package
- enable unicode
- use GDK_USE_XFT to enable Pango and fontconfig
- xrc moved from contrib to base -- making it no longer a subpackage
- making stc part of base too -- it's tiny, and doesn't introduce any
  additional deps
- leaving gl as a subpackage, though, since it's the only part that
  requires GL libs.
- add 'ogl' 2d drawing lib from contrib (needed for wxPython)
- add 'gizmos' from contrib (needed for wxPython)
- make wx-config actually part of the package, since there's no need
  to mess with moving it around
- the various afm fonts are gone in 2.5....
- use configure macro
- add provides for wxWidgets and wxWidgets-devel, because that
  seems like a good idea.

* Sun Jan 23 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.4.2-8
- Fix wx-config for x86_64 (#145508).
- Honor $RPM_OPT_FLAGS better, as well as %%{__cc} and %%{__cxx}.

* Mon Dec  6 2004 Ville Skyttä <ville.skytta at iki.fi> - 2.4.2-7
- Patch to avoid aclocal >= 1.8 warnings from wxwin.m4.
- Move unversioned *.so links for -gl, -stc and -xrc to -devel, make -devel
  require them.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 2.4.2-6
- Bump release to provide Extras upgrade path.
- Fix spaces/tabs in spec.
- Remove unneeded zero epochs.
- Add full source URL.

* Tue Jun 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.4.2-0.fdr.2
- s/wxWindows/wxWidgets/
- Fix release tag.

* Sat May 22 2004 Noa Resare <noa@resare.com> - 0:2.4.2-0.fdr.1.3
- Merged fix from wxGTK cvs head, now works with recent gtk2

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.4.2-0.fdr.1
- Update to 2.4.2.

* Mon Aug  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.4.1-0.fdr.4
- Borrow Matthias Saou's -gl and -stc subpackages.

* Mon Jun 16 2003 Dams <anvil[AT]livna.org> 0:2.4.1-0.fdr.3
- Removed libwx_gtk2_xrc*so* from wxGTK2/wxGTK2-devel packages

* Sun Jun 15 2003 Dams <anvil[AT]livna.org> 0:2.4.1-0.fdr.2
- Removed *-devel postun scriptlets (from Ville Skyttä)

* Sat Jun 14 2003 Dams <anvil[AT]livna.org> 0:2.4.1-0.fdr.1
- Updated to 2.4.1

* Wed May 28 2003 Dams <anvil[AT]livna.org> 0:2.4.0-0.fdr.7
- Added xrc contrib in separate packages

* Wed May 21 2003 Dams <anvil[AT]livna.org> 0:2.4.0-0.fdr.6
- Corrected typo in postun devel

* Wed May 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.4.0-0.fdr.5
- Make -devel packages require the corresponding GTK devel package.
- Save .spec in UTF-8.
- Fixes from Dams:
- Don't build --with-unicode, it breaks stuff (as was already noted by Dams).
- Don't remove wx-config symlinks on upgrades.
- Remove duplicates from docs.

* Tue May 20 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.4.0-0.fdr.4
- Split into subpackages, spec file rewrite.
- Use bzipped upstream tarball.
- Clean up BuildRequirement versions.

* Fri May  9 2003 Dams <anvil[AT]livna.org> 0:2.4.0-0.fdr.3
- Now build/include both gtk/gtk2 libs
- buildroot -> RPM_BUILD_ROOT

* Mon Mar  3 2003 Dams <anvil@livna.org>
- Initial build.
- Disable unicode as it breaks lmule
- use the %%find_lang macro for locale
