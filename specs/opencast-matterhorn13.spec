%define __os_install_post %{nil}

# TODO: Build a proper SPEC file:
#       https://fedoraproject.org/wiki/Packaging/Java

Name:           opencast-matterhorn13
Version:        1.3.1
Release:        9%{?dist}
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
Requires:      %{name}-base                  = %{version}-%{release}
Requires:      %{name}-distribution-default >= %{version}-%{release}

%package distribution-default
Summary: Default Matterhorn distribution
Requires: %{name}-profile-admin           >= %{version}-%{release}
Requires: %{name}-profile-dist            >= %{version}-%{release}
Requires: %{name}-profile-engage          >= %{version}-%{release}
Requires: %{name}-profile-worker          >= %{version}-%{release}
Requires: %{name}-profile-workspace       >= %{version}-%{release}
Requires: %{name}-profile-serviceregistry >= %{version}-%{release}
Requires: %{name}-profile-directory-db    >= %{version}-%{release}

%package base
Summary: Opencast Matterhorn base package
Requires(pre): /usr/sbin/useradd
Requires:      ffmpeg >= 0.9
Requires:      mediainfo = 0.7.35
Requires:      tesseract >= 3
Requires:      qt_sbtl_embedder >= 0.4
Requires:      bash
Requires:      java >= 1:1.6.0
Requires:      %{name}-maven-repo = %{version}-%{release}

%package maven-repo
Summary:       Maven Repository for Opencast Matterhorn
Requires: %{name}-base >= %{version}-%{release}

%package profile-admin
Summary: admin profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-admin-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-admin-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-admin-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-cas >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-conductor >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-episode-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-episode-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-ingest-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-ingest-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-lti >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-scheduler-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-scheduler-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-speech-recognition-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-solr >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-impl >= %{version}-%{release}

%package profile-ingest
Summary: ingest profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-ingest-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-ingest-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-solr >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workflow-service-remote >= %{version}-%{release}

%package profile-dist
Summary: dist profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-download >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-streaming >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-dist-stub
Summary: dist-stub profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-download-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-distribution-service-streaming-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dublincore >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-metadata-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-mpeg7 >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-engage
Summary: engage profile for Opencast Matterhorn
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
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-series-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-feeds >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-solr >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-usertracking-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-engage-stub
Summary: engage-stub profile for Opencast Matterhorn
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
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-search-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-worker
Summary: worker profile for Opencast Matterhorn
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
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-speech-recognition-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textextractor-tesseract >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-worker-stub
Summary: worker-stub profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-authorization-xacml >= %{version}-%{release}
Requires: %{name}-module-matterhorn-caption-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-caption-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-composer-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-composer-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-inspection-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-inspection-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-speech-recognition-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-textanalyzer-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-videosegmenter-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-workspace
Summary: workspace profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-working-file-repository-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-impl >= %{version}-%{release}

%package profile-workspace-stub
Summary: workspace-stub profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-working-file-repository-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-working-file-repository-service-remote >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-workspace-impl >= %{version}-%{release}

%package profile-serviceregistry
Summary: serviceregistry profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry >= %{version}-%{release}

%package profile-serviceregistry-stub
Summary: serviceregistry-stub profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-serviceregistry-remote >= %{version}-%{release}

%package profile-directory-db
Summary: directory-db profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-db >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-jpa >= %{version}-%{release}
Requires: %{name}-module-matterhorn-dataloader >= %{version}-%{release}

%package profile-directory-ldap
Summary: directory-ldap profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-userdirectory-ldap >= %{version}-%{release}

%package profile-capture
Summary: capture profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-common >= %{version}-%{release}
Requires: %{name}-module-matterhorn-json >= %{version}-%{release}
Requires: %{name}-module-matterhorn-kernel >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-admin-service-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-agent-api >= %{version}-%{release}
Requires: %{name}-module-matterhorn-capture-agent-impl >= %{version}-%{release}
Requires: %{name}-module-matterhorn-confidence-monitoring-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-runtime-info-ui >= %{version}-%{release}
Requires: %{name}-module-matterhorn-static >= %{version}-%{release}
Requires: %{name}-module-matterhorn-webconsole >= %{version}-%{release}

