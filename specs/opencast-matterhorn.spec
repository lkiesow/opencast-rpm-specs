Name:           opencast-matterhorn
Version:        1.3.1
Release:        3%{?dist}
Summary:        Open Source Lecture Capture & Video Management Tool

Group:          Applications/Multimedia
License:        ECL 2.0, APL2 and other
URL:            http://opencast.org/matterhorn/
    
Requires:       opencast-matterhorn13


%description
Matterhorn is a free, open-source platform to support the management of
educational audio and video content. Institutions will use Matterhorn to
produce lecture recordings, manage existing video, serve designated
distribution channels, and provide user interfaces to engage students with
educational videos.

This is a metapackage which keeps track of the newest Matterhorn version. Major
releases of Matterhorn ay be incompatible with each other. Thus this package
should not be used for regular updates on a productive system.

%prep
# nothing to do

%build
# nothing to do

%pre
# nothing to do

%post
# nothing to do

%install
# nothing to do

%clean
# nothing to do

%files
# nothing to do


%changelog
* Fri Aug 24 2012 Lars Kiesow <lkiesow@uos.de> - 1.3.1-3
- Created metapackage for newest matterhorn version
