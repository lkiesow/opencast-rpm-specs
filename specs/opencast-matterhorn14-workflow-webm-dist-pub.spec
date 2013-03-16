Name:     opencast-matterhorn14-workflow-webm-dist-pub
Version:  1.0
Release:  2%{?dist}
Summary:  WebM-HQ workflow for Opencast Matterhorn

License:   ECL 2.0
URL:       http://www.virtuos.uni-osnabrueck.de
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch

Requires: opencast-matterhorn14-base
Requires: opencast-matterhorn14-encodingprofile-webm-movies

%description
This Opencast Matterhorn workflow specification contains the following steps:
- Encode to WebM and thumbnail.
- Distribute to local repository.
- Publish to search index.

%prep
%setup -q


%build
# Normally we would build the sources here


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/matterhorn/workflows
cp webm-dist-pub.xml %{buildroot}%{_sysconfdir}/matterhorn/workflows


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/matterhorn/workflows/*



%changelog
* Sat Mar 16 2013 Lars Kiesow <lkiesow@uos.de> - 1.0-2
- Fixed workflow sirectory

* Sat Mar 16 2013 Lars Kiesow <lkiesow@uos.de> - 1.0-1
- Initial package
