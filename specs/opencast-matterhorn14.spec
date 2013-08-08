%define __os_install_post %{nil}

%global  matterhorn_user          matterhorn
%global  matterhorn_group         %{matterhorn_user}

%define __INTERNAL_VERSION 1.4.1-rc1

# TODO: Build a proper SPEC file:
#       https://fedoraproject.org/wiki/Packaging/Java

Name:           opencast-matterhorn14
Version:        1.4.1
Release:        0.2.rc1%{?dist}
Summary:        Open Source Lecture Capture & Video Management Tool

Group:          Applications/Multimedia
License:        ECL 2.0
URL:            http://opencast.org/matterhorn/
Source0:        matterhorn-%{__INTERNAL_VERSION}.tar.gz
Source10:       usr-sbin-matterhorn
Source11:       etc-init.d-matterhorn
Source12:       etc-matterhorn-service.conf
Source2:        maven-repo-matterhorn-%{__INTERNAL_VERSION}.tar.gz
Source3:        matterhorn-%{__INTERNAL_VERSION}-workflowoperation-mediapackagepost.tar.gz
Source4:        matterhorn.logrotate
Source5:        matterhorn.8.gz
Source6:        audio-1.0.mp3
Source7:        camera-1.0.mpg
Source8:        screen-1.0.mpg
Patch0:         matterhorn-config-%{__INTERNAL_VERSION}.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: maven >= 3
BuildRequires: java-devel >= 1:1.6.0
Requires:      %{name}-base                  = %{version}-%{release}
Requires:      %{name}-distribution-default >= %{version}-%{release}

BuildArch: noarch

%package base
Summary: Base package for Opencast Matterhorn 
Requires(pre): /usr/sbin/useradd
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts

Requires:      bash
Requires:      java >= 1:1.6.0


%package distribution-default
Summary: Default Matterhorn distribution
Requires: %{name}-profile-admin           >= %{version}-%{release}
Requires: %{name}-profile-dist            >= %{version}-%{release}
Requires: %{name}-profile-engage          >= %{version}-%{release}
Requires: %{name}-profile-worker          >= %{version}-%{release}
Requires: %{name}-profile-workspace       >= %{version}-%{release}
Requires: %{name}-profile-serviceregistry >= %{version}-%{release}
Requires: %{name}-profile-directory-db    >= %{version}-%{release}

%package distribution-capture-agent
Summary: Capture-Agent Matterhorn distribution
Requires: %{name}-profile-capture              >= %{version}-%{release}
Requires: %{name}-profile-serviceregistry-stub >= %{version}-%{release}

%package distribution-admin
Summary: Admin Matterhorn distribution
Requires: %{name}-profile-admin              >= %{version}-%{release}
Requires: %{name}-profile-workspace          >= %{version}-%{release}
Requires: %{name}-profile-dist-stub          >= %{version}-%{release}
Requires: %{name}-profile-engage-stub        >= %{version}-%{release}
Requires: %{name}-profile-worker-stub        >= %{version}-%{release}
Requires: %{name}-profile-serviceregistry    >= %{version}-%{release}
Requires: mysql-server >= 5

%package distribution-worker
Summary: Worker Matterhorn distribution
Requires: %{name}-profile-serviceregistry  >= %{version}-%{release}
Requires: %{name}-profile-workspace        >= %{version}-%{release}
Requires: %{name}-profile-worker           >= %{version}-%{release}

%package distribution-engage
Summary: Engage Matterhorn distribution
Requires: %{name}-profile-engage           >= %{version}-%{release}
Requires: %{name}-profile-serviceregistry  >= %{version}-%{release}
Requires: %{name}-profile-dist             >= %{version}-%{release}
Requires: %{name}-profile-workspace        >= %{version}-%{release}

%package distribution-admin-worker
Summary: Combined Admin/Worker Matterhorn distribution
Requires: %{name}-profile-admin              >= %{version}-%{release}
Requires: %{name}-profile-workspace          >= %{version}-%{release}
Requires: %{name}-profile-dist-stub          >= %{version}-%{release}
Requires: %{name}-profile-engage-stub        >= %{version}-%{release}
Requires: %{name}-profile-worker             >= %{version}-%{release}
Requires: %{name}-profile-serviceregistry    >= %{version}-%{release}

