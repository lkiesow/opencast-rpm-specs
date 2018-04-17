Name:           synfig
Version:        1.2.1
Release:        2%{?dist}
Summary:        Vector-based 2D animation rendering backend

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://synfig.org/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
#Source0:        synfig-core.tar.gz
Patch0:         synfig-1.1.10-optflags.patch
Patch1:         synfig-1.0.2-ltld.patch
#Patch2:         synfig-1.0.2-includes.patch
#Patch3:         synfig-0.64.1-ppc64le.patch
# Fix source to be valid C++11.
#Patch4:         synfig-0.64.3-cxx11.patch
# Workaround gcc5 bug https://gcc.gnu.org/bugzilla/show_bug.cgi?id=48891
#Patch5:         synfig-0.64.3-gcc5-bug.patch
#Patch6:         synfig-1.2.0-array.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExcludeArch: ppc64le

BuildRequires:  ETL-devel >= 0.04.21
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  boost-devel
BuildRequires:  libsigc++-devel
BuildRequires:  libxml++-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  freetype-devel
BuildRequires:  libtool
BuildRequires:  OpenEXR-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  libmng-devel
BuildRequires:  ImageMagick-c++-devel
BuildRequires:  libjpeg-devel
BuildRequires:  autoconf automake gettext-devel intltool
BuildRequires:  mlt-devel fftw-devel
# FIXME: Lack of this causes synfig to segfault
Requires:       urw-fonts

%description
Synfig is a powerful, industrial-strength vector-based 2D animation
software, designed from the ground-up for producing feature-film quality
animation with fewer people and resources.  It is designed to be capable of
producing feature-film quality animation. It eliminates the need for
tweening, preventing the need to hand-draw each frame. Synfig features
spatial and temporal resolution independence (sharp and smoothat any
resolution or framerate), high dynamic range images, and a flexible plugin
system.

This package contains the command-line-based rendering backend.
Install synfigstudio package for GUI-based animation studio.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries

Requires:       OpenEXR-devel
Requires:       ETL-devel
Requires:       libxml2-devel
Requires:       libxml++-devel
Requires:       libsigc++20-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p0 -b .optflags
%patch1 -p0 -b .ltdl
#%patch2 -p0 -b .includes
#%patch3 -p0 -b .ppc64le
#%patch4 -p1 -b .cxx11
#%patch5 -p1 -b .gcc5-bug
#%patch6 -p0 -b .array
rm -rf libltdl


%build
#aclocal -I m4
#automake --add-missing
#autoconf -i --force
autoreconf -if
intltoolize --force
autoreconf
export CXXFLAGS="${RPM_OPT_FLAGS} -std=gnu++11"
%configure --disable-static --with-imagemagick --with-magickpp \
        --without-libavcodec --without-opengl \
        CPPFLAGS='-DMagickLib=MagickCore -I/usr/include/ImageMagick'

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
%find_lang %{name}

touch -r README $RPM_BUILD_ROOT%{_bindir}/synfig-config


%post -p /sbin/ldconfig
%postun -p/sbin/ldconfig


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/synfig_modules.cfg
%{_bindir}/synfig
%{_libdir}/libsynfig.so.*
%{_libdir}/synfig
%doc README COPYING AUTHORS NEWS


%files devel
%defattr(-,root,root,-)
%{_bindir}/synfig-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/synfig.pc
%{_includedir}/synfig-1.0
%doc doc COPYING TODO


%changelog
* Thu Sep 14 2017 Pete Walter <pwalter@fedoraproject.org> - 1.2.1-2
- Rebuilt for ImageMagick 6.9.9 soname bump

* Mon Sep 11 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.2.1-1
- 1.2.1.

* Tue Sep 05 2017 Adam Williamson <awilliam@redhat.com> - 1.2.0-11
- Rebuild for ImageMagick 6 reversion, drop ImageMagick 7 patch

* Thu Aug 24 2017 Adam Williamson <awilliam@redhat.com> - 1.2.0-10
- Rebuild for ImageMagick 7.0.6 (patch from Packman / Olaf Hering)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Björn Esser <besser82@fedoraproject.org> - 1.2.0-7
- Rebuilt for Boost 1.64

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Wed Mar 15 2017 Jon Ciesla <limburgher@gmail.com> - 1.2.0-5
- Fix CPPFLAGS, BZ 1285806.

* Tue Mar 07 2017 Jon Ciesla <limburgher@gmail.com> - 1.2.0-4
- Patch from upstream git for FTBFS.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 1.2.0-2
- Rebuilt for Boost 1.63

* Mon Jan 09 2017 Jon Ciesla <limburgher@gmail.com> - 1.2.0-1
- 1.2.0

* Tue Jul 19 2016 Jon Ciesla <limburgher@gmail.com> - 1.1.10-0.20160719gitd4e547
- Build without opengl

