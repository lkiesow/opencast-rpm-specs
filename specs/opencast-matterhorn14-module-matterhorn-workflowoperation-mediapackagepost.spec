Name:     opencast-matterhorn14-module-matterhorn-workflowoperation-mediapackagepost
Version:  1.1
Release:  2%{?dist}
Summary:  Mediapackage POST workflow operation for Opencast Matterhorn

License:   ECL 2.0
URL:       http://www.virtuos.uni-osnabrueck.de
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch

Requires: opencast-matterhorn14-base

%description
This Opencast Matterhorn module contains a workflow operation which will send a
Matterhorn madiapackage as HTTP POST request to a specified URL.

%prep
%setup -q


%build
# Normally we would build the sources here


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/matterhorn/lib/matterhorn
cp matterhorn-workflowoperation-mediapackagepost-1.1.jar \
   %{buildroot}/opt/matterhorn/lib/matterhorn
mkdir -p %{buildroot}/opt/matterhorn/docs/
cp -r module-docs/ %{buildroot}/opt/matterhorn/docs/


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc /opt/matterhorn/docs/module-docs/
/opt/matterhorn/lib/matterhorn/*



%changelog
* Sat Mar 16 2013 Lars Kiesow <lkiesow@uos.de> - 1.1-2
- Fixed architecture
- Fixed license

* Sat Mar 16 2013 Lars Kiesow <lkiesow@uos.de> - 1.1-1
- Initial package
