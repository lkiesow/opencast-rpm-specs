%global api 140
%global gitdate 20131030
%global gitversion 2245
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}
%global branch stable
%global bname x264-snapshot-%{snapshot}

# old name
# x264-0.138-20131030-c628e3b.tar.bz2
# new name
# x264-snapshot-20131030-2245.tar.bz2

#global _with_bootstrap 1

%{?_with_bootstrap:
%global _without_libavformat 1
%global _without_libswscale  1
}

Summary: H264/AVC video streams encoder
Name: x264
Version: 0.%{api}
Release: 5%{?gver}%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://developers.videolan.org/x264.html
Source0: ftp://ftp.videolan.org/pub/videolan/x264/snapshots/%{bname}.tar.bz2
#Source1: x264-snapshot.sh
BuildRequires: perl-Digest-MD5-File

# don't remove config.h and don't re-run version.sh
Patch0: x264-nover.patch

BuildRequires: zlib-devel openssl-devel libpng-devel libjpeg-devel
# Deactivated because of loop x264 -> ffmpeg -> x264
#%{!?_without_libavformat:BuildRequires: ffmpeg-devel}
#%{?_with_ffmpegsource:BuildRequires: ffmpegsource-devel}
%{?_with_visualize:BuildRequires: libX11-devel}
BuildRequires: yasm >= 1.0.0
Requires: %{name}-libs = %{version}-%{release}

%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the frontend.

%package libs
Summary: Library for encoding H264/AVC video streams
Group: Development/Libraries

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary: Development files for the x264 library
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the development files.

%global x_configure \
./configure \\\
	--prefix=%{_prefix} \\\
	--exec-prefix=%{_exec_prefix} \\\
	--bindir=%{_bindir} \\\
	--includedir=%{_includedir} \\\
	--extra-cflags="$RPM_OPT_FLAGS" \\\
	%{?_with_visualize:--enable-visualize} \\\
	%{?_without_libavformat:--disable-lavf} \\\
	%{?_without_libswscale:--disable-swscale} \\\
	%{!?_with_ffmpegsource:--disable-ffms} \\\
	--enable-debug \\\
	--enable-shared \\\
	--system-libx264 \\\
	--enable-pic


%prep
%setup -q -c -n %{bname}
pushd %{bname}
#%patch0 -p1 -b .nover
popd

variants="generic generic10"
for variant in $variants ; do
  rm -rf ${variant}
  cp -pr %{bname} ${variant}
done


%build
pushd generic
%{x_configure}\
	--host=%{_target_platform} \
	--libdir=%{_libdir}

%{__make} %{?_smp_mflags}
popd

%if 0
pushd generic10
%{x_configure}\
	--host=%{_target_platform} \
	--libdir=%{_libdir}
	--bit-depth=10

sed -i -e "s/SONAME=libx264.so./SONAME=libx26410b.so./" config.mak

%{__make} %{?_smp_mflags}
popd
%endif


%install
pushd generic
%{__make} DESTDIR=%{buildroot} install
popd
%if 0
pushd generic10
SONAME=`grep "^SONAME=" config.mak`
export $SONAME
install -m 755 ${SONAME} %{buildroot}%{_libdir}
ln -fs ${SONAME} %{buildroot}%{_libdir}/libx26410b.so
popd
%endif

#Fix timestamp on x264 generated headers
# generic/version.h does not exist
#touch -r generic/version.h %{buildroot}%{_includedir}/x264.h %{buildroot}%{_includedir}/x264_config.h


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(644, root, root, 0755)
%doc generic/AUTHORS generic/COPYING
%attr(755,root,root) %{_bindir}/x264

%files libs
%defattr(644, root, root, 0755)
%{_libdir}/libx264.so.%{api}
#%{_libdir}/libx26410b.so.%{api}

