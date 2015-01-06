%global _enable_devel_packages 1

Summary: A minimalistic plugin API for video effects
Name: frei0r-plugins
Version: 1.3
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://frei0r.dyne.org/
#Source0: ftp://ftp.dyne.org/frei0r/releases/frei0r-plugins-%{version}.tar.gz
Source0: http://pkgs.fedoraproject.org/repo/pkgs/frei0r-plugins/frei0r-plugins-%{version}.tar.gz/a2eb63feeeb0c5cf439ccca276cbf70c/frei0r-plugins-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: opencv-devel >= 2.0.0, gavl-devel >= 0.2.3

%description
Frei0r is a minimalistic plugin API for video effects.

The main emphasis is on simplicity for an API that will round up the
most common video effects into simple filters, sources and mixers that
can be controlled by parameters.


%package devel
Summary:    Development files for frei0r-plugins
Group:      Development/Libraries
Requires:   %{name} = %{version}

%description devel
Development files for frei0r-plugins.


%prep
%setup -q -n frei0r-%{version}
pushd src/filter
chmod a-x */*
popd

%build
%configure --disable-static
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mv %{buildroot}%{_docdir}/%{name} %{buildroot}%{_docdir}/%{name}-%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_libdir}/frei0r-1

%files devel
%defattr(-,root,root,-)
%{_includedir}/frei0r.h
%{_libdir}/pkgconfig/frei0r.pc

%changelog
* Tue Aug 21 2012 Lars Kiesow <lkiesow@uos.de> - 1.3-3
- Fixed dependencies (OpenCV 1 was to old)

* Tue Feb 14 2012 Lars Kiesow <lkiesow@uos.de> - 1.3-2
- Fixed issue with include and pkgconfig files by building a devel package:
  "Installed (but unpackaged) file(s) found"

* Mon Mar 14 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3-1
- Initial build.