%package profile-admin
Summary: Admin profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-admin-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-caption-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-caption-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-admin-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-admin-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-conductor >= %{version}-%{release}
Requires: %{name}-module-matterhorn-composer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-fileupload >= %{version}-%{release}
Requires: %{name}-module-matterhorn-episode-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-episode-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-episode-service-filesystem >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-ingest-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-ingest-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-inspection-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-lti >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mediapackage-manipulator >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mediapackage-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-publication-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-scheduler-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-scheduler-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-speech-recognition-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static-mod >= %{version}-%{release}
Requires: %{name}-module-matterhorn-solr >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-analytics
Summary: Analytics profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-analytics-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-analytics-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static-mod >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-export-admin
Summary: Export-admin profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-export-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static-mod >= %{version}-%{release}

%package profile-export-worker
Summary: Export-worker profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-gstreamer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-impl >= %{version}-%{release}

%package profile-export-all-in-one
Summary: Export-all-in-one profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-export-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static-mod >= %{version}-%{release}

%package profile-ingest
Summary: Ingest profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-ingest-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-ingest-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mediapackage-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-solr >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-dist
Summary: Dist profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-dist-stub
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-acl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-download >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-streaming >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-publication-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-publication-service-youtube >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static-mod >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-dist-stub
Summary: Dist-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-dist
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-acl-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-download-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-streaming-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-publication-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-publication-service-youtube-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-engage
Summary: Engage profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-annotation-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-annotation-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-engage-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-lti >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-feeds >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-solr >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-engage-standalone
Summary: Engage-standalone profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-annotation-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-annotation-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-engage-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-lti >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-feeds >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-solr >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-engage-stub
Summary: Engage-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-download-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-streaming-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-lti >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-publication-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-publication-service-youtube-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-worker
Summary: Worker profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-worker-stub
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-caption-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-caption-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-composer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-composer-ffmpeg >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dictionary-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dictionary-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-inspection-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-inspection-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-speech-recognition-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textextractor-tesseract >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-worker-stub
Summary: Worker-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-worker
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-caption-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-caption-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-composer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-composer-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-inspection-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-inspection-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-speech-recognition-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-workspace
Summary: Workspace profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-workspace-stub
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-impl >= %{version}-%{release}

%package profile-workspace-stub
Summary: Workspace-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-workspace
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-impl >= %{version}-%{release}

%package profile-serviceregistry
Summary: Serviceregistry profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-serviceregistry-stub
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry >= %{version}-%{release}

%package profile-serviceregistry-stub
Summary: Serviceregistry-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-serviceregistry
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}

%package profile-oaipmh
Summary: Oaipmh profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-solr >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-oaipmh >= %{version}-%{release}

%package profile-directory-db
Summary: Directory-db profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dataloader >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-directory-ldap
Summary: Directory-ldap profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-security-ldap >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-ldap >= %{version}-%{release}

%package profile-directory-cas
Summary: Directory-cas profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-security-cas >= %{version}-%{release}

%package profile-directory-openid
Summary: Directory-openid profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-security-openid >= %{version}-%{release}

%package profile-capture
Summary: Capture profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-admin-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-agent-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-agent-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-confidence-monitoring-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static-mod >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-test-performance
Summary: Test-performance profile for Opencast Matterhorn %{__INTERNAL_VERSION}

%package profile-test-load
Summary: Test-load profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-load-test >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static-mod >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package module-matterhorn-videosegmenter-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-videosegmenter-api module for Opencast Matterhorn

%package module-matterhorn-analytics-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-analytics-impl module for Opencast Matterhorn

%package module-matterhorn-engage-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-engage-ui module for Opencast Matterhorn

%package module-matterhorn-analytics-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-analytics-ui module for Opencast Matterhorn

%package module-matterhorn-videosegmenter-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-videosegmenter-remote module for Opencast Matterhorn