%files devel
%defattr(644, root, root, 0755)
%doc generic/doc/*
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/libx264.so
%{_libdir}/pkgconfig/%{name}.pc
#%{_libdir}/libx26410b.so

%changelog
* Fri Sep 26 2014 Lars Kiesow <lkiesow@uos.de> - 0.%{api}-5%{?gver}
- Removed GPAC dependency. We don't need mp4 support for the x264 binary.

* Fri Apr 25 2014 Lars Kiesow <lkiesow@uos.de> - 0.138-3.20131030-c628e3b
- Fixed problem with yasm

* Tue Nov 05 2013 Sérgio Basto <sergio@serjux.com> - 0.138-2.20131030-c628e3b
- Unbootstrap.

* Sat Nov 02 2013 Sérgio Basto <sergio@serjux.com> - 0.138-1.20131030-c628e3b
- Update to 0.138 git c628e3b (stable branch) and bootstrap for new ffmpeg.

* Fri Oct 18 2013 Sérgio Basto <sergio@serjux.com> - 0.136-1.20131005git3361d59
- Update to 0.136 git 3361d59 (stable branch).

* Mon Sep 30 2013 Sérgio Basto <sergio@serjux.com> - 0.133-3.20130709git585324f
- Fix gpac detection.

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.133-2.20130709git585324f
- Rebuilt for FFmpeg 2.0.x

* Tue Jul 09 2013 Sérgio Basto <sergio@serjux.com> - 0.133-1.20130709git585324f
- Update to git 585324fee380109acd9986388f857f413a60b896 (HEAD of stable branch).

* Sat May 25 2013 Sérgio Basto <sergio@serjux.com> - 0.130-3.20130502git1db4621
- Build without bootstrap for F19.

* Fri May 24 2013 Sérgio Basto <sergio@serjux.com> - 0.130-2.20130502git1db4621
- Build with bootstrap for F19.

* Thu May 02 2013 Sérgio Basto <sergio@serjux.com> - 0.130-1.20130502git1db4621
- Update to git 1db4621

* Tue Mar 05 2013 Sérgio Basto <sergio@serjux.com> - 0.129-3.20130305gite403db4
- Update to git e403db4f9079811f5a1f9a1339e7c85b41800ca7

* Sun Jan 20 2013 Sérgio Basto <sergio@serjux.com> - 0.129-2.20130119git9c4ba4b
- Rebuild for ffmpeg-1.1.1 .

* Sat Jan 19 2013 Sérgio Basto <sergio@serjux.com> - 0.129-1.20130119git9c4ba4b
- Update to 9c4ba4bde8965571159eae2d79f85cabbb47416c, soname bump.
- Changed branch name by api number, is more readable.
- Drop upstreamed patch.

* Fri Nov 23 2012 Sérgio Basto <sergio@serjux.com> - 0.128-2.20121118gitf6a8615
- unbootstrap on F18.

* Mon Nov 19 2012 Sérgio Basto <sergio@serjux.com> - 0.128-1.20121118gitf6a8615
- Update to f6a8615ab0c922ac2cb5c82c9824f6f4742b1725.

* Sat Oct 06 2012 Sérgio Basto <sergio@serjux.com> - 0.125-4.20121006git68dfb7b
- Note: no source update.
- Just add git tag to package name, for faster check upstream.
- Add git tag in x264-snapshot.sh .
- Convert all defines in global. 

* Sun Sep 09 2012 Sérgio Basto <sergio@serjux.com> - 0.125-4.20120909
- unbootstrap on F18.

* Sun Sep 09 2012 Sérgio Basto <sergio@serjux.com> - 0.125-3.20120909
- update x264-0.125 from r2201 to r2209.

* Thu Sep 06 2012 Sérgio Basto <sergio@serjux.com> - 0.125-2.20120904
- unbootstrap

* Tue Sep 04 2012 Sérgio Basto <sergio@serjux.com> - 0.125-1.20120904
- Pulled latest stable patches, which bump version to 0.125.

* Mon Jun 25 2012 Sérgio Basto <sergio@serjux.com> - 0.124-5.20120616
- Fixed detection of gf_malloc and gf_free

* Sun Jun 24 2012 Sérgio Basto <sergio@serjux.com> - 0.124-4.20120616
- unbootstrap.

* Sat Jun 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.124-3.20120616
- Rework alternatives build
- Fix SONAME for x26410b

* Sun Jun 17 2012 Sérgio Basto <sergio@serjux.com> - 0.124-2.20120616
- use _libdir to fix build on x86_64.

* Sun Jun 17 2012 Sérgio Basto <sergio@serjux.com> - 0.124-1.20120616
- Update to 20120616
- Add one build with --bit-depth=10
- Enabled bootstrap, after rebuild ffmpeg, we rebuild x264 without bootstrap.

* Tue May 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.120-5.20120303
- Forward rhel patch
- Disable ASM on armv5tel armv6l
- Add --with bootstrap conditional
- Use %%{_isa} for devel requires

* Tue Mar 6 2012 Sérgio Basto <sergio@serjux.com> - 0.120-2.20120303
- Enable libavformat , after compile ffmeg with 0.120-1

* Sat Mar 3 2012 Sérgio Basto <sergio@serjux.com> - 0.120-1.20120303
- Change release number, upstream have release numbers at least on stable branch and as ffmpeg
  reported.
- Update to 20120303
- Update x264-nover.patch, as suggest by Joseph D. Wagner <joe@josephdwagner.info> 
- Dropped obsolete Buildroot and Clean.
- add BuildRequires: zlib-devel to enable gpac.

* Wed Feb 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.34.20120125
- Rebuilt for F-17 inter branch

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.33.20120125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.32.20120125
- Update to 20120125

* Mon Aug 22 2011 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.31.20110811
- 20110811 snapshot (ABI 116)
- fix snapshot script to include version.h properly
- link x264 binary to the shared library

* Thu Jul 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-0.30.20110714
- Update to 20110714 stable branch (ABI 115)
- Convert x264-snapshot to git (based on ffmpeg script).
- New Build Conditionals --with ffmpegsource libavformat
- Remove shared and strip patches - undeeded anymore
- Remove uneeded convertion of AUTHORS

* Mon Jan 10 2011 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.29.20110227
- 20110227 snapshot (ABI bump)

* Tue Jul 06 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.28.20100706gitd058f37
- 20100706 snapshot (ABI bump)
- drop old Obsoletes:

* Thu Apr 29 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.27.20100429gitd9db8b3
- 20100429 snapshot
- s/%%{ix86}/i686 (rfbz #1075)
- ship more docs in -devel

* Sat Jan 16 2010 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.26.20100116git3d0f110
- 20100116 snapshot (SO version bump)
- don't remove config.h and don't re-run version.sh
- link x264 binary to the shared library
- really don't strip if debug is enabled

* Mon Oct 26 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.26.20091026gitec46ace7
- 20091026 snapshot

* Thu Oct 15 2009 kwizart <kwizart at gmail.com > -  0.0.0-0.25.20091007git496d79d
- Update to 20091007git
- Move simd to %%{_libdir}/sse2

* Thu Mar 26 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.24.20090319gitc109c8
- 20090319 snapshot
- build with static gpac
- fix build on ppc

* Tue Feb 10 2009 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.23.20090119git451ba8d
- 20090119 snapshot
- fix BRs for build-time options

* Sat Dec 20 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.22.20081213git9089d21
- rebuild against new gpac

* Sat Dec 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.21.20081213git9089d21
- fix the libs split on x86

* Sat Dec 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.20.20081213git9089d21
- 20081213 snapshot
- drop the libs split on x86, it doesn't work right for P3/AthlonXP
- drop obsolete patch

* Thu Dec 04 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.19.20081202git71d34b4.1
- fix compilation on ppc

* Tue Dec 02 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.19.20081202git71d34b4
- 20081202 snapshot
- bring back asm optimized/unoptimized libs split
- rebase and improve patch
- GUI dropped upstream
- dropped redundant BRs

* Mon Nov 17 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.18.20080905
- partially revert latest changes (the separate sse2 libs part) until selinux
  policy catches up

* Fri Nov 07 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.17.20080905
- build libs without asm optimizations for less capable x86 CPUs (livna bug #2066)
- fix missing 0 in Obsoletes version (never caused any problems)

* Fri Sep 05 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.16.20080905
- 20080905 snapshot
- use yasm on all supported arches
- include mp4 output support via gpac by default
- drop/move obsolete fixups from %%prep
- fix icon filename in desktop file

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.0.0-0.15.20080613
- rebuild

* Sat Jun 14 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.14.20080613
- 20080613 snapshot (.so >= 59 is required by current mencoder)

* Mon May 05 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.13.20080420
- 20080420 snapshot
- split libs into a separate package
- svn -> git
- drop obsolete execstack patch
- fixed summaries and descriptions

* Wed Feb 27 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.12.20080227
- 20080227 snapshot
- fix build with gpac

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.0.0-0.11.20070819
- Merge freshrpms spec into livna spec for rpmfusion:
- Change version from 0 to 0.0.0 so that it is equal to the freshrpms versions,
  otherwise we would be older according to rpm version compare.
- Add Provides and Obsoletes x264-gtk to x264-gui for upgrade path from
  freshrpms
- Fix icon cache update scripts

* Sun Sep 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0-0.10.20070819
- Fix use of execstack on i386, closes livna bug #1659

* Sun Aug 19 2007 Dominik Mierzejewski <rpm@greysector.net> 0-0.9.20070819
- 20070819 snapshot, closes bug #1560

* Thu Nov 09 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.8.20061028
- use PIC on all platforms, fixes bug #1243

* Sun Oct 29 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.7.20061028
- fix desktop entry categories for devel

* Sun Oct 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.6.20061028
- fix BRs
- handle menu icon properly

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.5.20061028
- fix bad patch chunk
- fix 32bit build on x86_64

* Sat Oct 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.4.20061028
- Don't let ./configure to guess arch, pass it ourselves.
- Drop X-Livna desktop entry category.

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.3.20061028
- added GUI (based on kwizart's idea)
- latest snapshot
- added some docs to -devel

* Sun Oct 01 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.2.20061001
- add snapshot generator script
- fix make install
- make nasm/yasm BRs arch-dependent
- configure is not autoconf-based, call it directly

* Sat Sep 30 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.569
- Updated to latest SVN trunk
- specfile cleanups

* Mon Sep 04 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.558
- Updated to latest SVN trunk
- FE compliance

* Sun Mar 12 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.467
- Updated to latest SVN trunk
- Build shared library
- mp4 output requires gpac

* Mon Jan 02 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.394
- Updated to latest SVN trunk
- Change versioning scheme

* Sun Nov 27 2005 Dominik Mierzejewski <rpm@greysector.net> 0.0.375-1
- Updated to latest SVN trunk
- Added pkgconfig file to -devel

* Tue Oct  4 2005 Matthias Saou <http://freshrpms.net/> 0.0.315-1
- Update to svn 315.
- Disable vizualize since otherwise programs trying to link without -lX11 will
  fail (cinelerra in this particular case).

* Mon Aug 15 2005 Matthias Saou <http://freshrpms.net/> 0.0.285-1
- Update to svn 285.
- Add yasm build requirement (needed on x86_64).
- Replace X11 lib with lib/lib64 to fix x86_64 build.

* Tue Aug  2 2005 Matthias Saou <http://freshrpms.net/> 0.0.281-1
- Update to svn 281.

* Mon Jul 11 2005 Matthias Saou <http://freshrpms.net/> 0.0.273-1
- Initial RPM release.
