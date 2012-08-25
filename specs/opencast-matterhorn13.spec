#%define _disable_jar_repacking 1
%define __os_install_post %{nil}

# TODO: Build a proper SPEC file:
#       https://fedoraproject.org/wiki/Packaging/Java

Name:           opencast-matterhorn13
Version:        1.3.1
Release:        6%{?dist}
Summary:        Open Source Lecture Capture & Video Management Tool

Group:          Applications/Multimedia
License:        ECL 2.0, APL2 and other
URL:            http://opencast.org/matterhorn/
Source0:        matterhorn-%{version}.tar.gz
Source1:        org.apache.felix.main.distribution-3.2.2.tar.gz
Source2:        matterhorn-bin.tar.gz
Source3:        maven-repo-mh131.tar.gz
Patch0:         matterhorn-config-%{version}.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
    
BuildRequires: maven >= 3
BuildRequires: java-devel >= 1:1.6.0
Requires(pre): /usr/sbin/useradd
Requires:      ffmpeg >= 0.9
Requires:      mediainfo = 0.7.35
Requires:      tesseract >= 3
Requires:      qt_sbtl_embedder >= 0.4
Requires:      bash
Requires:      java >= 1:1.6.0


%description
Matterhorn is a free, open-source platform to support the management of
educational audio and video content. Institutions will use Matterhorn to
produce lecture recordings, manage existing video, serve designated
distribution channels, and provide user interfaces to engage students with
educational videos.
This is the 1.3.x release of Matterhorn. The major releases of Matterhorn may
be incompatible and not suited for direct update. Thus other versions are
available as different packages. However, there is a metapackage
opencast-matterhorn available which keeps track of the newest version.

%prep
%setup -q -c -a 0 -a 1 -a 2 -a 3
pushd matterhorn-%{version}
%patch0 -p1
popd


%build
#mvn


%pre
# Create matterhorn user.
/usr/sbin/useradd -M -r -d /var/matterhorn \
   -c "Opencast Matterhorn" matterhorn > /dev/null 2>&1 || :

%post
# Set owner of matterhorn content dir
chown -R matterhorn:matterhorn /var/matterhorn
chown -R matterhorn:matterhorn /opt/matterhorn


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/matterhorn
cp -r felix-framework-3.2.2/* $RPM_BUILD_ROOT/opt/matterhorn/
cp -rf matterhorn-%{version}/docs/felix/* $RPM_BUILD_ROOT/opt/matterhorn/
cp -r mvn2 $RPM_BUILD_ROOT/opt/matterhorn/
echo '<?xml version="1.0" encoding="UTF-8"?>' > settings.xml
echo '<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"' >> settings.xml
echo 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' >> settings.xml
echo 'xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 ' \
   'http://maven.apache.org/xsd/settings-1.0.0.xsd">' >> settings.xml
echo "<localRepository>$RPM_BUILD_ROOT/opt/matterhorn/mvn2/repository</localRepository>" >> settings.xml
echo '<offline>true</offline>' >> settings.xml
echo '</settings>' >> settings.xml
pushd matterhorn-%{version}
   MAVEN_OPTS='-Xms256m -Xmx960m -XX:PermSize=64m -XX:MaxPermSize=256m' \
      mvn -o -s ../settings.xml clean install \
      -DdeployTo=$RPM_BUILD_ROOT/opt/matterhorn/matterhorn/
popd
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -m 0755 matterhorn $RPM_BUILD_ROOT/%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}/var/matterhorn
mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
ln -s /opt/matterhorn/bin/matterhorn_init_d.sh \
   ${RPM_BUILD_ROOT}%{_initrddir}/matterhorn


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
/var/matterhorn
/opt/matterhorn
%{_initrddir}/*


%changelog
* Sat Aug 25 2012 Lars Kiesow <lkiesow@uos.de> - 1.3.1-5
- Fixed Java dependency issue

* Fri Aug 24 2012 Lars Kiesow <lkiesow@uos.de> - 1.3.1-4
- Fixed issue in start_matterhorn.sh

* Fri Aug 24 2012 Lars Kiesow <lkiesow@uos.de> - 1.3.1-3
- Switched to major release packages

* Thu Aug 23 2012 Lars Kiesow <lkiesow@uos.de> - 1.3.1-2
- Applied proper patches
- Fixed start_matterhorn shell script

* Wed Aug 15 2012 Lars Kiesow <lkiesow@uos.de> - 1.3.1-1
- Updated to Matterhorn 1.3.1

* Thu Apr 12 2012 Lars Kiesow <lkiesow@uos.de> - 1.3-3
- Fixed dependencies (added java)

* Thu Mar  1 2012 Lars Kiesow <lkiesow@uos.de> - 1.3-2
- Fixed service script

* Thu Mar  1 2012 Lars Kiesow <lkiesow@uos.de> - 1.3-1
- Created package
