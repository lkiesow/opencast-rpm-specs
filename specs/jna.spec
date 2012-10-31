Name:           jna
Version:        3.2.7
Release:        10%{?dist}
Summary:        Pure Java access to native libraries

Group:          Development/Libraries
License:        LGPLv2+
URL:            https://jna.dev.java.net/
# The source for this package was pulled from upstream's vcs. Use the
# following commands to generate the tarball:
#   svn export https://jna.dev.java.net/svn/jna/tags/%{version}/jnalib/ --username guest jna-%{version}
#   rm -rf jna-%{version}/dist/*
#   tar cjf ~/rpm/SOURCES/jna-%{version}.tar.bz2 jna-%{version}
Source0:        %{name}-%{version}.tar.bz2
Source1:	%{name}-pom.xml
# This patch is Fedora-specific for now until we get the huge
# JNI library location mess sorted upstream
Patch1:         jna-3.2.5-loadlibrary.patch
# The X11 tests currently segfault; overall I think the X11 JNA stuff is just a 
# Really Bad Idea, for relying on AWT internals, using the X11 API at all,
# and using a complex API like X11 through JNA just increases the potential
# for problems.
Patch2:         jna-3.2.4-tests-headless.patch
Patch3:         jna-3.2.7-javadoc.patch
# Build using GCJ javadoc
Patch4:         jna-3.2.7-gcj-javadoc.patch
# junit cames from rpm
Patch5:         jna-3.2.5-junit.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# We manually require libffi because find-requires doesn't work
# inside jars.
Requires:       java >= 1:1.6.0, jpackage-utils, libffi
Requires(post):	jpackage-utils
Requires(postun): jpackage-utils
BuildRequires:  java-devel >= 1:1.6.0, jpackage-utils, libffi-devel
BuildRequires:  ant, ant-junit, ant-nodeps, ant-trax, junit
BuildRequires:  libX11-devel, libXt-devel
# for ExclusiveArch see bug: 468831 640005 548099
%if 0%{?fedora} < 10 && 0%{?rhel} < 6
ExclusiveArch: %{ix86} x86_64
%endif


%description
JNA provides Java programs easy access to native shared libraries
(DLLs on Windows) without writing anything but Java code. JNA's
design aims to provide native access in a natural way with a
minimum of effort. No boilerplate or generated code is required.
While some attention is paid to performance, correctness and ease
of use take priority.


%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}


%description    javadoc
This package contains the javadocs for %{name}.


%package        contrib
Summary:        Contrib for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-examples


%description    contrib
This package contains the contributed examples for %{name}.


%prep
%setup -q -n %{name}-%{version}
sed -e 's|@JNIPATH@|%{_libdir}/%{name}|' %{PATCH1} | patch -p1
%patch2 -p1 -b .tests-headless
%patch3 -p1 -b .javadoc
# temporary hach for patch3 on epel5
chmod -Rf a+rX,u+w,g-w,o-w .
%patch4 -p0 -b .gcj-javadoc
%patch5 -p1 -b .junit
cp %{SOURCE1} ./

# UnloadTest fail during build since we modify class loading
rm test/com/sun/jna/JNAUnloadTest.java
# current bug: https://jna.dev.java.net/issues/show_bug.cgi?id=155
rm test/com/sun/jna/DirectTest.java

# all java binaries must be removed from the sources
#find . -name '*.jar' -delete
rm lib/junit.jar
find . -name '*.class' -delete

# remove internal copy of libffi
rm -rf native/libffi

# clean LICENSE.txt
sed -i 's/\r//' LICENSE.txt
chmod 0644 LICENSE.txt


%build
# We pass -Ddynlink.native which comes from our patch because
# upstream doesn't want to default to dynamic linking.
ant -Dcflags_extra.native="%{optflags}" -Ddynlink.native=true -Dnomixedjar.native=true jar contrib-jars javadoc
# remove compiled contribs
find contrib -name build -exec rm -rf {} \; || :
sed -i "s/VERSION/%{version}/" %{name}-pom.xml

%install
rm -rf %{buildroot}

# jars
install -D -m 644 build*/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir}/; for jar in `ls *-%{version}.jar`; do ln -s $jar `echo $jar | sed -e 's/-%{version}//'`; done)
install -d -m 755 %{buildroot}%{_javadir}/%{name}
find contrib -name '*.jar' -exec cp {} %{buildroot}%{_javadir}/%{name}/ \;
# NOTE: JNA has highly custom code to look for native jars in this
# directory.  Since this roughly matches the jpackage guidelines,
# we'll leave it unchanged.
install -d -m 755 %{buildroot}%{_libdir}/%{name}
install -m 755 build*/native/libjnidispatch*.so %{buildroot}%{_libdir}/%{name}/

%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
# install maven pom file
install -Dm 644 %{name}-pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# ... and maven depmap
%add_to_maven_depmap net.java.dev.jna %{name} %{version} JPP %{name}
%endif

# javadocs
install -p -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}


#if 0%{?rhel} >= 6 || 0%{?fedora} >= 9
%if 0%{?fedora} >= 9
%ifnarch ppc s390 s390x
%check
ant -Dcflags_extra.native="%{optflags}" -Ddynlink.native=true -Dnomixedjar.native=true test
%endif
%endif