%package module-matterhorn-workflow-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-workflow-service-api module for Opencast Matterhorn

%package module-matterhorn-ingest-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-ingest-service-impl module for Opencast Matterhorn

%package module-matterhorn-scheduler-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-scheduler-api module for Opencast Matterhorn

%package module-matterhorn-episode-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-episode-service-impl module for Opencast Matterhorn

%package module-matterhorn-workspace-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-workspace-api module for Opencast Matterhorn

%package module-matterhorn-textextractor-tesseract
Requires: %{name}-base >= %{version}-%{release}
Requires: tesseract >= 3
Summary: Matterhorn-textextractor-tesseract module for Opencast Matterhorn

%package module-matterhorn-episode-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-episode-service-api module for Opencast Matterhorn

%package module-matterhorn-dictionary-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-dictionary-api module for Opencast Matterhorn

%package module-matterhorn-mpeg7
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-mpeg7 module for Opencast Matterhorn

%package module-matterhorn-publication-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-publication-service-api module for Opencast Matterhorn

%package module-matterhorn-publication-service-youtube
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-publication-service-youtube-remote
Provides: %{name}-module-matterhorn-distribution-service-youtube = %{version}-%{release}
Obsoletes: %{name}-module-matterhorn-distribution-service-youtube < %{version}-%{release}
Summary: Matterhorn-publication-service-youtube module for Opencast Matterhorn

%package module-matterhorn-publication-service-youtube-remote
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-publication-service-youtube
Provides: %{name}-module-matterhorn-distribution-service-youtube-remote = %{version}-%{release}
Obsoletes: %{name}-module-matterhorn-distribution-service-youtube-remote < %{version}-%{release}
Summary: Publication-service-youtube-remote module for Opencast Matterhorn

%package module-matterhorn-search-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-search-service-remote module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Working-file-repository-service-impl module for Opencast Matterhorn

%package module-matterhorn-inspection-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-inspection-service-api module for Opencast Matterhorn

%package module-matterhorn-composer-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-composer-service-remote module for Opencast Matterhorn

%package module-matterhorn-composer-ffmpeg
Requires: %{name}-base >= %{version}-%{release}
# We omit the qt_sbtl_embedder dependency on Fedora as it causes some problems
# there. It should not be a problem as it is barely used in Matterhorn
%if 0%{?rhel}
Requires: qt_sbtl_embedder >= 0.4
%endif
Requires: ffmpeg >= 0.9
Summary: Matterhorn-composer-ffmpeg module for Opencast Matterhorn

%package module-matterhorn-static-mod
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-static module for Opencast Matterhorn

%package module-matterhorn-distribution-service-acl
Requires: %{name}-base >= %{version}-%{release}
# You cannot install remote and non-remote at the same time
Conflicts: %{name}-module-matterhorn-distribution-service-acl-remote
Summary: Matterhorn-distribution-service-acl module for Opencast Matterhorn

%package module-matterhorn-serviceregistry-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-serviceregistry-remote module for Opencast Matterhorn

%package module-matterhorn-search-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-search-service-impl module for Opencast Matterhorn

%package module-matterhorn-serviceregistry
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-serviceregistry module for Opencast Matterhorn

%package module-matterhorn-distribution-service-download-remote
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-download
Summary: Distribution-service-download-remote module for Opencast Matterhorn

%package module-matterhorn-usertracking-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-usertracking-impl module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-textanalyzer-impl module for Opencast Matterhorn

%package module-matterhorn-workflow-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-workflow-service-impl module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Working-file-repository-service-api module for Opencast Matterhorn

%package module-matterhorn-oaipmh
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-oaipmh module for Opencast Matterhorn

%package module-matterhorn-capture-admin-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-capture-admin-service-impl module for Opencast Matterhorn

%package module-matterhorn-dictionary-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-dictionary-impl module for Opencast Matterhorn

%package module-matterhorn-ingest-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-ingest-service-api module for Opencast Matterhorn

%package module-matterhorn-gstreamer-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-gstreamer-service-remote module for Opencast Matterhorn

