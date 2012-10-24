Name:           gstreamer-plugins-espeak
Version:        0.3.5
Release:        2%{?dist}
Summary:        A simple gstreamer plugin to use espeak

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://wiki.sugarlabs.org/go/Activity_Team/gst-plugins-espeak
Source0:        http://download.sugarlabs.org/sources/honey/gst-plugins-espeak/gst-plugins-espeak-%{version}.tar.gz

BuildRequires:  espeak-devel
BuildRequires:  glib2-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  gstreamer-devel

%description
A simple gstreamer plugin to use espeak as a sound source.
It was developed to simplify the espeak usage in the Sugar Speak activity.
The plugin uses given text to produce audio output. 

%prep
%setup -q -n gst-plugins-espeak-%{version}


%build
# make sure to build the plugin for release
sed -i 's/NANO=1/NANO=0/g' configure
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS
%{_libdir}/gstreamer-0.10/libgstespeak.so


%changelog
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.3.5-1
- Update to 0.3.5

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 26 2009 Sebastian Dziallas <sebastian@when.com> - 0.3.3-2
- make sure to build the plugin for release
- build on ppc and ppc64 again

* Sun Sep 20 2009 Sebastian Dziallas <sebastian@when.com> - 0.3.3-1
- intial packaging
