%define __os_install_post %{nil}

%global  matterhorn_user          matterhorn
%global  matterhorn_group         %{matterhorn_user}

%define __INTERNAL_VERSION 2.0.0-SNAPSHOT

%if 0%{?sles_version}
  %define __GST_SUFFIX -0_10
%else
  %define __GST_SUFFIX %{nil}
%endif

# Systemd or SysV-init
%if 0%{?fedora}%{?rhel} >= 7
	%define __use_systemd 1
%endif

%{?_matterhorn_institute: %define __MATTERHORN_INSTITUTE .%{?_matterhorn_institute} }


Name:           opencast-matterhorn20
Version:        2
Release:        0.prep1%{?__MATTERHORN_INSTITUTE}%{?dist}
Summary:        Open Source Lecture Capture & Video Management Tool

Group:          Applications/Multimedia
License:        ECL 2.0
URL:            http://opencast.org/matterhorn/
Source0:        https://github.com/lkiesow/opencast-matterhorn/archive/%{__INTERNAL_VERSION}.tar.gz
Source2:        maven-repo-matterhorn-%{__INTERNAL_VERSION}.tar.xz
Source3:        settings.xml
Source4:        matterhorn.logrotate
Patch0:         matterhorn-config-%{__INTERNAL_VERSION}.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Enable local builts to make themselves more important
%if 0%{?_matterhorn_importance}
Epoch:          %{?_matterhorn_importance}
%endif

# Get a shortcut for the version we are building
%define __FULL_VERSION %{?epoch}%{?epoch::}%{version}-%{release}

BuildRequires: maven >= 3.1
BuildRequires: tar

%if 0%{?sles_version}
BuildRequires: jdk >= 1:1.7.0
%else
%if 0%{?rhel} == 6
BuildRequires: java-1.7.0-openjdk-devel >= 1:1.7.0
%else
BuildRequires: java-devel >= 1:1.7.0
%endif
%endif
Requires:      %{name}-distribution-default = %{__FULL_VERSION}

BuildArch: noarch

%description
Matterhorn is a free, open-source platform to support the management of
educational audio and video content. Institutions will use Matterhorn to
produce lecture recordings, manage existing video, serve designated
distribution channels, and provide user interfaces to engage students with
educational videos.
This is the 1.4.0 release of Matterhorn. The major releases of Matterhorn may
be incompatible and not suited for direct update. Thus other versions are
available as different packages. However, there is a meta package
opencast-matterhorn available which keeps track of the newest version.


%files
%defattr(-,root,root,-)
# No files here


### BASE ####################################################################

%package base
Summary: Base package for Opencast Matterhorn
Group: Applications/Multimedia
Requires(pre): /usr/sbin/useradd

%{?__use_systemd:BuildRequires: systemd}
%{!?__use_systemd:
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
}

Requires:      bash
Requires:      sudo
%if 0%{?sles_version}
Requires: jdk >= 1:1.7.0
%else
Requires: java >= 1:1.7.0
%endif


%description base
Basic elements of each Opencast Matterhorn distribution.


