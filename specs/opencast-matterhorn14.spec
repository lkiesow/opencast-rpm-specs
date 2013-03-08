%define __os_install_post %{nil}

%define __INTERNAL_VERSION 1.4-SNAPSHOT

# TODO: Build a proper SPEC file:
#       https://fedoraproject.org/wiki/Packaging/Java

Name:           opencast-matterhorn14
Version:        1.4.0
Release:        9%{?dist}
Summary:        Open Source Lecture Capture & Video Management Tool

Group:          Applications/Multimedia
License:        ECL 2.0, APL2 and other
URL:            http://opencast.org/matterhorn/
Source0:        matterhorn-repo-%{version}.tar.gz
Source1:        matterhorn-bin-%{version}.tar.gz
Source2:        maven-repo-matterhorn-%{version}.tar.gz
Patch0:         matterhorn-config-%{version}.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: maven >= 3
BuildRequires: java-devel >= 1:1.6.0
Requires:      %{name}-base                  = %{version}-%{release}
Requires:      %{name}-distribution-default >= %{version}-%{release}


%package base
Summary: Base package for Opencast Matterhorn 
Requires(pre): /usr/sbin/useradd
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts

Requires:      ffmpeg >= 0.9
Requires:      mediainfo = 0.7.35
Requires:      tesseract >= 3
Requires:      qt_sbtl_embedder >= 0.4
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
Summary: admin profile for Opencast Matterhorn %{__INTERNAL_VERSION}
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
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-scheduler-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-scheduler-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-speech-recognition-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}
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
Summary: analytics profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-analytics-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-analytics-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-export-admin
Summary: export-admin profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-export-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}

%package profile-export-worker
Summary: export-worker profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-gstreamer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-impl >= %{version}-%{release}

%package profile-export-all-in-one
Summary: export-all-in-one profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-export-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-gstreamer-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}

%package profile-ingest
Summary: ingest profile for Opencast Matterhorn %{__INTERNAL_VERSION}
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
Summary: dist profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-dist-stub
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-acl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-download >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-streaming >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-youtube >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-dist-stub
Summary: dist-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Remote and non-remote module will not work together
Conflicts: %{name}-profile-dist
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-acl-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-download-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-streaming-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-youtube-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-engage
Summary: engage profile for Opencast Matterhorn %{__INTERNAL_VERSION}
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
Summary: engage-standalone profile for Opencast Matterhorn %{__INTERNAL_VERSION}
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
Summary: engage-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-download-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-streaming-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-youtube-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-lti >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}

%package profile-worker
Summary: worker profile for Opencast Matterhorn %{__INTERNAL_VERSION}
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
Summary: worker-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
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
Summary: workspace profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-workspace-stub
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-impl >= %{version}-%{release}

%package profile-workspace-stub
Summary: workspace-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-workspace
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-impl >= %{version}-%{release}

%package profile-serviceregistry
Summary: serviceregistry profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-serviceregistry-stub
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry >= %{version}-%{release}

%package profile-serviceregistry-stub
Summary: serviceregistry-stub profile for Opencast Matterhorn %{__INTERNAL_VERSION}
# Stub and non-stub profiles will not work together
Conflicts: %{name}-profile-serviceregistry
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}

%package profile-oaipmh
Summary: oaipmh profile for Opencast Matterhorn %{__INTERNAL_VERSION}
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
Summary: directory-db profile for Opencast Matterhorn %{__INTERNAL_VERSION}
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
Summary: directory-ldap profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-security-ldap >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-ldap >= %{version}-%{release}

%package profile-directory-cas
Summary: directory-cas profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-security-cas >= %{version}-%{release}

%package profile-directory-openid
Summary: directory-openid profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-security-openid >= %{version}-%{release}

%package profile-capture
Summary: capture profile for Opencast Matterhorn %{__INTERNAL_VERSION}
BuildRequires: gstreamer
BuildRequires: gstreamer-plugins-base
BuildRequires: gstreamer-plugins-good
BuildRequires: gstreamer-plugins-ugly
BuildRequires: gstreamer-plugins-bad
BuildRequires: gstreamer-ffmpeg
Requires: jv4linfo >= 0.2.1
Requires: v4l-utils
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-admin-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-agent-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-agent-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-confidence-monitoring-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-dependencies >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-test-performance
Summary: test-performance profile for Opencast Matterhorn %{__INTERNAL_VERSION}

