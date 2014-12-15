%define __os_install_post %{nil}

%global  matterhorn_user          matterhorn
%global  matterhorn_group         %{matterhorn_user}

%define __INTERNAL_VERSION 1.6.0

%if 0%{?sles_version}
  %define __GST_SUFFIX -0_10
%else
  %define __GST_SUFFIX %{nil}
%endif

# Systemd or SysV-init
%define __use_systemd 0%{?fedora}%{?rhel} >= 7

%{?_matterhorn_institute: %define __MATTERHORN_INSTITUTE .%{?_matterhorn_institute} }


Name:           opencast-matterhorn16
Version:        1.6.0
Release:        1%{?__MATTERHORN_INSTITUTE}%{?dist}
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

BuildRequires: maven >= 3
BuildRequires: tar

%if 0%{?sles_version}
BuildRequires: jdk >= 1:1.6.0
%else
%if 0%{?rhel} == 6
BuildRequires: java-1.7.0-openjdk-devel >= 1:1.7.0
%else
BuildRequires: java-devel >= 1:1.7.0
%endif
%endif
Requires:      %{name}-base                 = %{__FULL_VERSION}
Requires:      %{name}-distribution-default = %{__FULL_VERSION}

BuildArch: noarch

%package base
Summary: Base package for Opencast Matterhorn
Group: Applications/Multimedia
Requires(pre): /usr/sbin/useradd

%if %{__use_systemd}
BuildRequires: systemd
%else
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
%endif

Requires:      bash
Requires:      sudo
%if 0%{?sles_version}
Requires: jdk >= 1:1.6.0
%else
Requires: java >= 1:1.7.0
%endif


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

%package distribution-capture-agent
Summary: Capture-Agent Matterhorn distribution
Group: Applications/Multimedia
Requires: %{name}-profile-capture              = %{__FULL_VERSION}
Requires: %{name}-profile-serviceregistry-stub = %{__FULL_VERSION}

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

%package distribution-demo
Summary: Demo Matterhorn distribution (All-in-one + Demo Capture Agent)
Group: Applications/Multimedia
Requires: %{name}-profile-admin           = %{__FULL_VERSION}
Requires: %{name}-profile-capture         = %{__FULL_VERSION}
Requires: %{name}-profile-directory-db    = %{__FULL_VERSION}
Requires: %{name}-profile-dist            = %{__FULL_VERSION}
Requires: %{name}-profile-engage          = %{__FULL_VERSION}
Requires: %{name}-profile-serviceregistry = %{__FULL_VERSION}
Requires: %{name}-profile-worker          = %{__FULL_VERSION}
Requires: %{name}-profile-workspace       = %{__FULL_VERSION}

%package third-party-tools
Summary: All required third party tools for Matterhorn
Group: Applications/Multimedia
%if 0%{?sles_version}
BuildRequires: jdk >= 1:1.6.0
%else
BuildRequires: java >= 1:1.6.0
#Requires: java-devel >= 1:1.6.0
%endif
#Requires: maven >= 3
Requires: ffmpeg >= 1.1
Requires: gstreamer%{__GST_SUFFIX}
Requires: gstreamer%{__GST_SUFFIX}-ffmpeg
Requires: gstreamer%{__GST_SUFFIX}-plugins-base
Requires: gstreamer%{__GST_SUFFIX}-plugins-good
Requires: gstreamer%{__GST_SUFFIX}-plugins-ugly
%if 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version}
BuildRequires: gstreamer-plugins-bad-free
%endif
Requires: jv4linfo >= 0.2.1
Requires: mediainfo >= 0.7.35
Requires: qt_sbtl_embedder >= 0.4
Requires: tesseract >= 3
Requires: v4l-utils
Requires: gnonlin0.10

%package profile-admin
Summary: Admin profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-admin-ui                            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-authorization-manager               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-authorization-xacml                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-caption-api                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-caption-remote                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-capture-admin-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-capture-admin-service-impl          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-composer-service-api                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-conductor                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-api            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-episode-service-api                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-episode-service-filesystem          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-episode-service-impl                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-fileupload                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-gstreamer-service-api               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-ingest-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-ingest-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-inspection-service-api              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-lti                                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mediapackage-manipulator            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mediapackage-ui                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata                            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-scheduler-api                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-scheduler-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-silencedetection-api                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-smil-api                            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-smil-impl                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-solr                                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-speech-recognition-service-api      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-static-mod                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-sox-api                             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textanalyzer-api                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videoeditor-api                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videosegmenter-api                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workflow-service-api                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workflow-service-impl               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-working-file-repository-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                       = %{__FULL_VERSION}

%package profile-analytics
Summary: Analytics profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-static-mod         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-usertracking-api   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-usertracking-impl  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api      = %{__FULL_VERSION}

%package profile-export-admin
Summary: Export-admin profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-gstreamer-service-api    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-gstreamer-service-remote = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-serviceregistry          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-static-mod               = %{__FULL_VERSION}

%package profile-export-worker
Summary: Export-worker profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-gstreamer-service-api  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-gstreamer-service-impl = %{__FULL_VERSION}

%package profile-export-all-in-one
Summary: Export-all-in-one profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-gstreamer-service-api  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-gstreamer-service-impl = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-serviceregistry        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-static-mod             = %{__FULL_VERSION}

%package profile-ingest
Summary: Ingest profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-ingest-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-ingest-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-scheduler-api                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-scheduler-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-impl                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-serviceregistry                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workflow-service-api                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-working-file-repository-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                       = %{__FULL_VERSION}

%package profile-ingest-standalone
Summary: Ingest-standalone profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common                               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-ingest-service-api                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-ingest-service-impl                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-scheduler-api                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-scheduler-remote                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-remote                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-serviceregistry                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workflow-service-api                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workflow-service-remote              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-working-file-repository-service-api  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-working-file-repository-service-impl = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-impl                       = %{__FULL_VERSION}

