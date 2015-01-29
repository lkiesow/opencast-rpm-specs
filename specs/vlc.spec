# source: http://dl.atrpms.net/all/vlc.spec
%bcond_without full
%bcond_without xcb
%bcond_without v4l2
%bcond_with ggi
%bcond_with buggyglibc
%bcond_with ultimate
%bcond_with opencv
%bcond_with glide
%bcond_without directfb

%define opencv_ver %(rpm -q --qf %{VERSION} opencv-devel)

Name:    vlc
Version: 2.1.5
Release: 14%{?dist}
Summary: A free and cross-platform media player
Group:   Applications/Multimedia
License: GPLv2
URL:     http://www.videolan.org/
Source0: http://downloads.videolan.org/pub/videolan/%{name}/%{version}/%{name}-%{version}.tar.xz
Patch0:  vlc-2.1.0-fix_font_path.patch
Patch1:  vlc-2.0.0-pulse_default.patch
Patch4:  vlc-2.1.0-gtk.patch
Patch5:  vlc-2.1.0-lirc.patch
Patch6:  vlc-1.1.8-bugfix.opencv22.patch
Patch7:  vlc-2.0.4-bi_rgb.patch

BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: gettext-devel, libtool
BuildRequires: chrpath
BuildRequires: libdvbpsi-devel
BuildRequires: avahi-devel
BuildRequires: alsa-lib-devel
BuildRequires: cdparanoia-devel
%{?with_full:BuildRequires: fluidsynth-devel}
BuildRequires: desktop-file-utils
BuildRequires: dbus-devel
BuildRequires: gcc-c++
%{?with_full:BuildRequires: gnome-libs-devel}
BuildRequires: gnutls-devel
BuildRequires: gtk+-devel
BuildRequires: gsm-devel
BuildRequires: kdelibs-devel
BuildRequires: lame-devel
BuildRequires: libsysfs-devel
BuildRequires: libdvdcss-devel >= 1.2.8
# BuildRequires: libdvdplay-devel >= 1.0.1
%{?with_full:BuildRequires: libcddb-devel}
BuildRequires: libgcrypt-devel, libjpeg-devel
BuildRequires: libpng-devel
%{?with_full:BuildRequires: libtar-devel}
BuildRequires: libtiff-devel
%{?with_full:BuildRequires: libupnp-devel}
BuildRequires: libxml2-devel
BuildRequires: libXt-devel
BuildRequires: libXv-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXpm-devel
BuildRequires: libXvMC-devel
%{?with_xcb:BuildRequires: xcb-util-devel}
BuildRequires: lua-devel >= 5.1
BuildRequires: mesa-libGL-devel, mesa-libGLU-devel
%{?with_opencv:BuildRequires: opencv-devel}
BuildRequires: pkgconfig
BuildRequires: qt4-devel >= 4.6.0, taglib-devel
%{?with_full:BuildRequires: schroedinger-devel}
BuildRequires: xvidcore-devel >= 0.9.2
BuildRequires: zlib-devel
BuildRequires: a52dec-devel
BuildRequires: aalib-devel
BuildRequires: arts-devel
BuildRequires: dirac-devel
BuildRequires: esound-devel
BuildRequires: faac-devel
BuildRequires: faad2-devel
BuildRequires: ffmpeg-devel >= 0.4.9
BuildRequires: flac-devel >= 1.1.0
BuildRequires: fribidi-devel
BuildRequires: gnome-vfs2-devel
BuildRequires: jack-audio-connection-kit-devel
%{?with_full:BuildRequires: libcaca-devel}
BuildRequires: libavc1394-devel
# needs version 1.2.2
#BuildRequires: %{_includedir}/libdc1394/dc1394_control.h
BuildRequires: libdca-devel
BuildRequires: libcdio-devel
#BuildRequires: %{_includedir}/libsmbclient.h
BuildRequires: libsmbclient-devel
BuildRequires: libssh2-devel
BuildRequires: libdvdread-devel >= 0.9.4
BuildRequires: libdvdnav-devel >= 0.1.10
BuildRequires: libid3tag-devel
BuildRequires: libgoom2-devel
BuildRequires: libprojectM-devel
%{?with_full:BuildRequires: libkate-devel}
%{?with_full:BuildRequires: libtiger-devel}
BuildRequires: libmad-devel >= 0.15.0b
BuildRequires: libmatroska-devel >= 0.8.0
%{?with_full:BuildRequires: libmodplug-devel}
BuildRequires: musepack-tools-devel
BuildRequires: libogg-devel
%{?with_full:BuildRequires: pulseaudio-libs-devel >= 0.9.8}
%{?with_full:BuildRequires: libopendaap-devel}
BuildRequires: librsvg2-devel
%{?with_full:BuildRequires: libshout-devel}
BuildRequires: libtheora-devel
%{?with_full:BuildRequires: libudev-devel >= 142}
BuildRequires: libvorbis-devel
BuildRequires: lirc-devel
BuildRequires: live-devel
BuildRequires: mpeg2dec-devel >= 0.3.2
BuildRequires: ncurses-devel >= 5
%{?with_full:BuildRequires: openslp-devel}
BuildRequires: SDL-devel
%{?with_full:BuildRequires: SDL_image-devel}
BuildRequires: speex-devel >= 1.0.3
BuildRequires: svgalib-devel
BuildRequires: twolame-devel
BuildRequires: vcdimager-devel
BuildRequires: portaudio-devel
BuildRequires: nas-devel
BuildRequires: x264-devel
BuildRequires: xosd-devel >= 2.2.5
BuildRequires: libdv-devel >= 0.99
%{?with_glide:BuildRequires: Glide3-devel}
BuildRequires: pth-devel
BuildRequires: libquicktime-devel

