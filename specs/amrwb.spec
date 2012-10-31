Name:           amrwb
Version:        7.0.0.3
Release:        6%{?dist}
Summary:        Adaptive Multi-Rate - Wideband (AMR-WB) Speech Codec
Group:          System Environment/Libraries
License:        Distributable
URL:            http://www.penguin.cz/~utx/amr
Source0:        http://ftp.penguin.cz/pub/users/utx/amr/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  wget unzip

%description
Adaptive Multi-Rate Wideband decoder and encoder library.
(3GPP TS 26.204 V7.0.0)

http://www.3gpp.org/ftp/Specs/html-info/26204.htm


%package tools
Group:          Applications/Multimedia
Summary:        Adaptive Multi-Rate - Wideband (AMR-WB) Speech Codec tools
Requires:       %{name} = %{version}-%{release}

%description tools
Adaptive Multi-Rate Wideband decoding and encoding tools.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
# Note we do the wget ourselves so that we can use in IP in the URL as there
# is no /etc/resolv.conf in the buildroot
wget ftp://195.238.226.15/Specs/archive/26_series/26.204/26204-700.zip


%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr (-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO readme.txt
%{_libdir}/*.so.*

%files tools
%defattr (-,root,root,-)
%{_bindir}/*

%files devel
%defattr (-,root,root,-)
%{_includedir}/amrwb
%{_libdir}/*.so


%changelog
* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 7.0.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 7.0.0.3-5
- rebuild for new F11 features

* Sat Aug 16 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 7.0.0.3-4
- wget the needed sources in %%prep instead of letting the Makefile do it
  so that we can use an IP address to work around there being no
  /etc/resolv.conf in the buildroot

* Fri Jul 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 7.0.0.3-3
- Release bump for rpmfusion

* Thu Jun 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 7.0.0.3-2
- Fix rpath on x86_64
- Put tools in a seperate -tools package

* Thu Jun 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 7.0.0.3-1
- Initial rpmfusion package based on upstream specfile
