Name:			libvpx
Summary:		VP8 Video Codec SDK
Version:		0.9.7.1
Release:		1%{?dist}
License:		BSD
Group:			System Environment/Libraries
# sigh, non-canonical version strings.  clean up in 0.9.8 plz.
#Source0:		http://webm.googlecode.com/files/%{name}-v%{version}.tar.bz2
Source0:		http://webm.googlecode.com/files/%{name}-v0.9.7-p1.tar.bz2
# Probably this should be dropped now that upstream ships a vpx.pc;
# not for F16 though
Source1:		libvpx.pc
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
Requires:		%{name} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against 
libvpx.

%package utils
Summary:		VP8 utilities and tools
Group:			Development/Tools
Requires:		%{name} = %{version}-%{release}

%description utils
A selection of utilities and tools for VP8, including a sample encoder
and decoder.

%prep
#setup -q -n %{name}-v%{version}
%setup -q -n %{name}-v0.9.7-p1

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
# gcc -fPIC -shared -pthread -lm -Wl,--no-undefined -Wl,-soname,libvpx.so.0 -Wl,--version-script,%{SOURCE2} -Wl,-z,noexecstack -o libvpx.so.%{version} tmp/*.o
gcc -fPIC -shared -pthread -lm -Wl,--no-undefined -Wl,-soname,libvpx.so.0 -Wl,--version-script,%{SOURCE2} -Wl,-z,noexecstack -o libvpx.so.0.9.7 tmp/*.o
rm -rf tmp
%endif

# Temporarily dance the static libs out of the way
mv libvpx.a libNOTvpx.a
mv libvpx_g.a libNOTvpx_g.a

# We need to do this so the examples can link against it.
# ln -sf libvpx.so.%{version} libvpx.so
ln -sf libvpx.so.0.9.7 libvpx.so

make %{?_smp_mflags} verbose=true target=examples
make %{?_smp_mflags} verbose=true target=docs

# Put them back so the install doesn't fail
mv libNOTvpx.a libvpx.a
mv libNOTvpx_g.a libvpx_g.a

%install
make DIST_DIR=%{buildroot}%{_prefix} dist

# Install the pkg-config file
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
# Fill in the variables
sed -i "s|@PREFIX@|%{_prefix}|g" %{buildroot}%{_libdir}/pkgconfig/libvpx.pc
sed -i "s|@LIBDIR@|%{_libdir}|g" %{buildroot}%{_libdir}/pkgconfig/libvpx.pc
sed -i "s|@INCLUDEDIR@|%{_includedir}|g" %{buildroot}%{_libdir}/pkgconfig/libvpx.pc

# Simpler to label the dir as %doc.
mv %{buildroot}/usr/docs doc/

%if %{generic_target}
install -p libvpx.so.%{version} %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -sf libvpx.so.%{version} libvpx.so
ln -sf libvpx.so.%{version} libvpx.so.0
ln -sf libvpx.so.%{version} libvpx.so.0.9
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

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG LICENSE README
%{_libdir}/libvpx.so.*

%files devel
%defattr(-,root,root,-)
# These are SDK docs, not really useful to an end-user.
%doc docs/html/
%{_includedir}/vpx/
%{_libdir}/pkgconfig/libvpx.pc
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so

%files utils
%defattr(-,root,root,-)
%{_bindir}/*

%changelog
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
