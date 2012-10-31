%define         majorminor      0.10

Name:           gstreamer-python
Version:        0.10.22
Release:        2%{?dist}
Summary:        Python bindings for GStreamer

Group:          Development/Languages
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-python/gst-python-%{version}.tar.bz2
#Patch0:         gst-python-0.10.15-strayline.patch
Patch1:         0001-preset-expose-new-gst.preset_-set-get-_app_dir-on-py.patch

Requires:       python >= 2.3
Requires:       pygtk2 >= 2.8.0
Requires:       gstreamer >= 0.10.36
Requires:       gstreamer-plugins-base >= 0.10.36

BuildRequires:  python >= 2.3
BuildRequires:  python-devel >= 2.3
BuildRequires:  pygtk2-devel >= 2.8.0
# xwindowlistener needs X11 headers
BuildRequires:  libX11-devel
BuildRequires:  gstreamer-devel >= 0.10.36
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.36
BuildRequires:  pygobject2-devel >= 2.11.2


%description
This module contains a wrapper that allows GStreamer applications
to be written in Python.


%package        devel
Summary:        Headers for developing programs that will use %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       pygtk2-devel
Requires:       gstreamer-devel


%description devel
This package contains the static libraries and header files needed for
developing gstreamer-python applications.


%prep
%setup -q -n gst-python-%{version}
%{__sed} -i 's|^#!/usr/bin/env python$|#|' gst/extend/*.py
#%patch0 -p1 -b .strayline
%patch1 -p1 -b .gst_preset_set_app_dir


%build
%configure
make %{?_smp_mflags}


%install
rm -rf docs-to-include
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
mkdir -p docs-to-include/examples
chmod -x examples/*.py
cp examples/*.py docs-to-include/examples/
rm -fr $RPM_BUILD_ROOT%{_datadir}/gst-python/%{majorminor}/examples


%files
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/python?.?/site-packages/gst-%{majorminor}
%{_libdir}/python?.?/site-packages/pygst.py*
%{_libdir}/python?.?/site-packages/pygst.pth
%{_libdir}/python?.?/site-packages/gstoption.so
%{_libdir}/gstreamer-0.10/*
%dir %{_datadir}/gst-python
%dir %{_datadir}/gst-python/%{majorminor}
%dir %{_datadir}/gst-python/%{majorminor}/defs
%{_datadir}/gst-python/%{majorminor}/defs/*.defs


%files devel
%doc docs-to-include/*
%{_includedir}/gstreamer-0.10/gst/pygst*.h
%{_libdir}/pkgconfig/gst-python-%{majorminor}.pc


%changelog
* Sat Jul 14 2012 Kalev Lember <kalevlember@gmail.com> - 0.10.22-2
- Backport gst.preset_{set,get}_app_dir(), needed for transmageddon 0.21

* Sat Jul 14 2012 Kalev Lember <kalevlember@gmail.com> - 0.10.22-1
- Update to 0.10.22 (#750016)
- Include new headers in -devel subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Xavier Lamien <laxathom@fedoraproject.org> - 0.10.19-1
- Update release.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.10.16-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Aug 14 2009 Xavier Lamien <laxathom@fedoraproject.org> - 0.10-16-1
- Update release.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Denis Leroy <denis@poolshark.org> - 0.10.15-1
- Update to upstream 0.10.15 (#502812)
- Added git patch to fix compile fix

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Denis Leroy <denis@poolshark.org> - 0.10.14-1
- Update to upstream 0.10.14, with various bug fixes
- Removed problematic devel Provide

* Sat Jan 10 2009 Denis Leroy <denis@poolshark.org> - 0.10.13-1
- Update to upstraem 0.10.13
- Forked devel package with pkgconfig file (#477310)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.10.12-2
- Rebuild for Python 2.6

* Mon Aug 25 2008 Denis Leroy <denis@poolshark.org> - 0.10.12-1
- Update to upstream 0.10.12

* Fri Mar 28 2008 Denis Leroy <denis@poolshark.org> - 0.10.11-2
- Fixed datadir directory ownership (#439291)

* Sun Mar 23 2008 Denis Leroy <denis@poolshark.org> - 0.10.11-1
- Update to upstream 0.10.11, bugfix release updates

* Wed Feb 13 2008 Denis Leroy <denis@poolshark.org> - 0.10.10-1
- Update to upstream 0.10.10, BR updates

* Sun Dec  9 2007 Denis Leroy <denis@poolshark.org> - 0.10.9-1
- Update to upstream 0.10.9
- Removed exit patch, is upstream

* Fri Sep 14 2007 Denis Leroy <denis@poolshark.org> - 0.10.8-2
- Added patch to avoid crash on exit

* Mon Aug 20 2007 Denis Leroy <denis@poolshark.org> - 0.10.8-1
- Update to upstream 0.10.8
- License tag update

* Tue Feb 20 2007 Denis Leroy <denis@poolshark.org> - 0.10.7-2
- Ship examples in doc directory only, fixes multilib conflict (#228363)
- rpmlint cleanup

* Wed Feb 14 2007 Denis Leroy <denis@poolshark.org> - 0.10.7-1
- Update to 0.10.7
- Some spec cleanups

* Mon Dec 11 2006 Denis Leroy <denis@poolshark.org> - 0.10.6-1
- Update to 0.10.6, build with python 2.5

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.10.5-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Denis Leroy <denis@poolshark.org> - 0.10.5-1
- Update to 0.10.5

* Tue Sep 19 2006 Denis Leroy <denis@poolshark.org> - 0.10.4-2
- FE Rebuild

* Thu Jun 15 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.4-1
- new upstream release

* Tue Jan 24 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- update to GStreamer Python Bindings 0.10.2
- remove -devel requirements

* Thu May 19 2005 Thomas Vander Stichele <thomas at apestaart dot org> - 0.8.1-6
- disable docs build - they're already in the tarball

* Tue May 10 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0.8.1-5
- Move __init__.py* files from lib to _libdir on multilibarchs
  Found in thias spec file, fixes x86_64

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.8.1-3
- include missing directories

* Thu Mar 31 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.8.1-2
- add deps pygtk2-devel and gstreamer-devel for pkgconfig file

* Fri Dec 24 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.1-1: moved to Fedora Extras CVS

* Fri Dec 24 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.1-0.fdr.2: various cleanups

* Tue Dec 07 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.1-0.fdr.1: new upstream release

* Mon Nov 15 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.0-0.fdr.1: new upstream release

* Fri Nov 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.94-0.fdr.1: new upstream release

* Tue Oct 12 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.93-0.fdr.1: new upstream release

* Mon Jun 21 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.92-0.fdr.1: new upstream release

* Wed Mar 31 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.91-0.fdr.1: new upstream release

* Tue Sep 02 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.1.0-0.fdr.1: first fedora release
