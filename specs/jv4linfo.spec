Name:           jv4linfo
Version:        0.2.1
Release:        1%{?dist}
Summary:        Java API to query and control video4linux(two) devices through JNI

Group:          System Environment/Libraries
License:        LGPLv2+ or GPLv2+
URL:            http://luniks.net/java/jv4linfo.do
Source0:        http://luniks.net/luniksnet/download/java/jv4linfo/jv4linfo-0.2.1-src.jar

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant
Requires:       jpackage-utils
Requires:       java

%description
jv4linfo is a Java API that allows to query and control video4linux(two)
devices through the JNI. The data is organized in Java objects while trying to
use the same structure as the v4l/v4l2 API. Currently it does not support
capturing video, but it can be used to create a so-called "panel" application,
an application that controls a video device, such as selecting the frequency of
its tuner.
jv4linfo is under development and therefore incomplete and experimental. The
existing functionality should however work.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -c %{name}-%{version}

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%build
pushd jv4linfo/src
mv build.xml build.xml.bak
cat build.xml.bak | \
   sed -r 's/java.include" value="\/usr\/lib\/jvm\/java-6-openjdk\/inc/java.include" value="\/usr\/lib\/jvm\/java-openjdk\/inc/g' | \
   sed -r 's/<arg value="-shared"\/>/<arg value="-fPIC"\/><arg value="-shared"\/>/g' > build.xml
pushd net/luniks/linux/jv4linfo/
cp JV4LInfo.java JV4LInfo.java.bak 
cat JV4LInfo.java.bak | sed -r 's,System.loadLibrary\(LIBRARY\),System.load("%{_libdir}/%{name}/libjv4linfo.so"),g' > JV4LInfo.java
popd
ant
popd

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -p jv4linfo/lib/jv4linfo.jar   $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name}.jar
cp -p jv4linfo/lib/libjv4linfo.so $RPM_BUILD_ROOT%{_libdir}/%{name}/lib%{name}.so

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp jv4linfo/doc/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}
%doc

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}


%changelog
* Sat Nov 17 2012 Lars Kiesow <lkiesow@uos.de> - 0.2.1-1
- Initial build for CentOS 6
