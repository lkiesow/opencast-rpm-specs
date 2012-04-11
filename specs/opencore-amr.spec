Name:           opencore-amr
Version:        0.1.2
Release:        2%{?dist}
Summary:        OpenCORE Adaptive Multi Rate Narrowband and Wideband speech lib
Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://sourceforge.net/projects/opencore-amr/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Library of OpenCORE Framework implementation of Adaptive Multi Rate Narrowband
and Wideband speech codec.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
mv opencore/README opencore/README.opencore


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libopencore-amr??.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc LICENSE README opencore/ChangeLog opencore/NOTICE opencore/README.opencore
%{_libdir}/libopencore-amr??.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/opencore-amr??
%{_libdir}/libopencore-amr??.so
%{_libdir}/pkgconfig/opencore-amr??.pc

%changelog
* Wed Jan 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-2
- Rebuilt for target i686

* Sun Oct  4 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-1
- New upstream release 0.1.2

* Thu Jul 30 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.1-1
- First version of the RPM Fusion package
