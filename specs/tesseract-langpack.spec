%define upstreamname tesseract
Name:		%{upstreamname}-langpack
Version:	3.00
Release:	2
Summary:	Langpacks for tesseract

Group:		Applications/File
License:	ASL 2.0
URL:		http://code.google.com/p/tesseract-ocr/
Source1:	http://tesseract-ocr.googlecode.com/files/bul.traineddata.gz
Source2:	http://tesseract-ocr.googlecode.com/files/cat.traineddata.gz
Source3:	http://tesseract-ocr.googlecode.com/files/ces.traineddata.gz
Source4:	http://tesseract-ocr.googlecode.com/files/chi_sim.traineddata.gz
Source5:	http://tesseract-ocr.googlecode.com/files/chi_tra.traineddata.gz
Source6:	http://tesseract-ocr.googlecode.com/files/dan-frak.traineddata.gz
Source7:	http://tesseract-ocr.googlecode.com/files/dan.traineddata.gz
Source8:	http://tesseract-ocr.googlecode.com/files/deu.traineddata.gz
Source9:	http://tesseract-ocr.googlecode.com/files/deu-frak.traineddata.gz
Source10:	http://tesseract-ocr.googlecode.com/files/ell.traineddata.gz
Source11:	http://tesseract-ocr.googlecode.com/files/fin.traineddata.gz
Source12:	http://tesseract-ocr.googlecode.com/files/fra.traineddata.gz
Source13:	http://tesseract-ocr.googlecode.com/files/hun.traineddata.gz
Source14:	http://tesseract-ocr.googlecode.com/files/ind.traineddata.gz
Source15:	http://tesseract-ocr.googlecode.com/files/ita.traineddata.gz
Source16:	http://tesseract-ocr.googlecode.com/files/jpn.traineddata.gz
Source17:	http://tesseract-ocr.googlecode.com/files/kor.traineddata.gz
Source18:	http://tesseract-ocr.googlecode.com/files/lav.traineddata.gz
Source19:	http://tesseract-ocr.googlecode.com/files/lit.traineddata.gz
Source20:	http://tesseract-ocr.googlecode.com/files/nld.traineddata.gz
Source21:	http://tesseract-ocr.googlecode.com/files/nor.traineddata.gz
Source22:	http://tesseract-ocr.googlecode.com/files/pol.traineddata.gz
Source23:	http://tesseract-ocr.googlecode.com/files/por.traineddata.gz
Source24:	http://tesseract-ocr.googlecode.com/files/ron.traineddata.gz
Source25:	http://tesseract-ocr.googlecode.com/files/rus.traineddata.gz
Source26:	http://tesseract-ocr.googlecode.com/files/slk.traineddata.gz
Source27:	http://tesseract-ocr.googlecode.com/files/slv.traineddata.gz
Source28:	http://tesseract-ocr.googlecode.com/files/spa.traineddata.gz
Source29:	http://tesseract-ocr.googlecode.com/files/srp.traineddata.gz
Source30:	http://tesseract-ocr.googlecode.com/files/swe.traineddata.gz
Source31:	http://tesseract-ocr.googlecode.com/files/swe-frak.traineddata.gz
Source32:	http://tesseract-ocr.googlecode.com/files/tgl.traineddata.gz
Source33:	http://tesseract-ocr.googlecode.com/files/tur.traineddata.gz
Source34:	http://tesseract-ocr.googlecode.com/files/ukr.traineddata.gz
Source35:	http://tesseract-ocr.googlecode.com/files/vie.traineddata.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Group:		Applications/File
Requires:	%{upstreamname} >= 3.00

%package bul
Summary:	Bulgarian language data for Tesseract
%package cat
Summary:	Catalan language data for Tesseract
%package ces
Summary:	Czech language data for Tesseract
%package chi_sim
Summary:	Chinese (Simplified) language data for Tesseract
%package chi_tra
Summary:	Chinese (Traditional) language data for Tesseract
%package dan-frak
Summary:	Danish (Fraktur) language data for Tesseract
%package dan
Summary:	Danish language data for Tesseract
%package deu-frak
Summary:	German (Fraktur) language data for Tesseract
%package deu
Summary:	German language data for Tesseract
Obsoletes: %{name}-de
%package ell
Summary:	Greek language data for Tesseract
%package fin
Summary:	Finnish language data for Tesseract
%package fra
Summary:	French language data for Tesseract
Obsoletes: %{name}-fr
%package hun
Summary:	Hungarian language data for Tesseract
%package ind
Summary:	Indonesian language data for Tesseract
%package ita
Summary:	Italian language data for Tesseract
Obsoletes: %{name}-it
%package jpn
Summary:	Japanese language data for Tesseract
%package kor
Summary:	Korean language data for Tesseract
%package lav
Summary:	Latvian language data for Tesseract
%package lit
Summary:	Lithuanian language data for Tesseract
%package nld
Summary:	Dutch language data for Tesseract
Obsoletes: %{name}-nl
%package nor
Summary:	Norwegian language data for Tesseract
%package pol
Summary:	Polish language data for Tesseract
%package por
Summary:	Portuguese language data for Tesseract
%package ron
Summary:	Romanian language data for Tesseract
%package rus
Summary:	Russian language data for Tesseract
%package slk
Summary:	Slovakian language data for Tesseract
%package slv
Summary:	Slovenian language data for Tesseract
%package spa
Summary:	Spanish language data for Tesseract
Obsoletes: %{name}-es
%package srp
Summary:	Serbian (Latin) language data for Tesseract
%package swe-frak
Summary:	Swedish (Fraktur) language data for Tesseract
%package swe
Summary:	Swedish language data for Tesseract
%package tgl
Summary:	Tagalog language data for Tesseract
%package tur
Summary:	Turkish language data for Tesseract
%package ukr
Summary:	Ukrainian language data for Tesseract
%package vie
Summary:	Vietnamese language data for Tesseract

