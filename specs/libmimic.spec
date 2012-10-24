Name:           libmimic
Version:        1.0.4
Release:        5%{?dist}
Summary:        Encoding/decoding library for Mimic V2.x
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://farsight.sourceforge.net/
Source0:        http://downloads.sourceforge.net/farsight/%{name}-%{version}.tar.gz
# To regenerate:
# make <arch>
# cd libmimic-%{version}/doc/api
# tar cvfz ../../../libmimic-%{version}-pregenerated-docs.tar.gz html
Source1:        libmimic-%{version}-pregenerated-docs.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  doxygen glib2-devel

%description
libmimic is an open source video encoding/decoding library for Mimic V2.x-
encoded content (fourCC: ML20), which is the encoding used by MSN Messenger
for webcam conversations.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}, pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -a 1


%build
%configure --disable-static
make %{?_smp_mflags} libmimic_la_LIBADD="-lglib-2.0 -lm"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc html
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmimic.pc


%changelog
* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov  7 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.4-4
- Fix multilib conflict in -devel package (rf858)

* Fri Aug  7 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.4-3
- Actually link to glib-2.0 not the ancient glib (issue
  caused by the undefined-non-weak-symbol fix) (rf487)

* Thu Aug  6 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.4-2
- Fix undefined-non-weak-symbol in libmimic.so.0 (rf487)

* Sun Mar 29 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.4-1
- First version of the RPM Fusion package
