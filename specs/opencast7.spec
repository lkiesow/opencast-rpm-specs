# vim: et:ts=3:sw=3:sts=3

%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%define __requires_exclude_from ^.*\\.jar$
%define __provides_exclude_from ^.*\\.jar$

%define srcversion 7.5
%define uid   opencast
%define gid   opencast
%define nuid  7967
%define ngid  7967

%if "%{?ocdist}" == ""
%define ocdist allinone
%endif

Name:          opencast7-%{ocdist}
Version:       %{srcversion}
Release:       1%{?dist}
Summary:       Open Source Lecture Capture & Video Management Tool

Group:         Applications/Multimedia
License:       ECL 2.0
URL:           http://opencast.org
Source0:       https://github.com/opencast/opencast/archive/%{srcversion}.tar.gz
Source1:       jetty.xml
Source2:       settings-online.xml
Source3:       opencast.logrotate
Source4:       org.apache.aries.transaction.cfg

BuildRequires: bzip2
BuildRequires: ffmpeg >= 3
BuildRequires: hunspell >= 1.2.8
BuildRequires: java-devel >= 1:1.8.0
BuildRequires: maven >= 3.1
BuildRequires: sed
BuildRequires: sox >= 14
BuildRequires: tar
BuildRequires: tesseract >= 3
BuildRequires: tesseract-langpack-deu >= 3
BuildRequires: xz
BuildRequires: gzip
BuildRequires: git

Requires: ffmpeg >= 3
Requires: hunspell >= 1.2.8
Requires: java >= 1:1.8.0
Requires: sox >= 14
Requires: tesseract >= 3

# For the start/stop scripts:
Requires: bash
Requires: nc
Requires: sed

%if "%{?ocdist}" == "allinone"
Requires: activemq-dist >= 5.14
%endif

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

Provides: opencast = %{version}

BuildArch: noarch



%description
Opencast is a free, open-source platform to support the management of
educational audio and video content. Institutions will use Opencast to
produce lecture recordings, manage existing video, serve designated
distribution channels, and provide user interfaces to engage students with
educational videos.


%prep
%setup -q -c -a 0


%build
# Maven configuration
cp %{SOURCE2} settings.xml
sed -i "s#BUILDPATH#$(pwd)#" settings.xml

# Build Opencast
cd opencast-*
mvn -s ../settings.xml clean install

# Prepare base distribution
cd build
find ./* -maxdepth 0 -type d -exec rm -rf '{}' \;
tar xf opencast-dist-%{ocdist}-*.tar.gz

# Fix newline character at end of configuration files
find opencast-dist-%{ocdist}/etc -name '*.xml' \
   -o -name '*.cfg' -exec sed -i -e '$a\' '{}' \;
# ' fix vim hl
sed -i -e '$a\' opencast-dist-%{ocdist}/etc/shell.init.script
# ' fix vim hl


%install
rm -rf %{buildroot}

# Create directories
mkdir -m 755 -p %{buildroot}%{_datadir}
mkdir -m 755 -p %{buildroot}%{_sharedstatedir}
mkdir -m 755 -p %{buildroot}%{_sysconfdir}
mkdir -m 755 -p %{buildroot}/srv/opencast
mkdir -m 755 -p %{buildroot}%{_localstatedir}/log/opencast

# Move files into the package filesystem
mv opencast-*/build/opencast-dist-%{ocdist} \
   %{buildroot}%{_datadir}/opencast
mv %{buildroot}%{_datadir}/opencast/etc \
   %{buildroot}%{_sysconfdir}/opencast
mv %{buildroot}%{_datadir}/opencast/bin/setenv \
   %{buildroot}%{_sysconfdir}/opencast/setenv
mv %{buildroot}%{_datadir}/opencast/data \
   %{buildroot}%{_sharedstatedir}/opencast

# Create instances dir. This is still hardcoded in Karaf
mkdir %{buildroot}%{_sharedstatedir}/opencast/instances

# Create some links to circumvent Karaf bugs
ln -s %{_sysconfdir}/opencast \
   %{buildroot}%{_datadir}/opencast/etc
ln -s %{_sysconfdir}/opencast/setenv \
   %{buildroot}%{_datadir}/opencast/bin/setenv