%files base
%defattr(-,root,root,-)
%doc %{_datadir}/matterhorn/docs
%config(noreplace) %{_sysconfdir}/matterhorn/
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}-base
%{?__use_systemd:%{_unitdir}/*}
%{!?__use_systemd:%{_initrddir}/*}
%{_sbindir}/*
%dir %{_datadir}/matterhorn
%dir %{_datadir}/matterhorn/lib
%{_datadir}/matterhorn/lib/felix
%{_datadir}/matterhorn/bin
%dir /srv/matterhorn
%dir /srv/matterhorn/inbox
%dir %{_localstatedir}/log/matterhorn
%{_mandir}/man8/matterhorn.8.gz


%pre base
# Create matterhorn user.
getent group matterhorn > /dev/null || groupadd -r matterhorn
getent passwd matterhorn > /dev/null || \
   /usr/sbin/useradd -M -r -d /srv/matterhorn -g matterhorn \
   -c "Opencast Matterhorn" matterhorn > /dev/null 2>&1 || :

%post base
# Set owner of matterhorn content dir
chown -R matterhorn:matterhorn /srv/matterhorn
chown -R matterhorn:matterhorn %{_localstatedir}/log/matterhorn
# This adds the proper /etc/rc*.d links for the script
%{!?__use_systemd:/sbin/chkconfig --add matterhorn}

%preun base
# If this is really uninstall and not upgrade
if [ $1 -eq 0 ]; then
	%{?__use_systemd:systemctl stop matterhorn >/dev/null 2>&1}
	%{!?__use_systemd:
      /sbin/service matterhorn stop >/dev/null 2>&1
      /sbin/chkconfig --del matterhorn
	}
fi

%postun base
if [ "$1" -ge "1" ]; then
   %{?__use_systemd:systemctl try-restart matterhorn > /dev/null 2>&1 || :}
   %{!?__use_systemd:/sbin/service matterhorn condrestart > /dev/null 2>&1 || :}
fi


### THIRD-PARTY-TOOLS #######################################################

%package third-party-tools
Summary: All required third party tools for Matterhorn
Group: Applications/Multimedia
%if 0%{?sles_version}
BuildRequires: jdk >= 1:1.7.0
%else
BuildRequires: java >= 1:1.7.0
#Requires: java-devel >= 1:1.7.0
%endif
#Requires: maven >= 3
Requires: ffmpeg >= 1.1
Requires: qt_sbtl_embedder >= 0.4
Requires: tesseract >= 3
Requires: v4l-utils


%description third-party-tools
This package will pull in all required third party tools for the core
components of Opencast Matterhorn.


%files third-party-tools
%defattr(-,root,root,-)
# No files here


### DISTRIBUTIONS ###########################################################


%package distribution-default
Summary: Default Matterhorn distribution
Group: Applications/Multimedia
Requires: %{name}-profile-admin           = %{__FULL_VERSION}
Requires: %{name}-profile-dist            = %{__FULL_VERSION}
Requires: %{name}-profile-engage          = %{__FULL_VERSION}
Requires: %{name}-profile-worker          = %{__FULL_VERSION}
Requires: %{name}-profile-workspace       = %{__FULL_VERSION}
Requires: %{name}-profile-serviceregistry = %{__FULL_VERSION}
Requires: %{name}-profile-directory-db    = %{__FULL_VERSION}

%package distribution-admin
Summary: Admin Matterhorn distribution
Group: Applications/Multimedia
Requires: %{name}-profile-admin              = %{__FULL_VERSION}
Requires: %{name}-profile-workspace          = %{__FULL_VERSION}
Requires: %{name}-profile-dist-stub          = %{__FULL_VERSION}
Requires: %{name}-profile-engage-stub        = %{__FULL_VERSION}
Requires: %{name}-profile-worker-stub        = %{__FULL_VERSION}
Requires: %{name}-profile-serviceregistry    = %{__FULL_VERSION}

%package distribution-worker
Summary: Worker Matterhorn distribution
Group: Applications/Multimedia
Requires: %{name}-profile-serviceregistry   = %{__FULL_VERSION}
Requires: %{name}-profile-workspace         = %{__FULL_VERSION}
Requires: %{name}-profile-worker-standalone = %{__FULL_VERSION}

%package distribution-engage
Summary: Engage Matterhorn distribution
Group: Applications/Multimedia
Requires: %{name}-profile-engage-standalone = %{__FULL_VERSION}
Requires: %{name}-profile-serviceregistry   = %{__FULL_VERSION}
Requires: %{name}-profile-dist-standalone   = %{__FULL_VERSION}
Requires: %{name}-profile-workspace         = %{__FULL_VERSION}

%package distribution-admin-worker
Summary: Combined Admin/Worker Matterhorn distribution
Group: Applications/Multimedia
Requires: %{name}-profile-admin              = %{__FULL_VERSION}
Requires: %{name}-profile-workspace          = %{__FULL_VERSION}
Requires: %{name}-profile-dist-stub          = %{__FULL_VERSION}
Requires: %{name}-profile-engage-stub        = %{__FULL_VERSION}
Requires: %{name}-profile-worker             = %{__FULL_VERSION}
Requires: %{name}-profile-serviceregistry    = %{__FULL_VERSION}

%package distribution-devel
Summary: Matterhorn distribution for developers
Group: Applications/Multimedia
Requires: %{name}-base              = %{__FULL_VERSION}
Requires: %{name}-third-party-tools = %{__FULL_VERSION}


%description distribution-default
Default distribution of Opencast Matterhorn components.

This is the default package containing all three main profiles (Admin, Worker,
Engage). This installation is only recommended if you don't have many videos
that you want to ingest and you don't expect many viewers. This perfect for
first test and to get an impression of Matterhorn as it works out of the box
and does not need much configuration.


%description distribution-admin
Admin distribution of Opencast Matterhorn components.

On this server the Administrative services are hosted etc. You usually have at
least three servers on which you run Matterhorn if you select this package.


%description distribution-worker
Worker distribution of Opencast Matterhorn components.

This is the worker package that contains the modules that create the most CPU
load (encoding, OCR, etc). So it is recommended to deploy this on a more
powerful machine.


%description distribution-engage
Engage distribution of Opencast Matterhorn components.

This is the package for the Matterhorn Engage Modules which are the front-end
to the viewer of your videos. It is always highly recommended to keep these
separated from the rest of your system.


%description distribution-admin-worker
Combined Admin and Worker distribution of Opencast Matterhorn components.

This package is targeted at medium sized installations, where you want to
separate the "back-end" server that the admin accesses from the "front-end"
server that the viewers use.


%description distribution-devel
Distribution of Opencast Matterhorn components for developers.

This package will create the basic structure for an Opencast Matterhorn node
like the directries, the basic configuration, the SysV-init scripts and pull in
all required third party tools.


%files distribution-default
%defattr(-,root,root,-)
# No files here

%files distribution-admin
%defattr(-,root,root,-)
# No files here

%files distribution-worker
%defattr(-,root,root,-)

%files distribution-engage
%defattr(-,root,root,-)

%files distribution-admin-worker
%defattr(-,root,root,-)
# No files here

%files distribution-devel
%defattr(-,root,root,-)
# No files here


### PROFILES ############################################################


%package profile-admin
Summary: admin profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-admin-ui                                 = %{__FULL_VERSION}
Requires: %{name}-module-admin-ui-ng                              = %{__FULL_VERSION}
Requires: %{name}-module-archive-api                              = %{__FULL_VERSION}
Requires: %{name}-module-archive-base                             = %{__FULL_VERSION}
Requires: %{name}-module-archive-schema                           = %{__FULL_VERSION}
Requires: %{name}-module-archive-storage-fs                       = %{__FULL_VERSION}
Requires: %{name}-module-archive-workflowoperation                = %{__FULL_VERSION}
Requires: %{name}-module-authorization-manager                    = %{__FULL_VERSION}
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-caption-api                              = %{__FULL_VERSION}
Requires: %{name}-module-caption-remote                           = %{__FULL_VERSION}
Requires: %{name}-module-capture-admin-service-api                = %{__FULL_VERSION}
Requires: %{name}-module-capture-admin-service-impl               = %{__FULL_VERSION}
Requires: %{name}-module-capture-workflowoperation                = %{__FULL_VERSION}
Requires: %{name}-module-comments                                 = %{__FULL_VERSION}
Requires: %{name}-module-comments-workflowoperation               = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-composer-workflowoperation               = %{__FULL_VERSION}
Requires: %{name}-module-conductor                                = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-deprecated-workflowoperation             = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api                 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-workflowoperation           = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-fileupload                               = %{__FULL_VERSION}
Requires: %{name}-module-gstreamer-service-api                    = %{__FULL_VERSION}
Requires: %{name}-module-holdstate-workflowoperation              = %{__FULL_VERSION}
Requires: %{name}-module-incident-workflowoperation               = %{__FULL_VERSION}
Requires: %{name}-module-index-service                            = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-ingest-workflowoperation                 = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api                   = %{__FULL_VERSION}
Requires: %{name}-module-inspection-workflowoperation             = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-lti                                      = %{__FULL_VERSION}
Requires: %{name}-module-mediapackage-manipulator                 = %{__FULL_VERSION}
Requires: %{name}-module-mediapackage-ui                          = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-messages                                 = %{__FULL_VERSION}
Requires: %{name}-module-metadata                                 = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-notification-workflowoperation           = %{__FULL_VERSION}
Requires: %{name}-module-participation-api                        = %{__FULL_VERSION}
Requires: %{name}-module-presets                                  = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info-ui-ng                       = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api                            = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-impl                           = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-workflowoperation              = %{__FULL_VERSION}
Requires: %{name}-module-schema                                   = %{__FULL_VERSION}
Requires: %{name}-module-search                                   = %{__FULL_VERSION}
Requires: %{name}-module-search-api                               = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-search-workflowoperation                 = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-api                     = %{__FULL_VERSION}
Requires: %{name}-module-smil-api                                 = %{__FULL_VERSION}
Requires: %{name}-module-smil-impl                                = %{__FULL_VERSION}
Requires: %{name}-module-solr                                     = %{__FULL_VERSION}
Requires: %{name}-module-sox-api                                  = %{__FULL_VERSION}
Requires: %{name}-module-sox-workflowoperation                    = %{__FULL_VERSION}
Requires: %{name}-module-speech-recognition-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-speech-recognition-workflowoperation     = %{__FULL_VERSION}
Requires: %{name}-module-static                                   = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-api                         = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-workflowoperation           = %{__FULL_VERSION}
Requires: %{name}-module-themes                                   = %{__FULL_VERSION}
Requires: %{name}-module-themes-workflowoperation                 = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-api                          = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-workflowoperation            = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-api                       = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-workflowoperation         = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-impl                    = %{__FULL_VERSION}
Requires: %{name}-module-workflow-workflowoperation               = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api      = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-alternatives
Summary: alternatives profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-dictionary-hunspell                      = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-none                          = %{__FULL_VERSION}
Requires: %{name}-module-gstreamer-service-api                    = %{__FULL_VERSION}
Requires: %{name}-module-gstreamer-service-impl                   = %{__FULL_VERSION}
Requires: %{name}-module-gstreamer-service-remote                 = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-ffmpeg                    = %{__FULL_VERSION}

%package profile-directory-cas
Summary: directory-cas profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-security-cas                             = %{__FULL_VERSION}

%package profile-directory-db
Summary: directory-db profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-dataloader                               = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-directory-ldap
Summary: directory-ldap profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-security-ldap                            = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory-ldap                       = %{__FULL_VERSION}

%package profile-directory-openid
Summary: directory-openid profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-security-openid                          = %{__FULL_VERSION}

%package profile-directory-shibboleth
Summary: directory-shibboleth profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-security-shibboleth                      = %{__FULL_VERSION}

%package profile-dist
Summary: dist profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-acl                 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api                 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-download            = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-streaming           = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-youtube-v3           = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-static                                   = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-dist-standalone
Summary: dist-standalone profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-acl                 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api                 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-download            = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-streaming           = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-youtube-v3           = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info-ui                          = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-remote                    = %{__FULL_VERSION}
Requires: %{name}-module-static                                   = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-dist-stub
Summary: dist-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-acl-remote          = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api                 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-download-remote     = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-streaming-remote    = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-youtube-remote       = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-engage
Summary: engage profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-annotation-api                           = %{__FULL_VERSION}
Requires: %{name}-module-annotation-impl                          = %{__FULL_VERSION}
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api                       = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-core                      = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-controls           = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-custom-mhConnection = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-custom-notifications = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-custom-usertracking = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-description        = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-tab-description    = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-tab-shortcuts      = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-tab-slidetext      = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-timeline-statistics = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-video-videojs      = %{__FULL_VERSION}
Requires: %{name}-module-engage-ui                                = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-lti                                      = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-search-service-feeds                     = %{__FULL_VERSION}
Requires: %{name}-module-search-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-solr                                     = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-usertracking-api                         = %{__FULL_VERSION}
Requires: %{name}-module-usertracking-impl                        = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-engage-standalone
Summary: engage-standalone profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-annotation-api                           = %{__FULL_VERSION}
Requires: %{name}-module-annotation-impl                          = %{__FULL_VERSION}
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api                       = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-core                      = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-controls           = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-custom-mhConnection = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-custom-notifications = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-custom-usertracking = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-description        = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-tab-description    = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-tab-shortcuts      = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-tab-slidetext      = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-timeline-statistics = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-plugin-video-videojs      = %{__FULL_VERSION}
Requires: %{name}-module-engage-ui                                = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-lti                                      = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info-ui                          = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-search-service-feeds                     = %{__FULL_VERSION}
Requires: %{name}-module-search-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-remote                    = %{__FULL_VERSION}
Requires: %{name}-module-solr                                     = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-usertracking-api                         = %{__FULL_VERSION}
Requires: %{name}-module-usertracking-impl                        = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-engage-stub
Summary: engage-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api                 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-download-remote     = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-streaming-remote    = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-lti                                      = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-youtube-remote       = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-search-service-remote                    = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-ingest
Summary: ingest profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api                            = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-impl                           = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-serviceregistry                          = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api      = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-ingest-standalone
Summary: ingest-standalone profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info-ui                          = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api                            = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-remote                         = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-remote                    = %{__FULL_VERSION}
Requires: %{name}-module-serviceregistry                          = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-remote                  = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api      = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-impl     = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}
Requires: %{name}-module-workspace-impl                           = %{__FULL_VERSION}

%package profile-migration
Summary: migration profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-migration                                = %{__FULL_VERSION}

%package profile-oaipmh
Summary: oaipmh profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-oaipmh                                   = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-search-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-solr                                     = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-server-management
Summary: server-management profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-manager-api                              = %{__FULL_VERSION}
Requires: %{name}-module-manager-impl                             = %{__FULL_VERSION}

%package profile-serviceregistry
Summary: serviceregistry profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-serviceregistry                          = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api                     = %{__FULL_VERSION}

%package profile-serviceregistry-stub
Summary: serviceregistry-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-serviceregistry-remote                   = %{__FULL_VERSION}

%package profile-worker
Summary: worker profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-caption-api                              = %{__FULL_VERSION}
Requires: %{name}-module-caption-impl                             = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-composer-ffmpeg                          = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-api                           = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-regexp                        = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api                   = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-ffmpeg                = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-api                     = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-impl                    = %{__FULL_VERSION}
Requires: %{name}-module-smil-api                                 = %{__FULL_VERSION}
Requires: %{name}-module-smil-impl                                = %{__FULL_VERSION}
Requires: %{name}-module-solr                                     = %{__FULL_VERSION}
Requires: %{name}-module-sox-api                                  = %{__FULL_VERSION}
Requires: %{name}-module-sox-impl                                 = %{__FULL_VERSION}
Requires: %{name}-module-speech-recognition-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-api                         = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-impl                        = %{__FULL_VERSION}
Requires: %{name}-module-textextractor-tesseract                  = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-api                          = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-ffmpeg-impl                  = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-api                       = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-ffmpeg                    = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-worker-standalone
Summary: worker-standalone profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-caption-api                              = %{__FULL_VERSION}
Requires: %{name}-module-caption-impl                             = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-composer-ffmpeg                          = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-db                                       = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-api                           = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-regexp                        = %{__FULL_VERSION}
Requires: %{name}-module-dublincore                               = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api                   = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-ffmpeg                = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info                             = %{__FULL_VERSION}
Requires: %{name}-module-runtime-info-ui                          = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-series-service-remote                    = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-api                     = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-impl                    = %{__FULL_VERSION}
Requires: %{name}-module-smil-api                                 = %{__FULL_VERSION}
Requires: %{name}-module-smil-impl                                = %{__FULL_VERSION}
Requires: %{name}-module-sox-api                                  = %{__FULL_VERSION}
Requires: %{name}-module-sox-impl                                 = %{__FULL_VERSION}
Requires: %{name}-module-speech-recognition-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-api                         = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-impl                        = %{__FULL_VERSION}
Requires: %{name}-module-textextractor-tesseract                  = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory                            = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-api                          = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-ffmpeg-impl                  = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-api                       = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-ffmpeg                    = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-worker-stub
Summary: worker-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-authorization-xacml                      = %{__FULL_VERSION}
Requires: %{name}-module-caption-api                              = %{__FULL_VERSION}
Requires: %{name}-module-caption-remote                           = %{__FULL_VERSION}
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api                     = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-remote                  = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api                   = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-remote                = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-kernel                                   = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api                       = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api                             = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7                                    = %{__FULL_VERSION}
Requires: %{name}-module-runtime-dependencies                     = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api                       = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-api                     = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-remote                  = %{__FULL_VERSION}
Requires: %{name}-module-smil-api                                 = %{__FULL_VERSION}
Requires: %{name}-module-smil-impl                                = %{__FULL_VERSION}
Requires: %{name}-module-sox-api                                  = %{__FULL_VERSION}
Requires: %{name}-module-sox-remote                               = %{__FULL_VERSION}
Requires: %{name}-module-speech-recognition-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-api                         = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-remote                      = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-api                          = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-remote                       = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-api                       = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-remote                    = %{__FULL_VERSION}
Requires: %{name}-module-webconsole                               = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}

%package profile-workspace
Summary: workspace profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api      = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-impl     = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}
Requires: %{name}-module-workspace-impl                           = %{__FULL_VERSION}

%package profile-workspace-stub
Summary: workspace-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-common                                   = %{__FULL_VERSION}
Requires: %{name}-module-json                                     = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api      = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-remote   = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api                            = %{__FULL_VERSION}
Requires: %{name}-module-workspace-impl                           = %{__FULL_VERSION}

%description profile-directory-cas
directory-cas profile for Opencast Matterhorn

%description profile-dist
dist profile for Opencast Matterhorn

%description profile-alternatives
alternatives profile for Opencast Matterhorn

%description profile-migration
migration profile for Opencast Matterhorn

%description profile-engage-standalone
engage-standalone profile for Opencast Matterhorn

%description profile-worker-standalone
worker-standalone profile for Opencast Matterhorn

%description profile-ingest-standalone
ingest-standalone profile for Opencast Matterhorn

%description profile-worker-stub
worker-stub profile for Opencast Matterhorn

%description profile-workspace-stub
workspace-stub profile for Opencast Matterhorn

%description profile-serviceregistry-stub
serviceregistry-stub profile for Opencast Matterhorn

%description profile-oaipmh
oaipmh profile for Opencast Matterhorn

%description profile-directory-ldap
directory-ldap profile for Opencast Matterhorn

%description profile-dist-stub
dist-stub profile for Opencast Matterhorn

%description profile-worker
worker profile for Opencast Matterhorn

%description profile-serviceregistry
serviceregistry profile for Opencast Matterhorn

%description profile-directory-openid
directory-openid profile for Opencast Matterhorn

%description profile-server-management
server-management profile for Opencast Matterhorn

%description profile-engage
engage profile for Opencast Matterhorn

%description profile-dist-standalone
dist-standalone profile for Opencast Matterhorn

%description profile-admin
admin profile for Opencast Matterhorn

%description profile-ingest
ingest profile for Opencast Matterhorn

%description profile-directory-shibboleth
directory-shibboleth profile for Opencast Matterhorn

%description profile-directory-db
directory-db profile for Opencast Matterhorn

%description profile-engage-stub
engage-stub profile for Opencast Matterhorn

%description profile-workspace
workspace profile for Opencast Matterhorn

%files profile-directory-cas
# Nothing to do

%files profile-dist
# Nothing to do

%files profile-alternatives
# Nothing to do

%files profile-migration
# Nothing to do

%files profile-engage-standalone
# Nothing to do

%files profile-worker-standalone
# Nothing to do

%files profile-ingest-standalone
# Nothing to do

%files profile-worker-stub
# Nothing to do

%files profile-workspace-stub
# Nothing to do

%files profile-serviceregistry-stub
# Nothing to do

%files profile-oaipmh
# Nothing to do

%files profile-directory-ldap
# Nothing to do

%files profile-dist-stub
# Nothing to do

%files profile-worker
# Nothing to do

%files profile-serviceregistry
# Nothing to do

%files profile-directory-openid
# Nothing to do

%files profile-server-management
# Nothing to do

%files profile-engage
# Nothing to do

%files profile-dist-standalone
# Nothing to do

%files profile-admin
# Nothing to do

%files profile-ingest
# Nothing to do

%files profile-directory-shibboleth
# Nothing to do

%files profile-directory-db
# Nothing to do

%files profile-engage-stub
# Nothing to do

%files profile-workspace
# Nothing to do



### MODULES #############################################################


%package module-admin-ui
Summary: admin-ui module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-admin-ui-ng
Summary: admin-ui-ng module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-api = %{__FULL_VERSION}
Requires: %{name}-module-index-service = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api = %{__FULL_VERSION}
Requires: %{name}-module-presets = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-authorization-manager = %{__FULL_VERSION}
Requires: %{name}-module-capture-admin-service-api = %{__FULL_VERSION}
Requires: %{name}-module-comments = %{__FULL_VERSION}
Requires: %{name}-module-messages = %{__FULL_VERSION}
Requires: %{name}-module-themes = %{__FULL_VERSION}
Requires: %{name}-module-archive-api = %{__FULL_VERSION}
Requires: %{name}-module-archive-schema = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-participation-api = %{__FULL_VERSION}
Requires: %{name}-module-search-api = %{__FULL_VERSION}
Requires: %{name}-module-search = %{__FULL_VERSION}
Requires: %{name}-module-smil-api = %{__FULL_VERSION}
Requires: %{name}-module-smil-impl = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-annotation-api
Summary: annotation-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-annotation-impl
Summary: annotation-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-annotation-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-archive-api
Summary: archive-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-archive-base
Summary: archive-base module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-archive-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-solr = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-archive-schema
Summary: archive-schema module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-archive-base = %{__FULL_VERSION}
Requires: %{name}-module-schema = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-solr = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Requires: %{name}-module-kernel = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-archive-storage-fs
Summary: archive-storage-fs module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-archive-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-archive-workflowoperation
Summary: archive-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-archive-api = %{__FULL_VERSION}
Requires: %{name}-module-archive-schema = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-authorization-manager
Summary: authorization-manager module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-conductor = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-archive-api = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-authorization-xacml = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-download = %{__FULL_VERSION}
Requires: %{name}-module-distribution-workflowoperation = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-authorization-xacml
Summary: authorization-xacml module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-caption-api
Summary: caption-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-caption-impl
Summary: caption-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-caption-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Conflicts: %{name}-module-caption-remote
Group: Applications/Multimedia

%package module-caption-remote
Summary: caption-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-caption-api = %{__FULL_VERSION}
Conflicts: %{name}-module-caption-impl
Group: Applications/Multimedia

%package module-capture-admin-service-api
Summary: capture-admin-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-capture-admin-service-impl
Summary: capture-admin-service-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-capture-admin-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-capture-workflowoperation
Summary: capture-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-workflowoperation = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-comments
Summary: comments module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-comments-workflowoperation
Summary: comments-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-comments = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-common
Summary: common module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-composer-ffmpeg
Summary: composer-ffmpeg module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: ffmpeg >= 2.5
Requires: qt_sbtl_embedder >= 0.4
BuildRequires: ffmpeg >= 2.5
Conflicts: %{name}-module-composer-service-remote
Group: Applications/Multimedia

%package module-composer-service-api
Summary: composer-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-composer-service-remote
Summary: composer-service-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-composer-ffmpeg
Group: Applications/Multimedia

%package module-composer-workflowoperation
Summary: composer-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-inspection-workflowoperation = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-caption-api = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-conductor
Summary: conductor module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-archive-api = %{__FULL_VERSION}
Requires: %{name}-module-archive-schema = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-distribution-workflowoperation = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-dataloader
Summary: dataloader module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api = %{__FULL_VERSION}
Requires: %{name}-module-archive-api = %{__FULL_VERSION}
Requires: %{name}-module-kernel = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-db
Summary: db module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-deprecated-workflowoperation
Summary: deprecated-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-workflowoperation = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-dictionary-api
Summary: dictionary-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-dictionary-hunspell
Summary: dictionary-hunspell module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-api = %{__FULL_VERSION}
Requires: hunspell >= 1.2.8
BuildRequires: hunspell >= 1.2.8
Conflicts: %{name}-module-dictionary-none
Conflicts: %{name}-module-dictionary-regexp
Group: Applications/Multimedia

%package module-dictionary-none
Summary: dictionary-none module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-api = %{__FULL_VERSION}
Conflicts: %{name}-module-dictionary-hunspell
Conflicts: %{name}-module-dictionary-regexp
Group: Applications/Multimedia

%package module-dictionary-regexp
Summary: dictionary-regexp module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-api = %{__FULL_VERSION}
Conflicts: %{name}-module-dictionary-hunspell
Conflicts: %{name}-module-dictionary-none
Group: Applications/Multimedia

%package module-distribution-service-acl
Summary: distribution-service-acl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Conflicts: %{name}-module-distribution-service-acl-remote
Group: Applications/Multimedia

%package module-distribution-service-acl-remote
Summary: distribution-service-acl-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-distribution-service-acl
Group: Applications/Multimedia

%package module-distribution-service-api
Summary: distribution-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-distribution-service-download
Summary: distribution-service-download module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Conflicts: %{name}-module-distribution-service-download-remote
Group: Applications/Multimedia

%package module-distribution-service-download-remote
Summary: distribution-service-download-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-distribution-service-download
Group: Applications/Multimedia

%package module-distribution-service-streaming
Summary: distribution-service-streaming module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Conflicts: %{name}-module-distribution-service-streaming-remote
Group: Applications/Multimedia

%package module-distribution-service-streaming-remote
Summary: distribution-service-streaming-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-distribution-service-streaming
Group: Applications/Multimedia

%package module-distribution-workflowoperation
Summary: distribution-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-inspection-workflowoperation = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Requires: %{name}-module-distribution-service-api = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-dublincore
Summary: dublincore module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-api
Summary: engage-theodul-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-core
Summary: engage-theodul-core module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-kernel = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-controls
Summary: engage-theodul-plugin-controls module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-custom-mhConnection
Summary: engage-theodul-plugin-custom-mhConnection module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-custom-notifications
Summary: engage-theodul-plugin-custom-notifications module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-custom-usertracking
Summary: engage-theodul-plugin-custom-usertracking module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-description
Summary: engage-theodul-plugin-description module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-tab-description
Summary: engage-theodul-plugin-tab-description module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-tab-shortcuts
Summary: engage-theodul-plugin-tab-shortcuts module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-tab-slidetext
Summary: engage-theodul-plugin-tab-slidetext module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-timeline-statistics
Summary: engage-theodul-plugin-timeline-statistics module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-theodul-plugin-video-videojs
Summary: engage-theodul-plugin-video-videojs module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-engage-theodul-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-engage-ui
Summary: engage-ui module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-fileupload
Summary: fileupload module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-gstreamer-service-api
Summary: gstreamer-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-gstreamer-service-impl
Summary: gstreamer-service-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-gstreamer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-serviceregistry = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-gstreamer-service-remote
Summary: gstreamer-service-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-gstreamer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-serviceregistry = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-holdstate-workflowoperation
Summary: holdstate-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-workflowoperation = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-incident-workflowoperation
Summary: incident-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-index-service
Summary: index-service module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-authorization-manager = %{__FULL_VERSION}
Requires: %{name}-module-capture-admin-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-comments = %{__FULL_VERSION}
Requires: %{name}-module-participation-api = %{__FULL_VERSION}
Requires: %{name}-module-search = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-api = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-ingest-service-api
Summary: ingest-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-ingest-service-impl
Summary: ingest-service-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-authorization-xacml = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-ingest-workflowoperation
Summary: ingest-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-workflowoperation = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-inspection-service-api
Summary: inspection-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-inspection-service-ffmpeg
Summary: inspection-service-ffmpeg module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: ffmpeg >= 2.5
BuildRequires: ffmpeg >= 2.5
Conflicts: %{name}-module-inspection-service-remote
Group: Applications/Multimedia

%package module-inspection-service-remote
Summary: inspection-service-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-inspection-service-ffmpeg
Group: Applications/Multimedia

%package module-inspection-workflowoperation
Summary: inspection-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-json
Summary: json module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-kernel
Summary: kernel module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-lti
Summary: lti module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-manager-api
Summary: manager-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-manager-impl
Summary: manager-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-manager-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-mediapackage-manipulator
Summary: mediapackage-manipulator module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-mediapackage-ui
Summary: mediapackage-ui module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-message-broker-api
Summary: message-broker-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-archive-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-message-broker-impl
Summary: message-broker-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-messages
Summary: messages module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-kernel = %{__FULL_VERSION}
Requires: %{name}-module-comments = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-metadata
Summary: metadata module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-metadata-api
Summary: metadata-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-migration
Summary: migration module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-mpeg7
Summary: mpeg7 module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-metadata-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-notification-workflowoperation
Summary: notification-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-kernel = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-oaipmh
Summary: oaipmh module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-search-service-impl = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-participation-api
Summary: participation-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-messages = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-presets
Summary: presets module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-publication-service-api
Summary: publication-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-publication-service-youtube-remote
Summary: publication-service-youtube-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-publication-service-youtube-v3
Group: Applications/Multimedia

%package module-publication-service-youtube-v3
Summary: publication-service-youtube-v3 module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-publication-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Conflicts: %{name}-module-publication-service-youtube-remote
Group: Applications/Multimedia

%package module-runtime-dependencies
Summary: runtime-dependencies module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-ramework.ldap = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-runtime-info
Summary: runtime-info module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Requires: %{name}-module-userdirectory = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-runtime-info-ui
Summary: runtime-info-ui module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-runtime-info-ui-ng
Summary: runtime-info-ui-ng module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-scheduler-api
Summary: scheduler-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-scheduler-impl
Summary: scheduler-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-ingest-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-kernel = %{__FULL_VERSION}
Requires: %{name}-module-solr = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Conflicts: %{name}-module-scheduler-remote
Group: Applications/Multimedia

%package module-scheduler-remote
Summary: scheduler-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-scheduler-api = %{__FULL_VERSION}
Conflicts: %{name}-module-scheduler-impl
Group: Applications/Multimedia

%package module-scheduler-workflowoperation
Summary: scheduler-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-workflowoperation = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-schema
Summary: schema module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-search
Summary: search module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-search-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-search-api
Summary: search-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-search-service-api
Summary: search-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-search-service-feeds
Summary: search-service-feeds module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-search-service-impl
Summary: search-service-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-solr = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Requires: %{name}-module-series-service-impl = %{__FULL_VERSION}
Conflicts: %{name}-module-search-service-remote
Group: Applications/Multimedia

%package module-search-service-remote
Summary: search-service-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-search-service-impl
Group: Applications/Multimedia

%package module-search-workflowoperation
Summary: search-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-security-cas
Summary: security-cas module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-security-ldap
Summary: security-ldap module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-security-openid
Summary: security-openid module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-security-shibboleth
Summary: security-shibboleth module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-series-service-api
Summary: series-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-series-service-impl
Summary: series-service-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-solr = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Conflicts: %{name}-module-series-service-remote
Group: Applications/Multimedia

%package module-series-service-remote
Summary: series-service-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Conflicts: %{name}-module-series-service-impl
Group: Applications/Multimedia

%package module-serviceregistry
Summary: serviceregistry module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-serviceregistry-remote
Group: Applications/Multimedia

%package module-serviceregistry-remote
Summary: serviceregistry-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Conflicts: %{name}-module-serviceregistry
Group: Applications/Multimedia

%package module-silencedetection-api
Summary: silencedetection-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-silencedetection-impl
Summary: silencedetection-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-api = %{__FULL_VERSION}
Requires: %{name}-module-smil-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: ffmpeg >= 2.5
BuildRequires: ffmpeg >= 2.5
Conflicts: %{name}-module-silencedetection-remote
Group: Applications/Multimedia

%package module-silencedetection-remote
Summary: silencedetection-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Conflicts: %{name}-module-silencedetection-impl
Group: Applications/Multimedia

%package module-smil-api
Summary: smil-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-smil-impl
Summary: smil-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-smil-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-solr
Summary: solr module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-sox-api
Summary: sox-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-sox-impl
Summary: sox-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-sox-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: sox >= 14
BuildRequires: sox >= 14
Conflicts: %{name}-module-sox-remote
Group: Applications/Multimedia

%package module-sox-remote
Summary: sox-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-sox-api = %{__FULL_VERSION}
Conflicts: %{name}-module-sox-impl
Group: Applications/Multimedia

%package module-sox-workflowoperation
Summary: sox-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-sox-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-speech-recognition-service-api
Summary: speech-recognition-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-speech-recognition-workflowoperation
Summary: speech-recognition-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-speech-recognition-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-static
Summary: static module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-static-file-service-api
Summary: static-file-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-static-file-service-impl
Summary: static-file-service-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-textanalyzer-api
Summary: textanalyzer-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-textanalyzer-impl
Summary: textanalyzer-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-api = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Requires: %{name}-module-dictionary-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-textanalyzer-remote
Group: Applications/Multimedia

%package module-textanalyzer-remote
Summary: textanalyzer-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-api = %{__FULL_VERSION}
Conflicts: %{name}-module-textanalyzer-impl
Group: Applications/Multimedia

%package module-textanalyzer-workflowoperation
Summary: textanalyzer-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-api = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-textextractor-tesseract
Summary: textextractor-tesseract module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-textanalyzer-api = %{__FULL_VERSION}
Requires: tesseract >= 3
BuildRequires: tesseract >= 3
BuildRequires: tesseract-langpack-deu >= 3
Group: Applications/Multimedia

%package module-themes
Summary: themes module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-themes-workflowoperation
Summary: themes-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-themes = %{__FULL_VERSION}
Requires: %{name}-module-static-file-service-api = %{__FULL_VERSION}
Requires: %{name}-module-composer-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-userdirectory
Summary: userdirectory module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-kernel = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-userdirectory-ldap
Summary: userdirectory-ldap module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-usertracking-api
Summary: usertracking-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-usertracking-impl
Summary: usertracking-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-usertracking-api = %{__FULL_VERSION}
Requires: %{name}-module-search-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-videoeditor-api
Summary: videoeditor-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-videoeditor-ffmpeg-impl
Summary: videoeditor-ffmpeg-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-api = %{__FULL_VERSION}
Requires: %{name}-module-smil-api = %{__FULL_VERSION}
Requires: %{name}-module-smil-impl = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-ffmpeg = %{__FULL_VERSION}
Requires: %{name}-module-inspection-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: ffmpeg >= 2.5
BuildRequires: ffmpeg >= 2.5
Conflicts: %{name}-module-videoeditor-remote
Group: Applications/Multimedia

%package module-videoeditor-remote
Summary: videoeditor-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Conflicts: %{name}-module-videoeditor-ffmpeg-impl
Group: Applications/Multimedia

%package module-videoeditor-workflowoperation
Summary: videoeditor-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-smil-api = %{__FULL_VERSION}
Requires: %{name}-module-smil-impl = %{__FULL_VERSION}
Requires: %{name}-module-silencedetection-api = %{__FULL_VERSION}
Requires: %{name}-module-videoeditor-api = %{__FULL_VERSION}
Requires: %{name}-module-workflow-workflowoperation = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-videosegmenter-api
Summary: videosegmenter-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-mpeg7 = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-videosegmenter-ffmpeg
Summary: videosegmenter-ffmpeg module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: ffmpeg >= 2.5
BuildRequires: ffmpeg >= 2.5
Conflicts: %{name}-module-videosegmenter-remote
Group: Applications/Multimedia

%package module-videosegmenter-remote
Summary: videosegmenter-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-api = %{__FULL_VERSION}
Conflicts: %{name}-module-videosegmenter-ffmpeg
Group: Applications/Multimedia

%package module-videosegmenter-workflowoperation
Summary: videosegmenter-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-videosegmenter-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-webconsole
Summary: webconsole module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-workflow-service-api
Summary: workflow-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-workflow-service-impl
Summary: workflow-service-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-serviceregistry = %{__FULL_VERSION}
Requires: %{name}-module-dublincore = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-message-broker-api = %{__FULL_VERSION}
Requires: %{name}-module-solr = %{__FULL_VERSION}
Requires: %{name}-module-kernel = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Requires: %{name}-module-conductor = %{__FULL_VERSION}
Requires: %{name}-module-workflow-workflowoperation = %{__FULL_VERSION}
Conflicts: %{name}-module-workflow-service-remote
Group: Applications/Multimedia

%package module-workflow-service-remote
Summary: workflow-service-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Conflicts: %{name}-module-workflow-service-impl
Group: Applications/Multimedia

%package module-workflow-workflowoperation
Summary: workflow-workflowoperation module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-workflow-service-api = %{__FULL_VERSION}
Requires: %{name}-module-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-presets = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-working-file-repository-service-api
Summary: working-file-repository-service-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-working-file-repository-service-impl
Summary: working-file-repository-service-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-working-file-repository-service-remote
Summary: working-file-repository-service-remote module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Requires: %{name}-module-json = %{__FULL_VERSION}
Conflicts: %{name}-module-working-file-repository-service
Group: Applications/Multimedia

%package module-workspace-api
Summary: workspace-api module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%package module-workspace-impl
Summary: workspace-impl module for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-base = %{__FULL_VERSION}
Requires: %{name}-module-workspace-api = %{__FULL_VERSION}
Requires: %{name}-module-working-file-repository-service-api = %{__FULL_VERSION}
Requires: %{name}-module-common = %{__FULL_VERSION}
Group: Applications/Multimedia

%description module-admin-ui
admin-ui module for Opencast Matterhorn

%description module-admin-ui-ng
admin-ui-ng module for Opencast Matterhorn

%description module-annotation-api
annotation-api module for Opencast Matterhorn

%description module-annotation-impl
annotation-impl module for Opencast Matterhorn

%description module-archive-api
archive-api module for Opencast Matterhorn

%description module-archive-base
archive-base module for Opencast Matterhorn

%description module-archive-schema
archive-schema module for Opencast Matterhorn

%description module-archive-storage-fs
archive-storage-fs module for Opencast Matterhorn

%description module-archive-workflowoperation
archive-workflowoperation module for Opencast Matterhorn

%description module-authorization-manager
authorization-manager module for Opencast Matterhorn

%description module-authorization-xacml
authorization-xacml module for Opencast Matterhorn

%description module-caption-api
caption-api module for Opencast Matterhorn

%description module-caption-impl
caption-impl module for Opencast Matterhorn

%description module-caption-remote
caption-remote module for Opencast Matterhorn

%description module-capture-admin-service-api
capture-admin-service-api module for Opencast Matterhorn

%description module-capture-admin-service-impl
capture-admin-service-impl module for Opencast Matterhorn

%description module-capture-workflowoperation
capture-workflowoperation module for Opencast Matterhorn

%description module-comments
comments module for Opencast Matterhorn

%description module-comments-workflowoperation
comments-workflowoperation module for Opencast Matterhorn

%description module-common
common module for Opencast Matterhorn

%description module-composer-ffmpeg
composer-ffmpeg module for Opencast Matterhorn

%description module-composer-service-api
composer-service-api module for Opencast Matterhorn

%description module-composer-service-remote
composer-service-remote module for Opencast Matterhorn

%description module-composer-workflowoperation
composer-workflowoperation module for Opencast Matterhorn

%description module-conductor
conductor module for Opencast Matterhorn

%description module-dataloader
dataloader module for Opencast Matterhorn

%description module-db
db module for Opencast Matterhorn

%description module-deprecated-workflowoperation
deprecated-workflowoperation module for Opencast Matterhorn

%description module-dictionary-api
dictionary-api module for Opencast Matterhorn

%description module-dictionary-hunspell
dictionary-hunspell module for Opencast Matterhorn

%description module-dictionary-none
dictionary-none module for Opencast Matterhorn

%description module-dictionary-regexp
dictionary-regexp module for Opencast Matterhorn

%description module-distribution-service-acl
distribution-service-acl module for Opencast Matterhorn

%description module-distribution-service-acl-remote
distribution-service-acl-remote module for Opencast Matterhorn

%description module-distribution-service-api
distribution-service-api module for Opencast Matterhorn

%description module-distribution-service-download
distribution-service-download module for Opencast Matterhorn

%description module-distribution-service-download-remote
distribution-service-download-remote module for Opencast Matterhorn

%description module-distribution-service-streaming
distribution-service-streaming module for Opencast Matterhorn

%description module-distribution-service-streaming-remote
distribution-service-streaming-remote module for Opencast Matterhorn

%description module-distribution-workflowoperation
distribution-workflowoperation module for Opencast Matterhorn

%description module-dublincore
dublincore module for Opencast Matterhorn

%description module-engage-theodul-api
engage-theodul-api module for Opencast Matterhorn

%description module-engage-theodul-core
engage-theodul-core module for Opencast Matterhorn

%description module-engage-theodul-plugin-controls
engage-theodul-plugin-controls module for Opencast Matterhorn

%description module-engage-theodul-plugin-custom-mhConnection
engage-theodul-plugin-custom-mhConnection module for Opencast Matterhorn

%description module-engage-theodul-plugin-custom-notifications
engage-theodul-plugin-custom-notifications module for Opencast Matterhorn

%description module-engage-theodul-plugin-custom-usertracking
engage-theodul-plugin-custom-usertracking module for Opencast Matterhorn

%description module-engage-theodul-plugin-description
engage-theodul-plugin-description module for Opencast Matterhorn

%description module-engage-theodul-plugin-tab-description
engage-theodul-plugin-tab-description module for Opencast Matterhorn

%description module-engage-theodul-plugin-tab-shortcuts
engage-theodul-plugin-tab-shortcuts module for Opencast Matterhorn

%description module-engage-theodul-plugin-tab-slidetext
engage-theodul-plugin-tab-slidetext module for Opencast Matterhorn

%description module-engage-theodul-plugin-timeline-statistics
engage-theodul-plugin-timeline-statistics module for Opencast Matterhorn

%description module-engage-theodul-plugin-video-videojs
engage-theodul-plugin-video-videojs module for Opencast Matterhorn

%description module-engage-ui
engage-ui module for Opencast Matterhorn

%description module-fileupload
fileupload module for Opencast Matterhorn

%description module-gstreamer-service-api
gstreamer-service-api module for Opencast Matterhorn

%description module-gstreamer-service-impl
gstreamer-service-impl module for Opencast Matterhorn

%description module-gstreamer-service-remote
gstreamer-service-remote module for Opencast Matterhorn

%description module-holdstate-workflowoperation
holdstate-workflowoperation module for Opencast Matterhorn

%description module-incident-workflowoperation
incident-workflowoperation module for Opencast Matterhorn

%description module-index-service
index-service module for Opencast Matterhorn

%description module-ingest-service-api
ingest-service-api module for Opencast Matterhorn

%description module-ingest-service-impl
ingest-service-impl module for Opencast Matterhorn

%description module-ingest-workflowoperation
ingest-workflowoperation module for Opencast Matterhorn

%description module-inspection-service-api
inspection-service-api module for Opencast Matterhorn

%description module-inspection-service-ffmpeg
inspection-service-ffmpeg module for Opencast Matterhorn

%description module-inspection-service-remote
inspection-service-remote module for Opencast Matterhorn

%description module-inspection-workflowoperation
inspection-workflowoperation module for Opencast Matterhorn

%description module-json
json module for Opencast Matterhorn

%description module-kernel
kernel module for Opencast Matterhorn

%description module-lti
lti module for Opencast Matterhorn

%description module-manager-api
manager-api module for Opencast Matterhorn

%description module-manager-impl
manager-impl module for Opencast Matterhorn

%description module-mediapackage-manipulator
mediapackage-manipulator module for Opencast Matterhorn

%description module-mediapackage-ui
mediapackage-ui module for Opencast Matterhorn

%description module-message-broker-api
message-broker-api module for Opencast Matterhorn

%description module-message-broker-impl
message-broker-impl module for Opencast Matterhorn

%description module-messages
messages module for Opencast Matterhorn

%description module-metadata
metadata module for Opencast Matterhorn

%description module-metadata-api
metadata-api module for Opencast Matterhorn

%description module-migration
migration module for Opencast Matterhorn

%description module-mpeg7
mpeg7 module for Opencast Matterhorn

%description module-notification-workflowoperation
notification-workflowoperation module for Opencast Matterhorn

%description module-oaipmh
oaipmh module for Opencast Matterhorn

%description module-participation-api
participation-api module for Opencast Matterhorn

%description module-presets
presets module for Opencast Matterhorn

%description module-publication-service-api
publication-service-api module for Opencast Matterhorn

%description module-publication-service-youtube-remote
publication-service-youtube-remote module for Opencast Matterhorn

%description module-publication-service-youtube-v3
publication-service-youtube-v3 module for Opencast Matterhorn

%description module-runtime-dependencies
runtime-dependencies module for Opencast Matterhorn

%description module-runtime-info
runtime-info module for Opencast Matterhorn

%description module-runtime-info-ui
runtime-info-ui module for Opencast Matterhorn

%description module-runtime-info-ui-ng
runtime-info-ui-ng module for Opencast Matterhorn

%description module-scheduler-api
scheduler-api module for Opencast Matterhorn

%description module-scheduler-impl
scheduler-impl module for Opencast Matterhorn

%description module-scheduler-remote
scheduler-remote module for Opencast Matterhorn

%description module-scheduler-workflowoperation
scheduler-workflowoperation module for Opencast Matterhorn

%description module-schema
schema module for Opencast Matterhorn

%description module-search
search module for Opencast Matterhorn

%description module-search-api
search-api module for Opencast Matterhorn

%description module-search-service-api
search-service-api module for Opencast Matterhorn

%description module-search-service-feeds
search-service-feeds module for Opencast Matterhorn

%description module-search-service-impl
search-service-impl module for Opencast Matterhorn

%description module-search-service-remote
search-service-remote module for Opencast Matterhorn

%description module-search-workflowoperation
search-workflowoperation module for Opencast Matterhorn

%description module-security-cas
security-cas module for Opencast Matterhorn

%description module-security-ldap
security-ldap module for Opencast Matterhorn

%description module-security-openid
security-openid module for Opencast Matterhorn

%description module-security-shibboleth
security-shibboleth module for Opencast Matterhorn

%description module-series-service-api
series-service-api module for Opencast Matterhorn

%description module-series-service-impl
series-service-impl module for Opencast Matterhorn

%description module-series-service-remote
series-service-remote module for Opencast Matterhorn

%description module-serviceregistry
serviceregistry module for Opencast Matterhorn

%description module-serviceregistry-remote
serviceregistry-remote module for Opencast Matterhorn

%description module-silencedetection-api
silencedetection-api module for Opencast Matterhorn

%description module-silencedetection-impl
silencedetection-impl module for Opencast Matterhorn

%description module-silencedetection-remote
silencedetection-remote module for Opencast Matterhorn

%description module-smil-api
smil-api module for Opencast Matterhorn

%description module-smil-impl
smil-impl module for Opencast Matterhorn

%description module-solr
solr module for Opencast Matterhorn

%description module-sox-api
sox-api module for Opencast Matterhorn

%description module-sox-impl
sox-impl module for Opencast Matterhorn

%description module-sox-remote
sox-remote module for Opencast Matterhorn

%description module-sox-workflowoperation
sox-workflowoperation module for Opencast Matterhorn

%description module-speech-recognition-service-api
speech-recognition-service-api module for Opencast Matterhorn

%description module-speech-recognition-workflowoperation
speech-recognition-workflowoperation module for Opencast Matterhorn

%description module-static
static module for Opencast Matterhorn

%description module-static-file-service-api
static-file-service-api module for Opencast Matterhorn

%description module-static-file-service-impl
static-file-service-impl module for Opencast Matterhorn

%description module-textanalyzer-api
textanalyzer-api module for Opencast Matterhorn

%description module-textanalyzer-impl
textanalyzer-impl module for Opencast Matterhorn

%description module-textanalyzer-remote
textanalyzer-remote module for Opencast Matterhorn

%description module-textanalyzer-workflowoperation
textanalyzer-workflowoperation module for Opencast Matterhorn

%description module-textextractor-tesseract
textextractor-tesseract module for Opencast Matterhorn

%description module-themes
themes module for Opencast Matterhorn

%description module-themes-workflowoperation
themes-workflowoperation module for Opencast Matterhorn

%description module-userdirectory
userdirectory module for Opencast Matterhorn

%description module-userdirectory-ldap
userdirectory-ldap module for Opencast Matterhorn

%description module-usertracking-api
usertracking-api module for Opencast Matterhorn

%description module-usertracking-impl
usertracking-impl module for Opencast Matterhorn

%description module-videoeditor-api
videoeditor-api module for Opencast Matterhorn

%description module-videoeditor-ffmpeg-impl
videoeditor-ffmpeg-impl module for Opencast Matterhorn

%description module-videoeditor-remote
videoeditor-remote module for Opencast Matterhorn

%description module-videoeditor-workflowoperation
videoeditor-workflowoperation module for Opencast Matterhorn

%description module-videosegmenter-api
videosegmenter-api module for Opencast Matterhorn

%description module-videosegmenter-ffmpeg
videosegmenter-ffmpeg module for Opencast Matterhorn

%description module-videosegmenter-remote
videosegmenter-remote module for Opencast Matterhorn

%description module-videosegmenter-workflowoperation
videosegmenter-workflowoperation module for Opencast Matterhorn

%description module-webconsole
webconsole module for Opencast Matterhorn

%description module-workflow-service-api
workflow-service-api module for Opencast Matterhorn

%description module-workflow-service-impl
workflow-service-impl module for Opencast Matterhorn

%description module-workflow-service-remote
workflow-service-remote module for Opencast Matterhorn

%description module-workflow-workflowoperation
workflow-workflowoperation module for Opencast Matterhorn

%description module-working-file-repository-service-api
working-file-repository-service-api module for Opencast Matterhorn

%description module-working-file-repository-service-impl
working-file-repository-service-impl module for Opencast Matterhorn

%description module-working-file-repository-service-remote
working-file-repository-service-remote module for Opencast Matterhorn

%description module-workspace-api
workspace-api module for Opencast Matterhorn

%description module-workspace-impl
workspace-impl module for Opencast Matterhorn

%files module-admin-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-admin-ui-%{__INTERNAL_VERSION}.jar

%files module-admin-ui-ng
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-admin-ui-ng-%{__INTERNAL_VERSION}.jar

%files module-annotation-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-annotation-api-%{__INTERNAL_VERSION}.jar

%files module-annotation-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-annotation-impl-%{__INTERNAL_VERSION}.jar

%files module-archive-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-archive-api-%{__INTERNAL_VERSION}.jar

%files module-archive-base
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-archive-base-%{__INTERNAL_VERSION}.jar

%files module-archive-schema
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-archive-schema-%{__INTERNAL_VERSION}.jar

%files module-archive-storage-fs
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-archive-storage-fs-%{__INTERNAL_VERSION}.jar

%files module-archive-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-archive-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-authorization-manager
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-authorization-manager-%{__INTERNAL_VERSION}.jar

%files module-authorization-xacml
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-authorization-xacml-%{__INTERNAL_VERSION}.jar

%files module-caption-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-caption-api-%{__INTERNAL_VERSION}.jar

%files module-caption-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-caption-impl-%{__INTERNAL_VERSION}.jar

%files module-caption-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-caption-remote-%{__INTERNAL_VERSION}.jar

%files module-capture-admin-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-capture-admin-service-api-%{__INTERNAL_VERSION}.jar

%files module-capture-admin-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-capture-admin-service-impl-%{__INTERNAL_VERSION}.jar

%files module-capture-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-capture-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-comments
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-comments-%{__INTERNAL_VERSION}.jar

%files module-comments-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-comments-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-common
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-common-%{__INTERNAL_VERSION}.jar

%files module-composer-ffmpeg
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-composer-ffmpeg-%{__INTERNAL_VERSION}.jar

%files module-composer-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-composer-service-api-%{__INTERNAL_VERSION}.jar

%files module-composer-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-composer-service-remote-%{__INTERNAL_VERSION}.jar

%files module-composer-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-composer-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-conductor
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-conductor-%{__INTERNAL_VERSION}.jar

%files module-dataloader
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dataloader-%{__INTERNAL_VERSION}.jar

%files module-db
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-db-%{__INTERNAL_VERSION}.jar

%files module-deprecated-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-deprecated-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-dictionary-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-api-%{__INTERNAL_VERSION}.jar

%files module-dictionary-hunspell
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-hunspell-%{__INTERNAL_VERSION}.jar

%files module-dictionary-none
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-none-%{__INTERNAL_VERSION}.jar

%files module-dictionary-regexp
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-regexp-%{__INTERNAL_VERSION}.jar

%files module-distribution-service-acl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-acl-%{__INTERNAL_VERSION}.jar

%files module-distribution-service-acl-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-acl-remote-%{__INTERNAL_VERSION}.jar

%files module-distribution-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-api-%{__INTERNAL_VERSION}.jar

%files module-distribution-service-download
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-download-%{__INTERNAL_VERSION}.jar

%files module-distribution-service-download-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-download-remote-%{__INTERNAL_VERSION}.jar

%files module-distribution-service-streaming
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-streaming-%{__INTERNAL_VERSION}.jar

%files module-distribution-service-streaming-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-streaming-remote-%{__INTERNAL_VERSION}.jar

%files module-distribution-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-dublincore
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dublincore-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-api-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-core
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-core-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-controls
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-controls-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-custom-mhConnection
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-custom-mhConnection-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-custom-notifications
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-custom-notifications-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-custom-usertracking
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-custom-usertracking-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-description
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-description-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-tab-description
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-tab-description-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-tab-shortcuts
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-tab-shortcuts-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-tab-slidetext
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-tab-slidetext-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-timeline-statistics
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-timeline-statistics-%{__INTERNAL_VERSION}.jar

%files module-engage-theodul-plugin-video-videojs
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-theodul-plugin-video-videojs-%{__INTERNAL_VERSION}.jar

%files module-engage-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-ui-%{__INTERNAL_VERSION}.jar

%files module-fileupload
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-fileupload-%{__INTERNAL_VERSION}.jar

%files module-gstreamer-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-api-%{__INTERNAL_VERSION}.jar

%files module-gstreamer-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-impl-%{__INTERNAL_VERSION}.jar

%files module-gstreamer-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-remote-%{__INTERNAL_VERSION}.jar

%files module-holdstate-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-holdstate-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-incident-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-incident-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-index-service
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-index-service-%{__INTERNAL_VERSION}.jar

%files module-ingest-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-ingest-service-api-%{__INTERNAL_VERSION}.jar

%files module-ingest-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-ingest-service-impl-%{__INTERNAL_VERSION}.jar

%files module-ingest-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-ingest-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-inspection-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-service-api-%{__INTERNAL_VERSION}.jar

%files module-inspection-service-ffmpeg
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-service-ffmpeg-%{__INTERNAL_VERSION}.jar

%files module-inspection-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-service-remote-%{__INTERNAL_VERSION}.jar

%files module-inspection-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-json
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-json-%{__INTERNAL_VERSION}.jar

%files module-kernel
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-kernel-%{__INTERNAL_VERSION}.jar

%files module-lti
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-lti-%{__INTERNAL_VERSION}.jar

%files module-manager-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-manager-api-%{__INTERNAL_VERSION}.jar

%files module-manager-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-manager-impl-%{__INTERNAL_VERSION}.jar

%files module-mediapackage-manipulator
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-mediapackage-manipulator-%{__INTERNAL_VERSION}.jar

%files module-mediapackage-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-mediapackage-ui-%{__INTERNAL_VERSION}.jar

%files module-message-broker-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-message-broker-api-%{__INTERNAL_VERSION}.jar

%files module-message-broker-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-message-broker-impl-%{__INTERNAL_VERSION}.jar

%files module-messages
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-messages-%{__INTERNAL_VERSION}.jar

%files module-metadata
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-metadata-%{__INTERNAL_VERSION}.jar

%files module-metadata-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-metadata-api-%{__INTERNAL_VERSION}.jar

%files module-migration
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-migration-%{__INTERNAL_VERSION}.jar

%files module-mpeg7
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-mpeg7-%{__INTERNAL_VERSION}.jar

%files module-notification-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-notification-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-oaipmh
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-oaipmh-%{__INTERNAL_VERSION}.jar

%files module-participation-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-participation-api-%{__INTERNAL_VERSION}.jar

%files module-presets
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-presets-%{__INTERNAL_VERSION}.jar

%files module-publication-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-publication-service-api-%{__INTERNAL_VERSION}.jar

%files module-publication-service-youtube-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-publication-service-youtube-remote-%{__INTERNAL_VERSION}.jar

%files module-publication-service-youtube-v3
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-publication-service-youtube-v3-%{__INTERNAL_VERSION}.jar

%files module-runtime-dependencies
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/ext

%files module-runtime-info
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-runtime-info-%{__INTERNAL_VERSION}.jar

%files module-runtime-info-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-runtime-info-ui-%{__INTERNAL_VERSION}.jar

%files module-runtime-info-ui-ng
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-runtime-info-ui-ng-%{__INTERNAL_VERSION}.jar

%files module-scheduler-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-scheduler-api-%{__INTERNAL_VERSION}.jar

%files module-scheduler-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-scheduler-impl-%{__INTERNAL_VERSION}.jar

%files module-scheduler-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-scheduler-remote-%{__INTERNAL_VERSION}.jar

%files module-scheduler-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-scheduler-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-schema
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-schema-%{__INTERNAL_VERSION}.jar

%files module-search
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-%{__INTERNAL_VERSION}.jar

%files module-search-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-api-%{__INTERNAL_VERSION}.jar

%files module-search-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-service-api-%{__INTERNAL_VERSION}.jar

%files module-search-service-feeds
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-service-feeds-%{__INTERNAL_VERSION}.jar

%files module-search-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-service-impl-%{__INTERNAL_VERSION}.jar

%files module-search-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-service-remote-%{__INTERNAL_VERSION}.jar

%files module-search-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-security-cas
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-security-cas-%{__INTERNAL_VERSION}.jar

%files module-security-ldap
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-security-ldap-%{__INTERNAL_VERSION}.jar

%files module-security-openid
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-security-openid-%{__INTERNAL_VERSION}.jar

%files module-security-shibboleth
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-security-shibboleth-%{__INTERNAL_VERSION}.jar

%files module-series-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-series-service-api-%{__INTERNAL_VERSION}.jar

%files module-series-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-series-service-impl-%{__INTERNAL_VERSION}.jar

%files module-series-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-series-service-remote-%{__INTERNAL_VERSION}.jar

%files module-serviceregistry
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-serviceregistry-%{__INTERNAL_VERSION}.jar

%files module-serviceregistry-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-serviceregistry-remote-%{__INTERNAL_VERSION}.jar

%files module-silencedetection-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-silencedetection-api-%{__INTERNAL_VERSION}.jar

%files module-silencedetection-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-silencedetection-impl-%{__INTERNAL_VERSION}.jar

%files module-silencedetection-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-silencedetection-remote-%{__INTERNAL_VERSION}.jar

%files module-smil-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-smil-api-%{__INTERNAL_VERSION}.jar

%files module-smil-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-smil-impl-%{__INTERNAL_VERSION}.jar

%files module-solr
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-solr-%{__INTERNAL_VERSION}.jar

%files module-sox-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-sox-api-%{__INTERNAL_VERSION}.jar

%files module-sox-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-sox-impl-%{__INTERNAL_VERSION}.jar

%files module-sox-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-sox-remote-%{__INTERNAL_VERSION}.jar

%files module-sox-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-sox-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-speech-recognition-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-speech-recognition-service-api-%{__INTERNAL_VERSION}.jar

%files module-speech-recognition-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-speech-recognition-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-static
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-static-%{__INTERNAL_VERSION}.jar

%files module-static-file-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-static-file-service-api-%{__INTERNAL_VERSION}.jar

%files module-static-file-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-static-file-service-impl-%{__INTERNAL_VERSION}.jar

%files module-textanalyzer-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textanalyzer-api-%{__INTERNAL_VERSION}.jar

%files module-textanalyzer-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textanalyzer-impl-%{__INTERNAL_VERSION}.jar

%files module-textanalyzer-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textanalyzer-remote-%{__INTERNAL_VERSION}.jar

%files module-textanalyzer-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textanalyzer-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-textextractor-tesseract
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textextractor-tesseract-%{__INTERNAL_VERSION}.jar

%files module-themes
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-themes-%{__INTERNAL_VERSION}.jar

%files module-themes-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-themes-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-userdirectory
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-userdirectory-%{__INTERNAL_VERSION}.jar

%files module-userdirectory-ldap
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-userdirectory-ldap-%{__INTERNAL_VERSION}.jar

%files module-usertracking-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-usertracking-api-%{__INTERNAL_VERSION}.jar

%files module-usertracking-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-usertracking-impl-%{__INTERNAL_VERSION}.jar

%files module-videoeditor-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videoeditor-api-%{__INTERNAL_VERSION}.jar

%files module-videoeditor-ffmpeg-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videoeditor-ffmpeg-impl-%{__INTERNAL_VERSION}.jar

%files module-videoeditor-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videoeditor-remote-%{__INTERNAL_VERSION}.jar

%files module-videoeditor-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videoeditor-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-videosegmenter-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videosegmenter-api-%{__INTERNAL_VERSION}.jar

%files module-videosegmenter-ffmpeg
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videosegmenter-ffmpeg-%{__INTERNAL_VERSION}.jar

%files module-videosegmenter-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videosegmenter-remote-%{__INTERNAL_VERSION}.jar

%files module-videosegmenter-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videosegmenter-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-webconsole
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-webconsole-%{__INTERNAL_VERSION}.jar

%files module-workflow-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workflow-service-api-%{__INTERNAL_VERSION}.jar

%files module-workflow-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workflow-service-impl-%{__INTERNAL_VERSION}.jar

%files module-workflow-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workflow-service-remote-%{__INTERNAL_VERSION}.jar

%files module-workflow-workflowoperation
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workflow-workflowoperation-%{__INTERNAL_VERSION}.jar

%files module-working-file-repository-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-api-%{__INTERNAL_VERSION}.jar

%files module-working-file-repository-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-impl-%{__INTERNAL_VERSION}.jar

%files module-working-file-repository-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-remote-%{__INTERNAL_VERSION}.jar

%files module-workspace-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workspace-api-%{__INTERNAL_VERSION}.jar

%files module-workspace-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workspace-impl-%{__INTERNAL_VERSION}.jar



### BUILD PROCESS ############################################################


%prep
%setup -q -c -a 0 -a 2
pushd opencast-matterhorn-%{__INTERNAL_VERSION}
%patch0 -p1
popd


%build
#mvn


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/matterhorn
cp -rf opencast-matterhorn-%{__INTERNAL_VERSION}/bin $RPM_BUILD_ROOT%{_datadir}/matterhorn/

# Remove unnecessary scripts
rm $RPM_BUILD_ROOT%{_datadir}/matterhorn/bin/start-matterhorn
cp -rf opencast-matterhorn-%{__INTERNAL_VERSION}/lib $RPM_BUILD_ROOT%{_datadir}/matterhorn/
#
# Maven Configuration
cp %{SOURCE3} settings.xml
sed -i "s#BUILDPATH#$(pwd)#" settings.xml
#
# Build Matterhorn
pushd opencast-matterhorn-%{__INTERNAL_VERSION}
mvn -o -s ../settings.xml clean install -Dall \
   -DdeployTo=$RPM_BUILD_ROOT%{_datadir}/matterhorn/
popd
#
# Copy other stuff
mkdir -m 775 -p ${RPM_BUILD_ROOT}/srv/matterhorn/inbox
mkdir -m 755 -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/matterhorn
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/matterhorn
mv opencast-matterhorn-%{__INTERNAL_VERSION}/etc/* ${RPM_BUILD_ROOT}%{_sysconfdir}/matterhorn/

# Install logrotate configuration
install -p -D -m 0644 %{SOURCE4} \
   %{buildroot}%{_sysconfdir}/logrotate.d/%{name}-base

# Add documentation
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/scripts/ddl/
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/licenses/
pushd opencast-matterhorn-%{__INTERNAL_VERSION}/docs/
cp licenses.txt  ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/
cp licenses/*    ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/licenses/
cp scripts/ddl/* ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/scripts/ddl/
cp -r upgrade/   ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/
popd

pushd opencast-matterhorn-%{__INTERNAL_VERSION}/docs/scripts/init/system/
# Install binaries
install -p -D -m 0755 usr-sbin-matterhorn \
      $RPM_BUILD_ROOT%{_sbindir}/matterhorn
install -p -D -m 0644 etc-matterhorn-service.conf \
      ${RPM_BUILD_ROOT}%{_sysconfdir}/matterhorn/service.conf

# Install Systemd unit file
%{?__use_systemd:install -p -D -m 0755 etc-systemd-system-matterhorn.service \
         $RPM_BUILD_ROOT%{_unitdir}/matterhorn.service}
# Install SysV-init script
%{!?__use_systemd:install -p -D -m 0755 etc-init.d-matterhorn \
         $RPM_BUILD_ROOT%{_initddir}/matterhorn}

# Install manpage
cat matterhorn.8 | gzip > matterhorn.8.gz
install -p -D -m 0644 matterhorn.8.gz \
      $RPM_BUILD_ROOT%{_mandir}/man8/matterhorn.8.gz
popd


%clean
rm -rf $RPM_BUILD_ROOT



%changelog
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