%{?with_full:BuildRequires: libmtp-devel}
%{?with_full:BuildRequires: minizip-devel}
%{?with_full:BuildRequires: libproxy-devel}
BuildRequires: libnotify-devel
BuildRequires: live-devel
%{?with_v4l2:BuildRequires: libv4l-devel}
BuildRequires: zvbi-devel
%{?with_full:BuildRequires: libass-devel}
BuildRequires: pcre-devel
%{?with_directfb:BuildRequires: directfb-devel}
BuildRequires: libsamplerate-devel
BuildRequires: libbluray-devel >= 0.2.1
BuildRequires: libva-devel

# vlc 1.1.0 needs xdg-screensaver
Requires: xdg-utils
## default subtitle font
Requires: bitstream-vera-serif-fonts

Obsoletes: videolan-client < %{version}-%{release}
Provides:  videolan-client = %{version}-%{release}
Provides:  vlc-core%{_isa} = %{version}-%{release}
Obsoletes: vlc-plugin < %{version}-%{release}

%description
VLC media player is a highly portable multimedia player for various
audio and video formats (MPEG-1, MPEG-2, MPEG-4, DivX, mp3, ogg, ...)
as well as DVDs, VCDs, and various streaming protocols.
It can also be used as a server to stream in unicast or multicast in
IPv4 or IPv6 on a high-bandwidth network. 
It doesn't need any external codec or program to work.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This package contains development files for %{name}.

%prep
%setup -q
%patch0 -p1 -b .fix_font_path
%patch1 -p1 -b .pulse_default
%patch4 -p1 -b .gtk
%patch5 -p1 -b .lirc

%if %{with opencv}
%if "%{opencv_ver}" >= "2.2"
%patch6 -p1 -b .opencv22
%endif
%endif
%patch7 -p0 -b .bi_rgb

perl -pi -e's,#include <stream_,#include <FLAC/stream_,' modules/codec/flac.c

# Convert to utf8
for i in doc/fortunes.txt ChangeLog; do
        iconv -f iso-8859-1 -t utf-8 < "$i" > "${i}_"
        touch -r "$i" "${i}_"
        mv "${i}_" "$i"
done

%build
./bootstrap

