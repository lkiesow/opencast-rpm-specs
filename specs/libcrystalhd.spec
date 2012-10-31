%global date 20120405

Summary:        Broadcom Crystal HD device interface library
Name:           libcrystalhd
Version:        3.10.0
Release:        2%{?dist}
License:        LGPLv2
Group:          System Environment/Libraries
#Source:         http://www.broadcom.com/docs/support/crystalhd/crystalhd_linux_20100703.zip
# This tarball and README are inside the above zip file...
# Patch generated from http://git.linuxtv.org/jarod/crystalhd.git
Source0:        libcrystalhd-%{date}.tar.bz2
Source1:        README_07032010
# We're going to use even newer firmware for now
Source2:        bcm70012fw.bin
Source3:        bcm70015fw.bin
# LICENSE file is copy-n-pasted from http://www.broadcom.com/support/crystal_hd/
Source4:        LICENSE
Source9:        libcrystalhd-snapshot.sh
Patch0:         libcrystalhd-nosse2.patch
URL:            http://www.broadcom.com/support/crystal_hd/
ExcludeArch:    s390 s390x
BuildRequires:  autoconf automake libtool
Requires:       crystalhd-firmware

%description
The libcrystalhd library provides userspace access to Broadcom Crystal HD
video decoder devices. The device supports hardware decoding of MPEG-2,
h.264 and VC1 video codecs, up to 1080p at 40fps for the first-generation
bcm970012 hardware, and up to 1080p at 60fps for the second-generation
bcm970015 hardware.

%package devel
Summary:       Development libs for libcrystalhd
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description devel
Development libraries needed to build applications against libcrystalhd.

%package -n crystalhd-firmware
Summary:       Firmware for the Broadcom Crystal HD video decoder
License:       Redistributable, no modification permitted
BuildArch:     noarch
Group:         System Environment/Kernel
Requires:      %{name} = %{version}-%{release}

%description -n crystalhd-firmware
Firmwares for the Broadcom Crystal HD (bcm970012 and bcm970015)
video decoders.

%define        majorminor 0.10
%define        _gst 0.10.30
%define        _gstpb 0.10.30

%package -n gstreamer-plugin-crystalhd
Summary:       Gstreamer crystalhd decoder plugin
Group:         Applications/Multimedia
Requires:      %{name} = %{version}-%{release}
Requires:      gstreamer-plugins-base
BuildRequires: gstreamer-devel >= %{_gst}
BuildRequires: gstreamer-plugins-base-devel >= %{_gstpb}

%description -n gstreamer-plugin-crystalhd
Gstreamer crystalhd decoder plugin

%prep
%setup -q -n libcrystalhd-%{date}
cp %{SOURCE1} %{SOURCE4} .
%ifnarch %{ix86} ia64 x86_64
%patch0 -p1 -b .nosse2
sed -i -e 's|-msse2||' linux_lib/libcrystalhd/Makefile
%endif

%build
pushd linux_lib/libcrystalhd/ > /dev/null 2>&1
# FIXME: this doesn't work just yet...
#make CPPFLAGS="%{optflags}" %{?_smp_mflags}
make %{?_smp_mflags}
popd > /dev/null 2>&1
pushd filters/gst/gst-plugin/ > /dev/null 2>&1
sh autogen.sh || :
%configure
make %{?_smp_mflags} \
  CFLAGS="-I%{_builddir}/%{buildsubdir}/include -I%{_builddir}/%{buildsubdir}/linux_lib/libcrystalhd" \
  BCMDEC_LDFLAGS="-L%{_builddir}/%{buildsubdir}/linux_lib/libcrystalhd -lcrystalhd"
popd > /dev/null 2>&1

%install
pushd linux_lib/libcrystalhd/ > /dev/null 2>&1
make install LIBDIR=%{_libdir} DESTDIR=$RPM_BUILD_ROOT
popd > /dev/null 2>&1
pushd filters/gst/gst-plugin/ > /dev/null 2>&1
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/libgstbcmdec.{a,la}
popd > /dev/null 2>&1
rm -rf $RPM_BUILD_ROOT/lib/firmware/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/firmware/
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_prefix}/lib/firmware/
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_prefix}/lib/firmware/
#Install udev rule
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -pm 0644 driver/linux/20-crystalhd.rules \
  $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc README_07032010 LICENSE
%{_libdir}/libcrystalhd.so.*

%files devel
%defattr(-,root,root,0755)
%dir %{_includedir}/libcrystalhd
%{_includedir}/libcrystalhd/*
%{_libdir}/libcrystalhd.so

%files -n crystalhd-firmware
%defattr(-,root,root,0755)
%doc LICENSE
%config %{_sysconfdir}/udev/rules.d/20-crystalhd.rules
%{_prefix}/lib/firmware/bcm70012fw.bin
%{_prefix}/lib/firmware/bcm70015fw.bin

%files -n gstreamer-plugin-crystalhd
%defattr(-,root,root,0755)
%{_libdir}/gstreamer-%{majorminor}/*.so


%changelog
* Fri Aug 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.10.0-2
- Fix build on non-SSE2 arches
- Install CrystalHD udev rule
- Clean spec file

* Thu Apr 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 28 2010 Jarod Wilson <jarod@redhat.com> - 3.5.1-1
- Update to v3.5.1, now with nv12 support

* Sun Jul 25 2010 Jarod Wilson <jarod@redhat.com> - 3.5.0-2
- Tarball had object files in it, clean them out before building

* Sat Jul 24 2010 Jarod Wilson <jarod@redhat.com> - 3.5.0-1
- Rebase to 07032010 crystalhd sources
- Large version-bump as driver and lib are now essentially 100%
  in sync with the Windows driver and lib
- Ship firmware, now that Broadcom has posted a redistribution,
  no modification license to cover it
- Build the gstreamer decoder plugin (will be moved to its own
  package sooner or later)

* Sun Apr 04 2010 Jarod Wilson <jarod@redhat.com> - 0.9.25-4
- Fix segfault on firmware upload

* Fri Mar 26 2010 Jarod Wilson <jarod@redhat.com> - 0.9.25-3
- Update to pre-0.9.26 libcrystalhd, which contains support
  for the new Broadcom BCM970015 Crystal HD decoder card

* Thu Mar 11 2010 Jarod Wilson <jarod@redhat.com> - 0.9.25-2
- Minor fixups to the as-yet-not-enabled firmware sub-package

* Wed Jan 06 2010 Jarod Wilson <jarod@redhat.com> - 0.9.25-1
- Initial package
