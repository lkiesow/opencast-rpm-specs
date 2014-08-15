Name:           maven
Version:        3.2.1
Release:        2%{?dist}
Summary:        Java project management and project comprehension tool

Group:          Applications/Multimedia
License:        APL2
URL:            http://maven.apache.org/
Source0:        http://mirror.serversupportforum.de/apache/maven/maven-3/%{version}/binaries/apache-%{name}-%{version}-bin.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
    
BuildArch: noarch

%if 0%{?rhel} == 6
Requires: java-1.7.0-openjdk-devel >= 1:1.7.0
%else
Requires: java-devel >= 1:1.7.0
%endif


%description
Apache Maven is a software project management and comprehension tool. Based on
the concept of a project object model (POM), Maven can manage a project's
build, reporting and documentation from a central piece of information.

%prep
%setup -qn apache-%{name}-%{version}
pushd conf
   chmod a-x settings.xml
   chmod g-w settings.xml
popd


%build
#Nothing to do


%install
rm -rf %{buildroot}
install -dm 755 %{buildroot}%{_bindir}
install -dm 755 %{buildroot}%{_datadir}/%{name}/{bin,boot,conf/logging,lib/ext}
install -dm 755 %{buildroot}%{_datadir}/java/%{name}
install -dm 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 755 bin/mvn           %{buildroot}%{_datadir}/%{name}/bin
install -m 755 bin/mvnDebug      %{buildroot}%{_datadir}/%{name}/bin
install -m 755 bin/mvnyjp        %{buildroot}%{_datadir}/%{name}/bin
install -m 644 bin/m2.conf       %{buildroot}%{_sysconfdir}/%{name}
install -m 644 conf/settings.xml %{buildroot}%{_sysconfdir}/%{name}
install -m 644 conf/logging/simplelogger.properties %{buildroot}%{_sysconfdir}/%{name}
install -m 644 lib/*.jar         %{buildroot}%{_datadir}/java/%{name}
#%__install -dm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
# Install symlinks
ln -s %{_datadir}/%{name}/bin/mvn         %{buildroot}%{_bindir}/mvn
ln -s %{_datadir}/%{name}/bin/mvnDebug    %{buildroot}%{_bindir}/mvnDebug
ln -s %{_datadir}/%{name}/bin/mvnyjp      %{buildroot}%{_bindir}/mvnyjp
ln -s %{_sysconfdir}/%{name}/m2.conf      %{buildroot}%{_datadir}/%{name}/bin/m2.conf
ln -s %{_sysconfdir}/%{name}/settings.xml %{buildroot}%{_datadir}/%{name}/conf/settings.xml
ln -s %{_sysconfdir}/%{name}/simplelogger.properties %{buildroot}%{_datadir}/%{name}/conf/logging/simplelogger.properties
pushd %{buildroot}%{_datadir}/java/%{name}
   for i in *.jar
   do
      ln -s "%{_datadir}/java/%{name}/$i" "%{buildroot}%{_datadir}/%{name}/lib/$i"
   done
popd
install -m 644 boot/plexus-classworlds-2.5.1.jar  %{buildroot}%{_datadir}/java/%{name}
ln -s %{_datadir}/java/%{name}/plexus-classworlds-2.5.1.jar \
   %{buildroot}%{_datadir}/%{name}/boot/plexus-classworlds-2.5.1.jar



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/%{name}
%{_datadir}/java/%{name}


%changelog
* Thu Aug 14 2014 Lars Kiesow <lkiesow@uos.de> - 3.2.1-2
- Set to use OpenJDK 1.7

* Fri Apr 11 2014 Lars Kiesow <lkiesow@uos.de> - 3.2.1-1
- Update to version 3.2.1

* Fri Mar  9 2012 Lars Kiesow <lkiesow@uos.de> - 3.0.4-1
- Created package