%package module-matterhorn-inspection-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-inspection-service-remote module for Opencast Matterhorn

%package module-matterhorn-episode-service-filesystem
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-episode-service-filesystem module for Opencast Matterhorn

%package module-matterhorn-fileupload
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-fileupload module for Opencast Matterhorn

%package module-matterhorn-series-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-series-service-api module for Opencast Matterhorn

%package module-matterhorn-userdirectory-jpa
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-userdirectory-jpa module for Opencast Matterhorn

%package module-matterhorn-capture-admin-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-capture-admin-service-api module for Opencast Matterhorn

%package module-matterhorn-json
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-json module for Opencast Matterhorn

%package module-matterhorn-admin-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-admin-ui module for Opencast Matterhorn

%package module-matterhorn-gstreamer-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-gstreamer-service-api module for Opencast Matterhorn

%package module-matterhorn-workspace-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-workspace-impl module for Opencast Matterhorn

%package module-matterhorn-videosegmenter-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-videosegmenter-impl module for Opencast Matterhorn

%package module-matterhorn-confidence-monitoring-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-confidence-monitoring-ui module for Opencast Matterhorn

%package module-matterhorn-db
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-db module for Opencast Matterhorn

%package module-matterhorn-distribution-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-distribution-service-api module for Opencast Matterhorn

%package module-matterhorn-dublincore
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-dublincore module for Opencast Matterhorn

%package module-matterhorn-distribution-service-acl-remote
Requires: %{name}-base >= %{version}-%{release}
# You cannot install remote and non-remote at the same time
Conflicts: %{name}-module-matterhorn-distribution-service-acl
Summary: Distribution-service-acl-remote module for Opencast Matterhorn

%package module-matterhorn-series-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-series-service-remote module for Opencast Matterhorn

%package module-matterhorn-composer-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-composer-service-api module for Opencast Matterhorn

%package module-matterhorn-solr
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-solr module for Opencast Matterhorn

%package module-matterhorn-series-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-series-service-impl module for Opencast Matterhorn

%package module-matterhorn-distribution-service-download
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-download-remote
Summary: Matterhorn-distribution-service-download module for Opencast Matterhorn

%package module-matterhorn-mediapackage-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-mediapackage-ui module for Opencast Matterhorn

%package module-matterhorn-scheduler-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-scheduler-impl module for Opencast Matterhorn

%package module-matterhorn-export-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-export-impl module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-textanalyzer-remote module for Opencast Matterhorn

%package module-matterhorn-security-cas
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-security-cas module for Opencast Matterhorn

%package module-matterhorn-security-openid
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-security-openid module for Opencast Matterhorn

%package module-matterhorn-distribution-service-streaming
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-streaming-remote
Summary: Matterhorn-distribution-service-streaming module for Opencast Matterhorn

%package module-matterhorn-caption-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-caption-api module for Opencast Matterhorn

%package module-matterhorn-runtime-info-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-runtime-info-ui module for Opencast Matterhorn

%package module-matterhorn-metadata
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-metadata module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-working-file-repository-service-remote module for Opencast Matterhorn

%package module-matterhorn-load-test
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-load-test module for Opencast Matterhorn

%package module-matterhorn-mediapackage-manipulator
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-mediapackage-manipulator module for Opencast Matterhorn

%package module-matterhorn-metadata-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-metadata-api module for Opencast Matterhorn

%package module-matterhorn-distribution-service-streaming-remote
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-streaming
Summary: Matterhorn-distribution-service-streaming-remote module for Opencast Matterhorn

%package module-matterhorn-common
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-common module for Opencast Matterhorn

%package module-matterhorn-gstreamer-service-impl
Requires: %{name}-base >= %{version}-%{release}
Requires: gstreamer
Requires: gstreamer-plugins-base
Summary: Matterhorn-gstreamer-service-impl module for Opencast Matterhorn

%package module-matterhorn-dataloader
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-dataloader module for Opencast Matterhorn

%package module-matterhorn-kernel
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-kernel module for Opencast Matterhorn

%package module-matterhorn-webconsole
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-webconsole module for Opencast Matterhorn

