Name:           libzen
Version:        0.4.23
Release:        0.20120109.1%{?dist}
Summary:        Supplies information about a video or audio file

Group:          System Environment/Libraries
License:        LGPLv3
# Should be URL: http://zenlib.sourceforge.net
# but the URL above is not helpful.
URL:            http://sourceforge.net/projects/zenlib
Source0:        http://downloads.sourceforge.net/zenlib/libzen_%{version}.tar.bz2
Patch0:         libzen-0.4.19.diff


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  automake libtool
BuildRequires:  /usr/bin/doxygen
BuildRequires:  /usr/bin/dos2unix

# For Debian/openSUSE/upstream package compatibility
Provides:       libzen0 = %{version}-%{release}

# Kick out ZenLib packages
Provides:       ZenLib = %{version}-%{release}
Obsoletes:      ZenLib < %{version}-%{release}

%description
%{summary}

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       libzen0-devel = %{version}-%{release}
Provides:       ZenLib-devel = %{version}-%{release}
Obsoletes:      ZenLib-devel < %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -c -T -n %{name}-%{version}
%setup -q -T -D -n %{name}-%{version} -a0
cd ZenLib
%patch0 -p1
cd ..

# Fix broken permissions
find ZenLib -type f -exec chmod -x {} \;

# Convert to unix
/usr/bin/dos2unix ZenLib/*.txt

# Update Doxyfile
pushd ZenLib/Source/Doc
/usr/bin/doxygen -u Doxyfile
popd


# Fix up Makefile.am
cat << EOF >> ZenLib/Project/GNU/Library/Makefile.am

bin_SCRIPTS = libzen-config

pkgconfigdir = \$(libdir)/pkgconfig
pkgconfig_DATA = libzen.pc

EOF

pushd ZenLib/Source
for dir in \
ZenLib \
ZenLib/HTTP_Client \
ZenLib/Base64 \
ZenLib/Format/Html \
ZenLib/Format/Http \
ZenLib/TinyXml; do
destdir=$(echo $dir | tr / _)
cat << EOF >> ../Project/GNU/Library/Makefile.am
${destdir}dir = \$(includedir)/$dir
${destdir}_HEADERS =
EOF
for f in $dir/*.h; do
echo "${destdir}_HEADERS += ../../../Source/$f" >> ../Project/GNU/Library/Makefile.am
done
done
popd

pushd ZenLib/Project/GNU/Library > /dev/null
autoreconf -fi
chmod +x configure
popd > /dev/null

%build
pushd ZenLib/Project/GNU/Library > /dev/null
%configure --disable-static --enable-shared
make %{?_smp_mflags}
popd > /dev/null

pushd ZenLib/Source/Doc > /dev/null
/usr/bin/doxygen Doxyfile
popd > /dev/null

# Pulls in bogus package deps
rm -f ZenLib/Doc/installdox

%install
pushd ZenLib/Project/GNU/Library > /dev/null
make install DESTDIR=$RPM_BUILD_ROOT
popd > /dev/null

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc ZenLib/License.txt
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc ZenLib/ReadMe.txt ZenLib/History.txt ZenLib/Doc/*
%{_bindir}/libzen-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libzen.pc

%changelog
* Mon Jan 09 2012 Ralf Corsépius <ralf@links2linux.de> - 0.4.23-0.20120109.1
- Upstream update.

* Wed Sep 21 2011 Ralf Corsépius <ralf@links2linux.de> - 0.4.21-0.20110921.1
- Upstream update.

* Fri Apr 15 2011 Ralf Corsépius <ralf@links2linux.de> - 0.4.19-0.20110415.1
- Install ZenLib/TinyXml headers.

* Fri Apr 15 2011 Ralf Corsépius <ralf@links2linux.de> - 0.4.19-0.20110415.0
- Upstream update.
- Spec file cleanup.

* Mon Mar 15 2010 Ralf Corsépius <ralf@links2linux.de> - 0.4.12-0.20100315.1
- More spec-file tweaks.

* Sun Mar 14 2010 Ralf Corsépius <ralf@links2linux.de> - 0.4.12-0.20100314.1
- rm -f instdox.

* Sun Mar 14 2010 Ralf Corsépius <ralf@links2linux.de> - 0.4.12-0.20100314.0
- Rework libzen-config.

* Fri Mar 12 2010 Ralf Corsépius <ralf@links2linux.de> - 0.4.12-0.20100312.0
- Initial Fedora package.
