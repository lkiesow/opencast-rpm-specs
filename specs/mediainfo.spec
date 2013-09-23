Name:          mediainfo
Version:       0.7.35
Release:       3%{?dist}
Summary:       Supplies technical and tag information about a video or audio file
Group:         Applications/Multimedia
License:       LGPLv3
URL:           http://mediainfo.sourceforge.net/
Source0:       http://downloads.sourceforge.net/project/%{name}/binary/%{name}/%{version}/MediaInfo_CLI_%{version}_GNU_FromSource.tar.bz2

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: dos2unix
BuildRequires: gcc-c++
BuildRequires: pkgconfig
BuildRequires: zlib-devel

#%global _enable_debug_package 0
#%global debug_package %{nil}
#%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

%description
MediaInfo CLI (Command Line Interface).

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


%prep
%setup -q -n MediaInfo_CLI_GNU_FromSource
pushd MediaInfo
	dos2unix     *.html *.txt Release/*.txt
	%__chmod 644 *.html *.txt Release/*.txt
popd


%build
# build ZenLib
pushd ZenLib/Project/GNU/Library
   ./configure --enable-static
	sed -i '1i#include <stddef.h>' ../../../Source/ZenLib/Thread.h
   %__make
popd
# build LIB
pushd MediaInfoLib/Project/GNU/Library/
   ./configure --enable-static
   %__make
popd
# build CLI
pushd MediaInfo/Project/GNU/CLI/
   ./configure --enable-staticlibs
   %__make
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd MediaInfo/Project/GNU/CLI/
	install -p -D -m 0755 mediainfo $RPM_BUILD_ROOT%{_bindir}/mediainfo
popd


%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "" ] && %__rm -rf "%{buildroot}"

%files
%defattr(-,root,root,-)
%doc MediaInfo/Release/ReadMe_CLI_Linux.txt
%doc MediaInfo/License.html MediaInfo/History_CLI.txt
%{_bindir}/mediainfo

%changelog
* Wed Sep 18 2013 Lars Kiesow <lkiesow@uos.de> - 0.7.35-3
- Fix for system libzen

* Thu Aug 16 2012 <lkiesow@uos.de> - 0.7.35-2
- CentOS 5 compatibility fixes

* Thu Feb 02 2012 <lkiesow@uos.de> - 0.7.35-1%{?dist}
- Removed RPM warnings
- Downgraded to v0.7.35

* Tue Jan 01 2009 MediaArea.net <info@mediaarea.net> - 0.7.39-0
- See History.txt for more info and real dates
- Previous packages made by Toni Graffy <toni@links2linux.de>