%package module-matterhorn-usertracking-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-usertracking-api module for Opencast Matterhorn

%package module-matterhorn-search-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-search-service-api module for Opencast Matterhorn

%package module-matterhorn-runtime-dependencies
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-runtime-dependencies module for Opencast Matterhorn

%package module-matterhorn-search-service-feeds
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-search-service-feeds module for Opencast Matterhorn

%package module-matterhorn-inspection-service-impl
Requires: %{name}-base >= %{version}-%{release}
Requires:     mediainfo = 0.7.35
Summary: Matterhorn-inspection-service-impl module for Opencast Matterhorn

%package module-matterhorn-conductor
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-conductor module for Opencast Matterhorn

%package module-matterhorn-caption-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-caption-remote module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-textanalyzer-api module for Opencast Matterhorn

%package module-matterhorn-userdirectory-ldap
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-userdirectory-ldap module for Opencast Matterhorn

%package module-matterhorn-capture-agent-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-capture-agent-api module for Opencast Matterhorn

%package module-matterhorn-annotation-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-annotation-api module for Opencast Matterhorn

%package module-matterhorn-authorization-xacml
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-authorization-xacml module for Opencast Matterhorn

%package module-matterhorn-caption-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-caption-impl module for Opencast Matterhorn

%package module-matterhorn-security-ldap
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-security-ldap module for Opencast Matterhorn

%package module-matterhorn-capture-agent-impl
BuildRequires: gstreamer
BuildRequires: gstreamer-plugins-base
BuildRequires: gstreamer-plugins-good
BuildRequires: gstreamer-plugins-bad
BuildRequires: gstreamer-plugins-bad-nonfree
BuildRequires: gstreamer-plugins-ugly
BuildRequires: gstreamer-ffmpeg
Requires: gstreamer
Requires: gstreamer-plugins-base
Requires: gstreamer-plugins-good
Requires: gstreamer-plugins-bad
Requires: gstreamer-plugins-bad-nonfree
Requires: gstreamer-plugins-ugly
Requires: gstreamer-ffmpeg
Requires: jv4linfo >= 0.2.1
Requires: v4l-utils
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-capture-agent-impl module for Opencast Matterhorn

%package module-matterhorn-lti
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-lti module for Opencast Matterhorn

%package module-matterhorn-speech-recognition-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-speech-recognition-service-api module for Opencast Matterhorn

%package module-matterhorn-annotation-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: Matterhorn-annotation-impl module for Opencast Matterhorn


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

%description profile-dist
dist profile for Opencast Matterhorn

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

%description profile-capture
capture profile for Opencast Matterhorn

%description profile-test-performance
test-performance profile for Opencast Matterhorn

%description profile-test-load
test-load profile for Opencast Matterhorn

%description module-matterhorn-videosegmenter-api
Matterhorn-videosegmenter-api module for Opencast Matterhorn

%description module-matterhorn-analytics-impl
Matterhorn-analytics-impl module for Opencast Matterhorn

%description module-matterhorn-engage-ui
Matterhorn-engage-ui module for Opencast Matterhorn

%description module-matterhorn-analytics-ui
Matterhorn-analytics-ui module for Opencast Matterhorn

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

%description module-matterhorn-dictionary-impl
Matterhorn-dictionary-impl module for Opencast Matterhorn

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

%description module-matterhorn-userdirectory-jpa
Matterhorn-userdirectory-jpa module for Opencast Matterhorn

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

%description module-matterhorn-export-impl
Matterhorn-export-impl module for Opencast Matterhorn

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

%description module-matterhorn-load-test
Matterhorn-load-test module for Opencast Matterhorn

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

%description module-matterhorn-inspection-service-impl
Matterhorn-inspection-service-impl module for Opencast Matterhorn

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

%files profile-dist
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

%files profile-capture
# Nothing to do

%files profile-test-performance
# Nothing to do

%files profile-test-load
# Nothing to do

%files module-matterhorn-videosegmenter-api
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-videosegmenter-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-analytics-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-analytics-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-engage-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-engage-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-analytics-ui
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-analytics-ui-%{__INTERNAL_VERSION}.jar

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