%package profile-dist
Summary: Dist profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-dist-stub
Conflicts: %{name}-profile-dist-standalone
Requires: %{name}-module-matterhorn-authorization-xacml            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-acl       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-api       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-download  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-streaming = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-api        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-youtube    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-impl            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-static-mod                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workflow-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                  = %{__FULL_VERSION}

%package profile-dist-standalone
Summary: Dist profile without series service for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-dist-stub
Conflicts: %{name}-profile-dist
Requires: %{name}-module-matterhorn-authorization-xacml            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-acl       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-api       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-download  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-streaming = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-api        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-youtube    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-remote          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-static-mod                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workflow-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                  = %{__FULL_VERSION}

%package profile-dist-stub
Summary: Dist-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-dist
Conflicts: %{name}-profile-dist-standalone
Requires: %{name}-module-matterhorn-authorization-xacml                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-acl-remote       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-api              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-download-remote  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-streaming-remote = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-api               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-youtube-remote    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                         = %{__FULL_VERSION}

%package profile-engage
Summary: Engage profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-annotation-api       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-annotation-impl      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-authorization-xacml  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-engage-ui            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-lti                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-impl  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-api   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-feeds = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-impl  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-solr                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-usertracking-api     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-usertracking-impl    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api        = %{__FULL_VERSION}

%package profile-engage-standalone
Summary: Engage-standalone profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-annotation-api        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-annotation-impl       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-authorization-xacml   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-engage-ui             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-lti                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-remote = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-api    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-feeds  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-impl   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-solr                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-usertracking-api      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-usertracking-impl     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api         = %{__FULL_VERSION}

%package profile-engage-stub
Summary: Engage-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-authorization-xacml                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-api              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-download-remote  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-distribution-service-streaming-remote = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-lti                                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-api               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-publication-service-youtube-remote    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-api                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-remote                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                         = %{__FULL_VERSION}

%package profile-worker
Summary: Worker profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-worker-stub
Requires: %{name}-module-matterhorn-authorization-xacml            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-caption-api                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-caption-impl                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-composer-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-composer-ffmpeg                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dictionary-api                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dictionary-regexp              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-inspection-service-api         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-inspection-service-ffmpeg      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-impl            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-silencedetection-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-silencedetection-impl          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-smil-api                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-smil-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-sox-api                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-sox-impl                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-speech-recognition-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textanalyzer-api               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textanalyzer-impl              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textextractor-tesseract        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videoeditor-api                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videoeditor-impl               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videosegmenter-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videosegmenter-impl            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                  = %{__FULL_VERSION}

%package profile-worker-standalone
Summary: Worker profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-worker-stub
Requires: %{name}-module-matterhorn-authorization-xacml            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-caption-api                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-caption-impl                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-composer-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-composer-ffmpeg                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dictionary-api                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dictionary-regexp              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-inspection-service-api         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-inspection-service-ffmpeg      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-remote          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-silencedetection-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-silencedetection-impl          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-smil-api                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-smil-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-sox-api                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-sox-impl                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-speech-recognition-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textanalyzer-api               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textanalyzer-impl              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textextractor-tesseract        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory                  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videoeditor-api                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videoeditor-impl               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videosegmenter-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videosegmenter-impl            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                  = %{__FULL_VERSION}

%package profile-worker-stub
Summary: Worker-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-worker
Requires: %{name}-module-matterhorn-authorization-xacml            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-caption-api                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-caption-remote                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-common                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-composer-service-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-composer-service-remote        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-inspection-service-api         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-inspection-service-remote      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-silencedetection-api           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-silencedetection-remote        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-smil-api                       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-smil-impl                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-sox-api                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-sox-remote                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-speech-recognition-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textanalyzer-api               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-textanalyzer-remote            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videoeditor-api                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videoeditor-remote             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videosegmenter-api             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-videosegmenter-remote          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                     = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api = %{__FULL_VERSION}

%package profile-workspace
Summary: Workspace profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-workspace-stub
Requires: %{name}-module-matterhorn-common                               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-working-file-repository-service-api  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-working-file-repository-service-impl = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-impl                       = %{__FULL_VERSION}

%package profile-workspace-stub
Summary: Workspace-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-workspace
Requires: %{name}-module-matterhorn-common                                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-working-file-repository-service-api    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-working-file-repository-service-remote = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api                          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-impl                         = %{__FULL_VERSION}

%package profile-serviceregistry
Summary: Serviceregistry profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-serviceregistry-stub
Requires: %{name}-module-matterhorn-common          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json            = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-serviceregistry = %{__FULL_VERSION}

%package profile-serviceregistry-stub
Summary: Serviceregistry-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-serviceregistry
Requires: %{name}-module-matterhorn-common                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                   = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-serviceregistry-remote = %{__FULL_VERSION}

%package profile-oaipmh
Summary: Oaipmh profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common              = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-api  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-search-service-impl = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-impl = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-solr                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore          = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-mpeg7               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-oaipmh              = %{__FULL_VERSION}

%package profile-directory-db
Summary: Directory-db profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dataloader         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-db                 = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-dublincore         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-metadata-api       = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-series-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-workspace-api      = %{__FULL_VERSION}

%package profile-directory-ldap
Summary: Directory-ldap profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common             = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json               = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-security-ldap      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-userdirectory-ldap = %{__FULL_VERSION}

%package profile-directory-cas
Summary: Directory-cas profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-security-cas = %{__FULL_VERSION}

%package profile-directory-openid
Summary: Directory-openid profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-security-openid = %{__FULL_VERSION}

%package profile-directory-shibboleth
Summary: Directory-shibboleth profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-security-shibboleth = %{__FULL_VERSION}

%package profile-capture
Summary: Capture profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-common                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-json                      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-kernel                    = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-capture-admin-service-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-capture-agent-api         = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-capture-agent-impl        = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-confidence-monitoring-ui  = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-dependencies      = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-runtime-info-ui           = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-static-mod                = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-webconsole                = %{__FULL_VERSION}