ln -s %{_sharedstatedir}/opencast \
   %{buildroot}%{_datadir}/opencast/data
ln -s %{_sharedstatedir}/opencast/instances \
   %{buildroot}%{_datadir}/opencast/instances

# Add custom jetty.xml
# Otherwise Karaf will attempt to do that and fail to start
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/opencast/jetty.xml

# Install logrotate configuration
install -p -D -m 0644 %{SOURCE3} \
   %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install workaround dummy file in /etc
install -p -D -m 0644 %{SOURCE4} \
   %{buildroot}%{_sysconfdir}/opencast

# Install Systemd unit file
install -p -D -m 0644 \
   %{buildroot}%{_datadir}/opencast/docs/scripts/service/opencast.service \
   %{buildroot}%{_unitdir}/opencast.service

# Patch up some directories

# Systemd unit file (path to binary)
sed -i 's#/opt/#/usr/share/#' %{buildroot}%{_unitdir}/opencast.service

# Binary file configuration
echo "export KARAF_DATA=%{_sharedstatedir}/opencast" >> \
   %{buildroot}%{_sysconfdir}/opencast/setenv
echo "export KARAF_ETC=%{_sysconfdir}/opencast" >> \
   %{buildroot}%{_sysconfdir}/opencast/setenv

# Patch log file locations
sed -i 's#fileName *= *${karaf.data}/log#fileName = %{_localstatedir}/log/opencast#' \
   %{buildroot}%{_sysconfdir}/opencast/org.ops4j.pax.logging.cfg

# Patch storage dir
sed -i 's#^\(org.opencastproject.storage.dir\)=.*$#\1=/srv/opencast#' \
   %{buildroot}%{_sysconfdir}/opencast/custom.properties



%clean
rm -rf ${buildroot}



%pre
# Create user and group if nonexistent
# Try using a common numeric uid/gid if possible
if [ ! $(getent group %{gid}) ]; then
   if [ ! $(getent group %{ngid}) ]; then
      groupadd -r -g %{ngid} %{gid} > /dev/null 2>&1 || :
   else
      groupadd -r %{gid} > /dev/null 2>&1 || :
   fi
fi
if [ ! $(getent passwd %{uid}) ]; then
   if [ ! $(getent passwd %{nuid}) ]; then
      useradd -M -r -u %{nuid} -d /srv/opencast -g %{gid} %{uid} > /dev/null 2>&1 || :
   else
      useradd -M -r -d /srv/opencast -g %{gid} %{uid} > /dev/null 2>&1 || :
   fi
fi


%post
%systemd_post opencast.service


%preun
%systemd_preun opencast.service


%postun
%systemd_postun_with_restart opencast.service