%package profile-cas
Summary: cas profile for Opencast Matterhorn
Requires: %{name}-module-matterhorn-cas >= %{version}-%{release}

%package profile-oaipmh
Summary: oaipmh profile for Opencast Matterhorn
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

%package module-matterhorn-admin-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-admin-ui module for Opencast Matterhorn

%package module-matterhorn-annotation-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-annotation-api module for Opencast Matterhorn

%package module-matterhorn-annotation-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-annotation-impl module for Opencast Matterhorn

%package module-matterhorn-authorization-xacml
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-authorization-xacml module for Opencast Matterhorn

%package module-matterhorn-caption-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-caption-api module for Opencast Matterhorn

%package module-matterhorn-caption-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-caption-impl module for Opencast Matterhorn

%package module-matterhorn-capture-admin-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-capture-admin-service-api module for Opencast Matterhorn

%package module-matterhorn-capture-admin-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-capture-admin-service-impl module for Opencast Matterhorn

%package module-matterhorn-capture-agent-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-capture-agent-api module for Opencast Matterhorn

%package module-matterhorn-capture-agent-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-capture-agent-impl module for Opencast Matterhorn

%package module-matterhorn-cas
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-cas module for Opencast Matterhorn

%package module-matterhorn-common
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-common module for Opencast Matterhorn

%package module-matterhorn-composer-ffmpeg
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-composer-ffmpeg module for Opencast Matterhorn

%package module-matterhorn-composer-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-composer-service-api module for Opencast Matterhorn

%package module-matterhorn-composer-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-composer-service-remote module for Opencast Matterhorn

%package module-matterhorn-conductor
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-conductor module for Opencast Matterhorn

%package module-matterhorn-confidence-monitoring-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-confidence-monitoring-ui module for Opencast Matterhorn

%package module-matterhorn-dataloader
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-dataloader module for Opencast Matterhorn

%package module-matterhorn-db
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-db module for Opencast Matterhorn

%package module-matterhorn-dictionary-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-dictionary-api module for Opencast Matterhorn

%package module-matterhorn-dictionary-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-dictionary-impl module for Opencast Matterhorn

%package module-matterhorn-distribution-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-distribution-service-api module for Opencast Matterhorn

%package module-matterhorn-distribution-service-download
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-distribution-service-download module for Opencast Matterhorn

%package module-matterhorn-distribution-service-download-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-distribution-service-download-remote module for Opencast Matterhorn

%package module-matterhorn-distribution-service-streaming
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-distribution-service-streaming module for Opencast Matterhorn

%package module-matterhorn-distribution-service-streaming-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-distribution-service-streaming-remote module for Opencast Matterhorn

%package module-matterhorn-dublincore
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-dublincore module for Opencast Matterhorn

%package module-matterhorn-engage-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-engage-ui module for Opencast Matterhorn

%package module-matterhorn-episode-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-episode-service-api module for Opencast Matterhorn

%package module-matterhorn-episode-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-episode-service-impl module for Opencast Matterhorn

%package module-matterhorn-ingest-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-ingest-service-api module for Opencast Matterhorn

%package module-matterhorn-ingest-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-ingest-service-impl module for Opencast Matterhorn

%package module-matterhorn-inspection-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-inspection-service-api module for Opencast Matterhorn

%package module-matterhorn-inspection-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-inspection-service-impl module for Opencast Matterhorn

%package module-matterhorn-inspection-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-inspection-service-remote module for Opencast Matterhorn

%package module-matterhorn-json
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-json module for Opencast Matterhorn

%package module-matterhorn-kernel
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-kernel module for Opencast Matterhorn

%package module-matterhorn-lti
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-lti module for Opencast Matterhorn

%package module-matterhorn-metadata
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-metadata module for Opencast Matterhorn

%package module-matterhorn-metadata-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-metadata-api module for Opencast Matterhorn

%package module-matterhorn-mpeg7
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-mpeg7 module for Opencast Matterhorn

%package module-matterhorn-oaipmh
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-oaipmh module for Opencast Matterhorn

%package module-matterhorn-runtime-info-ui
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-runtime-info-ui module for Opencast Matterhorn

%package module-matterhorn-scheduler-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-scheduler-api module for Opencast Matterhorn

