%global shortname lept
%global libname lib%{shortname}
%global pkg_config_dir %{_libdir}/pkgconfig 
Name:    leptonica
Version: 1.69
Release: 10%{?dist}
Summary: C library for efficient image processing and image analysis operations

Group:  System Environment/Libraries
License: Leptonica
URL:     http://code.google.com/p/leptonica/
Source0: http://leptonica.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0: %{name}-%{version}.pkg-config.patch

BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: giflib-devel
BuildRequires: libwebp-devel
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The library supports many operations that are useful on
 * Document images
 * Natural images

Fundamental image processing and image analysis operations
 * Rasterop (aka bitblt)
 * Affine transforms (scaling, translation, rotation, shear)
   on images of arbitrary pixel depth
 * Projective and bi-linear transforms
 * Binary and gray scale morphology, rank order filters, and
   convolution
 * Seed-fill and connected components
 * Image transformations with changes in pixel depth, both at
   the same scale and with scale change
 * Pixelwise masking, blending, enhancement, arithmetic ops,
   etc.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .pkg-config

%build
autoreconf -ivf
%configure --disable-static --disable-rpath --program-prefix=leptonica-
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/%{libname}.la
rm -rf %{buildroot}%{_bindir}
mkdir -p %{buildroot}/%{pkg_config_dir}
install %{shortname}.pc %{buildroot}/%{pkg_config_dir}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc leptonica-license.txt README.html version-notes.html
%{_libdir}/%{libname}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{libname}.so
%{pkg_config_dir}/%{shortname}.pc

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.69-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Ding-Yi Chen <dchen at redhat.com> - 1.69-9
- Fixed Bug 904805 - [PATCH] Provide pkg-config file


* Fri Mar 08 2013 Ding-Yi Chen <dchen at redhat.com> - 1.69-8
- Rebuild to resolves #914124

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.69-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 24 2013 Ding-Yi Chen <dchen at redhat.com> - 1.69-6
- Rebuild for dependency libwebp-0.2.1-1

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.69-5
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.69-4
- Rebuild, see
  http://lists.fedoraproject.org/pipermail/devel/2012-December/175685.html

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.69-3
- rebuild against new libjpeg

* Thu Aug 02 2012 Ding-Yi Chen <dchen at redhat.com> - 1.69-2
- Fixed issues addressed in Review Request comment #8.

* Wed Jul 25 2012 Ding-Yi Chen <dchen at redhat.com> - 1.69-1
- Upstream update to 1.69
- Add program-prefix in configure.

* Wed Jun 20 2012 Ding-Yi Chen <dchen at redhat.com> - 1.68-4
- Remove util package and its binary files.

* Mon Jun 11 2012 Ding-Yi Chen <dchen at redhat.com> - 1.68-3
- Split the binary into util package

* Wed May 09 2012 Ding-Yi Chen <dchen at redhat.com> - 1.68-2
- Add zlib.h to fix the koji build

* Wed May 09 2012 Ding-Yi Chen <dchen at redhat.com> - 1.68-1
- Initial import.