%files
%config(noreplace) %{_sysconfdir}/opencast/
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/opencast.service
%{_datadir}/opencast
%attr(755,%{uid},%{gid}) %{_datadir}/opencast/bin/*
%attr(755,%{uid},%{gid}) %dir /srv/opencast
%attr(755,%{uid},%{gid}) %dir %{_localstatedir}/log/opencast
%attr(755,%{uid},%{gid}) %{_sharedstatedir}/opencast


%changelog
* Tue Dec 10 2019 Lars Kiesow <lkiesow@uos.de> 7.5-1
- Update to 7.5

* Mon Oct 07 2019 Lars Kiesow <lkiesow@uos.de> 7.4-1
- Update to 7.4

* Mon Sep 23 2019 Lars Kiesow <lkiesow@uos.de> 7.3-1
- Update to 7.3

* Fri Aug 02 2019 Lars Kiesow <lkiesow@uos.de> 7.2-1
- Update to Opencast 7.2

* Wed Apr 03 2019 Lars Kiesow <lkiesow@uos.de> 6.4-1
- Update to Opencast 6.4

* Tue Mar 05 2019 Lars Kiesow <lkiesow@uos.de> 6.3-1
- Update to Opencast 6.3

* Mon Dec 10 2018 Lars Kiesow <lkiesow@uos.de> 6.x-1
- Update to Opencast 6.0

* Wed Oct 17 2018 Lars Kiesow <lkiesow@uos.de> 0.6.0-0.1
- test Update to Opencast 6 (pre-release)

* Mon Sep 03 2018 Lars Kiesow <lkiesow@uos.de> 5.1-1
- Update to Opencast 5.1

* Sun Jun 03 2018 Lars Kiesow <lkiesow@uos.de> 4.4-1
- Update to Opencast 4.4

* Wed Mar 28 2018 Lars Kiesow <lkiesow@uos.de> 4.3-1
- Update to Opencast 4.3

* Wed Mar 14 2018 Lars Kiesow <lkiesow@uos.de> 4.2-1
- Update to Opencast 4.2

* Wed Feb 07 2018 Lars Kiesow <lkiesow@uos.de> 4.1-1
- Update to Opencast 4.1
- Migration to Github

* Mon Dec 18 2017 Lars Kiesow <lkiesow@uos.de> 4.0-1
- Update to Opencast 4.0

* Mon Dec 18 2017 Lars Kiesow <lkiesow@uos.de> 3.4-1
- Update to Opencast 3.4

* Fri Sep 08 2017 Lars Kiesow <lkiesow@uos.de> 3.2-2
- Fixed broken allinone build

* Mon Aug 21 2017 Lars Kiesow <lkiesow@uos.de> 3.2-1
- Update to Opencast 3.2

* Mon Jun 26 2017 Lars Kiesow <lkiesow@uos.de> 3.0-1
- Update to Opencast 3.0

* Wed May 24 2017 Lars Kiesow <lkiesow@uos.de> 2.3.3-1
- Update to Opencast 2.3.3

* Mon Apr 03 2017 Lars Kiesow <lkiesow@uos.de> 2.3.2-2
- Fixed Systemd unit restart after upgrade

* Thu Mar 23 2017 Lars Kiesow <lkiesow@uos.de> 2.3.2-1
- Update to Opencast 2.3.2

* Wed Jan 25 2017 Lars Kiesow <lkiesow@uos.de> - 2.3.1-1
- Update to Opencast 2.3.1

* Mon Dec 19 2016 Lars Kiesow <lkiesow@uos.de> - 2.3.0-1
- Update to Opencast 2.3.0

* Tue Dec 06 2016 Lars Kiesow <lkiesow@uos.de> - 2.2.4-1
- Update to Opencast 2.2.4

* Thu Oct 13 2016 Lars Kiesow <lkiesow@uos.de> - 2.2.3-1
- Update to Opencast 2.2.3

* Tue Sep 13 2016 Lars Kiesow <lkiesow@uos.de> - 2.2.2-1
- Update to Opencast 2.2.2

* Fri Jul 29 2016 Lars Kiesow <lkiesow@uos.de> - 2.2.1-1
- Update to Opencast 2.2.1

* Thu Jul 07 2016 Lars Kiesow <lkiesow@uos.de> - 2.2.0-1
- Update to Opencast 2.2.0

* Mon Jun 20 2016 Lars Kiesow <lkiesow@uos.de> - 2.1.2-1
- Update to Opencast 2.1.2

* Sun Jan 24 2016 Lars Kiesow <lkiesow@uos.de> - 2.1.1-1
- Update to Opencast 2.1.1

* Tue Jan 19 2016 Lars Kiesow <lkiesow@uos.de> - 2.1.1-0.rc1
- Update to Opencast 2.1.1-rc1
- Fix sed commands
- Fix required FFmpeg version

* Wed Jan  6 2016 Lars Kiesow <lkiesow@uos.de> - 2.1.0-0
- Opencast 2.1.0

* Tue Sep 15 2015 Lars Kiesow <lkiesow@uos.de> - 2.0.1-4
- Fix systemd unit file

* Fri Sep  4 2015 Lars Kiesow <lkiesow@uos.de> - 2.0.1-3
- Fix problem with SysV-init scripts

* Thu Sep  3 2015 Lars Kiesow <lkiesow@uos.de> - 2.0.1-2
- Update to Opencast 2.0.1

* Thu Aug 13 2015 Lars Kiesow <lkiesow@uos.de> - 2.0.0-2
- Fixed pre-uninstall scripts

* Tue Aug  4 2015 Lars Kiesow <lkiesow@uos.de> - 2.0.0-1
- Update to Opencast 2.0.0

* Fri Jun 19 2015 Lars Kiesow <lkiesow@uos.de> - 2.0.0-0.1.rc1
- Rename to Opencast
- Update to 2.0.0-rc1

* Sun Apr 26 2015 Lars Kiesow <lkiesow@uos.de> - 2-0.4.beta2
- Update to Matterhorn 2.0.0-beta2

* Mon Apr 20 2015 Lars Kiesow <lkiesow@uos.de> - 2-0.3.beta1
- Fixed test module dependencies

* Tue Apr 14 2015 Lars Kiesow <lkiesow@uos.de> - 2-0.2.beta1
- Fixed comflict in admin-profile (caption-remote)

* Mon Apr 13 2015 Lars Kiesow <lkiesow@uos.de> - 2-0.1.beta1
- Update to Matterhorn 2.0.0-beta1

* Fri Mar  6 2015 Lars Kiesow <lkiesow@uos.de> - 1.6.1-1
- Update to Matterhorn 1.6.1

* Tue Feb 24 2015 Lars Kiesow <lkiesow@uos.de> - 1.6.1-0.2.RC1
- Fixed Systemd/Init installation macros

* Tue Feb 24 2015 Lars Kiesow <lkiesow@uos.de> - 1.6.1-0.1.RC1
- Update to Matterhorn 1.6.1-RC1

* Mon Dec 15 2014 Lars Kiesow <lkiesow@uos.de> - 1.6.0-1
- Update to Matterhorn 1.6.0

* Mon Dec  8 2014 Lars Kiesow <lkiesow@uos.de> - 1.6.0-0.5.RC1
- Update to Matterhorn 1.6.0-RC1
- Proper systemd integration

* Sun Nov  9 2014 Lars Kiesow <lkiesow@uos.de> - 1.6.0-0.4.beta4
- Update to Matterhorn 1.6.0-beta4
- Disabled test profiles

* Tue Oct 28 2014 Lars Kiesow <lkiesow@uos.de> - 1.6.0-0.3.beta3
- Update to 1.6.0-beta3
- Switched to tar.xz package for sources

* Thu Oct  2 2014 Lars Kiesow <lkiesow@uos.de> - 1.6.0-0.1.beta1
- First beta build for Matterhorn 1.6.0

* Sat Sep 27 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.9.rc7
- Update to Matterhorn 1.5.0-rc7
- Added demo distribution
- Fixed GStreamer dependency

* Mon Aug 18 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.8.rc5
- Fixed inspection service dependency

* Thu Aug 14 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.7.rc5
- Fixed some smaller spec issues

* Thu Aug  7 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.6.rc5
- Update to Matterhorn 1.5.0-rc5
-

* Wed Jul 16 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.5.rc4
- Update to Matterhorn 1.5.0-rc4

* Sat May 17 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.4.rc3
- Update to 1.5.0-rc3

* Wed Apr 30 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.3.rc2
- Unmark SysV-init script as configuration
- Renamed logrotate configuration
- Fixed mediainfo version

* Sat Apr 12 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.2.rc2
- Fixed issue with non linked configuration dir

* Fri Apr 11 2014 Lars Kiesow <lkiesow@uos.de> - 1.5.0-0.1.rc2
- First build of Opencast Matterhorn 1.5.0-rc2

* Wed Apr  9 2014 Lars Kiesow <lkiesow@uos.de> - 1.4.3-4
- Merged SLES, Fedora and RHEL specs

* Wed Feb 12 2014 Per Pascal Grube <pascal.grube@tik.uni-stuttgart.de> - 1.4.3-3
- Merge changes to compile on SLES 11SP3

* Wed Feb  5 2014 Lars Kiesow <lkiesow@uos.de> - 1.4.3-2
- Fixed problem with inspection-service packets

* Tue Feb  4 2014 Lars Kiesow <lkiesow@uos.de> - 1.4.3-1
- Update to 1.4.3
- Included backport of inspection-service-ffmpeg

* Wed Jan 29 2014 Per Pascal Grube <pascal.grube@rus.uni-stuttgart.de - 1.4.2-0.rc2.1
- Updated SPEC to build on SLES 11-SP3

* Sat Jan 25 2014 Lars Kiesow <lkiesow@uos.de> - 1.4.2-0.rc2
- Update to 1.4.2-rc2

* Sun Jan 19 2014 Lars Kiesow <lkiesow@uos.de> - 1.4.2-0.rc1
- Update to 1.4.2-rc1

* Sun Nov 24 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-1
- Update to 1.4.1

* Wed Nov 13 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.11.rc7
- Update to 1.4.1-rc7

* Mon Nov 11 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.10.rc6
- Update to 1.4.1-rc6

* Sun Oct 13 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.9.rc5
- Fixed build issue

* Sat Oct 12 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.8.rc5
- Update to 1.4.1-rc5

* Mon Sep 23 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.7.rc4
- Update to 1.4.1-rc4

* Fri Sep 20 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.6.rc3
- Some minor fixes for Fedora

* Wed Sep 18 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.5.rc3
- Update to 1.4.1-rc3

* Thu Sep  5 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.4.rc2
- Fixed some distributions (standalone vs. shared storage distributions)

* Tue Aug 27 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.3.rc2
- Enabled missing modules

* Fri Aug 16 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.2.rc2
- Update to MH 1.4.1-rc2
- Allowed users in the group matterhoprn to put files into inbox

* Sat Aug  3 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.1.rc1
- Update to MH 1.4.1-rc1
- Moved dependencies to modules

* Sat Jul 13 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-31
- Added manpage
- Fixed logrotate configuration (log4j)
- Fixed encoding profile for OCR

* Tue Jun  4 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-30
- Update to 1.4.0 final release

* Fri May 24 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-29.rc10
- Fixed samples and some dirs

* Thu May 23 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-28.rc10
- Update to 1.4-rc10

* Tue May 14 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-27.rc9
- Fixed issue with useradd

* Tue May 14 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-26.rc9
- Update to Matterhorn 1.4.0-rc9

* Mon Apr 29 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-25.rc8
- Fixed groupdel for post uninstall of base

* Sat Apr 20 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-24.rc8
- Fix for renaming of ...-distribution-service-youtube

* Fri Apr 19 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-23.rc7
- Update to 1.4.0-rc8
- Inclusion of new startup scripts

* Sun Apr  7 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.0-22.rc7
- Fixed executable path in configuration

* Fri Apr  5 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-21-rc7
- Updated workflowoperationhandler-mediapackagepost to git.4361b7b69d

* Tue Apr  2 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-20-rc7
- Another fix for workflowoperationhandler-mediapackagepost

* Tue Apr  2 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-19-rc7
- Fixed SysVInit script

* Tue Apr  2 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-18-rc7
- New start and sysvinit scripts
- Fix for workflowoperationhandler-mediapackagepost

* Thu Mar 28 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-17-rc7
- Added custom module "workflowoperation-mediapackagepost"

* Thu Mar 14 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-16-rc7
- Added documentation (licenses, ddl scripts, etc.)

* Wed Mar 13 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-15.rc7
- Update from 1.4-rc6 to 1.4-rc7

* Mon Mar 11 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-14
- Fixed bug in files section for base package (modules were assigned to base)

* Mon Mar 11 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-13
- Fixed unowned directory issue
- Removed Windows scripts

* Mon Mar 11 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-12
- Fixed configuration files (noreplace)

* Sun Mar 10 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-11
- Moved Gstreamer CA dependencies to module

* Sun Mar 10 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-10
- Fixed dependency issue for Capture-Agent

* Fri Mar  8 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-9
- Added distribution descriptions.

* Thu Feb 21 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-8
- Really fixed useradd command
- Fixed some SysV-Init script related stuff

* Thu Feb 21 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-7
- Fixed useradd command

* Tue Feb 19 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-6
- Marked some module conflicts inside of Matterhorn

* Thu Feb 14 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-5
- Fixed build dependency issue of capture agent
- Added more distribution packages
- Fixed pre/post/postun tags for base

* Thu Feb 14 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-4
- Fixed dependency issue of capture agent

* Tue Feb 12 2013 Lars Kiesow <lkiesow@uos.de> - 1.4-3
- Fixed required dependency version and missing distribution-default package

* Fri Feb  8 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-2
- Modifications for el6

* Thu Jan 31 2013 Christian Greweling <cgreweling@uos.de> - 1.4-1
- Created SPEC for 1.4 (Based on SPEC for 1.3.1)
