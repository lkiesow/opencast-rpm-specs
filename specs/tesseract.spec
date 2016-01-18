%global fullname tesseract-ocr
%global pre rc1

Name:		tesseract
Version:	3.03
Release:	0.4%{?pre:.%pre}%{?dist}
Summary:	Raw OCR Engine

Group:		Applications/File
License:	ASL 2.0
URL:		http://code.google.com/p/%{fullname}/
# The downloads are now posted on google-drive which has impossible download URLS...
# The url of the drive is
#     https://drive.google.com/folderview?id=0B7l10Bj_LprhQnpSRkpGMGV2eE0
Source0:	%{name}-%{version}%{?pre:-%pre}.tar.gz
Source1:	http://tesseract-ocr.googlecode.com/files/%{fullname}-3.02.eng.tar.gz
Source2:	http://tesseract-ocr.googlecode.com/files/%{fullname}-3.01.osd.tar.gz
BuildRequires:	libtiff-devel
BuildRequires:	leptonica-devel
BuildRequires:	cairo-devel
BuildRequires:	libicu-devel
BuildRequires:	pango-devel
BuildRequires:	automake libtool
Obsoletes:	tesseract < 3.02.02

%package devel
Summary:	Development files for %{fullname}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%package osd
Summary:	Orientation & Script Detection Data for %{fullname}
Group:		Applications/File
Requires:	%{name} = %{version}-%{release}

%description
A commercial quality OCR engine originally developed at HP between 1985 and
1995. In 1995, this engine was among the top 3 evaluated by UNLV. It was
open-sourced by HP and UNLV in 2005.

%description devel
The %{name}-devel package contains header file for
developing applications that use %{name}.

%description osd
Orientation & Script Detection Data for %{fullname}

%prep
%setup -q -n %{name}-%{version} -a1 -a2

%build
sed -i 's#-DTESSDATA_PREFIX=@datadir@/#-DTESSDATA_PREFIX=@datadir@/%{name}/##' ccutil/Makefile.*
autoreconf -ifv
%configure --disable-static
make %{?_smp_mflags}
# Remove compiled files, see https://groups.google.com/forum/#!topic/tesseract-dev/ARKOSV3zpWo
make -C training clean
make %{?_smp_mflags} training

%install
%make_install
%make_install training-install
rm -f %{buildroot}%{_libdir}/*la
mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{_datadir}/tessdata %{buildroot}%{_datadir}/%{name}
install -m 0644 %{fullname}/tessdata/* %{buildroot}%{_datadir}/%{name}/tessdata

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/ambiguous_words
%{_bindir}/classifier_tester
%{_bindir}/combine_tessdata
%{_bindir}/dawg2wordlist
%{_bindir}/set_unicharset_properties
%{_bindir}/shapeclustering
%{_bindir}/*training
%{_bindir}/%{name}
%{_bindir}/text2image
%{_bindir}/unicharset_extractor
%{_bindir}/wordlist2dawg
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/tessdata
%{_datadir}/%{name}/tessdata/configs
%{_datadir}/%{name}/tessdata/tessconfigs
%{_datadir}/%{name}/tessdata/eng.*
%{_datadir}/%{name}/tessdata/pdf.ttf
%{_datadir}/%{name}/tessdata/pdf.ttx
%{_libdir}/lib%{name}*.so.*
%{_mandir}/man1/*
%{_mandir}/man5/*

%doc AUTHORS ChangeLog COPYING eurotext.tif NEWS phototest.tif README 

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc

%files osd
%{_datadir}/%{name}/tessdata/osd.traineddata

%changelog
* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 3.03-0.4.rc1
- rebuild for ICU 54.1

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 3.03-0.3.rc1
- rebuild for ICU 53.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.03-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Sandro Mani <manisandro@gmail.com> - 3.03-0.1.rc1
- Update to v3.03-rc1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.02.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Karol Trzcionka <karlik at fedoraproject.org> - 3.02.02-3
- Fix rhbz#1037350 (-Werror=format-security)
- Add OSD data
- Remove BuildRoot tag

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.02.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr 27 2013 Karol Trzcionka <karlik at fedoraproject.org> - 3.02.02-1
- Update to v3.02.02
- Apply pkgconfig patch rhbz#904806

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 06 2012 Karol Trzcionka <karlik at fedoraproject.org> - 3.01-1
- Update to v3.01
- Add manual pages
- Add BRs leptonica, automake

* Tue Jul 31 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.00-6
- Fix FTBFS with g++ 4.7

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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
* Sat Jan 27 2007 Karol Trzcionka <karlikt at gmail.com> - 1.02-3
- Update BRs
- Fix x86_64 compile
* Sat Dec 30 2006 Karol Trzcionka <karlikt at gmail.com> - 1.02-2
- Fixed rpmlint warning in SRPM
* Fri Dec 29 2006 Karol Trzcionka <karlikt at gmail.com> - 1.02-1
- Initial Release
