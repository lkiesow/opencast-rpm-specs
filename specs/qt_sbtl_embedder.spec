Name:           qt_sbtl_embedder
Version:        0.4
Release:        1%{?dist}
Summary:        QuickTime subtitle embedder

Group:          Applications/Multimedia
License:        ECL 2.0
#URL:            
Source0:        qt_sbtl_embedder-0.4.tar.gz
Patch0:         qt_sbtl_embedder-0.4.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
    
BuildRequires:  mp4v2-devel >= 1.9.1


%description
The QuickTime subtitle embedder.

%prep
%setup -q
pushd ..
%patch0 -p0
popd
chmod a-x src/*


%build
%configure
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*


%changelog
* Thu Mar  1 2012 Lars Kiesow <lkiesow@uos.de> - 0.4-1
- Created package
