Name:     opencast-matterhorn14-encodingprofile-webm-movies
Version:  1.0
Release:  1%{?dist}
Summary:  High Quality WebM encoding profile for Opencast Matterhorn

License:   ECL 2.0
URL:       http://www.virtuos.uni-osnabrueck.de
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch

Requires: opencast-matterhorn14-base

%description
This Opencast Matterhorn module will convert a video into the WebM format.

%prep
%setup -q


%build
# Normally we would build the sources here


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/matterhorn/encoding
cp webm-movies.properties %{buildroot}%{_sysconfdir}/matterhorn/encoding


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/matterhorn/encoding/*



%changelog
* Sat Mar 16 2013 Lars Kiesow <lkiesow@uos.de> - 1.0-1
- Initial package