%package profile-test-load
Summary: test-load profile for Opencast Matterhorn %{__INTERNAL_VERSION}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-load-test >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package module-matterhorn-videosegmenter-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-videosegmenter-api module for Opencast Matterhorn

%package module-matterhorn-analytics-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-analytics-impl module for Opencast Matterhorn

%package module-matterhorn-distribution-service-youtube
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-youtube-remote
Summary: matterhorn-distribution-service-youtube module for Opencast Matterhorn

%package module-matterhorn-engage-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-engage-ui module for Opencast Matterhorn

%package module-matterhorn-analytics-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-analytics-ui module for Opencast Matterhorn

%package module-matterhorn-videosegmenter-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-videosegmenter-remote module for Opencast Matterhorn

%package module-matterhorn-workflow-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workflow-service-api module for Opencast Matterhorn

%package module-matterhorn-ingest-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-ingest-service-impl module for Opencast Matterhorn

%package module-matterhorn-scheduler-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-scheduler-api module for Opencast Matterhorn

%package module-matterhorn-episode-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-episode-service-impl module for Opencast Matterhorn

%package module-matterhorn-workspace-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workspace-api module for Opencast Matterhorn

%package module-matterhorn-distribution-service-youtube-remote
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-youtube
Summary: matterhorn-distribution-service-youtube-remote module for Opencast Matterhorn

%package module-matterhorn-textextractor-tesseract
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-textextractor-tesseract module for Opencast Matterhorn

%package module-matterhorn-episode-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-episode-service-api module for Opencast Matterhorn

%package module-matterhorn-dictionary-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-dictionary-api module for Opencast Matterhorn

%package module-matterhorn-mpeg7
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-mpeg7 module for Opencast Matterhorn

%package module-matterhorn-search-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-search-service-remote module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-working-file-repository-service-impl module for Opencast Matterhorn

%package module-matterhorn-inspection-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-inspection-service-api module for Opencast Matterhorn

%package module-matterhorn-composer-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-composer-service-remote module for Opencast Matterhorn

%package module-matterhorn-composer-ffmpeg
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-composer-ffmpeg module for Opencast Matterhorn

%package module-matterhorn-static
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-static module for Opencast Matterhorn

%package module-matterhorn-distribution-service-acl
Requires: %{name}-base >= %{version}-%{release}
# You cannot install remote and non-remote at the same time
Conflicts: %{name}-module-matterhorn-distribution-service-acl-remote
Summary: matterhorn-distribution-service-acl module for Opencast Matterhorn

%package module-matterhorn-serviceregistry-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-serviceregistry-remote module for Opencast Matterhorn

%package module-matterhorn-search-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-search-service-impl module for Opencast Matterhorn

%package module-matterhorn-serviceregistry
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-serviceregistry module for Opencast Matterhorn

%package module-matterhorn-distribution-service-download-remote
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-download
Summary: matterhorn-distribution-service-download-remote module for Opencast Matterhorn

%package module-matterhorn-usertracking-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-usertracking-impl module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-textanalyzer-impl module for Opencast Matterhorn

%package module-matterhorn-workflow-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workflow-service-impl module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-working-file-repository-service-api module for Opencast Matterhorn

%package module-matterhorn-oaipmh
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-oaipmh module for Opencast Matterhorn

%package module-matterhorn-capture-admin-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-capture-admin-service-impl module for Opencast Matterhorn

%package module-matterhorn-dictionary-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-dictionary-impl module for Opencast Matterhorn

%package module-matterhorn-ingest-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-ingest-service-api module for Opencast Matterhorn

%package module-matterhorn-gstreamer-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-gstreamer-service-remote module for Opencast Matterhorn

%package module-matterhorn-inspection-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-inspection-service-remote module for Opencast Matterhorn

