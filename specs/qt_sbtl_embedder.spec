Name:           qt_sbtl_embedder
Version:        0.4
Release:        4%{?dist}
Summary:        QuickTime subtitle embedder

Group:          Applications/Multimedia
License:        ECL 2.0
#URL:            
Source0:        qt_sbtl_embedder-0.4.tar.gz
Source1:        http://mp4v2.googlecode.com/files/mp4v2-1.9.1.tar.bz2
Patch0:         qt_sbtl_embedder-0.4.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
    
# BuildRequires:  mp4v2-devel >= 1.9.1
# Though normally we should not do this, because of imcompatibilities to Fedora
# repository libraries we will link mp4v2 statically into the qt_sbtl_embedder


%description
The QuickTime subtitle embedder.

%prep
%setup -q -c -a 0 -a 1
%patch0 -p0
chmod a-x qt_sbtl_embedder*/src/*


%build
pushd mp4v2-1.9.1
	./configure  --enable-shared --enable-static
	make
popd
pushd qt_sbtl_embedder-0.4/
	CPPFLAGS=-I../mp4v2-1.9.1/include/ LDFLAGS=-L../mp4v2-1.9.1/.libs/ \
		./configure
	g++ -I../mp4v2-1.9.1/include/ -DHAVE_CONFIG_H -g -O2 -MT \
		src/qt_sbtl_embedder.o -MD -MP -MF src/.deps/qt_sbtl_embedder.TPo \
		-c -o src/qt_sbtl_embedder.o src/qt_sbtl_embedder.cc
	g++ -o qtsbtlembedder src/qt_sbtl_embedder.o -L../mp4v2-1.9.1/.libs/ \
		-Wl,-Bstatic -lmp4v2 -Wl,-Bdynamic
popd


%install
rm -rf $RPM_BUILD_ROOT
install -p -D -m 0755 qt_sbtl_embedder-0.4/qtsbtlembedder \
      $RPM_BUILD_ROOT%{_bindir}/qtsbtlembedder


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/qtsbtlembedder


%changelog
* Fri Sep 20 2013 Lars Kiesow <lkiesow@uos.de> - 0.4-4
- Version update to override old fake package

* Fri Sep 20 2013 Lars Kiesow <lkiesow@uos.de> - 0.4-2
- Static linked mp4v2 to circumvent conflict with libs in Fedora system repository.

* Thu Mar  1 2012 Lars Kiesow <lkiesow@uos.de> - 0.4-1
- Created package
