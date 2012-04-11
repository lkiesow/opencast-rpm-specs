Name:		tesseract
Version:	3.00
Release:	3%{?dist}
Summary:	Raw OCR Engine 

Group:		Applications/File
License:	ASL 2.0
URL:		http://code.google.com/p/tesseract-ocr/
Source0:	http://tesseract-ocr.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:	http://tesseract-ocr.googlecode.com/files/eng.traineddata.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtiff-devel


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}


%description
A commercial quality OCR engine originally developed at HP between 1985 and
1995. In 1995, this engine was among the top 3 evaluated by UNLV. It was
open-sourced by HP and UNLV in 2005.


%description devel
The %{name}-devel package contains header file for
developing applications that use %{name}.


%prep
%setup -q
gzip -dc %{SOURCE1} > eng.traineddata
chmod a-x ccmain/*.*


%build
sed -i 's#-DTESSDATA_PREFIX=@datadir@/#-DTESSDATA_PREFIX=@datadir@/%{name}/##' ccutil/Makefile.*
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*la
mkdir -p $RPM_BUILD_ROOT%{_datadir}/tesseract
mv $RPM_BUILD_ROOT%{_datadir}/tessdata $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 0644 eng.traineddata $RPM_BUILD_ROOT%{_datadir}/%{name}/tessdata


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/combine_tessdata
%{_bindir}/*training
%{_bindir}/unicharset_extractor
%{_bindir}/wordlist2dawg
%{_datadir}/%{name}
%{_libdir}/lib%{name}*.so.*
%doc AUTHORS ChangeLog COPYING eurotext.tif NEWS phototest.tif README 


%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/lib%{name}*.so
%doc AUTHORS ChangeLog COPYING eurotext.tif NEWS phototest.tif README 

%changelog
* Sat Mar  3 2012 Lars Kiesow <lkiesow@uos.de> - 3.00-3
- Ported to CentOS 6.2.
- Fixed some packaging issues.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 16 2010 Karol Trzcionka <karlikt at gmail.com> - 3.00-1
- Update to v3.00
- Remove static libs and add dynamic

* Wed Oct 21 2009 Karol Trzcionka <karlikt at gmail.com> - 2.04-1
- Update to v2.04
- Add static libraries to -devel subpackage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 04 2009 Caolán McNamara <caolanm@redhat.com> - 2.03-3
- include stdio.h for snprintf

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun May 04 2008 Karol Trzcionka <karlikt at gmail.com> - 2.03-1
- Update to v2.03
* Sat Feb 09 2008 Karol Trzcionka <karlikt at gmail.com> - 2.01-2
- Rebuild for gcc43
* Fri Sep 07 2007 Karol Trzcionka <karlikt at gmail.com> - 2.01-1
- Upgrade to v2.01
* Tue Aug 21 2007 Karol Trzcionka <karlikt at gmail.com> - 2.00-1
- Upgrade to v2.00
* Thu Mar 22 2007 Karol Trzcionka <karlikt at gmail.com> - 1.04-1
- Change url and source
- Update to v1.04
- Make patch bases on upstream's v1.04b
- Change compilefix patch
- Adding -devel subpackage
* Thu Mar 22 2007 Karol Trzcionka <karlikt at gmail.com> - 1.03-2
- Including patch bases on cvs
* Tue Feb 13 2007 Karol Trzcionka <karlikt at gmail.com> - 1.03-1
- Update to v1.03
* Sat Jan 26 2007 Karol Trzcionka <karlikt at gmail.com> - 1.02-3
- Update BRs
- Fix x86_64 compile
* Sat Dec 30 2006 Karol Trzcionka <karlikt at gmail.com> - 1.02-2
- Fixed rpmlint warning in SRPM
* Fri Dec 29 2006 Karol Trzcionka <karlikt at gmail.com> - 1.02-1
- Initial Release