%package module-matterhorn-episode-service-filesystem
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-episode-service-filesystem module for Opencast Matterhorn

%package module-matterhorn-fileupload
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-fileupload module for Opencast Matterhorn

%package module-matterhorn-series-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-series-service-api module for Opencast Matterhorn

%package module-matterhorn-userdirectory-jpa
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-userdirectory-jpa module for Opencast Matterhorn

%package module-matterhorn-capture-admin-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-capture-admin-service-api module for Opencast Matterhorn

%package module-matterhorn-json
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-json module for Opencast Matterhorn

%package module-matterhorn-admin-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-admin-ui module for Opencast Matterhorn

%package module-matterhorn-gstreamer-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-gstreamer-service-api module for Opencast Matterhorn

%package module-matterhorn-workspace-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workspace-impl module for Opencast Matterhorn

%package module-matterhorn-videosegmenter-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-videosegmenter-impl module for Opencast Matterhorn

%package module-matterhorn-confidence-monitoring-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-confidence-monitoring-ui module for Opencast Matterhorn

%package module-matterhorn-db
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-db module for Opencast Matterhorn

%package module-matterhorn-distribution-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-distribution-service-api module for Opencast Matterhorn

%package module-matterhorn-dublincore
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-dublincore module for Opencast Matterhorn

%package module-matterhorn-distribution-service-acl-remote
Requires: %{name}-base >= %{version}-%{release}
# You cannot install remote and non-remote at the same time
Conflicts: %{name}-module-matterhorn-distribution-service-acl
Summary: matterhorn-distribution-service-acl-remote module for Opencast Matterhorn

%package module-matterhorn-series-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-series-service-remote module for Opencast Matterhorn

%package module-matterhorn-composer-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-composer-service-api module for Opencast Matterhorn

%package module-matterhorn-solr
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-solr module for Opencast Matterhorn

%package module-matterhorn-series-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-series-service-impl module for Opencast Matterhorn

%package module-matterhorn-distribution-service-download
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-download-remote
Summary: matterhorn-distribution-service-download module for Opencast Matterhorn

%package module-matterhorn-mediapackage-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-mediapackage-ui module for Opencast Matterhorn

%package module-matterhorn-scheduler-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-scheduler-impl module for Opencast Matterhorn

%package module-matterhorn-export-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-export-impl module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-textanalyzer-remote module for Opencast Matterhorn

%package module-matterhorn-security-cas
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-security-cas module for Opencast Matterhorn

%package module-matterhorn-security-openid
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-security-openid module for Opencast Matterhorn

%package module-matterhorn-distribution-service-streaming
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-streaming-remote
Summary: matterhorn-distribution-service-streaming module for Opencast Matterhorn

%package module-matterhorn-caption-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-caption-api module for Opencast Matterhorn

%package module-matterhorn-runtime-info-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-runtime-info-ui module for Opencast Matterhorn

%package module-matterhorn-metadata
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-metadata module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-working-file-repository-service-remote module for Opencast Matterhorn

%package module-matterhorn-load-test
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-load-test module for Opencast Matterhorn

%package module-matterhorn-mediapackage-manipulator
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-mediapackage-manipulator module for Opencast Matterhorn

%package module-matterhorn-metadata-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-metadata-api module for Opencast Matterhorn

%package module-matterhorn-distribution-service-streaming-remote
Requires: %{name}-base >= %{version}-%{release}
# Remote and non-remote module will not work together
Conflicts: %{name}-module-matterhorn-distribution-service-streaming
Summary: matterhorn-distribution-service-streaming-remote module for Opencast Matterhorn

%package module-matterhorn-common
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-common module for Opencast Matterhorn

%package module-matterhorn-gstreamer-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-gstreamer-service-impl module for Opencast Matterhorn

%package module-matterhorn-dataloader
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-dataloader module for Opencast Matterhorn

%package module-matterhorn-kernel
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-kernel module for Opencast Matterhorn

%package module-matterhorn-webconsole
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-webconsole module for Opencast Matterhorn

%package module-matterhorn-usertracking-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-usertracking-api module for Opencast Matterhorn

%package module-matterhorn-search-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-search-service-api module for Opencast Matterhorn