%files module-matterhorn-dictionary-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-dictionary-impl-%{__INTERNAL_VERSION}.jar

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

%files module-matterhorn-userdirectory-jpa
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-userdirectory-jpa-%{__INTERNAL_VERSION}.jar

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

%files module-matterhorn-export-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-export-impl-%{__INTERNAL_VERSION}.jar

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

%files module-matterhorn-load-test
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-load-test-%{__INTERNAL_VERSION}.jar

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

%files module-matterhorn-inspection-service-impl
%defattr(-,root,root,-)
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-inspection-service-impl-%{__INTERNAL_VERSION}.jar

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


# Aditional modules


%package module-matterhorn-workflowoperation-mediapackagepost
Requires: %{name}-base >= %{version}-%{release}
Summary: Mediapackage POST work-flow operation for Opencast Matterhorn

%description module-matterhorn-workflowoperation-mediapackagepost
This Opencast Matterhorn module contains a work-flow operation which will send a
Matterhorn Media-package as HTTP POST request to a specified URL.

%files module-matterhorn-workflowoperation-mediapackagepost
%defattr(-,root,root,-)
%doc %{_datadir}/matterhorn/docs/module-docs/workflowoperation-mediapackagepost-example.xml
%{_datadir}/matterhorn/lib/matterhorn/matterhorn-workflowoperation-mediapackagepost-*





%prep
%setup -q -c -a 0 -a 2 -a 3
pushd matterhorn-%{__INTERNAL_VERSION}
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
/sbin/chkconfig --add matterhorn

%preun base
# If this is really uninstall and not upgrade
if [ $1 -eq 0 ]; then
   /sbin/service matterhorn stop >/dev/null 2>&1
   /sbin/chkconfig --del matterhorn
fi

%postun base
if [ "$1" -ge "1" ]; then
   /sbin/service matterhorn condrestart > /dev/null 2>&1 || :
fi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/matterhorn
cp -rf matterhorn-%{__INTERNAL_VERSION}/bin $RPM_BUILD_ROOT%{_datadir}/matterhorn/

# Remove unnecessary scripts
rm $RPM_BUILD_ROOT%{_datadir}/matterhorn/bin/start_matterhorn.bat
rm $RPM_BUILD_ROOT%{_datadir}/matterhorn/bin/start_matterhorn.sh
rm $RPM_BUILD_ROOT%{_datadir}/matterhorn/bin/shutdown_matterhorn.sh
cp -rf matterhorn-%{__INTERNAL_VERSION}/etc $RPM_BUILD_ROOT%{_datadir}/matterhorn/
cp -rf matterhorn-%{__INTERNAL_VERSION}/lib $RPM_BUILD_ROOT%{_datadir}/matterhorn/
echo '<?xml version="1.0" encoding="UTF-8"?>' > settings.xml
echo '<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"' >> settings.xml
echo 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' >> settings.xml
echo 'xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 ' \
   'http://maven.apache.org/xsd/settings-1.0.0.xsd">' >> settings.xml
echo "<localRepository>`pwd`/mvn2</localRepository>" >> settings.xml
echo '<offline>true</offline>' >> settings.xml
echo '</settings>' >> settings.xml
pushd matterhorn-%{__INTERNAL_VERSION}
   MAVEN_OPTS='-Xms512m -Xmx960m -XX:PermSize=128m -XX:MaxPermSize=512m' \
      mvn -o -s ../settings.xml clean install -P \
         admin,analytics,export-admin,export-worker,export-all-in-one,ingest,dist,dist-stub,engage,engage-standalone,engage-stub,worker,worker-stub,workspace,workspace-stub,serviceregistry,serviceregistry-stub,oaipmh,directory-db,directory-ldap,directory-cas,directory-openid,test-load,capture \
         -DdeployTo=$RPM_BUILD_ROOT%{_datadir}/matterhorn/
