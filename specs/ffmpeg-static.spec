%define debug_package %{nil}

Name:          ffmpeg
Summary:       Hyper fast MPEG1/MPEG4/H263/RV and AC3/MPEG audio encoder
Version:       4.0
Release:       1%{?dist}
License:       GPLv3+
Group:         System Environment/Libraries

Source:        https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
URL:           http://ffmpeg.org
BuildRoot:     %{_tmppath}/%{name}-root


%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.


%prep
%setup -q -n %{name}-%{version}-64bit-static


%build


%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_bindir}
install -p ffmpeg %{buildroot}%{_bindir}
install -p ffprobe %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc GPLv3.txt
%{_bindir}/*


%changelog
* Tue Apr 24 2018 Lars Kiesow <lkiesow@uos.de> 4.0-1
- Update to FFmpeg 4.0

* Tue Dec 19 2017 Lars Kiesow <lkiesow@uos.de> 3.4-1
- Update to FFmpeg 3.4.1

* Tue Oct 17 2017 Lars Kiesow <lkiesow@uos.de> 3.4-1
- Update to FFmpeg 3.4

* Mon Sep 18 2017 Lars Kiesow <lkiesow@uos.de> 3.3.4-1
- Update to FFmpeg 3.3.4

* Mon Jun 12 2017 Lars Kiesow <lkiesow@uos.de> 3.3.2-1
- Update to FFmpeg 3.3.2

* Thu Jun 01 2017 Lars Kiesow <lkiesow@uos.de> 3.3.1-1
- Update to FFmpeg 3.3.1

* Wed Feb 15 2017 Lars Kiesow <lkiesow@uos.de> - 3.2.4-1
- Update to FFmpeg 3.2.4

* Thu Dec 08 2016 Lars Kiesow <lkiesow@uos.de> - 3.2-1
- Update to FFmpeg 3.2.2

* Wed Nov 23 2016 Lars Kiesow <lkiesow@uos.de> - 3.2-1
- Update to FFmpeg 3.2

* Thu Oct 13 2016 Lars Kiesow <lkiesow@uos.de> - 3.1.4-1
- Update to FFmpeg 3.1.4

* Mon Sep 05 2016 Lars Kiesow <lkiesow@uos.de> - 3.1.3-1
- Update to FFmpeg 3.1.3

* Wed Aug 17 2016 Lars Kiesow <lkiesow@uos.de> - 3.1.2-2
- Fixed requirements

* Mon Jul 25 2016 Lars Kiesow <lkiesow@uos.de> - 3.1.2-1
- Static build of FFmpeg
- Update to FFmpeg 3.1.2

* Wed Jul 13 2016 Lars Kiesow <lkiesow@uos.de> - 3.1.1-1
- Dependency cleanup
- Update to FFmpeg 3.1.1

* Tue May 03 2016 Lars Kiesow <lkiesow@uos.de> - 3.0.2-1
- Update to FFmpeg 3.0.2

* Sun Jan 24 2016 Lars Kiesow <lkiesow@uos.de> - 2.8.5-1
- Update to FFmpeg 2.8.5

* Fri Jan  8 2016 Lars Kiesow <lkiesow@uos.de> - 2.8.4-1
- Update to FFmpeg 2.8.4

* Sun Nov  1 2015 Lars Kiesow <lkiesow@uos.de> - 2.8.1-1
- Update to FFmpeg 2.8.1

* Wed Sep 16 2015 Lars Kiesow <lkiesow@uos.de> - 2.8-1
- Update to FFmpeg 2.8

* Tue Aug 11 2015 Lars Kiesow <lkiesow@uos.de> - 2.7.2-1
- Update to FFmpeg 2.7.2

* Mon Jun 15 2015 Lars Kiesow <lkiesow@uos.de> - 2.7-1
- Update to FFmpeg 2.7

* Sun Apr  5 2015 Lars Kiesow <lkiesow@uos.de> - 2.6.1-1
- Update to FFmpeg 2.6.1

* Mon Mar  9 2015 Lars Kiesow <lkiesow@uos.de> - 2.6-1
- Update to FFmpeg 2.6

* Mon Feb 23 2015 Lars Kiesow <lkiesow@uos.de> - 2.5.4-1
- Update to FFmpeg 2.5.4

* Wed Jan  7 2015 Lars Kiesow <lkiesow@uos.de> - 2.5.2-1
- Update to FFmpeg 2.5.2

* Tue Dec  9 2014 Lars Kiesow <lkiesow@uos.de> - 2.5-1
- Update to FFmpeg 2.5

* Mon Nov 10 2014 Lars Kiesow <lkiesow@uos.de> - 2.4.3-1
- Update to FFmpeg 2.4.3

* Wed Oct  8 2014 Lars Kiesow <lkiesow@uos.de> - 2.4.2-1
- Update to FFmpeg 2.4.2
- Some condition clean-up

* Fri Sep 26 2014 Lars Kiesow <lkiesow@uos.de> - 2.4.1-1
- Update to FFmpeg 2.4.1
- Removed frei0r dependency for RHEL 6.x
- Removed librtmp dependency for RHEL 6.x

* Mon Aug  4 2014 Lars Kiesow <lkiesow@uos.de> - 2.3.1-1
- Update to FFmpeg 2.3.1

* Wed Jul 16 2014 Lars Kiesow <lkiesow@uos.de> - 2.3-1
- Update to FFmpeg 2.3

* Sat Jun 28 2014 Lars Kiesow <lkiesow@uos.de> - 2.2.4-1
- Update to FFmpeg 2.2.4

* Mon May  5 2014 Lars Kiesow <lkiesow@uos.de> - 2.2.2-1
- Update to FFmpeg 2.2.2

* Sat Apr 12 2014 Lars Kiesow <lkiesow@uos.de> - 2.2.1-1
- Update to FFmpeg 2.2.1

* Fri Feb 28 2014 Lars Kiesow <lkiesow@uos.de> - 2.1.4-2
- Fixed libvpx dependency

* Fri Feb 28 2014 Lars Kiesow <lkiesow@uos.de> - 2.1.4-1
- Update to FFmpeg 2.1.4

* Sun Jan 19 2014 Lars Kiesow <lkiesow@uos.de> - 2.1.3-1
- Update to FFmpeg 2.1.3

* Wed Jan 15 2014 Lars Kiesow <lkiesow@uos.de> - 2.1.2-1
- Update to FFmpeg 2.1.2

* Thu Nov 21 2013 Lars Kiesow <lkiesow@uos.de> - 2.1.1-1
- Update to FFmpeg 2.1.1

* Thu Oct 31 2013 Lars Kiesow <lkiesow@uos.de> - 2.1-1
- Update to FFmpeg 2.1

* Sat Oct 12 2013 Lars Kiesow <lkiesow@uos.de> - 2.0.2-1
- Update to FFmpeg 2.0.2

* Tue Sep 24 2013 Lars Kiesow <lkiesow@uos.de> - 2.0.1-1
- Update to FFmpeg 2.0.1

* Sat Jul 13 2013 Lars Kiesow <lkiesow@uos.de> - 2.0-1
- Update to version 2.0

* Sun May 19 2013 Lars Kiesow <lkiesow@uos.de> - 1.2.1-1
- Update to version 1.2.1

* Mon Apr 29 2013 Lars Kiesow <lkiesow@uos.de> - 1.1.4-3
- Update to version 1.1.4
- Enabled fdk-aacenc

* Sun Apr 28 2013 Lars Kiesow <lkiesow@uos.de> - 1.1.1-2
- Enabled more build opetion
- Updated libvpx

* Mon Jan 28 2013 Lars Kiesow <lkiesow@uos.de> - 1.1.1-1
- Update to ffmpeg 1.1.1

* Thu Aug 23 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-59
- Fixed dependency and added libvorbis on el5

* Fri Aug 17 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-58
- Port to RHEL 5.x (with schroedinger, speex and theora disabled)

* Tue Mar  6 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-57
- Added requirements for manpages

* Tue Mar  6 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-56
- Fixed some packaging issues.

* Thu Feb 16 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-55
- Enabled libvo-aacenc AAC encoder
- Added missing build dependency for librtmp-devel

* Thu Feb 16 2012 Lars Kiesow <lkiesow@uos.de> - 0.10-54
- Fixed issues with CentOS
- Build devel and libs package

* Fri Feb 10 2012 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.10-53
- Update to 0.10.

* Tue Jan  3 2012 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.9-52
- Update to 0.9.

* Tue Jan  3 2012 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8.9-51
- Update to 0.8.9.

* Sat Nov 26 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8.7-50
- Update to 0.8.7.

* Sat Nov 12 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8.6-49
- Update to 0.8.6.

* Fri Sep 23 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8.4-48
- Update to 0.8.4.

* Mon Jul 25 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.8-47
- Update to 0.8.

* Mon Jul 25 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.1-46
- Update to 0.7.1.

* Thu Jun  2 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.3-43
- Update to 0.6.3.

* Fri Mar 25 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.1-42_git20110322
- Update to latest git master.

* Mon Mar 14 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.1-39_git20110314
- Update to latest git master.

* Sat Jan 15 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.1-38_git20110115
- Update to latest git master.

* Sun Oct 24 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6-37_git20101024
- Update to latest git master.

* Thu Jul 22 2010 Paulo Roma <roma@lcg.ufrj.br> - 0.6-35
- Added BR libva-devel.

* Tue Jul 20 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6-34
- Update to 0.6.

* Sun Apr  4 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.5-32_git20100404
- Update to latest git.

* Fri Nov 20 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.5-31_git20091120
- Update to latest git.

* Sun Jan 18 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-29_r16671
- Update to latest svn version.

* Sun Nov 16 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-28_r15845
- ffmpeg-libs from a 3rd party repo generates conflicts.

* Sun Nov  9 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-27_r15797
- Update to latest svn version.

* Mon Feb 18 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-26_r12135
- Update to latest svn version.

* Sat Jan 12 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-25_r11517
- Update to latest svn version.
- libdca nd libogg are not (directly) needed anymore.

* Sat Oct 27 2007 Paulo Roma <roma@lcg.ufrj.br> - 0.4.9-24_r8743
- Compiling with --enable-liba52 for vob->avi using AC3.
- Added --enable-libaad.
- Added libnut-devel as a conditional BuildRequires.
- Using libdc1394-1.2.2, because version 2 does not work.

* Mon Apr 23 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-23_r8743
- Add some more dependencies (#1172).

* Sun Apr 22 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-21_r8743
- Add some dependencies on the devel package (#1172).

* Sun Apr 15 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-20_r8742
- Update to latest svn version.

* Wed Jan  3 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9_19_r7407
- Update to latest svn version.

* Fri Oct 27 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-18_r6524
- Add faac support.

* Mon Oct  2 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-17_r6524
- Update to latest svn version.
- Fix revision in release tag.

* Wed Sep  6 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.4.9-15_r19707
- Update to latest svn version.

* Wed Mar  1 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs20060301.
- Fix bug #752.

* Mon Feb 27 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Move compatibility provides to devel package (bug #750).

* Wed Feb 15 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs20060215.

* Sun Jun 12 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs20050612.

* Tue May 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs 20050517.

* Mon Apr 18 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to cvs 20050418.

* Tue Nov 23 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.9-pre1.

* Thu Oct 16 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.8.

* Tue Jul  1 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to a CVS snapshot as videolan-client 0.6.0 needs it.
- Enable faad, imlib2 and SDL support.
- Disable mmx until it doesn't make the build fail anymore :-/

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.
- Hardcode provides in order to get it right :-/