%description
%description bul
Bulgarian language data for Tesseract 
%description cat
Catalan language data for Tesseract
%description ces
Czech language data for Tesseract
%description chi_sim
Chinese (Simplified) language data for Tesseract
%description chi_tra
Chinese (Traditional) language data for Tesseract
%description dan-frak
Danish (Fraktur) language data for Tesseract
%description dan
Danish language data for Tesseract
%description deu-frak
German (Fraktur) language data for Tesseract
%description deu
German language data for Tesseract
%description ell
Greek language data for Tesseract
%description fin
Finnish language data for Tesseract
%description fra
French language data for Tesseract
%description hun
Hungarian language data for Tesseract
%description ind
Indonesian language data for Tesseract
%description ita
Italian language data for Tesseract
%description jpn
Japanese language data for Tesseract
%description kor
Korean language data for Tesseract
%description lav
Latvian language data for Tesseract
%description lit
Lithuanian language data for Tesseract
%description nld
Dutch language data for Tesseract
%description nor
Norwegian language data for Tesseract
%description pol
Polish language data for Tesseract
%description por
Portuguese language data for Tesseract
%description ron
Romanian language data for Tesseract
%description rus
Russian language data for Tesseract
%description slk
Slovakian language data for Tesseract
%description slv
Slovenian language data for Tesseract
%description spa
Spanish language data for Tesseract
%description srp
Serbian (Latin) language data for Tesseract
%description swe-frak
Swedish (Fraktur) language data for Tesseract
%description swe
Swedish language data for Tesseract
%description tgl
Tagalog language data for Tesseract
%description tur
Turkish language data for Tesseract
%description ukr
Ukrainian language data for Tesseract
%description vie
Vietnamese language data for Tesseract

%prep
%setup -c -T
for i in %sources;\
		do cp -a $i .;\
done;
for i in *;\
		do gzip -d $i;
done;

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{upstreamname}/tessdata/
install -p -m 644 *.traineddata $RPM_BUILD_ROOT%{_datadir}/%{upstreamname}/tessdata/

%clean
rm -rf $RPM_BUILD_ROOT

%files bul
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/bul.traineddata

%files cat
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/cat.traineddata

%files ces
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/ces.traineddata

%files chi_sim
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/chi_sim.traineddata

%files chi_tra
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/chi_tra.traineddata

%files dan-frak
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/dan-frak.traineddata

%files dan
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/dan.traineddata

%files deu-frak
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/deu-frak.traineddata

%files deu
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/deu.traineddata

%files ell
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/ell.traineddata

%files fin
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/fin.traineddata

%files fra
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/fra.traineddata

%files hun
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/hun.traineddata

%files ind
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/ind.traineddata

%files ita
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/ita.traineddata

%files jpn
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/jpn.traineddata

%files kor
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/kor.traineddata

%files lav
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/lav.traineddata

%files lit
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/lit.traineddata

%files nld
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/nld.traineddata

%files nor
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/nor.traineddata

%files pol
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/pol.traineddata

%files por
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/por.traineddata

%files ron
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/ron.traineddata

%files rus
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/rus.traineddata

%files slk
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/slk.traineddata

%files slv
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/slv.traineddata

%files spa
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/spa.traineddata

%files srp
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/srp.traineddata

%files swe-frak
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/swe-frak.traineddata

%files swe
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/swe.traineddata

%files tgl
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/tgl.traineddata

%files tur
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/tur.traineddata

%files ukr
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/ukr.traineddata

%files vie
%defattr(-,root,root,-)
%{_datadir}/%{upstreamname}/tessdata/vie.traineddata

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 01 2010 Karol Trzcionka <karlikt at gmail.com> - 3.00-1
- Update to v3.00+
- Naming based on upstream

* Thu Dec 10 2009 Karol Trzcionka <karlikt at gmail.com> - 2.00-6
- Delete %%{?dist} macro

* Thu Dec 10 2009 Karol Trzcionka <karlikt at gmail.com> - 2.00-5
- Fix typo

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 24 2007 Karol Trzcionka <karlikt at gmail.com> - 2.00-2
- Fixed executable file in nl
* Tue Aug 21 2007 Karol Trzcionka <karlikt at gmail.com> - 2.00-1
- Initial Release