%package module-matterhorn-runtime-dependencies
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-runtime-dependencies module for Opencast Matterhorn

%package module-matterhorn-search-service-feeds
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-search-service-feeds module for Opencast Matterhorn

%package module-matterhorn-inspection-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-inspection-service-impl module for Opencast Matterhorn

%package module-matterhorn-conductor
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-conductor module for Opencast Matterhorn

%package module-matterhorn-caption-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-caption-remote module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-textanalyzer-api module for Opencast Matterhorn

%package module-matterhorn-userdirectory-ldap
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-userdirectory-ldap module for Opencast Matterhorn

%package module-matterhorn-capture-agent-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-capture-agent-api module for Opencast Matterhorn

%package module-matterhorn-annotation-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-annotation-api module for Opencast Matterhorn

%package module-matterhorn-authorization-xacml
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-authorization-xacml module for Opencast Matterhorn

%package module-matterhorn-caption-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-caption-impl module for Opencast Matterhorn

%package module-matterhorn-security-ldap
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-security-ldap module for Opencast Matterhorn

%package module-matterhorn-capture-agent-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-capture-agent-impl module for Opencast Matterhorn

%package module-matterhorn-lti
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-lti module for Opencast Matterhorn

%package module-matterhorn-speech-recognition-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-speech-recognition-service-api module for Opencast Matterhorn

%package module-matterhorn-annotation-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-annotation-impl module for Opencast Matterhorn


%description
Matterhorn is a free, open-source platform to support the management of
educational audio and video content. Institutions will use Matterhorn to
produce lecture recordings, manage existing video, serve designated
distribution channels, and provide user interfaces to engage students with
educational videos.
This is the 1.4.x release of Matterhorn. The major releases of Matterhorn may
be incompatible and not suited for direct update. Thus other versions are
available as different packages. However, there is a metapackage
opencast-matterhorn available which keeps track of the newest version.

%description base
Basic elements of each Opencast Matterhorn distribution.

%description distribution-default
Default distribution of Opencast Matterhorn components.

This is the default package containing all three main profiles (Admin, Worker,
Engage). This installation is only recommended if you dont have many videos
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
least three servers on which you run matterhorn if you select this package.


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
Combined Adminand Worker distribution of Opencast Matterhorn components.

This package is targeted at medium sized installations, where you want to
seperate the "backend" server that the admin accesses from the "frontend"
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
Summary: matterhorn-videosegmenter-api module for Opencast Matterhorn

%description module-matterhorn-analytics-impl
Summary: matterhorn-analytics-impl module for Opencast Matterhorn

%description module-matterhorn-distribution-service-youtube
Summary: matterhorn-distribution-service-youtube module for Opencast Matterhorn

%description module-matterhorn-engage-ui
Summary: matterhorn-engage-ui module for Opencast Matterhorn

%description module-matterhorn-analytics-ui
Summary: matterhorn-analytics-ui module for Opencast Matterhorn

%description module-matterhorn-videosegmenter-remote
Summary: matterhorn-videosegmenter-remote module for Opencast Matterhorn

%description module-matterhorn-workflow-service-api
Summary: matterhorn-workflow-service-api module for Opencast Matterhorn

%description module-matterhorn-ingest-service-impl
Summary: matterhorn-ingest-service-impl module for Opencast Matterhorn

%description module-matterhorn-scheduler-api
Summary: matterhorn-scheduler-api module for Opencast Matterhorn

%description module-matterhorn-episode-service-impl
Summary: matterhorn-episode-service-impl module for Opencast Matterhorn

%description module-matterhorn-workspace-api
Summary: matterhorn-workspace-api module for Opencast Matterhorn

%description module-matterhorn-distribution-service-youtube-remote
Summary: matterhorn-distribution-service-youtube-remote module for Opencast Matterhorn

%description module-matterhorn-textextractor-tesseract
Summary: matterhorn-textextractor-tesseract module for Opencast Matterhorn

%description module-matterhorn-episode-service-api
Summary: matterhorn-episode-service-api module for Opencast Matterhorn

