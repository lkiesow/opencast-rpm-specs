Name:          opus
Version:       1.0.1
Release:       2%{?dist}
Summary:       An audio codec for use in low-delay speech and audio communication

Group:         System Environment/Libraries
License:       BSD
URL:           http://www.opus-codec.org/
Source0:       http://downloads.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz
# This is the current IETF Working Group draft
Source1:       http://tools.ietf.org/rfc/rfc6716.txt 

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

%package devel
Summary: Development package for opus
Group: Development/Libraries
Requires: libogg-devel
Requires: opus = %{version}-%{release}

%description devel
Files for development with opus.

%prep
%setup -q
cp %{SOURCE1} .

%build
%configure

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove libtool archives and static libs
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README rfc6716.txt
%doc %{_mandir}/man3/opus*
%doc %{_defaultdocdir}/opus/
%{_libdir}/libopus.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/opus
%{_libdir}/libopus.so
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4

%changelog
* Fri Oct 19 2012 Lars Kiesow <lkiesow@uos.de> - 1.0.1-2
- Packaged documentation

* Wed Sep 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1-1
- Official 1.0.1 release now rfc6716 is stable

* Tue Sep  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1rc3-0.1
- Update to 1.0.1rc3

* Thu Aug  9 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0rc1-0.1
- Update to 1.0.0rc1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.14-1
- Update to 0.9.14

* Sat May 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.10-2
- Add make check - fixes RHBZ # 821128

* Fri Apr 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.10-1
- Update to 0.9.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  8 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.8-1
- Update to 0.9.8

* Mon Oct 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.6-1
- Initial packaging
