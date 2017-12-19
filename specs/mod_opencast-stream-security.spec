%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0-0)}}

%global gitversion 790ef6f0e5f8
%global srcname apache-httpd-stream-security-plugin

Name:          mod_opencast-stream-security
Summary:       Opencast Stream Security URL Signing Provider for the Apache HTTPd server
Version:       0
Release:       0.1.%{gitversion}%{?dist}
License:       ECL2

Source:        https://bitbucket.org/opencast-community/%{srcname}/get/790ef6f0e5f8.tar.gz
URL:           https://bitbucket.org/opencast-community/%{srcname}
BuildRoot:     %{_tmppath}/%{name}-root

BuildRequires: jansson-devel
BuildRequires: httpd-devel
BuildRequires: libtool
BuildRequires: openssl-devel

Requires: httpd
Requires: httpd-mmn = %{_httpd_mmn}


%description
This plugin brings Opencast Stream Security to the Apache HTTPd server.

Opencast installations can use Apache HTTPd to distribute files over HTTP(S),
with the verification of signed URLs carried out by this module.


%prep
%setup -q -n opencast-community-%{srcname}-%{gitversion}

%build
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
            --mandir=%{_mandir}
make


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_httpd_modconfdir}
echo -n 'LoadModule stream_security_module modules/mod_stream_security.so' \
	> %{buildroot}%{_httpd_modconfdir}/00-stream-security.conf


%clean
rm -rf %{buildroot}


#%post -p /sbin/ldconfig
#%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README* NOTICES LICENSE
%config %{_httpd_modconfdir}/00-stream-security.conf
%{_libdir}/httpd/modules/mod_stream_security.so


%changelog
* Mon Mar 13 2017 Lars Kiesow <lkiesow@uos.de> 0-0.1.
- Initial build