%package module-matterhorn-scheduler-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-scheduler-impl module for Opencast Matterhorn

%package module-matterhorn-search-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-search-service-api module for Opencast Matterhorn

%package module-matterhorn-search-service-feeds
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-search-service-feeds module for Opencast Matterhorn

%package module-matterhorn-search-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-search-service-impl module for Opencast Matterhorn

%package module-matterhorn-search-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-search-service-remote module for Opencast Matterhorn

%package module-matterhorn-series-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-series-service-api module for Opencast Matterhorn

%package module-matterhorn-series-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-series-service-impl module for Opencast Matterhorn

%package module-matterhorn-serviceregistry
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-serviceregistry module for Opencast Matterhorn

%package module-matterhorn-serviceregistry-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-serviceregistry-remote module for Opencast Matterhorn

%package module-matterhorn-solr
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-solr module for Opencast Matterhorn

%package module-matterhorn-speech-recognition-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-speech-recognition-service-api module for Opencast Matterhorn

%package module-matterhorn-static
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-static module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-textanalyzer-api module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-textanalyzer-impl module for Opencast Matterhorn

%package module-matterhorn-textanalyzer-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-textanalyzer-remote module for Opencast Matterhorn

%package module-matterhorn-textextractor-tesseract
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-textextractor-tesseract module for Opencast Matterhorn

%package module-matterhorn-userdirectory-jpa
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-userdirectory-jpa module for Opencast Matterhorn

%package module-matterhorn-userdirectory-ldap
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-userdirectory-ldap module for Opencast Matterhorn

%package module-matterhorn-usertracking-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-usertracking-api module for Opencast Matterhorn

%package module-matterhorn-usertracking-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-usertracking-impl module for Opencast Matterhorn

%package module-matterhorn-videosegmenter-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-videosegmenter-api module for Opencast Matterhorn

%package module-matterhorn-videosegmenter-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-videosegmenter-impl module for Opencast Matterhorn

%package module-matterhorn-videosegmenter-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-videosegmenter-remote module for Opencast Matterhorn

%package module-matterhorn-webconsole
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-webconsole module for Opencast Matterhorn

%package module-matterhorn-workflow-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workflow-service-api module for Opencast Matterhorn

%package module-matterhorn-workflow-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workflow-service-impl module for Opencast Matterhorn

%package module-matterhorn-workflow-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workflow-service-remote module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-working-file-repository-service-api module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-working-file-repository-service-impl module for Opencast Matterhorn

%package module-matterhorn-working-file-repository-service-remote
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-working-file-repository-service-remote module for Opencast Matterhorn

%package module-matterhorn-workspace-api
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workspace-api module for Opencast Matterhorn

%package module-matterhorn-workspace-impl
Requires: %{name}-base >= %{version}-%{release}
Summary: matterhorn-workspace-impl module for Opencast Matterhorn

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

%description base
Basic elements of each Opencast Matterhorn distribution.

%description distribution-default
Default distribution of Opencast Matterhorn components.

%description maven-repo
Maven repository for Opencast Matterhorn.

%description profile-admin
admin profile for Opencast Matterhorn

%description profile-ingest
ingest profile for Opencast Matterhorn

%description profile-dist
dist profile for Opencast Matterhorn

%description profile-dist-stub
dist-stub profile for Opencast Matterhorn

%description profile-engage
engage profile for Opencast Matterhorn

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

%description profile-directory-db
directory-db profile for Opencast Matterhorn

%description profile-directory-ldap
directory-ldap profile for Opencast Matterhorn

%description profile-capture
capture profile for Opencast Matterhorn

%description profile-cas
cas profile for Opencast Matterhorn

%description profile-oaipmh
oaipmh profile for Opencast Matterhorn

%description module-matterhorn-admin-ui
Summary: matterhorn-admin-ui module for Opencast Matterhorn

%description module-matterhorn-annotation-api
Summary: matterhorn-annotation-api module for Opencast Matterhorn

%description module-matterhorn-annotation-impl
Summary: matterhorn-annotation-impl module for Opencast Matterhorn

%description module-matterhorn-authorization-xacml
Summary: matterhorn-authorization-xacml module for Opencast Matterhorn

