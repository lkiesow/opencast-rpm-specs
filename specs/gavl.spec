Name:           gavl
Version:        1.1.2
Release:        2%{?dist}
Summary:        A library for handling uncompressed audio and video data

Group:          System Environment/Libraries
License:        GPLv3+
URL:            http://gmerlin.sourceforge.net/
Source0:        http://downloads.sourceforge.net/gmerlin/gavl-%{version}.tar.gz
Patch1:         gavl-1.1.1-system_libgdither.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  libtool

BuildRequires:  doxygen

BuildRequires:  libpng-devel >= 1.0.8
BuildRequires:  libgdither-devel
# Gavl use an internal tweaked libsamplerate version
# ufortunately the libsamplerate doesn't want a patch 
# that will break ABI
#BuildRequires: libsamplerate-devel



%description
Gavl is a library for handling and converting uncompressed audio and
video data. It provides datatypes for audio/video formats and standardized
structures to store the data. It supports converting between all formats.
Some conversion functions are available in multiple versions (MMX...),
which are selected by compile time configuration, CPU autodetection and
user options.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch1 -p1 -b .gdither

#Disable buildtime cpu detection
sed -i -i 's/LQT_TRY_CFLAGS/dnl LQT_TRY_CFLAGS/g' configure.ac
sed -i -i 's/LQT_OPT_CFLAGS/dnl LQT_OPT_CFLAGS/g' configure.ac

#Regenerate build tool
sh autogen.sh



%build
%configure \
  --disable-static \
  --disable-cpu-clip \
  --enable-libgdither


make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%if 0%{?el5}
if [ -d "$RPM_BUILD_ROOT/apiref" ]; then
   mkdir -p "$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/"
   mv "$RPM_BUILD_ROOT/apiref" "$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/"
fi
%endif

# Prevent timestamps build difference
touch -r include/gavl/gavl.h $RPM_BUILD_ROOT%{_includedir}/gavl/gavl_version.h


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc %{_docdir}/gavl*
%{_includedir}/gavl/
%{_libdir}/*.so
%{_libdir}/pkgconfig/gavl.pc


%changelog
* Thu Aug 16 2012 Lars Kiesow <lkiesow@uos.de> - 1.1.2-2
- Some fixed for RHEL5.x

* Sat May 01 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2

* Tue Oct 27 2009 kwizart < kwizart at gmail.com > - 1.1.1-1
- Update to 1.1.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 24 2009 kwizart < kwizart at gmail.com > - 1.1.0-1
- Update to 1.1.0
- Disable buildtime CPU detection.

* Tue Jul 29 2008 kwizart < kwizart at gmail.com > - 1.0.1-1
- Update to 1.0.1

* Tue Jul 22 2008 kwizart < kwizart at gmail.com > - 1.0.0-2
- Add --enable-libgdither for system libgdither
- Add --enable-debug to disable LQT_OPT_CFLAGS
- Add -DHAVE_GAVLCONFIG_H to include gavlconfig.h when needed

* Mon May 19 2008 kwizart < kwizart at gmail.com > - 1.0.0-1
- Update to 1.0.0 api stable

* Mon May 19 2008 kwizart < kwizart at gmail.com > - 0.2.7-4
- Initial package for Fedora