%description module-matterhorn-dictionary-api
Summary: matterhorn-dictionary-api module for Opencast Matterhorn

%description module-matterhorn-mpeg7
Summary: matterhorn-mpeg7 module for Opencast Matterhorn

%description module-matterhorn-search-service-remote
Summary: matterhorn-search-service-remote module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-impl
Summary: matterhorn-working-file-repository-service-impl module for Opencast Matterhorn

%description module-matterhorn-inspection-service-api
Summary: matterhorn-inspection-service-api module for Opencast Matterhorn

%description module-matterhorn-composer-service-remote
Summary: matterhorn-composer-service-remote module for Opencast Matterhorn

%description module-matterhorn-composer-ffmpeg
Summary: matterhorn-composer-ffmpeg module for Opencast Matterhorn

%description module-matterhorn-static
Summary: matterhorn-static module for Opencast Matterhorn

%description module-matterhorn-distribution-service-acl
Summary: matterhorn-distribution-service-acl module for Opencast Matterhorn

%description module-matterhorn-serviceregistry-remote
Summary: matterhorn-serviceregistry-remote module for Opencast Matterhorn

%description module-matterhorn-search-service-impl
Summary: matterhorn-search-service-impl module for Opencast Matterhorn

%description module-matterhorn-serviceregistry
Summary: matterhorn-serviceregistry module for Opencast Matterhorn

%description module-matterhorn-distribution-service-download-remote
Summary: matterhorn-distribution-service-download-remote module for Opencast Matterhorn

%description module-matterhorn-usertracking-impl
Summary: matterhorn-usertracking-impl module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-impl
Summary: matterhorn-textanalyzer-impl module for Opencast Matterhorn

%description module-matterhorn-workflow-service-impl
Summary: matterhorn-workflow-service-impl module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-api
Summary: matterhorn-working-file-repository-service-api module for Opencast Matterhorn

%description module-matterhorn-oaipmh
Summary: matterhorn-oaipmh module for Opencast Matterhorn

%description module-matterhorn-capture-admin-service-impl
Summary: matterhorn-capture-admin-service-impl module for Opencast Matterhorn

%description module-matterhorn-dictionary-impl
Summary: matterhorn-dictionary-impl module for Opencast Matterhorn

%description module-matterhorn-ingest-service-api
Summary: matterhorn-ingest-service-api module for Opencast Matterhorn

%description module-matterhorn-gstreamer-service-remote
Summary: matterhorn-gstreamer-service-remote module for Opencast Matterhorn

%description module-matterhorn-inspection-service-remote
Summary: matterhorn-inspection-service-remote module for Opencast Matterhorn

%description module-matterhorn-episode-service-filesystem
Summary: matterhorn-episode-service-filesystem module for Opencast Matterhorn

%description module-matterhorn-fileupload
Summary: matterhorn-fileupload module for Opencast Matterhorn

%description module-matterhorn-series-service-api
Summary: matterhorn-series-service-api module for Opencast Matterhorn

%description module-matterhorn-userdirectory-jpa
Summary: matterhorn-userdirectory-jpa module for Opencast Matterhorn

%description module-matterhorn-capture-admin-service-api
Summary: matterhorn-capture-admin-service-api module for Opencast Matterhorn

%description module-matterhorn-json
Summary: matterhorn-json module for Opencast Matterhorn

%description module-matterhorn-admin-ui
Summary: matterhorn-admin-ui module for Opencast Matterhorn

%description module-matterhorn-gstreamer-service-api
Summary: matterhorn-gstreamer-service-api module for Opencast Matterhorn

%description module-matterhorn-workspace-impl
Summary: matterhorn-workspace-impl module for Opencast Matterhorn

%description module-matterhorn-videosegmenter-impl
Summary: matterhorn-videosegmenter-impl module for Opencast Matterhorn

%description module-matterhorn-confidence-monitoring-ui
Summary: matterhorn-confidence-monitoring-ui module for Opencast Matterhorn

%description module-matterhorn-db
Summary: matterhorn-db module for Opencast Matterhorn

%description module-matterhorn-distribution-service-api
Summary: matterhorn-distribution-service-api module for Opencast Matterhorn