%description module-matterhorn-caption-api
Summary: matterhorn-caption-api module for Opencast Matterhorn

%description module-matterhorn-caption-impl
Summary: matterhorn-caption-impl module for Opencast Matterhorn

%description module-matterhorn-capture-admin-service-api
Summary: matterhorn-capture-admin-service-api module for Opencast Matterhorn

%description module-matterhorn-capture-admin-service-impl
Summary: matterhorn-capture-admin-service-impl module for Opencast Matterhorn

%description module-matterhorn-capture-agent-api
Summary: matterhorn-capture-agent-api module for Opencast Matterhorn

%description module-matterhorn-capture-agent-impl
Summary: matterhorn-capture-agent-impl module for Opencast Matterhorn

%description module-matterhorn-cas
Summary: matterhorn-cas module for Opencast Matterhorn

%description module-matterhorn-common
Summary: matterhorn-common module for Opencast Matterhorn

%description module-matterhorn-composer-ffmpeg
Summary: matterhorn-composer-ffmpeg module for Opencast Matterhorn

%description module-matterhorn-composer-service-api
Summary: matterhorn-composer-service-api module for Opencast Matterhorn

%description module-matterhorn-composer-service-remote
Summary: matterhorn-composer-service-remote module for Opencast Matterhorn

%description module-matterhorn-conductor
Summary: matterhorn-conductor module for Opencast Matterhorn

%description module-matterhorn-confidence-monitoring-ui
Summary: matterhorn-confidence-monitoring-ui module for Opencast Matterhorn

%description module-matterhorn-dataloader
Summary: matterhorn-dataloader module for Opencast Matterhorn

%description module-matterhorn-db
Summary: matterhorn-db module for Opencast Matterhorn

%description module-matterhorn-dictionary-api
Summary: matterhorn-dictionary-api module for Opencast Matterhorn

%description module-matterhorn-dictionary-impl
Summary: matterhorn-dictionary-impl module for Opencast Matterhorn

%description module-matterhorn-distribution-service-api
Summary: matterhorn-distribution-service-api module for Opencast Matterhorn

%description module-matterhorn-distribution-service-download
Summary: matterhorn-distribution-service-download module for Opencast Matterhorn

%description module-matterhorn-distribution-service-download-remote
Summary: matterhorn-distribution-service-download-remote module for Opencast Matterhorn

%description module-matterhorn-distribution-service-streaming
Summary: matterhorn-distribution-service-streaming module for Opencast Matterhorn

%description module-matterhorn-distribution-service-streaming-remote
Summary: matterhorn-distribution-service-streaming-remote module for Opencast Matterhorn

%description module-matterhorn-dublincore
Summary: matterhorn-dublincore module for Opencast Matterhorn

%description module-matterhorn-engage-ui
Summary: matterhorn-engage-ui module for Opencast Matterhorn

%description module-matterhorn-episode-service-api
Summary: matterhorn-episode-service-api module for Opencast Matterhorn

%description module-matterhorn-episode-service-impl
Summary: matterhorn-episode-service-impl module for Opencast Matterhorn

%description module-matterhorn-ingest-service-api
Summary: matterhorn-ingest-service-api module for Opencast Matterhorn

%description module-matterhorn-ingest-service-impl
Summary: matterhorn-ingest-service-impl module for Opencast Matterhorn

%description module-matterhorn-inspection-service-api
Summary: matterhorn-inspection-service-api module for Opencast Matterhorn

%description module-matterhorn-inspection-service-impl
Summary: matterhorn-inspection-service-impl module for Opencast Matterhorn

%description module-matterhorn-inspection-service-remote
Summary: matterhorn-inspection-service-remote module for Opencast Matterhorn

%description module-matterhorn-json
Summary: matterhorn-json module for Opencast Matterhorn

%description module-matterhorn-kernel
Summary: matterhorn-kernel module for Opencast Matterhorn

%description module-matterhorn-lti
Summary: matterhorn-lti module for Opencast Matterhorn

%description module-matterhorn-metadata
Summary: matterhorn-metadata module for Opencast Matterhorn

%description module-matterhorn-metadata-api
Summary: matterhorn-metadata-api module for Opencast Matterhorn

