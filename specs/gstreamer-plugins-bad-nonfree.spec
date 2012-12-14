%define majorminor   0.10

Summary:        Non Free GStreamer streaming media framework "bad" plug-ins
Name:           gstreamer-plugins-bad-nonfree
Version:        0.10.22
Release:        3%{?dist}
License:        LGPLv2+
Group:          Applications/Multimedia
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gstreamer-devel gstreamer-plugins-base-devel
BuildRequires:  amrwb-devel faac-devel liboil-devel
BuildRequires:  check gettext-devel PyXML

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that depend upon non-free libraries.


%prep
%setup -q -n gst-plugins-bad-%{version}


%build
%configure \
    --with-package-name="gst-plugins-bad rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug --disable-static
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
pushd ext/amrwbenc
make %{?_smp_mflags} V=2
popd
pushd ext/faac
make %{?_smp_mflags} V=2
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd ext/amrwbenc
make install V=2 DESTDIR=$RPM_BUILD_ROOT
popd
pushd ext/faac
make install V=2 DESTDIR=$RPM_BUILD_ROOT
popd
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgst*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README REQUIREMENTS
%{_datadir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstamrwbenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaac.so


%changelog
* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.10.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Aug 27 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.22-2
- Rebuild for Fedora 16

* Tue May 17 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.22-1
- New upstream release 0.10.22

* Thu Apr 21 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.21-2
- Rebuild for proper package kit magic provides (rhbz#695730)

* Fri Jan 28 2011 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.21-1
- New upstream release 0.10.21

* Sun Mar 14 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.18-1
- New upstream release 0.10.18

* Tue Jan  5 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.17-2
- Various small specfile fixes from review (rf1015)

* Sat Dec 19 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.17-1
- Initial RPM Fusion package
