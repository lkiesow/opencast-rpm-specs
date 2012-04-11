Name:           vo-aacenc
Version:        0.1.2
Release:        2%{?dist}
Summary:        VisualOn AAC encoder library

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://sourceforge.net/projects/opencore-amr/
Source0:        http://netcologne.dl.sourceforge.net/project/opencore-amr/vo-aacenc/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description
This library contains an encoder implementation of the Advanced Audio Coding
(AAC) audio codec. The library is based on a codec implementation by VisualOn
as part of the Stagefright framework from the Google Android project.

%description devel
The %{name}-devel package contains header file for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --enable-static=no
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT%{_libdir}
   mv libvo-aacenc.so.0.0.3 libvo-aacenc.so.%{version}
   ln -fs libvo-aacenc.so.%{version} libvo-aacenc.so.0
   ln -fs libvo-aacenc.so.%{version} libvo-aacenc.so
popd
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README
%{_libdir}/lib%{name}*.so.*

%files devel
%defattr(-,root,root,-)
%doc COPYING ChangeLog README
%{_includedir}/vo-aacenc
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Mar  2 2012 Lars Kiesow <lkiesow@uos.de> - 0.1.2-2
- Corrected some minor packaging issues.
- Fixed library filename
* Fri Feb 24 2012 Lars Kiesow <lkiesow@uos.de> - 0.1.2-1
- Initial package for vo-aacenc.