%description module-matterhorn-mpeg7
Summary: matterhorn-mpeg7 module for Opencast Matterhorn

%description module-matterhorn-oaipmh
Summary: matterhorn-oaipmh module for Opencast Matterhorn

%description module-matterhorn-runtime-info-ui
Summary: matterhorn-runtime-info-ui module for Opencast Matterhorn

%description module-matterhorn-scheduler-api
Summary: matterhorn-scheduler-api module for Opencast Matterhorn

%description module-matterhorn-scheduler-impl
Summary: matterhorn-scheduler-impl module for Opencast Matterhorn

%description module-matterhorn-search-service-api
Summary: matterhorn-search-service-api module for Opencast Matterhorn

%description module-matterhorn-search-service-feeds
Summary: matterhorn-search-service-feeds module for Opencast Matterhorn

%description module-matterhorn-search-service-impl
Summary: matterhorn-search-service-impl module for Opencast Matterhorn

%description module-matterhorn-search-service-remote
Summary: matterhorn-search-service-remote module for Opencast Matterhorn

%description module-matterhorn-series-service-api
Summary: matterhorn-series-service-api module for Opencast Matterhorn

%description module-matterhorn-series-service-impl
Summary: matterhorn-series-service-impl module for Opencast Matterhorn

%description module-matterhorn-serviceregistry
Summary: matterhorn-serviceregistry module for Opencast Matterhorn

%description module-matterhorn-serviceregistry-remote
Summary: matterhorn-serviceregistry-remote module for Opencast Matterhorn

%description module-matterhorn-solr
Summary: matterhorn-solr module for Opencast Matterhorn

%description module-matterhorn-speech-recognition-service-api
Summary: matterhorn-speech-recognition-service-api module for Opencast Matterhorn

%description module-matterhorn-static
Summary: matterhorn-static module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-api
Summary: matterhorn-textanalyzer-api module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-impl
Summary: matterhorn-textanalyzer-impl module for Opencast Matterhorn

%description module-matterhorn-textanalyzer-remote
Summary: matterhorn-textanalyzer-remote module for Opencast Matterhorn

%description module-matterhorn-textextractor-tesseract
Summary: matterhorn-textextractor-tesseract module for Opencast Matterhorn

%description module-matterhorn-userdirectory-jpa
Summary: matterhorn-userdirectory-jpa module for Opencast Matterhorn

%description module-matterhorn-userdirectory-ldap
Summary: matterhorn-userdirectory-ldap module for Opencast Matterhorn

%description module-matterhorn-usertracking-api
Summary: matterhorn-usertracking-api module for Opencast Matterhorn

%description module-matterhorn-usertracking-impl
Summary: matterhorn-usertracking-impl module for Opencast Matterhorn

%description module-matterhorn-videosegmenter-api
Summary: matterhorn-videosegmenter-api module for Opencast Matterhorn

%description module-matterhorn-videosegmenter-impl
Summary: matterhorn-videosegmenter-impl module for Opencast Matterhorn

%description module-matterhorn-videosegmenter-remote
Summary: matterhorn-videosegmenter-remote module for Opencast Matterhorn

%description module-matterhorn-webconsole
Summary: matterhorn-webconsole module for Opencast Matterhorn

%description module-matterhorn-workflow-service-api
Summary: matterhorn-workflow-service-api module for Opencast Matterhorn

%description module-matterhorn-workflow-service-impl
Summary: matterhorn-workflow-service-impl module for Opencast Matterhorn

%description module-matterhorn-workflow-service-remote
Summary: matterhorn-workflow-service-remote module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-api
Summary: matterhorn-working-file-repository-service-api module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-impl
Summary: matterhorn-working-file-repository-service-impl module for Opencast Matterhorn

%description module-matterhorn-working-file-repository-service-remote
Summary: matterhorn-working-file-repository-service-remote module for Opencast Matterhorn

%description module-matterhorn-workspace-api
Summary: matterhorn-workspace-api module for Opencast Matterhorn

