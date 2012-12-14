%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:		gstreamer-rtsp
Version:	0.10.8
Release:	2%{?dist}
Summary:	GStreamer RTSP server library

Group:		Applications/Multimedia
License:	LGPLv2+
URL:		http://people.freedesktop.org/~wtay/
Source0:	http://gstreamer.freedesktop.org/src/gst-rtsp/gst-rtsp-%{version}.tar.bz2
Patch0:		gst-rtsp-fixpygo.patch

BuildRequires:	gstreamer-devel gstreamer-plugins-base-devel
BuildRequires:	python-devel gstreamer-python-devel pygobject2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	vala-devel vala-tools
BuildRequires:	chrpath

BuildRequires: automake autoconf libtool

%description
A GStreamer-based RTSP server library, with Python and Vala bindings.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Group:		Development/Libraries
License:	LGPLv2+
Requires:	pkgconfig
Requires:	gstreamer-devel
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for %{name}, the GStreamer RTSP server library.

%package python
Summary:	Python bindings for %{name}
Requires:	%{name} = %{version}-%{release}
License:	LGPLv2+
Requires:	gstreamer-python
Requires:	%{name} = %{version}-%{release}

%description python
Python bindings for %{name}, the GStreamer RTSP server library.

%package vala
Summary:	Vala bindings for %{name}
Requires:	%{name} = %{version}-%{release}
License:	LGPLv2+
Requires:	vala
Requires:	%{name} = %{version}-%{release}

%description vala
Vala bindings for %{name}, the GStreamer RTSP server library.

%prep
%setup -q -n gst-rtsp-%{version}
%patch0 -p1 -b .fix-pygo

autoreconf -f

%build
# Until https://bugzilla.gnome.org/show_bug.cgi?id=634376 is fixed, disable introspection
%configure

make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

#Remove libtool archives and static
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
# can't tweak libtool, see:
# https://bugzilla.gnome.org/show_bug.cgi?id=634376#c1
chrpath --delete %{buildroot}%{_libdir}/libgstrtspserver-0.10.so*
chrpath --delete %{buildroot}%{python_sitearch}/gst-0.10/gst/rtspserver.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING.LIB README TODO NEWS
%{_libdir}/libgstrtspserver-0.10.so.0
%{_libdir}/libgstrtspserver-0.10.so.0.0.0
%{_libdir}/girepository-1.0/GstRtspServer-0.10.typelib

%files devel
%defattr(-,root,root,-)
%{_includedir}/gstreamer-0.10/gst/rtsp-server
%{_libdir}/libgstrtspserver-0.10.so
%{_libdir}/pkgconfig/gst-rtsp-server-0.10.pc
%{_datadir}/gir-1.0/GstRtspServer-0.10.gir
%{_datadir}/gst-rtsp/0.10/defs/rtspserver-types.defs
%{_datadir}/gst-rtsp/0.10/defs/rtspserver.defs

%files python
%defattr(-,root,root,-)
%{python_sitearch}/gst-0.10/gst/rtspserver.so

%files vala
%defattr(-,root,root,-)
%{_datadir}/vala/vapi/gst-rtsp-server-0.10.deps
%{_datadir}/vala/vapi/gst-rtsp-server-0.10.vapi

%changelog
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.8-1
- Update to 0.10.8, cleanup spec file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Bastien Nocera <bnocera@redhat.com> 0.10.7-2
- Enable introspection, thanks Colin

* Fri Nov 05 2010 Bastien Nocera <bnocera@redhat.com> 0.10.7-1
- Update to 0.10.7

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Dec 16 2009 Bastien Nocera <bnocera@redhat.com> 0.10.5-1
- Update to 0.10.5

* Sat Aug  8 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.4-1
- Update to 0.10.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 0.10.3-1
- Update to 0.10.3 (#501159)

* Thu Apr 23 2009 - Bastien Nocera <bnocera@redhat.com> - 0.10.1.0-3
- Update for missing Requires, and ldconfig calls, with help from
  Peter Lemenkov <lemenkov@gmail.com>

* Thu Apr 23 2009 - Bastien Nocera <bnocera@redhat.com> - 0.10.1.0-2
- Require gstreamer-python-devel in F11

* Tue Feb 03 2009 - Bastien Nocera <bnocera@redhat.com> - 0.10.1.0
- First version

