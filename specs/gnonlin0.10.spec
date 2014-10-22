%define         gst_req                 0.10.24
%define         gst_plugins_base_req    0.10.24

Name:           gnonlin0.10
Version:        0.10.17
Release:        5%{?dist}
Summary:        GStreamer extension library for non-linear editing

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://gnonlin.sourceforge.net/
Source:         http://gstreamer.freedesktop.org/src/gnonlin/gnonlin-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gstreamer-devel >= %{gst_req}
BuildRequires:  gstreamer-plugins-base-devel >= %{gst_plugins_base_req}

Requires:       gstreamer-plugins-base >= %{gst_plugins_base_req}
Obsoletes:      gnonlin0.10-devel < %{version}-%{release}
Provides:       gnonlin0.10-devel = %{version}-%{release}

%description
Gnonlin is a library built on top of GStreamer (http://gstreamer.net)
which provides support for writing non-linear audio and video editing
applications. It introduces the concept of a timeline.
This is the legacy version for GStreamer 0.10.x

%prep
%setup -q -n gnonlin-%{version}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB README
%{_libdir}/gstreamer-0.10/libgnl.so

%changelog
* Mon Oct 20 2014 Lars Kiesow <lkiesow@uos.de> - 0.10.17-5
- Changed name to gstreamer0.10

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 16 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.17-1
- Update to 0.10.17 "Flight from Hawaii coming out of the sun"
-
- Features of this release
-
-       * documentation and debugging fixes
-       * Use glib 2.22 API if available
-
- Bugs fixed in this release
-
-       * 628943 : make check fails if videomixer element can't be found
-       * 633721 : tests: gnl/simple: test_one_under_another failure / timeout


* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.16-1
- Update to 0.10.16 "I needed time to think to get the memories from my mind"
-
- Features of this release
-
-       * More race fixes
-       * gnlcomposition: propagate caps to childs
-       * gnlurisource: Only use needed streams
-       * gnlcomposition: Fix QoS handling
-
- Bugs fixed in this release
-
-       * 613283 : gst_element_class_set_details = > gst_element_class_set_details_simple
-       * 626501 : Caps property of gnlfilesource works incorrectly
-       * 626733 : Race in gnlcomposition between no_more_pads_object_cb and compare_relink_single_node

* Tue Mar 09 2010 Benjamin Otte <otte@redhat.com> - 0.10.15-1
- Update to 0.10.15 "I missed the snow in Barcelona"
-
- Features of this release
-
-     * Many fixes for complex compositions
-
- Bugs fixed in this release
-
-     * 609689 : compositions containing gnloperation
-                videomixer/adder freeze when input is another gnloperation
-     * 609792 : black frame flashing in rendered files when using transitions

* Thu Feb 11 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.14-1
- Update to 0.10.14 "Slicing, Dicing and Chopping"
-
- Features of this release
-
-     * New gnlurisource element
-     * Documentation update
-
- Bugs fixed in this release
-
-     * 595570 : Add a GnlURISource

* Thu Dec 10 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.13.2-1
- Update to prerelease version.

* Mon Sep  7 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.13-1
- Update to 0.10.13 "Service of Quality"
-
- Features of this release
-
-       * Fix QoS event handling
-       * Fix racyness in source pad handlings
-       * GnlOperation: Add signal to know input stream priorities
-
- Bugs fixed in this releas
-
-       * 583145 : Seeking on pending pipelines should return True.

* Wed Sep  2 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.12.3-0.2
- Doh!

* Wed Sep  2 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.12.3-0.1
- Update to latest prelrelease

* Sat Aug 29 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.12.2-0.1
- Update to prerelease for 0.10.13

* Tue Aug 11 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.12-1
- Update to 0.10.12 "Lots of people on the clothesline"
-
- Features of this release
-
-       * New property for faster composition updates
-       * Speedups
-       * various fixes

* Wed Aug  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.11.3-0.1
- Update to latest prerelease.
- Clean up some rpmlint warnings

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.11.2-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.11.2-0.1
- Update to gnonlin prerelease.

* Thu May 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.11-1
- This is GNonLin 0.10.11 "How about green for the bikeshed?"
-
- Features of this release
-
-  * Speedup option to avoid recalculation during composition changes
-  * Switch to regular seeks for more efficient beheaviour
-  * More GstQuery/GstEvent handling
-  * Bugfixes on GnlOperation
-  * Switch to GIT
-  * Documentation

* Mon May 18 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.10.3-1
- Update to prerelease for 0.10.11

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.10-2
- Don't forget to upload the new sources!

* Mon Nov  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.10-1
- Update to 0.10.10

* Thu Oct 30 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.9.2-1
- Update to 0.10.9.2

* Tue Mar  4 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.9-4
- Update source url.

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.10.9-3
- Rebuild for gcc-4.3.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.10.9-2
- Rebuild.

* Wed Aug  8 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.10.9-1
- Update to 0.10.9.

* Sun Aug  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.10.8-2
- Update license tag.

* Tue May 15 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.10.8-1
- Update to 0.10.8.

* Mon Feb  5 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.10.7-1
- Update to 0.10.7.
- Bump gstreamer version required.

* Tue Nov 28 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.10.6-1
- Add dist tag.
- Update to 0.10.6.

* Mon Oct 16 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.10.5-3
- Unorphan & rebuild.
- Require gstreamer-plugins-base.
- Don't build static libraries.
- Bump minimum requirement for gst-plugins-base.

* Thu Sep 07 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.5-2
- rebuild for FC6.

* Tue Jul 25 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.5-1
- updated package to 0.10.5

* Thu May 18 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.4-1
- updated package to 0.10.4
- add Obsoletes: gnonlin-devel

* Wed Apr 26 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.3-2
- simplified install
- require gstreamer-plugins-base-devel
- remove -devel package

* Tue Apr 25 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.3-1
- updated package to 0.10.3
- remove gnonlin.pc

* Fri Feb 17 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.0.5-6
- bump release because of build system problem

* Fri Feb 17 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.0.5-5
- bump release because of build system problem

* Fri Feb 17 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.0.5-4
- rebuild for Fedora Extras 5

* Wed Feb 08 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.0.5-3
- remove gettext-devel requirement as aclocal and autoconf not run
- remove pre and post requirements
- update URL
- fix Groups
- ensure proper license is included

* Tue Feb 07 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.0.5-2
- remove %%define name
- BuildRequires gettext-devel
- remove gst-register
- rm %%{_libdir}/gstreamer-0.10/libgnl.la after install
- -devel package owns %%{_includedir}/gnl
- avoid %%makeinstall
- remove aclocal and autoconf from %%prep

* Mon Jan 23 2006 W. Michael Petullo <mike[@]flyn.org> 0.10.0.5-1
- updated package to 0.10.0.5 and Fedora

* Wed Jun 29 2005 Götz Waschk <waschk@mandriva.org> 0.2.2-1mdk
- initial package

* Mon Mar 21 2005 Edward Hervey <bilboed at bilboed dot com>
- First version of spec