%description module-matterhorn-workspace-impl
Summary: matterhorn-workspace-impl module for Opencast Matterhorn

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
rm -f matterhorn-%{version}/docs/felix/bin/start_matterhorn.bat
cp -rf matterhorn-%{version}/docs/felix/* $RPM_BUILD_ROOT/opt/matterhorn/
pushd $RPM_BUILD_ROOT/opt/matterhorn/
   mv DEPENDENCIES  felix.DEPENDENCIES
   mv LICENSE       felix.LICENSE
   mv LICENSE.kxml2 felix.LICENSE.kxml2
   mv NOTICE        felix.NOTICE
popd
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
      mvn -o -s ../settings.xml clean install -P admin,ingest,dist,dist-stub,engage,engage-stub,worker,worker-stub,workspace,workspace-stub,serviceregistry,serviceregistry-stub,directory-db,directory-ldap,capture,cas,oaipmh \
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
# nothing to do

%files base
%defattr(-,root,root,-)
%{_bindir}/*
/var/matterhorn
/opt/matterhorn/felix.*
/opt/matterhorn/bin
/opt/matterhorn/bundle
/opt/matterhorn/conf
/opt/matterhorn/doc
/opt/matterhorn/etc
/opt/matterhorn/inbox
/opt/matterhorn/lib
/opt/matterhorn/load
%{_initrddir}/*

%files distribution-default
# Nothing to do

%files profile-admin
# Nothing to do

%files profile-ingest
# Nothing to do

%files profile-dist
# Nothing to do

%files profile-dist-stub
# Nothing to do

%files profile-engage
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

%files profile-directory-db
# Nothing to do

%files profile-directory-ldap
# Nothing to do

%files profile-capture
# Nothing to do

%files profile-cas
# Nothing to do

%files profile-oaipmh
# Nothing to do




%files maven-repo
%defattr(-,root,root,-)
/opt/matterhorn/mvn2

%files module-matterhorn-admin-ui
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-admin-ui-%{version}.jar

%files module-matterhorn-annotation-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-annotation-api-%{version}.jar

%files module-matterhorn-annotation-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-annotation-impl-%{version}.jar

%files module-matterhorn-authorization-xacml
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-authorization-xacml-%{version}.jar

%files module-matterhorn-caption-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-caption-api-%{version}.jar

%files module-matterhorn-caption-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-caption-impl-%{version}.jar

%files module-matterhorn-capture-admin-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-capture-admin-service-api-%{version}.jar

%files module-matterhorn-capture-admin-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-capture-admin-service-impl-%{version}.jar

%files module-matterhorn-capture-agent-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-capture-agent-api-%{version}.jar

%files module-matterhorn-capture-agent-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-capture-agent-impl-%{version}.jar

%files module-matterhorn-cas
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-cas-%{version}.jar

%files module-matterhorn-common
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-common-%{version}.jar

%files module-matterhorn-composer-ffmpeg
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-composer-ffmpeg-%{version}.jar

%files module-matterhorn-composer-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-composer-service-api-%{version}.jar

%files module-matterhorn-composer-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-composer-service-remote-%{version}.jar

%files module-matterhorn-conductor
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-conductor-%{version}.jar

%files module-matterhorn-confidence-monitoring-ui
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-confidence-monitoring-ui-%{version}.jar

%files module-matterhorn-dataloader
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-dataloader-%{version}.jar

%files module-matterhorn-db
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-db-%{version}.jar

%files module-matterhorn-dictionary-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-dictionary-api-%{version}.jar

%files module-matterhorn-dictionary-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-dictionary-impl-%{version}.jar

%files module-matterhorn-distribution-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-distribution-service-api-%{version}.jar

%files module-matterhorn-distribution-service-download
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-distribution-service-download-%{version}.jar

%files module-matterhorn-distribution-service-download-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-distribution-service-download-remote-%{version}.jar

%files module-matterhorn-distribution-service-streaming
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-distribution-service-streaming-%{version}.jar

%files module-matterhorn-distribution-service-streaming-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-distribution-service-streaming-remote-%{version}.jar

%files module-matterhorn-dublincore
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-dublincore-%{version}.jar

%files module-matterhorn-engage-ui
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-engage-ui-%{version}.jar

%files module-matterhorn-episode-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-episode-service-api-%{version}.jar

%files module-matterhorn-episode-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-episode-service-impl-%{version}.jar

%files module-matterhorn-ingest-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-ingest-service-api-%{version}.jar

%files module-matterhorn-ingest-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-ingest-service-impl-%{version}.jar

%files module-matterhorn-inspection-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-inspection-service-api-%{version}.jar

%files module-matterhorn-inspection-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-inspection-service-impl-%{version}.jar

%files module-matterhorn-inspection-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-inspection-service-remote-%{version}.jar

%files module-matterhorn-json
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-json-%{version}.jar

%files module-matterhorn-kernel
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-kernel-%{version}.jar

%files module-matterhorn-lti
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-lti-%{version}.jar

%files module-matterhorn-metadata
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-metadata-%{version}.jar

%files module-matterhorn-metadata-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-metadata-api-%{version}.jar

%files module-matterhorn-mpeg7
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-mpeg7-%{version}.jar

%files module-matterhorn-oaipmh
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-oaipmh-%{version}.jar

%files module-matterhorn-runtime-info-ui
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-runtime-info-ui-%{version}.jar

%files module-matterhorn-scheduler-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-scheduler-api-%{version}.jar

%files module-matterhorn-scheduler-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-scheduler-impl-%{version}.jar

%files module-matterhorn-search-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-search-service-api-%{version}.jar

%files module-matterhorn-search-service-feeds
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-search-service-feeds-%{version}.jar

%files module-matterhorn-search-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-search-service-impl-%{version}.jar

%files module-matterhorn-search-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-search-service-remote-%{version}.jar

%files module-matterhorn-series-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-series-service-api-%{version}.jar

%files module-matterhorn-series-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-series-service-impl-%{version}.jar

%files module-matterhorn-serviceregistry
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-serviceregistry-%{version}.jar

%files module-matterhorn-serviceregistry-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-serviceregistry-remote-%{version}.jar

%files module-matterhorn-solr
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-solr-%{version}.jar

%files module-matterhorn-speech-recognition-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-speech-recognition-service-api-%{version}.jar

%files module-matterhorn-static
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-static-%{version}.jar

%files module-matterhorn-textanalyzer-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-textanalyzer-api-%{version}.jar

%files module-matterhorn-textanalyzer-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-textanalyzer-impl-%{version}.jar

%files module-matterhorn-textanalyzer-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-textanalyzer-remote-%{version}.jar

%files module-matterhorn-textextractor-tesseract
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-textextractor-tesseract-%{version}.jar

%files module-matterhorn-userdirectory-jpa
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-userdirectory-jpa-%{version}.jar

%files module-matterhorn-userdirectory-ldap
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-userdirectory-ldap-%{version}.jar

%files module-matterhorn-usertracking-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-usertracking-api-%{version}.jar

%files module-matterhorn-usertracking-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-usertracking-impl-%{version}.jar

%files module-matterhorn-videosegmenter-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-videosegmenter-api-%{version}.jar

%files module-matterhorn-videosegmenter-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-videosegmenter-impl-%{version}.jar

%files module-matterhorn-videosegmenter-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-videosegmenter-remote-%{version}.jar

%files module-matterhorn-webconsole
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-webconsole-%{version}.jar

%files module-matterhorn-workflow-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-workflow-service-api-%{version}.jar

%files module-matterhorn-workflow-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-workflow-service-impl-%{version}.jar

%files module-matterhorn-workflow-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-workflow-service-remote-%{version}.jar

%files module-matterhorn-working-file-repository-service-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-working-file-repository-service-api-%{version}.jar

%files module-matterhorn-working-file-repository-service-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-working-file-repository-service-impl-%{version}.jar

%files module-matterhorn-working-file-repository-service-remote
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-working-file-repository-service-remote-%{version}.jar

%files module-matterhorn-workspace-api
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-workspace-api-%{version}.jar

%files module-matterhorn-workspace-impl
%defattr(-,root,root,-)
/opt/matterhorn/matterhorn/matterhorn-workspace-impl-%{version}.jar

%changelog
* Sat Aug 29 2012 Lars Kiesow <lkiesow@uos.de> - 1.3.1-9
- Fixed requirements (switched from eq to geq for most dependencies)

* Sat Aug 28 2012 Lars Kiesow <lkiesow@uos.de> - 1.3.1-8
- Splite into modules, profiles and distributions

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
