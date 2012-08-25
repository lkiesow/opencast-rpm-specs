Name:          libmediainfo0
Version:       0.7.35
Release:       2%{?dist}
Summary:       Supplies technical and tag information about a video or audio file
Group:         System Environment/Libraries
License:       LGPLv3
URL:           http://mediainfo.sourceforge.net/
Source0:       %{name}-%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: dos2unix
BuildRequires: gcc-c++
BuildRequires: libzen0-devel >= 0.4.19
BuildRequires: pkgconfig
BuildRequires: zlib-devel
BuildRequires: doxygen
Requires:      libzen0 >= 0.4.19

%if 0%{?rhel} < 6
BuildRequires: curl-devel
%else
BuildRequires: libcurl-devel
%endif


%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%description
MediaInfo supplies technical and tag information about a video or
audio file.

What information can I get from MediaInfo?
* General: title, author, director, album, track number, date, duration...
* Video: codec, aspect, fps, bitrate...
* Audio: codec, sample rate, channels, language, bitrate...
* Text: language of subtitle
* Chapters: number of chapters, list of chapters

DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1,
MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime,
RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2, MSMPEG4v3,
VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

What format (container) does MediaInfo support?
* Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1,
  MPEG-2, MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP,
  H.264, AVC...)
* Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
* Subtitles: SRT, SSA, ASS, SAMI

This package contains the shared library for MediaInfo.

%package -n libmediainfo0-devel
Summary:    Include files and mandatory libraries for development
Group:      Development/Libraries
Requires:   libmediainfo0 = %{version}
Requires:   libzen0-devel >= 0.4.19

%description -n libmediainfo0-devel
Include files and mandatory libraries for development.

%prep
%setup -q -n libmediainfo0-%{version}
cp           Release/ReadMe_DLL_Linux.txt ReadMe.txt
mv           History_DLL.txt History.txt
dos2unix     *.txt *.html
%__chmod 644 *.txt *.html

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CPPFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

pushd Project/GNU/Library
   %configure --enable-shared --with-libcurl

   %__make clean
   %__make %{?jobs:-j%{jobs}}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd Project/GNU/Library/
   %__make install-strip DESTDIR=%{buildroot}
popd

# MediaInfoDLL headers and MediaInfo-config
%__install -dm 755 %{buildroot}%{_includedir}/MediaInfo
%__install -m 644 Source/MediaInfo/MediaInfo.h %{buildroot}%{_includedir}/MediaInfo
%__install -m 644 Source/MediaInfo/MediaInfoList.h %{buildroot}%{_includedir}/MediaInfo
%__install -m 644 Source/MediaInfo/MediaInfo_Const.h %{buildroot}%{_includedir}/MediaInfo
%__install -m 644 Source/MediaInfo/MediaInfo_Events.h %{buildroot}%{_includedir}/MediaInfo
%__install -dm 755 %{buildroot}%{_includedir}/MediaInfoDLL
%__install -m 644 Source/MediaInfoDLL/MediaInfoDLL.h %{buildroot}%{_includedir}/MediaInfoDLL
%__install -m 644 Source/MediaInfoDLL/MediaInfoDLL_Static.h %{buildroot}%{_includedir}/MediaInfoDLL

%__sed -i -e 's|Version: |Version: %{version}|g' \
   Project/GNU/Library/libmediainfo.pc
%__install -dm 755 %{buildroot}%{_libdir}/pkgconfig
%__install -m 644 Project/GNU/Library/libmediainfo.pc \
   %{buildroot}%{_libdir}/pkgconfig
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "" ] && %__rm -rf "%{buildroot}"

%post -n libmediainfo0 -p /sbin/ldconfig

%postun -n libmediainfo0 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc History.txt License.html ReadMe.txt
%{_libdir}/libmediainfo.so.*

%files -n libmediainfo0-devel
%defattr(-,root,root,-)
%doc Changes.txt
%dir %{_includedir}/MediaInfo
%{_includedir}/MediaInfo/*
%dir %{_includedir}/MediaInfoDLL
%{_includedir}/MediaInfoDLL/*
%{_libdir}/libmediainfo.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Aug 16 2012 <lkiesow@uos.de> - 0.7.35-2
- CentOS 5 compatibility fixes

* Thu Feb 02 2012 <lkiesow@uos.de> - 0.7.35-1
- Removed RPM warnings
- Downgraded to v0.7.35

* Tue Jan 01 2009 MediaArea.net <info@mediaarea.net> - 0.7.43-0
- See History.txt for more info and real dates
- Previous packages made by Toni Graffy <toni@links2linux.de>
