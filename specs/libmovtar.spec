Summary: Tools for the movtar MJPEG video format
Name: libmovtar
Version: 0.1.3
Release: 9%{?dist}
License: GPL
URL: http://mjpeg.sourceforge.net/
Group: Applications/Multimedia
Source0: http://prdownloads.sourceforge.net/mjpeg/libmovtar-%{version}.tar.gz
Source1: http://prdownloads.sourceforge.net/mjpeg/jpeg-mmx-0.1.6.tar.gz
Patch0: jpeg-mmx-0.1.6-asm.patch
Patch1: libmovtar-0.1.3.patch
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: SDL-devel >= 1.1.3, glib-devel >= 1.2.0
BuildRequires: libjpeg-devel
BuildRequires: nasm

%description
This package includes libmovtar, the support library, and various
tools which together implement the movtar MJPEG video format.

%package devel
Summary: Development headers and libraries for the movtar MJPEG video format.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains static libraries and C system header files
needed to compile applications that use part of the libraries
of the mjpegtools package.

%prep
%setup -q -a1
%patch0 -p0 -b .jpegmmx
%patch1 -p1 -b .libmovtar

%build
%ifnarch %ix86
export CFLAGS="%{optflags} -I`pwd`/jpeg-mmx"
%configure
%else
cd jpeg-mmx
%configure
make
cd ..
export CFLAGS="%{optflags} -I`pwd`/jpeg-mmx"
%configure --with-jpeg-mmx=`pwd`/jpeg-mmx
%endif

make

%install
rm -rf %{buildroot}
%makeinstall

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README*
%{_bindir}/movtar_*
%{_bindir}/pnm2rtj
%{_bindir}/rtjshow

%files devel
%defattr(-,root,root,-)
%{_bindir}/movtar-config
%{_includedir}/*
%{_libdir}/*.a
%{_datadir}/aclocal/*

%changelog
* Tue Apr 13 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Unbundle jpeg-mmx.

* Sat Oct 18 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Added dependency to XFree86-devel, because SDL-devel under RH7.3 is missing it.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial release for Red Hat Linux 9.