%configure \
	--disable-dependency-tracking \
	--disable-rpath \
	--with-binary-version=%{version}-%{release} \
	--with-pic \
	%{?with_buggyglibc:--disable-nls} \
	\
	--with-tuning=no \
	--enable-run-as-root \
	--enable-growl \
	\
	--enable-live555 \
	%{?with_opencv:--enable-opencv} \
	--enable-sftp \
	%{!?with_v4l2:--disable-v4l2 --disable-libv4l2} \
	--enable-pvr \
	--enable-vcdx \
	\
	--enable-wma-fixed \
	--enable-shine \
	--enable-omxil \
	--enable-switcher \
	--enable-faad \
	--enable-real \
	--enable-realrtsp \
	--enable-tremor \
	\
	%{!?with_xcb:--disable-xcb} \
	%{?with_directfb:--enable-directfb} \
	%{?with_ggi:--enable-ggi} \
	--enable-aa \
	\
	--enable-ncurses \
	--enable-xosd \
	--enable-fbosd \
	--enable-lirc \
	\
	--enable-update-check \
%ifarch %{ix86}
	--enable-loader \
%endif

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# So that the icon gets themable (still required in 0.8.6)
%{__mkdir_p} %{buildroot}%{_datadir}/pixmaps
%{__cp} -ap %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/vlc.png \
            %{buildroot}%{_datadir}/pixmaps/vlc.png