%description module-matterhorn-dublincore
Summary: matterhorn-dublincore module for Opencast Matterhorn

%description module-matterhorn-distribution-service-acl-remote
Summary: matterhorn-distribution-service-acl-remote module for Opencast Matterhorn

%description module-matterhorn-series-service-remote
Summary: matterhorn-series-service-remote module for Opencast Matterhorn

%description module-matterhorn-composer-service-api
Summary: matterhorn-composer-service-api module for Opencast Matterhorn

%description module-matterhorn-solr
Summary: matterhorn-solr module for Opencast Matterhorn

%description module-matterhorn-series-service-impl
Summary: matterhorn-series-service-impl module for Opencast Matterhorn

%description module-matterhorn-distribution-service-download
Summary: matterhorn-distribution-service-download module for Opencast Matterhorn

%description module-matterhorn-mediapackage-ui
Summary: matterhorn-mediapackage-ui module for Opencast Matterhorn

%description module-matterhorn-scheduler-impl
Summary: matterhorn-scheduler-impl module for Opencast Matterhorn

%description module-matterhorn-export-impl
Summary: matterhorn-export-impl module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-remote
Summary: matterhorn-textanalyzer-remote module for Opencast Matterhorn

%description module-matterhorn-security-cas
Summary: matterhorn-security-cas module for Opencast Matterhorn

%description module-matterhorn-security-openid
Summary: matterhorn-security-openid module for Opencast Matterhorn

%description module-matterhorn-distribution-service-streaming
Summary: matterhorn-distribution-service-streaming module for Opencast Matterhorn

%description module-matterhorn-caption-api
Summary: matterhorn-caption-api module for Opencast Matterhorn

%description module-matterhorn-runtime-info-ui
Summary: matterhorn-runtime-info-ui module for Opencast Matterhorn

%description module-matterhorn-metadata
Summary: matterhorn-metadata module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-remote
Summary: matterhorn-working-file-repository-service-remote module for Opencast Matterhorn

%description module-matterhorn-load-test
Summary: matterhorn-load-test module for Opencast Matterhorn

%description module-matterhorn-mediapackage-manipulator
Summary: matterhorn-mediapackage-manipulator module for Opencast Matterhorn

%description module-matterhorn-metadata-api
Summary: matterhorn-metadata-api module for Opencast Matterhorn

%description module-matterhorn-distribution-service-streaming-remote
Summary: matterhorn-distribution-service-streaming-remote module for Opencast Matterhorn

%description module-matterhorn-common
Summary: matterhorn-common module for Opencast Matterhorn

%description module-matterhorn-gstreamer-service-impl
Summary: matterhorn-gstreamer-service-impl module for Opencast Matterhorn

%description module-matterhorn-dataloader
Summary: matterhorn-dataloader module for Opencast Matterhorn

%description module-matterhorn-kernel
Summary: matterhorn-kernel module for Opencast Matterhorn

%description module-matterhorn-webconsole
Summary: matterhorn-webconsole module for Opencast Matterhorn

%description module-matterhorn-usertracking-api
Summary: matterhorn-usertracking-api module for Opencast Matterhorn

%description module-matterhorn-search-service-api
Summary: matterhorn-search-service-api module for Opencast Matterhorn

%description module-matterhorn-runtime-dependencies
Summary: matterhorn-runtime-dependencies module for Opencast Matterhorn

%description module-matterhorn-search-service-feeds
Summary: matterhorn-search-service-feeds module for Opencast Matterhorn

%description module-matterhorn-inspection-service-impl
Summary: matterhorn-inspection-service-impl module for Opencast Matterhorn

%description module-matterhorn-conductor
Summary: matterhorn-conductor module for Opencast Matterhorn

%description module-matterhorn-caption-remote
Summary: matterhorn-caption-remote module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-api
Summary: matterhorn-textanalyzer-api module for Opencast Matterhorn

%description module-matterhorn-userdirectory-ldap
Summary: matterhorn-userdirectory-ldap module for Opencast Matterhorn

%description module-matterhorn-capture-agent-api
Summary: matterhorn-capture-agent-api module for Opencast Matterhorn

