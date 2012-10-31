%bcond_without schroedinger

Summary: A library for reading and writing quicktime files
Name: libquicktime
Version: 1.2.3
Release: 32%{?dist}
License: GPL
Group: System Environment/Libraries
Source0: http://downloads.sourceforge.net/libquicktime/%{name}-%{version}.tar.gz
Patch0: libquicktime-oldstyle-tooltips.diff
#Patch1: libquicktime-lib64.diff
#Patch2: libquicktime-cflags.diff
URL: http://libquicktime.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-root
#BuildRequires: autoconf, libtool
BuildRequires: gcc-c++, gettext
BuildRequires: libXt-devel, libXaw-devel, libXv-devel
BuildRequires: libGL-devel, libGLU-devel
BuildRequires: gtk2-devel >= 2.4.0, libdv-devel, libvorbis-devel, lame-devel
BuildRequires: libpng-devel, libjpeg-devel
BuildRequires: libraw1394-devel, libavc1394-devel
BuildRequires: alsa-lib-devel, ffmpeg-devel
#%{?with_schroedinger:BuildRequires: schroedinger-devel}
BuildRequires: faac-devel
BuildRequires: doxygen
Provides: libquicktime0 = %{name}-%{version}

%description
libquicktime is a library for reading and writing quicktime files. It
is based on the quicktime4linux library, with many extensions.

%package devel
Summary: Development files for %{name}

%description devel
libquicktime is a library for reading and writing quicktime files. It
is based on the quicktime4linux library, with many extensions.

%package -n libquicktime0
Summary: Shared libraries for package libquicktime

%description -n libquicktime0
This package provides the shared libraries libquicktime.so.0* for
the package libquicktime. Shared libraries are required at runtime
for software built against libquicktime. Keeping shared libraries
in a separate package enables their use as forward/backward
compatibility packages.


%prep
%setup -q
%patch0 -p0
#patch1 -p1 -b .lib64
#patch2 -p1 -b .cflags

%build
#libtoolize --force
#autoreconf --force --install
%configure \
	--with-x \
	--with-cpuflags="%{optflags}" \
	--enable-gpl \
	--docdir=%{_defaultdocdir}/%{name}-%{version}
#	--with-x --x-includes=%{_x_includes} --x-libraries=%{_x_libraries} \

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
rm -rf %{buildroot}
#export LIBRARY_PATH=%{buildroot}%{_libdir}
make install DESTDIR=%{buildroot} \
  docdir=%{_defaultdocdir}/%{name}-%{version}

rm %{buildroot}%{_libdir}/*.la
rm %{buildroot}%{_libdir}/libquicktime/*.la

%find_lang %{name}

cat > develfiles.list << EOF
%defattr(-,root,root,-)
%{_bindir}/libquicktime_config
#%{_bindir}/lqt-config
%dir %{_libdir}/%{name}
EOF

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/lqtplay
%{_bindir}/libquicktime_config
%{_bindir}/qt*
%{_bindir}/lqt_transcode
#%{_bindir}/lqtvrplay
%{_bindir}/lqtremux
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/lqt/
%{_libdir}/pkgconfig/libquicktime.pc

%files -n libquicktime0
%defattr(-,root,root,-)
%{_libdir}/libquicktime*so*


%changelog
* Wed Oct 24 2012 Lars Kiesow <lkiesow@uos.de> - 1.2.3-32
- Fixed issue with shared library

* Tue Oct 23 2012 Lars Kiesow <lkiesow@uos.de> - 1.2.3-31
- Port for matterhorn repo.

* Sun Nov 13 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.3-30
- Update to 1.2.3.

* Sat Apr 30 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.2-29
- Update to 1.2.2.

* Sun Jun 27 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.5-28
- Update to 1.1.5.

* Sun Jan 10 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.4-27
- Update to 1.1.4.

* Tue Jul 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.3-26
- Update to 1.1.3.

* Sun Jan 18 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.1-25
- update to 1.1.1.

* Sun Nov  9 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.0-24
- Update to 1.1.0.

* Thu Jul 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.3-23
- Update to 1.0.3.

* Wed Jan  9 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.2-22
- Update to 1.0.2.

* Sun Oct 21 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.1-21
- Update to 1.0.1.

* Sat Oct 13 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.0-20
- Enable oldstyle tooltips (Wes Shull <wes.shull@gmail.com>).

* Wed Apr 18 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.0-19
- Update to 1.0.0.

* Thu Jan  4 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.9.10-18
- Update to 0.9.10.

* Mon Jul 10 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.9.

* Fri Feb  3 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.8.

* Tue May 31 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Sync with freshrpms.

* Sat May 28 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.7.

* Sat May 21 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.6.

* Sun May 15 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.5.

* Thu Jan 13 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.4.

* Wed Jul 21 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.9.3.

* Sun Apr 11 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Rebuilt against newer libdv.

* Thu Oct 16 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Updated to 0.9.2 final.

* Tue Apr 22 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Fix plugin compilation, thanks to Dag.

* Wed Apr  9 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