# remove .la files
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%if %{with buggyglibc}
touch %{name}.lang
%else
%find_lang %{name}
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
%{_libdir}/vlc/vlc-cache-gen %{_libdir}/vlc/plugins/

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root,-)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%doc doc/fortunes.txt doc/intf-vcd.txt
%doc doc/bugreport-howto.txt
%exclude %{_datadir}/doc/vlc/*
%{_bindir}/*vlc
%{_bindir}/vlc-wrapper
%{_libdir}/vlc
%{_libdir}/libvlc.so.*
%{_libdir}/libvlccore.so.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/vlc.png
%{_datadir}/vlc
%{_datadir}/icons/hicolor/*/apps/vlc*.png
%{_datadir}/icons/hicolor/*/apps/vlc*.xpm
%{_datadir}/kde4/apps/solid/actions/vlc-*.desktop
%{_mandir}/man1/vlc*.1*

%files devel
%defattr(-, root, root,-)
%{_includedir}/vlc
%{_libdir}/libvlc.so
%{_libdir}/libvlccore.so
%{_libdir}/pkgconfig/*

%changelog
* Mon Apr 14 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.4-13
- Update to 2.1.4.

* Sun Mar  9 2014 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.3-12
- Update to 2.1.3.

* Sun Nov 17 2013 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.1-11
- Update to 2.1.1.

* Sat Oct 05 2013 Paulo Roma <roma@lcg.ufrj.br> - 2.1.0-10
- Update to 2.1.0.
- Adapted fix_font_path.patch, lirc.patch and gtk.patch for version 2.1.0
- No more .hosts file.

* Wed Aug 14 2013 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.0.8-9
- Update to 2.0.8.

* Mon Jun 17 2013 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.0.7-8
- Update to 2.0.7.

* Sun Apr 28 2013 Paulo Roma <roma@lcg.ufrj.br> - 2.0.6-6
- Updated to 2.0.6

* Sat Dec 22 2012 Paulo Roma <roma@lcg.ufrj.br> - 2.0.5-5
- Updated to 2.0.5

* Fri Oct 26 2012 Paulo Roma <roma@lcg.ufrj.br> - 2.0.4-5
- Applied vlc-2.0.4-bi_rgb.patch for 32 bits.

* Sun Oct 21 2012 Paulo Roma <roma@lcg.ufrj.br> - 2.0.4-4
- Update to 2.0.4

* Sun Aug 19 2012 Paulo Roma <roma@lcg.ufrj.br> - 2.0.3-4
- Update to 2.0.3

* Sun Jul 08 2012 Paulo Roma <roma@lcg.ufrj.br> - 2.0.2-3
- Update to 2.0.2
- Removed deprecated patch FF_API_OLD_FF_PICT_TYPES.
- Avoid overriding .hosts at each update.

* Mon Mar 19 2012 Paulo Roma <roma@lcg.ufrj.br> - 2.0.1-2
- Update to 2.0.1
- Providing vlc-core.

* Sun Feb 26 2012 Paulo Roma <roma@lcg.ufrj.br> - 2.0.0-1
- Update to 2.0.0
- Adapted spec file.
- No more mozilla plugin.
- Added BR libsamplerate-devel and libbluray-devel.

* Tue Jan  3 2012 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.13-74
- Update to 1.1.13.

* Wed Nov 02 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.1.12-73
- Update to 1.1.12.

* Thu Aug 11 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.11-72
- Update to 1.1.11.

* Wed Jun  8 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.10-70
- Update to 1.1.10.

* Sun Apr 17 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.1.9-69
- Update to 1.1.9.

* Fri Mar 25 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.1.8-68.1
- Update to 1.1.8.
- Removed libnotify-0.7.patch
- Applied opencv patch for F15.

* Tue Feb 22 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.1.7-67
- Rebuilt for new libva.

* Fri Feb 04 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.1.7-66
- Update to 1.1.7.

* Sun Jan 30 2011 Paulo Roma <roma@lcg.ufrj.br> - 1.1.6-65
- Update to 1.1.6.
- Applied lirc patch.

* Thu Nov 25 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.5-63
- Update to 1.1.5.

* Fri Aug 27 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.4-59
- Update to 1.1.4.

* Tue Aug 17 2010 Paulo Roma <roma@lcg.ufrj.br> - 1.1.2-58
- Updated to 1.1.2.

* Wed Jul 28 2010 Paulo Roma <roma@lcg.ufrj.br> - 1.1.1-57
- Updated to 1.1.1
- Added BR libva-devel

* Fri Jun 25 2010 Paulo Roma <roma@lcg.ufrj.br> - 1.1.0-54
- Removed deprecated options from configure.
- Enabled sftp and omxil.
- Disabled --enable-omapfb because it is not compiling anymore.

* Thu Jun 24 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1.0-53
- Update to 1.1.0.

* Thu May 27 2010 Paulo Roma <roma@lcg.ufrj.br> - 1.0.6-52
- Applied xulrunner patch for F13.

* Tue May 04 2010 Paulo Roma <roma@lcg.ufrj.br> - 1.0.6-51
- Update to 1.0.6.

* Mon Feb 01 2010 Paulo Roma <roma@lcg.ufrj.br> - 1.0.5-50
- Update to 1.0.5.

* Mon Dec 28 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.4-49
- Update to 1.0.4.

* Sun Nov 01 2009 Paulo Roma <roma@lcg.ufrj.br> - 1.0.3-48
- Update to 1.0.3.

* Sat Sep 26 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.2-45
- Update to 1.0.2.

* Thu Aug 13 2009 Paulo Roma <roma@lcg.ufrj.br> - 1.0.1-44
- Include patch magic for RHEL5.

* Thu Aug 04 2009 Paulo Roma <roma@lcg.ufrj.br> - 1.0.1-43
- Updated to 1.0.1
- Activating libcdio by default.

* Wed Jul 15 2009 Axel Thimm <Axel.Thimm@jATrpms.net> - 1.0.0-42
- Reorder and simplify the bcond conditionals introdusing some more
  build dependencies.

* Wed Jul 08 2009 Paulo Roma<roma@lcg.ufrj.br> - 1.0.0-40
- Update to 1.0.0.
- Removed obsolete patch vlc-xul191.patch
- Converted ChangeLog to utf8.
- Removed some obsolete configure options. 
- Added some new options for building on RHEL5.
  bsrpm vlc.spec --without compat_wxwindows --without opencv 
                 --without mkv --without daap --without schroedinger 
                 --without fluidsynth --without gnome-libs --without mozilla
                 --without v4l2 --without modplug --without shout --without nls

* Sat Jun  6 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.0-38_rc3
- Update to 1.0.0-rc3.

* Wed May 20 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0.0-36_rc1
- Update to 1.0.0-rc1.

* Wed Apr 08 2009 Paulo Roma <roma@lcg.ufrj.br> 0.9.9a-35
- Updated to 0.9.9a
- Added BR dirac-devel.

* Sun Dec 14 2008 Paulo Roma <roma@lcg.ufrj.br> 0.9.8a-34
- Updated to 0.9.8a

* Sat Nov 08 2008 Paulo Roma <roma@lcg.ufrj.br> 0.9.6-33
- Updated to 0.9.6
- Included man pages.
- Removed ffmpeg/postproc hack in vlc-config.
- Added BR schroedinger-devel and libkate-devel.
- Disabled rpath.

* Sat Nov 01 2008 Paulo Roma <roma@lcg.ufrj.br> 0.9.5-32
- Updated to 0.9.5

* Thu Oct 09 2008 Paulo Roma <roma@lcg.ufrj.br> 0.9.4-32
- Updated to 0.9.4
- enabled xvmc and added BR libXvMC-devel.
- Replaced libsmbclient.devel for %%{_includedir}/libsmbclient.h

* Sun Sep 27 2008 Paulo Roma <roma@lcg.ufrj.br> 0.9.3-31
- Updated to 0.9.3
- dc1394 needs 1.2.2 version.

* Sun Sep 14 2008 Paulo Roma <roma@lcg.ufrj.br> 0.9.2-30
- Updated to 0.9.2
- Removed all old patches. Adapting font and pulse default.
- Fixing the default font.
- Added BR qt4-devel, opencv-devel, dbus-devel, fluidsynth-devel,
  lua-devel, taglib-devel
- Using kdelibs again.
- Enabled openvc, lua, and gnomevfs.
- Removed deprecated --with-wx-config and --with-ffmpeg-tree.
- Using external ffmpeg by default.

* Wed Jul 16 2008 Paulo Roma <roma@lcg.ufrj.br> 0.8.6i-29
- Updated to 0.8.6i
- BR ffmpeg-devel is no longer needed.
- Converted fortunes.txt to utf8.

* Fri Jun 06 2008 Paulo Roma <roma@lcg.ufrj.br> 0.8.6h-28
- Updated to 0.8.6h
- Removed patch1 (wx28.patch), patch3 (230_all_libcdio-0.78.2.patch)
  and patch8 (double free).

* Fri May 30 2008 Paulo Roma <roma@lcg.ufrj.br> 0.8.6g-27
- Using BR ffmpeg-devel according to embedded_ffmpeg.
- Unconditional BR lame-devel and alsa-lib-devel.
- Changed BR lirc-lib-devel for lirc-devel.
- Applied patch 8 (playlist double free).

* Thu May 22 2008 Paulo Roma <roma@lcg.ufrj.br> 0.8.6g-26
- Updated to 0.8.6g
- Removed BR qt-devel and changed kdelibs-devel for kdelibs3-devel.
- Added BR libXpm-devel.
- Changed descriptions.

* Wed Apr 16 2008 Paulo Roma <roma@lcg.ufrj.br> 0.8.6f-25
- Rebuilt for Fedora 9.
- Replaced BR firefox-devel for gecko-devel.
- Patched for using xulrunner in F9.
- Added BRs avahi-devel and cdparanoia-devel.

* Sat Apr 12 2008 Paulo Roma <roma@lcg.ufrj.br> 0.8.6f-24
- Added BR libdc1394-devel for using a shared ffmpeg
  (vlc compiles, but does not detect recent ffmpeg 
   versions at run time).
- Updated ffmpeg to 20071011.
- Conditionally enabled pulseaudio (does not sound good enough yet).
- Applied pulse patches.
- Using appropriate PIC options for each built package.

* Sat Apr 05 2008 Paulo Roma <roma@lcg.ufrj.br> 0.8.6f-23
- Updated to 0.8.6f
- Removed faad2 patch.
- Enabled --enable-snapshot and --enable-portaudio.

* Sat Mar 01 2008 Paulo Roma <roma@lcg.ufrj.br> 0.8.6e-22
- Updated to 0.8.6e and libdvbpsi5-0.1.6
- Added mesa BRs.

* Sun Dec 23 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6d-21
- Added X-libs BRs.

* Thu Nov 29 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6d-20
- Updated to 0.8.6d
- Applied dts to dca patch.
- BR gsm-devel.
- Replaced %%fedora >= 6 for appropriate bcond_without.

* Sat Nov 24 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6c-19
- Fixed BR lirc-lib-devel.
- Using portaudio-devel for Fedora 8.

* Thu Nov 22 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6c-18
- Conditional build without mozilla.
- Added cvs as a BR to avoid a bootstrap error.

* Sun Nov 11 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6c-17
- Patched for compiling with libcdio-0.78.2
- Changed license to GPLv2.
- Using compat-wxGTK26-devel for Fedora > 6.
  Otherwise, the volume control disappears.

* Fri Jul 06 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6c-16
- Updated to 0.8.6c
- Removed flac patch.

* Mon Jun 11 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6b-16
- Patched for flac support in F7.
- No more plugin hacks.
- Added BR automake17 and enabled svgalib.

* Fri Apr 27 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6b-15
- Updated to 0.8.6b
- Removed unecessary mozilla include hack.

* Sun Apr 01 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6a-14
- Passing -fPIC in CFLAGS before compiling libdvbpsi4 for x86_64
- Excluded static libraries

* Sun Mar 18 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6a-13
- Using embedded libdvbpsi

* Sun Mar 04 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6a-12
- Seamonkey 1.0.8 and firefox 1.5.0.10
- Enabled galaktos

* Tue Feb 22 2007 Paulo Roma <roma@lcg.ufrj.br> 0.8.6a-11
- Added vlc plugin package.

* Tue Feb 20 2007 Paulo Roma <roma@lcg.ufrj.br>
- Removed obsolete configure options.
- Added option for using embedded ffmpeg.

* Tue Jan 09 2007 Paulo Roma <roma@lcg.ufrj.br>
- Updated to 0.8.6a

* Sat Dec 29 2006 Paulo Roma <roma@lcg.ufrj.br>
- Updated ffmpeg to 0.7.20061215.fc6

* Sat Dec 16 2006 Paulo Roma <roma@lcg.ufrj.br>
- Updated to 0.8.6
- No more creating desktop file.
- Fixed dependencies.
- Rebuilt with faad2-2.5 installed.

* Mon Dec 11 2006 Paulo Roma <roma@lcg.ufrj.br>
- Rebuit for Fedora 6.

* Wed May 17 2006 Paulo Roma <roma@lcg.ufrj.br>
- Update to 0.8.5
- Optional build without jack

* Sun Dec 11 2005 Paulo Roma <roma@lcg.ufrj.br>
- Update to 0.8.4
- Optional build without hal
- Removed creation of /dev/dvd

* Thu Nov 25 2004 Jason Luka
- Update to 0.8.1
- Added livedotcom, faac, faad lines
- Removed xosd requirement
- Reworked the hack for mozilla 1.7.3 (Thanks Torsten)

* Sun Oct 10 2004 Jason Luka
- Update to 0.8.0-test2
- Inserted static ffmpeg routine
- Removed outdated kde, qt, gnome, and gtk+ interfaces
- Added livedotcom dependancy
- Openslp is broken, temporarily removed
- Added EXPORTs and bootstrap
- Removed ffmpeg dependancy as the static lib works better for now

* Sun Sep 19 2004 Jason Luka
- Update to 0.8.0-test1
- Added --enable-gpl
- Updated Mozilla version for FC2

* Fri Mar 19 2004 Jason Luka
- Removed dependancy on XFree86 as FC2 now calls the same package xorg

* Mon Mar 15 2004 Jason Luka
- Update to 0.7.1

* Tue Dec 2 2003 Jason Luka
- Added fribidi support
- Added fribidi and mkv options to configure

* Sat Nov 29 2003 Jason Luka
- Fixed Matroska/EBML problem
- Updated script for mozilla plugin installation

* Fri Nov 28 2003 Jason Luka
- Update to 0.7.0-test1
- Updated version numbers on dependancies
- Removed ALSA support until RH/FC turns to kernel 2.6
- Added --enable-speex and --enable-pp
- Mozilla plugin now built for 1.4.1
- Currently broken (Matroska/EBML problems)

* Mon Aug 25 2003 Jason Luka
- Added matroska support
- Corrected some symlinking problems with the mozilla plugin

* Fri Aug 22 2003 Jason Luka <jason@geshp.com>
- Update to 0.6.2
- Changed menu item name to VideoLAN Media Player
- Added openslp support
- Added libtar support (needed for skins)
- Added symlink to libxvidcore.so, thanks to new version of that software

* Fri Aug 1 2003 Jason Luka <jason@geshp.com>
- Update to 0.6.1
- Fixed file structure problems I created to accomodate the mozilla plugin
- Changed vendor name for desktop install
- Moved vlc to base menu
- Moved plugins from /usr/lib/mozilla to /usr/lib/mozilla-x.x.x
- Added custom patch to accomodate mozilla plugin
- Added execution of bootstrap since Makefile.am was altered

* Tue Jul 8 2003 Jason Luka <jason@geshp.com>
- Update to 0.6.0
- Add id3lib, dv, faad, qt, kde, and mozilla plugin support
- Added script to symlink mozilla-1.2.1 directories to mozilla so build can complete

* Sat Apr 5 2003 Jason Luka <jason@geshp.com>
- Rebuilt for Red Hat 9
- Changed dependencies for ffmpeg's new name
- Required lirc support at build-time 

* Sat Mar 25 2003 Jason Luka <jason@geshp.com>
- Fixed Buildrequire statements to require all plugins at compile-time
- Fixed Require statements so users don't have to install every plugin

* Thu Mar 23 2003 Jason Luka <jason@geshp.com>
- Renamed ffmpeg to libffmpeg
- Rebuilt for videolan site
- Autolinked /dev/dvd to /dev/cdrom

* Tue Mar 11 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.5.2.
- Fix the dv build dependency, thanks to Alan Hagge.
- Added flac support.
- Fixed the libdvbpsi requirements.

* Mon Feb 24 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt against the new xosd lib.

* Wed Feb 19 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.5.1.
- Major spec file update.

* Fri Nov 15 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.4.6.

* Tue Oct 22 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.4.5.
- Minor --with / --without adjustments.

* Sun Oct  6 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 8.0.
- New menu entry.
- Added all --without options and --with qt.

* Mon Aug 12 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.4.4.

* Fri Jul 26 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.4.3.

* Fri Jul 12 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.4.2.

* Wed Jun  5 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.4.1.

* Fri May 24 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.4.0.
- Disabled qt interface, it's hell to build with qt2/3!
- Use %%find_lang and %%{?_smp_mflags}.

* Fri Apr 19 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.3.1.

* Mon Apr  8 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.3.0.

* Sat Jan 12 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Removed the dependency on libdvdcss package, use the built in one instead,
  because 1.x.x is not as good as 0.0.3.ogle3.

* Tue Jan  1 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.2.92.
- Build fails with libdvdcss < 1.0.1.

* Tue Nov 13 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.2.91 and now requires libdvdcss 1.0.0.

* Mon Oct 22 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Split libdvdcss into a separate package since it's also needed by the
  xine menu plugin.

* Thu Oct 11 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Updated to 0.2.90.
- Removed ggi, svgalib and aalib since they aren't included in Red Hat 7.2.

* Mon Aug 27 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Updated to 0.2.83.

* Sat Aug 11 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Updated to 0.2.82.

* Mon Jul 30 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Updated to 0.2.81.
- Added all the new split libdvdcss.* files to the %%files section.

* Tue Jun  5 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Updated to the latest release, 0.2.80.

* Wed May 30 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Updated to today's CVS version, works great! :-)
- Fixed the desktop menu entry.

* Tue May 22 2001 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Spec file cleanup to make it look more like others do.
- Added the use of many macros.
- Disabled automatic requires and provides (the package always needed qt,
  gtk+, gnome etc. otherwise).
- Added a system desktop menu entry.

* Mon Apr 30 2001 Arnaud Gomes-do-Vale <arnaud@glou.org>
Added relocation support and compile fixes for Red Hat 7.x.

* Sat Apr 28 2001 Henri Fallon <henri@videolan.org>
New upstream release (0.2.73)

* Mon Apr 16 2001 Samuel Hocevar <sam@zoy.org>
New upstream release (0.2.72)

* Fri Apr 13 2001 Samuel Hocevar <sam@zoy.org>
New upstream release (0.2.71)

* Sun Apr 8 2001 Christophe Massiot <massiot@via.ecp.fr>
New upstream release (0.2.70)

* Fri Feb 16 2001 Samuel Hocevar <sam@via.ecp.fr>
New upstream release

* Tue Aug  8 2000 Samuel Hocevar <sam@via.ecp.fr>
Added framebuffer support

* Sun Jun 18 2000 Samuel Hocevar <sam@via.ecp.fr>
Took over the package

* Thu Jun 15 2000 Eric Doutreleau <Eric.Doutreleau@int-evry.fr>
Initial package
