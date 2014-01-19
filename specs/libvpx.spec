%global majorver 1
%global minorver 3
%global tinyver  0

Name:			libvpx
Summary:		VP8 Video Codec SDK
Version:		%{majorver}.%{minorver}.%{tinyver}
%global soversion	%{version}
Release:		1%{?dist}
License:		BSD
Group:			System Environment/Libraries
# Google forgot to make a 1.2.0 tarball, so I made one from the git tag.
# git clone https://code.google.com/p/webm.libvpx/ libvpx
# cd libvpx
# git checkout v1.2.0
# rm -rf .git*
# cd ..
# mv libvpx libvpx-v1.2.0
# tar xvfj libvpx-v1.2.0.tar.bz2 libvpx-v1.2.0
Source0:		http://webm.googlecode.com/files/%{name}-v%{version}.tar.bz2
# Thanks to debian.
Source2:		libvpx.ver
URL:			http://www.webmproject.org/tools/vp8-sdk/
%ifarch %{ix86} x86_64
BuildRequires:		yasm
%endif
BuildRequires:		doxygen, php-cli

%description
libvpx provides the VP8 SDK, which allows you to integrate your applications 
with the VP8 video codec, a high quality, royalty free, open source codec 
deployed on millions of computers and devices worldwide. 

%package devel
Summary:		Development files for libvpx
Group:			Development/Libraries
Requires:		%{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against 
libvpx.

%package utils
Summary:		VP8 utilities and tools
Group:			Development/Tools
Requires:		%{name}%{?_isa} = %{version}-%{release}

%description utils
A selection of utilities and tools for VP8, including a sample encoder
and decoder.

%prep
%setup -q -n %{name}-v%{version}

%build
%ifarch %{ix86}
%global vpxtarget x86-linux-gcc
%else
%ifarch	x86_64
%global	vpxtarget x86_64-linux-gcc
%else
%global vpxtarget generic-gnu
%endif
%endif

# The configure script will reject the shared flag on the generic target
# This means we need to fall back to the manual creation we did before. :P
%if "%{vpxtarget}" == "generic-gnu"
%global generic_target 1
%else
%global	generic_target 0
%endif

./configure --target=%{vpxtarget} --enable-pic --disable-install-srcs \
%if ! %{generic_target}
--enable-shared \
%endif
--prefix=%{_prefix} --libdir=%{_libdir}

# Hack our optflags in.
sed -i "s|-O3|%{optflags}|g" libs-%{vpxtarget}.mk
sed -i "s|-O3|%{optflags}|g" examples-%{vpxtarget}.mk
sed -i "s|-O3|%{optflags}|g" docs-%{vpxtarget}.mk

make %{?_smp_mflags} verbose=true target=libs

%if %{generic_target}
# Manual shared library creation
mkdir tmp
cd tmp
ar x ../libvpx_g.a
cd ..
gcc -fPIC -shared -pthread -lm -Wl,--no-undefined -Wl,-soname,libvpx.so.%{majorver} -Wl,--version-script,%{SOURCE2} -Wl,-z,noexecstack -o libvpx.so.%{soversion} tmp/*.o
rm -rf tmp
%endif

# Temporarily dance the static libs out of the way
mv libvpx.a libNOTvpx.a
mv libvpx_g.a libNOTvpx_g.a

# We need to do this so the examples can link against it.
ln -sf libvpx.so.%{soversion} libvpx.so

make %{?_smp_mflags} verbose=true target=examples CONFIG_SHARED=1
make %{?_smp_mflags} verbose=true target=docs

# Put them back so the install doesn't fail
mv libNOTvpx.a libvpx.a
mv libNOTvpx_g.a libvpx_g.a

%install
make DIST_DIR=%{buildroot}%{_prefix} dist

# Simpler to label the dir as %doc.
mv %{buildroot}/usr/docs doc/

%if %{generic_target}
install -p libvpx.so.%{soversion} %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -sf libvpx.so.%{soversion} libvpx.so
ln -sf libvpx.so.%{soversion} libvpx.so.%{majorver}
ln -sf libvpx.so.%{soversion} libvpx.so.%{majorver}.%{minorver}
popd
%endif

pushd %{buildroot}
# Stuff we don't need.
rm -rf usr/build/ usr/md5sums.txt usr/lib*/*.a usr/CHANGELOG usr/README
# Rename a few examples
mv usr/bin/postproc usr/bin/vp8_postproc
mv usr/bin/simple_decoder usr/bin/vp8_simple_decoder
mv usr/bin/simple_encoder usr/bin/vp8_simple_encoder
mv usr/bin/twopass_encoder usr/bin/vp8_twopass_encoder
# Fix the binary permissions
chmod 755 usr/bin/*
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS CHANGELOG LICENSE README
%{_libdir}/libvpx.so.*

%files devel
# These are SDK docs, not really useful to an end-user.
%doc docs/html/
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so

%files utils
%{_bindir}/*

%changelog
* Wed Jan 15 2014 Lars Kiesow <lkiesow@uos.de> - 		1.3.0-1
- Update to 1.3.0

* Thu Feb 28 2013 Tom Callaway <spot@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Tom Callaway <spot@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Tue May 29 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0-3
- fix vpx.pc file to include -lm (bz825754)

* Fri May 11 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0-2
- use included vpx.pc file (drop local libvpx.pc)
- apply upstream fix to vpx.pc file (bz 814177)

* Mon Jan 30 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0-1
- update to 1.0.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Dan Horák <dan[at]danny.cz> - 0.9.7.1-3
- use macro instead of hard-coded version

* Mon Sep 12 2011 Dan Horák <dan[at]danny.cz> - 0.9.7.1-2
- fix build on generic targets

* Tue Aug 16 2011 Adam Jackson <ajax@redhat.com> 0.9.7.1-1
- libvpx 0.9.7-p1

* Tue Aug 09 2011 Adam Jackson <ajax@redhat.com> 0.9.7-1
- libvpx 0.9.7

* Mon Mar 21 2011 Dan Horák <dan[at]danny.cz> - 0.9.6-2
- add 2 symbols to the shared library for generic targets

* Thu Mar 10 2011 Tom Callaway <spot@fedoraproject.org> - 0.9.6-1
- update to 0.9.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.5-2
- apply patch from upstream git (Change I6266aba7), should resolve CVE-2010-4203

* Mon Nov  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.5-1
- update to 0.9.5

* Wed Sep  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.1-3
- only package html docs to avoid multilib conflict (bz 613185)

* Thu Jun 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.1-2
- build shared library the old way for generic arches

* Thu Jun 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.1-1
- update to 0.9.1

* Fri Jun 11 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-7
- update to git revision 8389f1967c5f8b3819cca80705b1b4ba04132b93
- upstream fix for bz 599147
- proper shared library support

* Wed Jun  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-6
- add hackish fix for bz 599147 
  (upstream will hopefully fix properly in future release)

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-5
- fix noexecstack flag

* Thu May 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-4
- BuildRequires: yasm (we're optimized again)

* Thu May 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-3
- add pkg-config file
- move headers into include/vpx/
- enable optimization

* Thu May 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-2
- fix permissions on binaries
- rename generic binaries to v8_*
- link shared library to -lm, -lpthread to resolve missing weak symbols

* Wed May 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-1
- Initial package for Fedora