%clean
rm -rf %{buildroot}


%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
%post
%update_maven_depmap


%postun
%update_maven_depmap
%endif


%files
%defattr(-,root,root,-)
%doc LICENSE.txt release-notes.html 
%{_libdir}/%{name}
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
%{_mavenpomdir}/*.pom
%{_mavendepmapfragdir}/%{name}
%endif


%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}


%files contrib
%defattr(-,root,root,-)
%{_javadir}/%{name}


%changelog
* Fri Dec  3 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-10
- fix pom file name #655810

* Fri Nov  5 2010 Dan Horák <dan[at]danny.cz> - 3.2.7-9
- exclude checks on s390(x)

* Tue Oct 12 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-8
- exclude check on ppc

* Fri Oct  8 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-7
- fix excludearch condition

* Wed Oct  6 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-6
- readd excludearch for old release fix #548099

* Fri Oct 01 2010 Dennis Gilmore <dennis@ausil.us> - 3.2.7-5.1
- remove the ExcludeArch it makes no sense

* Sun Aug  1 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-5
- reenable test and clean up contrib files

* Tue Jul 27 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-4
- add Obsoletes for jna-examples

* Sat Jul 24 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-3
- upstream 64bit fixes

* Thu Jul 23 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-2
- Temporary hack for 64bit build

* Thu Jul 22 2010 Levente Farkas <lfarkas@lfarkas.org> - 3.2.7-1
- Rebase on upstream 3.2.7

* Wed Jul 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2.4-6
- Add maven depmap

* Thu Apr 22 2010 Colin Walters <walters@verbum.org> - 3.2.4-5
- Add patches to make the build happen with gcj

* Wed Apr 21 2010 Colin Walters <walters@verbum.org> - 3.2.4-4
- Fix the build by removing upstream's hardcoded md5

* Thu Dec 17 2009 Levente Farkas <lfarkas@lfarkas.org> - 3.2.4-3
- add proper ExclusiveArch

* Thu Dec 17 2009 Alexander Kurtakov <akurtako@redhat.com> 3.2.4-2
- Comment rhel ExclusiveArchs - not correct applies on Fedora.

* Sat Nov 14 2009 Levente Farkas <lfarkas@lfarkas.org> - 3.2.4-1
- Rebase on upstream 3.2.4

* Thu Oct 29 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.9-6
- Add examples subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Colin Walters <walters@redhat.com> - 3.0.9-3
- Add patch to allow opening current process

* Sun Nov 30 2008 Colin Walters <walters@redhat.com> - 3.0.9-2
- Fix library mapping, remove upstreamed patches

* Fri Oct 31 2008 Colin Walters <walters@redhat.com> - 3.0.9-1
- Rebase on upstream 3.0.9

* Tue Oct 14 2008 Colin Walters <walters@redhat.com> - 3.0.4-10.svn729
- Add patch to support String[] returns

* Wed Oct 01 2008 Colin Walters <walters@redhat.com> - 3.0.4-9.svn729
- Add new patch to support NativeMapped[] which I want

* Wed Oct 01 2008 Colin Walters <walters@redhat.com> - 3.0.4-8.svn729
- Update to svn r729
- drop upstreamed typemapper patch

* Tue Sep 18 2008 Colin Walters <walters@redhat.com> - 3.0.4-7.svn700
- Add patch to make typemapper always accessible
- Add patch to skip cracktastic X11 test bits which currently fail

* Tue Sep 09 2008 Colin Walters <walters@redhat.com> - 3.0.4-5.svn700
- Update to upstream SVN r700; drop all now upstreamed patches

* Sat Sep 06 2008 Colin Walters <walters@redhat.com> - 3.0.4-3.svn630
- A few more patches for JGIR

* Thu Sep 04 2008 Colin Walters <walters@redhat.com> - 3.0.4-2.svn630
- Add two (sent upstream) patches that I need for JGIR

* Thu Jul 31 2008 Colin Walters <walters@redhat.com> - 3.0.4-1.svn630
- New upstream version, drop upstreamed patch parts
- New patch jna-3.0.4-nomixedjar.patch which ensures that we don't
  include the .so in the .jar

* Fri Apr 04 2008 Colin Walters <walters@redhat.com> - 3.0.2-7
- Add patch to use JPackage-compatible JNI library path
- Do build debuginfo package
- Refactor build patch greatly so it's hopefully upstreamable
- Install .so directly to JNI directory, rather than inside jar
- Clean up Requires/BuildRequires (thanks Mamoru Tasaka)

* Sun Mar 30 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-6
- -javadocs should be -javadoc.
- %%files section cleaned a bit.

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-5
- -javadocs package should be in group "Documentation".

* Mon Mar 17 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-4
- License should be LGPLv2+, not GPLv2+.
- Several minor fixes.
- Fix Requires in javadoc package.

* Sun Mar 16 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-3
- Don't use internal libffi.

* Thu Mar 6 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-2
- Don't pull in jars from the web.

* Mon Mar 3 2008 Conrad Meyer <konrad@tylerc.org> - 3.0.2-1
- Initial package.
