Name:           soxr
Version:        0.1.1
Release:        1%{?dist}
Summary:        The SoX Resampler library

License:        LGPLv2+
URL:            https://sourceforge.net/p/soxr/wiki/Home/ 
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-Source.tar.xz

BuildRequires:  cmake

%description
The SoX Resampler library `libsoxr' performs one-dimensional sample-rate
conversion -- it may be used, for example, to resample PCM-encoded audio.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}-Source

# Fix Cmake version (2.6 is sufficient)
sed -i 's/cmake_minimum_required (VERSION 2.8 FATAL_ERROR)/cmake_minimum_required (VERSION 2.6 FATAL_ERROR)/' CMakeLists.txt


%build
rm -rf build && mkdir build && pushd build
export LDFLAGS="-Wl,--as-needed"
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       ../
make %{?_smp_mflags}


%install
pushd build
%make_install

# Remove docs and use the rpmbuild macro instead
rm -rf %{buildroot}%{_docdir}/*



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc LICENCE NEWS README
%{_libdir}/*.so.*

%files devel
%doc examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/soxr-lsr.pc
%{_libdir}/pkgconfig/soxr.pc


%changelog
* Mon Apr 29 2013 Richard Shaw <hobbes1069@gmail.com> - 0.1.1-1
- Initial packaging.
