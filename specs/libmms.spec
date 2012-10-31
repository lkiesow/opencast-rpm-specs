Name:          libmms
Version:       0.6.2
Release:       4%{?dist}
Summary:       MMS stream protocol library
License:       LGPLv2+
Group:         System Environment/Libraries
URL:           http://sourceforge.net/projects/libmms
Source:        http://downloads.sourceforge.net/libmms/libmms-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glib2-devel

%description
Library implementing the MMS streaming protocol.


%package devel
Summary:  Development files for libmms
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files required for developing applications that
will use the MMS streaming protocol using libmms.


%prep
%setup -q


%build
%configure --disable-static
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB ChangeLog README*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libmms/
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmms.pc


%changelog

* Sun Mar 13 2011 Paulo Roma <roma@lcg.ufrj.br> 0.6.2-4
- Updated to 0.6.2

* Sun Jun 20 2010 Paulo Roma <roma@lcg.ufrj.br> 0.6-3
- Updated to 0.6

* Thu Apr 02 2009 Paulo Roma <roma@lcg.ufrj.br> 0.4-2
- Rebuilt for Fedora 10.

* Sun Mar 18 2008 Matthias Saou <http://freshrpms.net/> 0.4-1
- Update to 0.4.

* Wed Mar  7 2007 Matthias Saou <http://freshrpms.net/> 0.3-1
- Update to 0.3.
- Remove HTTP_PROXY support patch which is now included.

* Tue Mar 28 2006 Matthias Saou <http://freshrpms.net/> 0.2-2
- Add HTTP_PROXY support patch from Daniel S. Rogers.

* Thu Mar 23 2006 Matthias Saou <http://freshrpms.net/> 0.2-1
- Initial RPM release.