popd
#
# Build additional modules:
pushd matterhorn-%{__INTERNAL_VERSION}/modules/matterhorn-workflowoperation-mediapackagepost/
   MAVEN_OPTS='-Xms256m -Xmx960m -XX:PermSize=64m -XX:MaxPermSize=256m' \
      mvn -o -s ../../../settings.xml clean install \
         -DdeployTo=$RPM_BUILD_ROOT%{_datadir}/matterhorn/
popd
#
# Copy other stuff
mkdir -m 755 -p ${RPM_BUILD_ROOT}/srv/matterhorn/inbox
mkdir -m 755 -p ${RPM_BUILD_ROOT}%{_localstatedir}/log/matterhorn
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/matterhorn
mv ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/etc/* ${RPM_BUILD_ROOT}%{_sysconfdir}/matterhorn/

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/etc/
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/logs

ln -s %{_sysconfdir}/matterhorn/       ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/etc
ln -s %{_localstatedir}/log/matterhorn ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/logs
ln -s /srv/matterhorn                  ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/storage
ln -s /srv/matterhorn/inbox            ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/inbox
ln -s /usr/sbin/matterhorn             ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/bin/matterhorn

# Install samples
install -p -D -m 0644 %{SOURCE6} \
   ${RPM_BUILD_ROOT}/srv/matterhorn/samples/audio-1.0.mp3
install -p -D -m 0644 %{SOURCE7} \
   ${RPM_BUILD_ROOT}/srv/matterhorn/samples/camera-1.0.mpg
install -p -D -m 0644 %{SOURCE8} \
   ${RPM_BUILD_ROOT}/srv/matterhorn/samples/screen-1.0.mpg

# Install binaries
install -p -D -m 0755 %{SOURCE10} \
      $RPM_BUILD_ROOT%{_sbindir}/matterhorn
install -p -D -m 0644 %{SOURCE12} \
      ${RPM_BUILD_ROOT}%{_sysconfdir}/matterhorn/service.conf

# Install SysV-init script
install -p -D -m 0755 %{SOURCE11} \
      $RPM_BUILD_ROOT%{_initddir}/matterhorn

# Install logrotate configuration
install -p -D -m 0644 %{SOURCE4} \
   %{buildroot}%{_sysconfdir}/logrotate.d/opencast-matterhorn14-base

# Add documentation
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/scripts/ddl/
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/licenses/
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/module-docs/
cp matterhorn-%{__INTERNAL_VERSION}/docs/licenses.txt  ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/
cp matterhorn-%{__INTERNAL_VERSION}/docs/licenses/*    ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/licenses/
cp matterhorn-%{__INTERNAL_VERSION}/docs/scripts/ddl/* ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/scripts/ddl/
cp matterhorn-%{__INTERNAL_VERSION}/docs/module-docs/* ${RPM_BUILD_ROOT}%{_datadir}/matterhorn/docs/module-docs/

# Install manpage
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man8/matterhorn.8.gz



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
# No files here


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
# No files here

%files distribution-engage
%defattr(-,root,root,-)
# No files here

%files distribution-admin-worker
%defattr(-,root,root,-)
# No files here

%files base
%defattr(-,root,root,-)
%doc %{_datadir}/matterhorn/docs
%config(noreplace) %{_sysconfdir}/matterhorn/
%config(noreplace) %{_sysconfdir}/logrotate.d/opencast-matterhorn14-base
%{_initrddir}/*
%{_sbindir}/*
%dir %{_datadir}/matterhorn
%dir %{_datadir}/matterhorn/lib
%dir %{_datadir}/matterhorn/lib/matterhorn
%{_datadir}/matterhorn/lib/felix
%{_datadir}/matterhorn/bin
%{_datadir}/matterhorn/etc
%{_datadir}/matterhorn/logs
%{_datadir}/matterhorn/storage
%{_datadir}/matterhorn/inbox
%dir /srv/matterhorn
%dir /srv/matterhorn/inbox
%dir %{_localstatedir}/log/matterhorn
%{_mandir}/man8/matterhorn.8.gz


%changelog
* Thu Aug  8 2013 Lars Kiesow <lkiesow@uos.de> - 1.4.1-0.2.rc1
- Excluded qt_sbtl_embedder on Fedora systems

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