%description module-matterhorn-annotation-api
Summary: matterhorn-annotation-api module for Opencast Matterhorn

%description module-matterhorn-authorization-xacml
Summary: matterhorn-authorization-xacml module for Opencast Matterhorn

%description module-matterhorn-caption-impl
Summary: matterhorn-caption-impl module for Opencast Matterhorn

%description module-matterhorn-security-ldap
Summary: matterhorn-security-ldap module for Opencast Matterhorn

%description module-matterhorn-capture-agent-impl
Summary: matterhorn-capture-agent-impl module for Opencast Matterhorn

%description module-matterhorn-lti
Summary: matterhorn-lti module for Opencast Matterhorn

%description module-matterhorn-speech-recognition-service-api
Summary: matterhorn-speech-recognition-service-api module for Opencast Matterhorn

%description module-matterhorn-annotation-impl
Summary: matterhorn-annotation-impl module for Opencast Matterhorn

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
/opt/matterhorn/lib/matterhorn/matterhorn-videosegmenter-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-analytics-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-analytics-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-youtube
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-youtube-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-engage-ui
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-engage-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-analytics-ui
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-analytics-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-videosegmenter-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-videosegmenter-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workflow-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-workflow-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-ingest-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-ingest-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-scheduler-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-scheduler-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-episode-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-episode-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workspace-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-workspace-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-youtube-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-youtube-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-textextractor-tesseract
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-textextractor-tesseract-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-episode-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-episode-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dictionary-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-dictionary-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-mpeg7
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-mpeg7-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-search-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-search-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-working-file-repository-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-inspection-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-inspection-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-composer-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-composer-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-composer-ffmpeg
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-composer-ffmpeg-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-static
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-static-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-acl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-acl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-serviceregistry-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-serviceregistry-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-search-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-search-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-serviceregistry
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-serviceregistry-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-download-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-download-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-usertracking-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-usertracking-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-textanalyzer-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-textanalyzer-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workflow-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-workflow-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-working-file-repository-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-oaipmh
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-oaipmh-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-capture-admin-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-capture-admin-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dictionary-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-dictionary-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-ingest-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-ingest-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-gstreamer-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-inspection-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-inspection-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-episode-service-filesystem
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-episode-service-filesystem-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-fileupload
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-fileupload-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-series-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-series-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-userdirectory-jpa
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-userdirectory-jpa-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-capture-admin-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-capture-admin-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-json
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-json-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-admin-ui
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-admin-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-gstreamer-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-workspace-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-workspace-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-videosegmenter-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-videosegmenter-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-confidence-monitoring-ui
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-confidence-monitoring-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-db
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-db-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dublincore
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-dublincore-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-acl-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-acl-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-series-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-series-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-composer-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-composer-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-solr
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-solr-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-series-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-series-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-download
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-download-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-mediapackage-ui
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-mediapackage-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-scheduler-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-scheduler-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-export-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-export-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-textanalyzer-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-textanalyzer-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-security-cas
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-security-cas-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-security-openid
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-security-openid-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-streaming
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-streaming-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-caption-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-caption-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-runtime-info-ui
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-runtime-info-ui-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-metadata
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-metadata-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-working-file-repository-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-working-file-repository-service-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-load-test
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-load-test-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-mediapackage-manipulator
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-mediapackage-manipulator-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-metadata-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-metadata-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-distribution-service-streaming-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-distribution-service-streaming-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-common
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-common-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-gstreamer-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-gstreamer-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-dataloader
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-dataloader-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-kernel
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-kernel-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-webconsole
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-webconsole-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-usertracking-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-usertracking-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-search-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-search-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-runtime-dependencies
%defattr(-,root,root,-)
/opt/matterhorn/lib/ext/*.jar

%files module-matterhorn-search-service-feeds
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-search-service-feeds-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-inspection-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-inspection-service-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-conductor
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-conductor-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-caption-remote
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-caption-remote-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-textanalyzer-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-textanalyzer-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-userdirectory-ldap
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-userdirectory-ldap-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-capture-agent-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-capture-agent-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-annotation-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-annotation-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-authorization-xacml
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-authorization-xacml-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-caption-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-caption-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-security-ldap
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-security-ldap-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-capture-agent-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-capture-agent-impl-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-lti
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-lti-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-speech-recognition-service-api
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-speech-recognition-service-api-%{__INTERNAL_VERSION}.jar

%files module-matterhorn-annotation-impl
%defattr(-,root,root,-)
/opt/matterhorn/lib/matterhorn/matterhorn-annotation-impl-%{__INTERNAL_VERSION}.jar


%prep
%setup -q -c -a 0 -a 1 -a 2 
pushd matterhorn-%{version}
%patch0 -p1
popd


%build
#mvn


%pre base
# Create matterhorn user.
/usr/sbin/useradd -M -r -d /var/matterhorn \
   -c "Opencast Matterhorn" matterhorn > /dev/null 2>&1 || :

%post base
# Set owner of matterhorn content dir
chown -R matterhorn:matterhorn /var/matterhorn
chown -R matterhorn:matterhorn /var/log/matterhorn
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add matterhorn

%preun base
# If this is really uninstall and not upgrade
if [ $1 -eq 0 ]; then
   /sbin/service matterhorn stop >/dev/null 2>&1
   /sbin/chkconfig --del matterhorn
   /usr/sbin/userdel matterhorn
fi

%postun base
if [ "$1" -ge "1" ]; then
   # WARNING: This should be a condrestart instead of a restart.
   #          but matterhorn restart at the moment behaves like
   #          condrestart should.
   /sbin/service matterhorn restart > /dev/null 2>&1 || :
fi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/matterhorn
cp -rf matterhorn-%{version}/bin $RPM_BUILD_ROOT/opt/matterhorn/
cp -rf matterhorn-%{version}/etc $RPM_BUILD_ROOT/opt/matterhorn/
cp -rf matterhorn-%{version}/lib $RPM_BUILD_ROOT/opt/matterhorn/
echo '<?xml version="1.0" encoding="UTF-8"?>' > settings.xml
echo '<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"' >> settings.xml
echo 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' >> settings.xml
echo 'xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 ' \
   'http://maven.apache.org/xsd/settings-1.0.0.xsd">' >> settings.xml
echo "<localRepository>`pwd`/mvn2/repository</localRepository>" >> settings.xml
echo '<offline>true</offline>' >> settings.xml
echo '</settings>' >> settings.xml
pushd matterhorn-%{version}
   MAVEN_OPTS='-Xms256m -Xmx960m -XX:PermSize=64m -XX:MaxPermSize=256m' \
      mvn -o -s ../settings.xml clean install -P \
         admin,analytics,export-admin,export-worker,export-all-in-one,ingest,dist,dist-stub,engage,engage-standalone,engage-stub,worker,worker-stub,workspace,workspace-stub,serviceregistry,serviceregistry-stub,oaipmh,directory-db,directory-ldap,directory-cas,directory-openid,test-load,capture \
         -DdeployTo=$RPM_BUILD_ROOT/opt/matterhorn/
popd
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -m 0755 matterhorn $RPM_BUILD_ROOT%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}/var/matterhorn/work
mkdir -p ${RPM_BUILD_ROOT}/var/matterhorn/storage
mkdir -p ${RPM_BUILD_ROOT}/var/log/matterhorn
rm -rf  ${RPM_BUILD_ROOT}/opt/matterhorn/logs
ln -s /var/log/matterhorn ${RPM_BUILD_ROOT}/opt/matterhorn/logs
ln -s /var/matterhorn/work ${RPM_BUILD_ROOT}/opt/matterhorn/work
mkdir -p ${RPM_BUILD_ROOT}%{_initddir}
cp -rf matterhorn-%{version}/docs/scripts/init/matterhorn_init_d.sh $RPM_BUILD_ROOT%{_initddir}/matterhorn



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
%{_bindir}/*
/opt/matterhorn/bin
/opt/matterhorn/etc
/opt/matterhorn/lib/felix
%{_initrddir}/*
/var/matterhorn
/var/log/matterhorn
/opt/matterhorn/work
/opt/matterhorn/logs


%changelog
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