%package profile-server-management
Summary: Server management profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Group: Applications/Multimedia
Requires: %{name}-module-matterhorn-manager-api = %{__FULL_VERSION}
Requires: %{name}-module-matterhorn-manager-impl = %{__FULL_VERSION}

%package module-matterhorn-videosegmenter-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-videosegmenter-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-engage-ui
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-engage-ui module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-videosegmenter-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-videosegmenter-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-workflow-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-workflow-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-ingest-service-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-ingest-service-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-scheduler-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-scheduler-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-episode-service-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-episode-service-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-workspace-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-workspace-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-textextractor-tesseract
Requires: %{name}-base = %{__FULL_VERSION}
Requires: tesseract >= 3
BuildRequires: tesseract >= 3
BuildRequires: tesseract-langpack-deu >= 3
Summary: Matterhorn-textextractor-tesseract module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-episode-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-episode-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-dictionary-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-dictionary-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-mpeg7
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-mpeg7 module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-publication-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-publication-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-publication-service-youtube
Requires: %{name}-base = %{__FULL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-publication-service-youtube-remote
Provides: %{name}-module-matterhorn-distribution-service-youtube = %{__FULL_VERSION}
Obsoletes: %{name}-module-matterhorn-distribution-service-youtube < %{__FULL_VERSION}
Summary: Matterhorn-publication-service-youtube module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-publication-service-youtube-remote
Requires: %{name}-base = %{__FULL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-publication-service-youtube
Provides: %{name}-module-matterhorn-distribution-service-youtube-remote = %{__FULL_VERSION}
Obsoletes: %{name}-module-matterhorn-distribution-service-youtube-remote < %{__FULL_VERSION}
Summary: Publication-service-youtube-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-search-service-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-search-service-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-working-file-repository-service-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Working-file-repository-service-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-inspection-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-inspection-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-composer-service-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-composer-service-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-composer-ffmpeg
Requires: %{name}-base = %{__FULL_VERSION}
Requires: qt_sbtl_embedder >= 0.4
Requires: ffmpeg >= 1.1
BuildRequires: ffmpeg >= 1.1
Summary: Matterhorn-composer-ffmpeg module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-static-mod
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-static module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-distribution-service-acl
Requires: %{name}-base = %{__FULL_VERSION}
# You cannot install remote and non-remote at the same time
Conflicts: %{name}-module-matterhorn-distribution-service-acl-remote
Summary: Matterhorn-distribution-service-acl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-serviceregistry-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-serviceregistry-remote module for Opencast Matterhorn
Conflicts: %{name}-module-matterhorn-serviceregistry-impl
Group: Applications/Multimedia

%package module-matterhorn-search-service-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-search-service-impl module for Opencast Matterhorn
Conflicts: %{name}-module-matterhorn-serviceregistry-remote
Group: Applications/Multimedia

%package module-matterhorn-serviceregistry
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-serviceregistry module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-distribution-service-download-remote
Requires: %{name}-base = %{__FULL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-download
Summary: Distribution-service-download-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-usertracking-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-usertracking-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-textanalyzer-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-textanalyzer-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-workflow-service-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-workflow-service-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-working-file-repository-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Working-file-repository-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-oaipmh
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-oaipmh module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-capture-admin-service-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-capture-admin-service-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-dictionary-regexp
Requires: %{name}-base = %{__FULL_VERSION}
Summary: RegExp based DictionaryService implementation for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-dictionary-hunspell
Requires: %{name}-base = %{__FULL_VERSION}
BuildRequires: hunspell >= 1.2.8
Requires: hunspell >= 1.2.8
Summary: Hunspell based DictionaryService implementation for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-dictionary-none
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Pass-through DictionaryService implementation for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-ingest-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-ingest-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-gstreamer-service-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-gstreamer-service-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-inspection-service-remote
Requires: %{name}-base = %{__FULL_VERSION}
Conflicts: %{name}-module-matterhorn-inspection-service-ffmpeg
Conflicts: %{name}-module-matterhorn-inspection-service-mediainfo
Summary: Matterhorn-inspection-service-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-episode-service-filesystem
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-episode-service-filesystem module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-fileupload
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-fileupload module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-series-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-series-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-userdirectory
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-userdirectory module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-capture-admin-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-capture-admin-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-json
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-json module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-admin-ui
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-admin-ui module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-gstreamer-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-gstreamer-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-workspace-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-workspace-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-videosegmenter-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-videosegmenter-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-confidence-monitoring-ui
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-confidence-monitoring-ui module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-db
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-db module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-distribution-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-distribution-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-dublincore
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-dublincore module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-distribution-service-acl-remote
Requires: %{name}-base = %{__FULL_VERSION}
# You cannot install remote and non-remote at the same time
Conflicts: %{name}-module-matterhorn-distribution-service-acl
Summary: Distribution-service-acl-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-series-service-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-series-service-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-composer-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-composer-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-solr
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-solr module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-series-service-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-series-service-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-distribution-service-download
Requires: %{name}-base = %{__FULL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-download-remote
Summary: Matterhorn-distribution-service-download module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-mediapackage-ui
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-mediapackage-ui module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-scheduler-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-scheduler-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-textanalyzer-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-textanalyzer-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-security-cas
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-security-cas module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-security-openid
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-security-openid module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-distribution-service-streaming
Requires: %{name}-base = %{__FULL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-streaming-remote
Summary: Matterhorn-distribution-service-streaming module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-caption-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-caption-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-runtime-info-ui
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-runtime-info-ui module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-metadata
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-metadata module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-working-file-repository-service-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-working-file-repository-service-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-mediapackage-manipulator
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-mediapackage-manipulator module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-metadata-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-metadata-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-distribution-service-streaming-remote
Requires: %{name}-base = %{__FULL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-streaming
Summary: Matterhorn-distribution-service-streaming-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-common
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-common module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-gstreamer-service-impl
Requires: %{name}-base = %{__FULL_VERSION}
Requires: gstreamer%{__GST_SUFFIX}
Requires: gstreamer%{__GST_SUFFIX}-plugins-base
Summary: Matterhorn-gstreamer-service-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-dataloader
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-dataloader module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-kernel
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-kernel module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-webconsole
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-webconsole module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-usertracking-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-usertracking-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-search-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-search-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-runtime-dependencies
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-runtime-dependencies module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-search-service-feeds
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-search-service-feeds module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-inspection-service-mediainfo
Requires: %{name}-base = %{__FULL_VERSION}
Requires:     mediainfo >= 0.7.35
# There can only be one inspection service
Conflicts: %{name}-module-matterhorn-inspection-service-ffmpeg
Conflicts: %{name}-module-matterhorn-inspection-service-remote
Summary: Matterhorn-inspection-service-mediainfo module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-inspection-service-ffmpeg
Requires: %{name}-base = %{__FULL_VERSION}
Requires: ffmpeg >= 1.1
BuildRequires: ffmpeg >= 1.1
# There can only be one inspection service
Conflicts: %{name}-module-matterhorn-inspection-service-mediainfo
Conflicts: %{name}-module-matterhorn-inspection-service-remote
Summary: FFmpeg (ffprobe) based inspection-service module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-conductor
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-conductor module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-caption-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-caption-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-textanalyzer-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-textanalyzer-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-userdirectory-ldap
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-userdirectory-ldap module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-capture-agent-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-capture-agent-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-annotation-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-annotation-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-authorization-xacml
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-authorization-xacml module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-caption-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-caption-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-security-ldap
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-security-ldap module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-capture-agent-impl
BuildRequires: gstreamer%{__GST_SUFFIX}
BuildRequires: gstreamer%{__GST_SUFFIX}-plugins-base
BuildRequires: gstreamer%{__GST_SUFFIX}-plugins-good
BuildRequires: gstreamer%{__GST_SUFFIX}-plugins-ugly
BuildRequires: gstreamer%{__GST_SUFFIX}-ffmpeg
Requires: gstreamer%{__GST_SUFFIX}
Requires: gstreamer%{__GST_SUFFIX}-plugins-base
Requires: gstreamer%{__GST_SUFFIX}-plugins-good
Requires: gstreamer%{__GST_SUFFIX}-plugins-ugly
Requires: gstreamer%{__GST_SUFFIX}-ffmpeg
%if 0%{?fedora}%{?rhel}
BuildRequires: gstreamer-plugins-bad-free
%endif
Requires: jv4linfo >= 0.2.1
Requires: v4l-utils
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-capture-agent-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-lti
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-lti module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-speech-recognition-service-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-speech-recognition-service-api module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-annotation-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-annotation-impl module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-scheduler-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-scheduler-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-workflow-service-remote
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Matterhorn-workflow-service-remote module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-authorization-manager
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Authorization Manager Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-security-shibboleth
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Shibboleth Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-manager-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Configuration Manager API Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-manager-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Configuration Manager Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-silencedetection-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Silencedetection API Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-silencedetection-remote
Requires: %{name}-base = %{__FULL_VERSION}
Conflicts: %{name}-module-matterhorn-silencedetection-impl
Summary: Remote Silencedetection Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-silencedetection-impl
Requires: %{name}-base = %{__FULL_VERSION}
Conflicts: %{name}-module-matterhorn-silencedetection-remote
BuildRequires: gstreamer%{__GST_SUFFIX}
BuildRequires: gstreamer%{__GST_SUFFIX}-plugins-base
BuildRequires: gstreamer%{__GST_SUFFIX}-plugins-good
Requires: gstreamer%{__GST_SUFFIX}
Requires: gstreamer%{__GST_SUFFIX}-plugins-base
Requires: gstreamer%{__GST_SUFFIX}-plugins-good
Requires: gstreamer%{__GST_SUFFIX}-plugins-ugly
Requires: gstreamer%{__GST_SUFFIX}-ffmpeg
%if 0%{?fedora}%{?rhel}
Requires: gstreamer-plugins-bad-free
%endif
Summary: Silencedetection Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-smil-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Smil API Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-smil-impl
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Smil Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-sox-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: SoX API Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-sox-remote
Requires: %{name}-base = %{__FULL_VERSION}
Conflicts: %{name}-module-matterhorn-sox-impl
Summary: Remote SoX Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-sox-impl
Requires: %{name}-base = %{__FULL_VERSION}
Requires: sox >= 14
Conflicts: %{name}-module-matterhorn-sox-remote
Summary: SoX Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-videoeditor-api
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Videoeditor API Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-videoeditor-remote
Requires: %{name}-base = %{__FULL_VERSION}
Conflicts: %{name}-module-matterhorn-videoeditor-impl
Summary: Remote Videoeditor Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-videoeditor-impl
Requires: %{name}-base = %{__FULL_VERSION}
Conflicts: %{name}-module-matterhorn-videoeditor-remote
BuildRequires: gstreamer%{__GST_SUFFIX}
BuildRequires: gstreamer%{__GST_SUFFIX}-plugins-base
BuildRequires: gstreamer%{__GST_SUFFIX}-plugins-good
BuildRequires: gstreamer%{__GST_SUFFIX}-plugins-ugly
BuildRequires: gstreamer%{__GST_SUFFIX}-ffmpeg
BuildRequires: gnonlin0.10
Requires: gnonlin0.10
Requires: gstreamer%{__GST_SUFFIX}
Requires: gstreamer%{__GST_SUFFIX}-plugins-base
Requires: gstreamer%{__GST_SUFFIX}-plugins-good
Requires: gstreamer%{__GST_SUFFIX}-plugins-ugly
Requires: gstreamer%{__GST_SUFFIX}-ffmpeg
%if 0%{?fedora}%{?rhel}
Requires: gstreamer-plugins-bad-free
%endif
Summary: Videoeditor Module for Opencast Matterhorn
Group: Applications/Multimedia

%package module-matterhorn-migration
Requires: %{name}-base = %{__FULL_VERSION}
Summary: Migration Module for Opencast Matterhorn
Group: Applications/Multimedia



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

%description base
Basic elements of each Opencast Matterhorn distribution.

%description distribution-default
Default distribution of Opencast Matterhorn components.

This is the default package containing all three main profiles (Admin, Worker,
Engage). This installation is only recommended if you don't have many videos
that you want to ingest and you don't expect many viewers. This perfect for
first test and to get an impression of Matterhorn as it works out of the box
and does not need much configuration.


%description distribution-capture-agent
Capture-Agent distribution of Opencast Matterhorn components.

This package will install the Matterhorn reference Capture Agent with remote
service registry.


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


%description distribution-demo
All-in-one Matterhorn distribution with attached demo refernece capture agent.
This package is not meant for production use.


%description third-party-tools
This package will pull in all required third party tools for the core
components of Opencast Matterhorn.


%description profile-admin
admin profile for Opencast Matterhorn

%description profile-analytics
analytics profile for Opencast Matterhorn

%description profile-export-admin
export-admin profile for Opencast Matterhorn

%description profile-export-worker
export-worker profile for Opencast Matterhorn

%description profile-export-all-in-one
export-all-in-one profile for Opencast Matterhorn

%description profile-ingest
ingest profile for Opencast Matterhorn

%description profile-ingest-standalone
Ingest-standalone profile for Opencast Matterhorn

%description profile-dist
dist profile for Opencast Matterhorn

%description profile-dist-standalone
dist profile without series-service-imple module for engage-standalone
distribution of Opencast Matterhorn

%description profile-dist-stub
dist-stub profile for Opencast Matterhorn

%description profile-engage
engage profile for Opencast Matterhorn

%description profile-engage-standalone
engage-standalone profile for Opencast Matterhorn

%description profile-engage-stub
engage-stub profile for Opencast Matterhorn

%description profile-worker
worker profile for Opencast Matterhorn

%description profile-worker-standalone
Worker profile for Opencast Matterhorn

%description profile-worker-stub
worker-stub profile for Opencast Matterhorn

%description profile-workspace
workspace profile for Opencast Matterhorn

%description profile-workspace-stub
workspace-stub profile for Opencast Matterhorn

%description profile-serviceregistry
serviceregistry profile for Opencast Matterhorn

%description profile-serviceregistry-stub
serviceregistry-stub profile for Opencast Matterhorn

%description profile-oaipmh
oaipmh profile for Opencast Matterhorn

%description profile-directory-db
directory-db profile for Opencast Matterhorn

%description profile-directory-ldap
directory-ldap profile for Opencast Matterhorn

%description profile-directory-cas
directory-cas profile for Opencast Matterhorn

%description profile-directory-openid
directory-openid profile for Opencast Matterhorn

%description profile-directory-shibboleth
directory-shibboleth profile for Opencast Matterhorn

%description profile-server-management
server-management profile for Opencast Matterhorn

%description profile-capture
capture profile for Opencast Matterhorn

%description module-matterhorn-videosegmenter-api
Matterhorn-videosegmenter-api module for Opencast Matterhorn

%description module-matterhorn-engage-ui
Matterhorn-engage-ui module for Opencast Matterhorn

%description module-matterhorn-videosegmenter-remote
Matterhorn-videosegmenter-remote module for Opencast Matterhorn

%description module-matterhorn-workflow-service-api
Matterhorn-workflow-service-api module for Opencast Matterhorn

%description module-matterhorn-ingest-service-impl
Matterhorn-ingest-service-impl module for Opencast Matterhorn

%description module-matterhorn-scheduler-api
Matterhorn-scheduler-api module for Opencast Matterhorn

%description module-matterhorn-episode-service-impl
Matterhorn-episode-service-impl module for Opencast Matterhorn

%description module-matterhorn-workspace-api
Matterhorn-workspace-api module for Opencast Matterhorn

%description module-matterhorn-textextractor-tesseract
Matterhorn-textextractor-tesseract module for Opencast Matterhorn

%description module-matterhorn-episode-service-api
Matterhorn-episode-service-api module for Opencast Matterhorn

%description module-matterhorn-dictionary-api
Matterhorn-dictionary-api module for Opencast Matterhorn

%description module-matterhorn-mpeg7
Matterhorn-mpeg7 module for Opencast Matterhorn

%description module-matterhorn-publication-service-api
Matterhorn-publication-service-api module for Opencast Matterhorn

%description module-matterhorn-publication-service-youtube
Matterhorn-publication-service-youtube module for Opencast Matterhorn

%description module-matterhorn-publication-service-youtube-remote
Matterhorn-publication-service-youtube-remote module for Opencast Matterhorn

%description module-matterhorn-search-service-remote
Matterhorn-search-service-remote module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-impl
Matterhorn-working-file-repository-service-impl module for Opencast Matterhorn

%description module-matterhorn-inspection-service-api
Matterhorn-inspection-service-api module for Opencast Matterhorn

%description module-matterhorn-composer-service-remote
Matterhorn-composer-service-remote module for Opencast Matterhorn

%description module-matterhorn-composer-ffmpeg
Matterhorn-composer-ffmpeg module for Opencast Matterhorn

%description module-matterhorn-static-mod
Matterhorn-static module for Opencast Matterhorn

%description module-matterhorn-distribution-service-acl
Matterhorn-distribution-service-acl module for Opencast Matterhorn

%description module-matterhorn-serviceregistry-remote
Matterhorn-serviceregistry-remote module for Opencast Matterhorn

%description module-matterhorn-search-service-impl
Matterhorn-search-service-impl module for Opencast Matterhorn

%description module-matterhorn-serviceregistry
Matterhorn-serviceregistry module for Opencast Matterhorn

%description module-matterhorn-distribution-service-download-remote
Matterhorn-distribution-service-download-remote module for Opencast Matterhorn

%description module-matterhorn-usertracking-impl
Matterhorn-usertracking-impl module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-impl
Matterhorn-textanalyzer-impl module for Opencast Matterhorn

%description module-matterhorn-workflow-service-impl
Matterhorn-workflow-service-impl module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-api
Matterhorn-working-file-repository-service-api module for Opencast Matterhorn

%description module-matterhorn-oaipmh
Matterhorn-oaipmh module for Opencast Matterhorn

%description module-matterhorn-capture-admin-service-impl
Matterhorn-capture-admin-service-impl module for Opencast Matterhorn

%description module-matterhorn-dictionary-regexp
Summary: RegExp based DictionaryService implementation for Opencast Matterhorn

%description module-matterhorn-dictionary-hunspell
Summary: Hunspell based DictionaryService implementation for Opencast Matterhorn

%description module-matterhorn-dictionary-none
Summary: Pass-through DictionaryService implementation for Opencast Matterhorn

%description module-matterhorn-ingest-service-api
Matterhorn-ingest-service-api module for Opencast Matterhorn

%description module-matterhorn-gstreamer-service-remote
Matterhorn-gstreamer-service-remote module for Opencast Matterhorn

%description module-matterhorn-inspection-service-remote
Matterhorn-inspection-service-remote module for Opencast Matterhorn

%description module-matterhorn-episode-service-filesystem
Matterhorn-episode-service-filesystem module for Opencast Matterhorn

%description module-matterhorn-fileupload
Matterhorn-fileupload module for Opencast Matterhorn

%description module-matterhorn-series-service-api
Matterhorn-series-service-api module for Opencast Matterhorn

%description module-matterhorn-userdirectory
Matterhorn-userdirectory module for Opencast Matterhorn

%description module-matterhorn-capture-admin-service-api
Matterhorn-capture-admin-service-api module for Opencast Matterhorn

%description module-matterhorn-json
Matterhorn-json module for Opencast Matterhorn

%description module-matterhorn-admin-ui
Matterhorn-admin-ui module for Opencast Matterhorn

%description module-matterhorn-gstreamer-service-api
Matterhorn-gstreamer-service-api module for Opencast Matterhorn

%description module-matterhorn-workspace-impl
Matterhorn-workspace-impl module for Opencast Matterhorn

%description module-matterhorn-videosegmenter-impl
Matterhorn-videosegmenter-impl module for Opencast Matterhorn

%description module-matterhorn-confidence-monitoring-ui
Matterhorn-confidence-monitoring-ui module for Opencast Matterhorn

%description module-matterhorn-db
Matterhorn-db module for Opencast Matterhorn

%description module-matterhorn-distribution-service-api
Matterhorn-distribution-service-api module for Opencast Matterhorn

%description module-matterhorn-dublincore
Matterhorn-dublincore module for Opencast Matterhorn

%description module-matterhorn-distribution-service-acl-remote
Matterhorn-distribution-service-acl-remote module for Opencast Matterhorn

%description module-matterhorn-series-service-remote
Matterhorn-series-service-remote module for Opencast Matterhorn

%description module-matterhorn-composer-service-api
Matterhorn-composer-service-api module for Opencast Matterhorn

%description module-matterhorn-solr
Matterhorn-solr module for Opencast Matterhorn

%description module-matterhorn-series-service-impl
Matterhorn-series-service-impl module for Opencast Matterhorn

%description module-matterhorn-distribution-service-download
Matterhorn-distribution-service-download module for Opencast Matterhorn

%description module-matterhorn-mediapackage-ui
Matterhorn-mediapackage-ui module for Opencast Matterhorn

%description module-matterhorn-scheduler-impl
Matterhorn-scheduler-impl module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-remote
Matterhorn-textanalyzer-remote module for Opencast Matterhorn

%description module-matterhorn-security-cas
Matterhorn-security-cas module for Opencast Matterhorn

%description module-matterhorn-security-openid
Matterhorn-security-openid module for Opencast Matterhorn

%description module-matterhorn-distribution-service-streaming
Matterhorn-distribution-service-streaming module for Opencast Matterhorn

%description module-matterhorn-caption-api
Matterhorn-caption-api module for Opencast Matterhorn

%description module-matterhorn-runtime-info-ui
Matterhorn-runtime-info-ui module for Opencast Matterhorn

%description module-matterhorn-metadata
Matterhorn-metadata module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-remote
Matterhorn-working-file-repository-service-remote module for Opencast Matterhorn

%description module-matterhorn-mediapackage-manipulator
Matterhorn-mediapackage-manipulator module for Opencast Matterhorn

%description module-matterhorn-metadata-api
Matterhorn-metadata-api module for Opencast Matterhorn

%description module-matterhorn-distribution-service-streaming-remote
Matterhorn-distribution-service-streaming-remote module for Opencast Matterhorn

%description module-matterhorn-common
Matterhorn-common module for Opencast Matterhorn

%description module-matterhorn-gstreamer-service-impl
Matterhorn-gstreamer-service-impl module for Opencast Matterhorn

%description module-matterhorn-dataloader
Matterhorn-dataloader module for Opencast Matterhorn

%description module-matterhorn-kernel
Matterhorn-kernel module for Opencast Matterhorn

%description module-matterhorn-webconsole
Matterhorn-webconsole module for Opencast Matterhorn

%description module-matterhorn-usertracking-api
Matterhorn-usertracking-api module for Opencast Matterhorn

%description module-matterhorn-search-service-api
Matterhorn-search-service-api module for Opencast Matterhorn

%description module-matterhorn-runtime-dependencies
Matterhorn-runtime-dependencies module for Opencast Matterhorn

%description module-matterhorn-search-service-feeds
Matterhorn-search-service-feeds module for Opencast Matterhorn

%description module-matterhorn-inspection-service-mediainfo
Matterhorn-inspection-service-mediainfo module for Opencast Matterhorn based on mediainfo

%description module-matterhorn-inspection-service-ffmpeg
FFmpeg (ffprobe) based inspection-service module for Opencast Matterhorn

%description module-matterhorn-conductor
Matterhorn-conductor module for Opencast Matterhorn

%description module-matterhorn-caption-remote
Matterhorn-caption-remote module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-api
Matterhorn-textanalyzer-api module for Opencast Matterhorn

%description module-matterhorn-userdirectory-ldap
Matterhorn-userdirectory-ldap module for Opencast Matterhorn

%description module-matterhorn-capture-agent-api
Matterhorn-capture-agent-api module for Opencast Matterhorn

%description module-matterhorn-annotation-api
Matterhorn-annotation-api module for Opencast Matterhorn

%description module-matterhorn-authorization-xacml
Matterhorn-authorization-xacml module for Opencast Matterhorn

%description module-matterhorn-caption-impl
Matterhorn-caption-impl module for Opencast Matterhorn

%description module-matterhorn-security-ldap
Matterhorn-security-ldap module for Opencast Matterhorn

%description module-matterhorn-capture-agent-impl
Matterhorn-capture-agent-impl module for Opencast Matterhorn

%description module-matterhorn-lti
Matterhorn-lti module for Opencast Matterhorn

%description module-matterhorn-speech-recognition-service-api
Matterhorn-speech-recognition-service-api module for Opencast Matterhorn

%description module-matterhorn-annotation-impl
Matterhorn-annotation-impl module for Opencast Matterhorn

%description module-matterhorn-scheduler-remote
Matterhorn-scheduler-remote module for Opencast Matterhorn

%description module-matterhorn-workflow-service-remote
Matterhorn-workflow-service-remote module for Opencast Matterhorn

%description module-matterhorn-authorization-manager
Authorization Manager Module for Opencast Matterhorn

%description module-matterhorn-security-shibboleth
Shibboleth Module for Opencast Matterhorn

%description module-matterhorn-manager-api
Configuration Manager API Module for Opencast Matterhorn

%description module-matterhorn-manager-impl
Configuration Manager Module for Opencast Matterhorn

%description module-matterhorn-silencedetection-api
Silencedetection API Module for Opencast Matterhorn

%description module-matterhorn-silencedetection-remote
Silencedetection Remote Module for Opencast Matterhorn

%description module-matterhorn-silencedetection-impl
Silencedetection Module for Opencast Matterhorn

%description module-matterhorn-smil-api
Smil API Module for Opencast Matterhorn

%description module-matterhorn-smil-impl
Smil Module for Opencast Matterhorn

%description module-matterhorn-sox-api
SoX API Module for Opencast Matterhorn

%description module-matterhorn-sox-impl
SoX Module for Opencast Matterhorn

%description module-matterhorn-sox-remote
Remote SoX Module for Opencast Matterhorn

%description module-matterhorn-videoeditor-api
Videoeditor API Module for Opencast Matterhorn

%description module-matterhorn-videoeditor-remote
Remote Videoeditor Module for Opencast Matterhorn

%description module-matterhorn-videoeditor-impl
Videoeditor Module for Opencast Matterhorn

%description module-matterhorn-migration
Migration Module for Opencast Matterhorn




%files module-matterhorn-videosegmenter-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videosegmenter-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-engage-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-videosegmenter-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videosegmenter-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workflow-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workflow-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-ingest-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-ingest-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-scheduler-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-scheduler-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-episode-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-episode-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workspace-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workspace-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-textextractor-tesseract
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textextractor-tesseract-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-episode-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-episode-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dictionary-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-mpeg7
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-mpeg7-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-publication-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-publication-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-publication-service-youtube
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-publication-service-youtube-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-publication-service-youtube-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-publication-service-youtube-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-search-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-working-file-repository-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-inspection-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-composer-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-composer-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-composer-ffmpeg
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-composer-ffmpeg-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-static-mod
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-static-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-acl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-acl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-serviceregistry-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-serviceregistry-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-search-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-serviceregistry
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-serviceregistry-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-download-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-download-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-usertracking-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-usertracking-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-textanalyzer-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textanalyzer-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workflow-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workflow-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-working-file-repository-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-oaipmh
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-oaipmh-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-capture-admin-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-capture-admin-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dictionary-regexp
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-regexp-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dictionary-hunspell
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-hunspell-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dictionary-none
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-none-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-ingest-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-ingest-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-gstreamer-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-inspection-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-episode-service-filesystem
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-episode-service-filesystem-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-fileupload
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-fileupload-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-series-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-series-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-userdirectory
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-userdirectory-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-capture-admin-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-capture-admin-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-json
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-json-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-admin-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-admin-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-gstreamer-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workspace-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workspace-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-videosegmenter-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videosegmenter-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-confidence-monitoring-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-confidence-monitoring-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-db
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-db-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dublincore
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dublincore-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-acl-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-acl-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-series-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-series-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-composer-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-composer-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-solr
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-solr-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-series-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-series-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-download
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-download-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-mediapackage-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-mediapackage-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-scheduler-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-scheduler-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-textanalyzer-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textanalyzer-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-security-cas
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-security-cas-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-security-openid
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-security-openid-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-streaming
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-streaming-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-caption-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-caption-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-runtime-info-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-runtime-info-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-metadata
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-metadata-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-working-file-repository-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-mediapackage-manipulator
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-mediapackage-manipulator-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-metadata-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-metadata-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-streaming-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-distribution-service-streaming-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-common
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-common-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-gstreamer-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dataloader
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dataloader-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-kernel
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-kernel-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-webconsole
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-webconsole-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-usertracking-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-usertracking-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-search-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-runtime-dependencies
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/ext

%files module-matterhorn-search-service-feeds
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-search-service-feeds-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-inspection-service-mediainfo
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-inspection-service-ffmpeg
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-service-ffmpeg-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-conductor
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-conductor-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-caption-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-caption-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-textanalyzer-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-textanalyzer-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-userdirectory-ldap
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-userdirectory-ldap-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-capture-agent-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-capture-agent-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-annotation-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-annotation-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-authorization-xacml
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-authorization-xacml-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-caption-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-caption-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-security-ldap
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-security-ldap-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-capture-agent-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-capture-agent-impl-%{__INTERNAL_VERSION}.jar
# This directory contains the sample files for the demo capture agent
/srv/matterhorn/samples

%files module-matterhorn-lti
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-lti-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-speech-recognition-service-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-speech-recognition-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-annotation-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-annotation-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-scheduler-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-scheduler-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workflow-service-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workflow-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-authorization-manager
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-authorization-manager-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-security-shibboleth
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-security-shibboleth-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-manager-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-manager-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-manager-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-manager-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-silencedetection-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-silencedetection-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-silencedetection-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-silencedetection-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-silencedetection-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-silencedetection-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-smil-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-smil-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-smil-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-smil-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-sox-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-sox-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-sox-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-sox-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-sox-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-sox-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-videoeditor-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videoeditor-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-videoeditor-remote
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videoeditor-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-videoeditor-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videoeditor-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-migration
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-migration-%{__INTERNAL_VERSION}.jar

%files profile-admin
# Nothing to do

%files profile-analytics
# Nothing to do

%files profile-export-admin
# Nothing to do

%files profile-export-worker
# Nothing to do

%files profile-export-all-in-one
# Nothing to do

%files profile-ingest
# Nothing to do

%files profile-ingest-standalone
# Nothing to do

%files profile-dist
# Nothing to do

%files profile-dist-standalone
# Nothing to do

%files profile-dist-stub
# Nothing to do

%files profile-engage
# Nothing to do

%files profile-engage-standalone
# Nothing to do

%files profile-engage-stub
# Nothing to do

%files profile-worker
# Nothing to do

%files profile-worker-standalone
# Nothing to do

%files profile-worker-stub
# Nothing to do

%files profile-workspace
# Nothing to do

%files profile-workspace-stub
# Nothing to do

%files profile-serviceregistry
# Nothing to do

%files profile-serviceregistry-stub
# Nothing to do

%files profile-oaipmh
# Nothing to do

%files profile-directory-db
# Nothing to do

%files profile-directory-ldap
# Nothing to do

%files profile-directory-cas
# Nothing to do

%files profile-directory-openid
# Nothing to do

%files profile-directory-shibboleth
# Nothing to do

%files profile-server-management
# Nothing to do

%files profile-capture
# Nothing to do

%files distribution-default
%defattr(-,root,root,-)
# No files here

%files distribution-capture-agent
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

%files distribution-demo
%defattr(-,root,root,-)
# No files here

%files third-party-tools
%defattr(-,root,root,-)
# No files here

%files
%defattr(-,root,root,-)
# No files here



%prep
%setup -q -c -a 0 -a 2
pushd opencast-matterhorn-%{__INTERNAL_VERSION}
%patch0 -p1
popd


%build
#mvn


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
   %if %{__use_systemd}
      systemctl stop matterhorn >/dev/null 2>&1
   %else
      /sbin/service matterhorn stop >/dev/null 2>&1
      /sbin/chkconfig --del matterhorn
   %endif
fi

%postun base
if [ "$1" -ge "1" ]; then
   %{?__use_systemd:systemctl try-restart matterhorn > /dev/null 2>&1 || :}
   %{!?__use_systemd:/sbin/service matterhorn condrestart > /dev/null 2>&1 || :}
fi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/matterhorn
cp -rf opencast-matterhorn-%{__INTERNAL_VERSION}/bin $RPM_BUILD_ROOT%{_datadir}/matterhorn/

# Remove unnecessary scripts
rm $RPM_BUILD_ROOT%{_datadir}/matterhorn/bin/start_matterhorn.sh
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

# Install samples
install -p -D -m 0644 \
   mvn2/org/opencastproject/samples/audio/1.0/audio-1.0.mp3 \
   ${RPM_BUILD_ROOT}/srv/matterhorn/samples/audio-1.0.mp3
install -p -D -m 0644 \
   mvn2/org/opencastproject/samples/camera/1.0/camera-1.0.mpg \
   ${RPM_BUILD_ROOT}/srv/matterhorn/samples/camera-1.0.mpg
install -p -D -m 0644 \
   mvn2/org/opencastproject/samples/screen/1.0/screen-1.0.mpg \
   ${RPM_BUILD_ROOT}/srv/matterhorn/samples/screen-1.0.mpg

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

pushd opencast-matterhorn-%{__INTERNAL_VERSION}/docs/scripts/init/new/
# Install binaries
install -p -D -m 0755 usr-sbin-matterhorn \
      $RPM_BUILD_ROOT%{_sbindir}/matterhorn
install -p -D -m 0644 etc-matterhorn-service.conf \
      ${RPM_BUILD_ROOT}%{_sysconfdir}/matterhorn/service.conf

%if %{__use_systemd}
   install -p -D -m 0755 etc-systemd-system-matterhorn.service \
         $RPM_BUILD_ROOT%{_unitdir}/matterhorn.service
%else
   # Install SysV-init script
   install -p -D -m 0755 etc-init.d-matterhorn \
         $RPM_BUILD_ROOT%{_initddir}/matterhorn
%endif

# Install manpage
cat matterhorn.8 | gzip > matterhorn.8.gz
install -p -D -m 0644 matterhorn.8.gz \
      $RPM_BUILD_ROOT%{_mandir}/man8/matterhorn.8.gz
popd


%clean
rm -rf $RPM_BUILD_ROOT



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


%changelog
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