* Wed Jul 06 2016 Jon Ciesla <limburgher@gmail.com> - 1.1.10-0.20160706gitd4e547
- Restore optflags patch, BZ 1352535.

* Fri Jun 24 2016 Jon Ciesla <limburgher@gmail.com> - 1.1.10-0.20160624gitd4e547
- Latest upstream.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.64.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Jonathan Wakely <jwakely@redhat.com> - 0.64.3-9
- Build as C++11

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.64.3-8
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64.3-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.64.3-6
- rebuild for Boost 1.58

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.64.3-4
- Rebuilt for GCC 5 C++11 ABI change

* Fri Mar 06 2015 Jon Ciesla <limburgher@gmail.com> - 0.64.3-3
- ImageMagick rebuild.

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.64.3-2
- Rebuild for boost 1.57.0

* Tue Dec 23 2014 Jon Ciesla <limburgher@gmail.com> - 0.64.3-1
- Latest upstream, BZ 1154005.

* Wed Nov 26 2014 Rex Dieter <rdieter@fedoraproject.org> 0.64.2-3
- tighten subpkg deps (via %{?_isa})

* Wed Nov 26 2014 Jon Ciesla <limburgher@gmail.com> - 0.64.2-2
- ilmbase rebuild.

* Fri Oct 17 2014 Jon Ciesla <limburgher@gmail.com> - 0.64.2-1
- Latest upstream, BZ 1154005.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Jon Ciesla <limburgher@gmail.com> - 0.64.1-7
- Patch for ppc64le, BZ 1125287.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.64.1-5
- Rebuild for boost 1.55.0

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 0.64.1-4
- rebuild for boost 1.55.0

* Mon Mar 31 2014 Jon Ciesla <limburgher@gmail.com> - 0.64.1-3
- ImageMagick rebuild.

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.64.1-2
- rebuild (openexr)

* Tue Nov 05 2013 Jon Ciesla <limburgher@gmail.com> - 0.64.1-1
- Latest upstream, BZ 1026737.

* Mon Sep 09 2013 Jon Ciesla <limburgher@gmail.com> - 0.64.0-6
- Rebuild for several solib changes.

* Mon Aug 26 2013 Jon Ciesla <limburgher@gmail.com> - 0.64.0-5
- libmng rebuild.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Jon Ciesla <limburgher@gmail.com> - 0.64.0-3
- Fix FTBFS.

* Sat Jul 27 2013 pmachata@redhat.com - 0.64.0-2
- Rebuild for boost 1.54.0

* Mon May 13 2013 Jon Ciesla <limburgher@gmail.com> - 0.64.0-1
- Latest upstream, BZ 962136.

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.63.05-6
- rebuild (OpenEXR)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 0.63.05-4
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.63.05-3
- rebuild against new libjpeg

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.63.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Jon Ciesla <limburgher@gmail.com> - 0.63.05-1
- Latest upstream.

* Wed Feb 15 2012 Lubomir Rintel <lkundrak@v3.sk> - 0.63.04-2
- Remove an upstreamed patch

* Sat Feb 11 2012 Luya Tshimbalanga <luya@fedoraproject.org> 0.63.04-1
- New upstream version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.62.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> 0.62.02-3
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 04 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.62.02-1
- Rebase

* Tue Nov 23 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.62.01-2
- Fix build (Gilles J. Seguin)
- Adjust the ltdl patch

* Sat Sep 4 2010 Luya Tshimbalanga <luya@fedoraproject.org> - 0.62.01-1
- New upstream release

* Thu Dec 24 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.62.00-3
- Actually apply the optflags patch
- Drop bundled libltdl

* Sun Dec 20 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.62.00-2
- Work around a segfault w/o urw-fonts

* Mon Dec 7 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.62.00-1.1
- Build with older ETL

* Sat Nov 14 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.62.00-1
- New upstream release

* Fri Oct 9 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.61.09-4
- Explicitely disable avcodec

* Thu Mar 19 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.61.09-3
- Fix use of compiler flags to generate useful debuginfo

* Wed Feb 4 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.61.09-2
- RPATH sanity (thanks Nicolas Chauvet)
- Make -devel depend on libxml++-devel (thanks Lorenzo Villani)

* Fri Jan 9 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.61.09-1
- New upstream version
- Change ETL dependency to ETL-devel
- Adjust description & summary
- Add missing documentation files

* Fri Mar 7 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.61.08-5
- Fixed build requires
- Put files in the right packages
- Made it look nicer

* Fri Mar 7 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.61.08-4
- removed ImageMagick-devel since it gets brought it anyways

* Thu Mar 6 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.61.08-3
- Advised by upstream to leave openexr off due to slowness.

* Thu Mar 6 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.61.08-2
- switch the so's around

* Thu Mar 6 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.61.08-1
- new release

* Sun Jan 13 2008 Marc Wiriadisasra <marc@mwiriadi.id.au> - 0.61.07-1
- Initial Spec file
