%global gstversion 0.10
%global gst_minver 0.10.13

Name:           gst-entrans
Version:        0.10.4
Release:        1%{?dist}
Summary:        Plug-ins and tools for transcoding and recording with GStreamer

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://gentrans.sourceforge.net/
Source0:        http://downloads.sourceforge.net/gentrans/%{name}-%{version}.tar.gz

BuildRequires:  gstreamer-devel >= %{gst_minver}
BuildRequires:  gstreamer-plugins-base-devel
Requires:       gstreamer >= %{gst_minver}
Requires:       gstreamer-plugins-entrans%{?_isa} = %{version}-%{release}
Requires:       gstreamer-python

%description
GEntrans is a software package providing a collection of plug-ins and tools 
for the GStreamer multimedia framework specifically geared towards transcoding 
and recording purposes.

GStreamer allows for easy multimedia processing and creation of multimedia 
applications, as e.g. demonstrated by a number of players and some other 
applications already built on it. The purpose here is to concentrate on using 
the framework for transcoding purposes.


%package -n gstreamer-plugins-entrans
Summary:        GStreamer plug-ins from GEntrans
Group:          Applications/Multimedia

%description -n gstreamer-plugins-entrans
GEntrans is a software package providing a collection of plug-ins and tools 
for the GStreamer multimedia framework specifically geared towards transcoding 
and recording purposes.

This package provides several GStreamer plugins from GEntrans.


%package -n gstreamer-plugins-entrans-docs
Summary:        Documentation for GStreamer plug-ins from GEntrans
Group:          Documentation
BuildArch:      noarch
BuildRequires:  gtk-doc

%description -n gstreamer-plugins-entrans-docs
GEntrans is a software package providing a collection of plug-ins and tools 
for the GStreamer multimedia framework specifically geared towards transcoding 
and recording purposes.

This package provides documentation for several GStreamer plugins from GEntrans.


%prep
%setup -q


%build
%configure --enable-debug --disable-static --enable-gtk-doc
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# These files shouldn't be in the RPM
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gstversion}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gstversion}/*.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%doc docs/manual/html/
%{_bindir}/entrans
%doc %{_mandir}/man1/entrans.*


%files -n gstreamer-plugins-entrans
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/gstreamer-%{gstversion}/libgstavidemux.so
%{_libdir}/gstreamer-%{gstversion}/libgstentrans.so
%{_libdir}/gstreamer-%{gstversion}/libgstmencoder.so
%{_libdir}/gstreamer-%{gstversion}/libgsttranscode.so
%{_libdir}/gstreamer-%{gstversion}/libgstvirtualdub.so
%{_libdir}/gstreamer-%{gstversion}/libgstyuv4mpeg.so


%files -n gstreamer-plugins-entrans-docs
%defattr(-,root,root,-)
%doc COPYING
%doc %{_datadir}/gtk-doc/html/%{name}-plugins-%{gstversion}/


%changelog
* Wed Jun 06 2012 Theodore Lee <theo148@gmail.com> - 0.10.4-1
- Update to 0.10.4 release
- Drop liboil-devel buildrequires

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Theodore Lee <theo148@gmail.com> - 0.10.3-4
- Drop requires on gtk-doc

* Sun Jun 19 2011 Theodore Lee <theo148@gmail.com> - 0.10.3-3
- Add license files to subpackages
- Move gtk-doc BuildRequires to plugin docs subpackage

* Fri Jun 10 2011 Theodore Lee <theo148@gmail.com> - 0.10.3-2
- Specify minimum GStreamer versions
- Be more specific in the files section
- Include documentation
- Split GStreamer plugins into separate packages

* Tue Nov 23 2010 Theodore Lee <theo148@gmail.com> - 0.10.3-1
- Latest upstream release

* Thu Sep 30 2010 Theodore Lee <theo148@gmail.com> - 0.10.2-1
- Tweaked install to remove static libraries

* Wed Sep 29 2010 Theodore Lee <theo148@gmail.com> - 0.10.2-0.1.aa
- Initial specfile
