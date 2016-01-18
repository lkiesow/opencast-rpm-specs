%define upstreamname tesseract-ocr
%define sname tesseract
Name:		tesseract-langpack
Version:	3.02
Release:	8%{?dist}
Summary:	Langpacks for tesseract

Group:		Applications/File
License:	ASL 2.0
URL:		http://code.google.com/p/%{upstreamname}/
Source0:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.afr.tar.gz
# ara archive has params for eng, fra, hin, ita, rus, spa
# not included in result package
Source1:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ara.tar.gz
Source2:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.aze.tar.gz
Source3:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.bel.tar.gz
Source4:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ben.tar.gz
Source5:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.bul.tar.gz
Source6:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.cat.tar.gz
Source7:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ces.tar.gz
Source8:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.chi_sim.tar.gz
Source9:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.chi_tra.tar.gz
Source10:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.chr.tar.gz
Source11:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.dan.tar.gz
Source12:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.deu.tar.gz
Source13:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ell.tar.gz
Source14:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.enm.tar.gz
Source15:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.epo_alt.tar.gz
Source16:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.epo.tar.gz
Source17:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.equ.tar.gz
Source18:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.est.tar.gz
Source19:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.eus.tar.gz
Source20:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.fin.tar.gz
Source21:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.fra.tar.gz
Source22:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.frk.tar.gz
Source23:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.frm.tar.gz
Source24:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.glg.tar.gz
Source25:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.grc.tar.gz
Source26:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.heb.tar.gz
Source27:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.hin.tar.gz
Source28:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.hrv.tar.gz
Source29:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.hun.tar.gz
Source30:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ind.tar.gz
Source31:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.isl.tar.gz
# ita_old is included in ita archive
#Source32:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ita_old.tar.gz
Source33:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ita.tar.gz
Source34:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.jpn.tar.gz
Source35:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.kan.tar.gz
Source36:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.kor.tar.gz
Source37:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.lav.tar.gz
Source38:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.lit.tar.gz
Source39:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.mal.tar.gz
Source40:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.mkd.tar.gz
Source41:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.mlt.tar.gz
Source42:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.msa.tar.gz
Source43:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.nld.tar.gz
Source44:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.nor.tar.gz
Source45:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.pol.tar.gz
Source46:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.por.tar.gz
Source47:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ron.tar.gz
Source48:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.rus.tar.gz
Source49:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.slk.tar.gz
Source50:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.slv.tar.gz
# spa_old is included in spa archive
#Source51:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.spa_old.tar.gz
Source52:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.spa.tar.gz
Source53:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.sqi.tar.gz
Source54:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.srp.tar.gz
Source55:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.swa.tar.gz
Source56:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.swe.tar.gz
Source57:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.tam.tar.gz
Source58:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.tel.tar.gz
Source59:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.tgl.tar.gz
Source60:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.tha.tar.gz
Source61:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.tur.tar.gz
Source62:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.ukr.tar.gz
Source63:	http://tesseract-ocr.googlecode.com/files/%{upstreamname}-%{version}.vie.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Group:		Applications/File

%package afr
Summary:	Afrikaans language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-af = %{version}-%{release}

%package ara
Summary:	Arabic language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ar = %{version}-%{release}

%package aze
Summary:	Azerbaijani language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-az = %{version}-%{release}

%package bel
Summary:	Belarusian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-be = %{version}-%{release}

%package ben
Summary:	Bengali language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-bn = %{version}-%{release}

%package bul
Summary:	Bulgarian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-bg = %{version}-%{release}

%package cat
Summary:	Catalan language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ca = %{version}-%{release}

%package ces
Summary:	Czech language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-cs = %{version}-%{release}

%package chi_sim
Summary:	Chinese (Simplified) language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-zh_CN = %{version}-%{release}

%package chi_tra
Summary:	Chinese (Traditional) language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-zh_TW = %{version}-%{release}

%package chr
Summary:	Cherokee language data for Tesseract
Requires:	%{sname} >= %{version}

%package dan
Summary:	Danish language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-da = %{version}-%{release}
Provides:	%{name}-dan-frak = %{version}-%{release}
Obsoletes:	%{name}-dan-frak < 3.02-5

%package deu
Summary:	German language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-de = %{version}-%{release}
Provides:	%{name}-deu-frak = %{version}-%{release}
Obsoletes:	%{name}-deu-frak < 3.02-5

%package ell
Summary:	Greek language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-el = %{version}-%{release}

%package enm
Summary:	Middle English (1100-1500) language data for Tesseract
Requires:	%{sname} >= %{version}

%package epo
Summary:	Esperanto language data for Tesseract
Requires:	%{sname} >= %{version}

%package epo_alt
Summary:	Esperanto alternative language data for Tesseract
Requires:	%{sname} >= %{version}

%package equ
Summary:	Math / equation detection module for Tesseract
Requires:	%{sname} >= %{version}

%package est
Summary:	Estonian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-et = %{version}-%{release}

%package eus
Summary:	Basque language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-eu = %{version}-%{release}

%package fin
Summary:	Finnish language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-fi = %{version}-%{release}

%package fra
Summary:	French language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-fr = %{version}-%{release}

%package frk
Summary:	Frankish language data for Tesseract
Requires:	%{sname} >= %{version}

%package frm
Summary:	Middle French (ca. 1400-1600) language data for Tesseract
Requires:	%{sname} >= %{version}

%package glg
Summary:	Galician language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-gl = %{version}-%{release}

%package grc
Summary:	Ancient Greek Language data for Tesseract
Requires:	%{sname} >= %{version}

%package heb
Summary:	Hebrew language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-he = %{version}-%{release}

%package hin
Summary:	Hindi language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-hi = %{version}-%{release}

%package hrv
Summary:	Croatian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-hr = %{version}-%{release}

%package hun
Summary:	Hungarian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-hu = %{version}-%{release}

%package ind
Summary:	Indonesian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-id = %{version}-%{release}

%package isl
Summary:	Icelandic language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-is = %{version}-%{release}

%package ita
Summary:	Italian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-it = %{version}-%{release}

%package ita_old
Summary:	Italian (Old) language data for Tesseract
Requires:	%{sname} >= %{version}

%package jpn
Summary:	Japanese language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ja = %{version}-%{release}

%package kan
Summary:	Kannada language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-kn = %{version}-%{release}

%package kor
Summary:	Korean language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ko = %{version}-%{release}

%package lav
Summary:	Latvian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-lv = %{version}-%{release}

%package lit
Summary:	Lithuanian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-lt = %{version}-%{release}

%package mal
Summary:	Malayalam language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ml = %{version}-%{release}

%package mkd
Summary:	Macedonian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-mk = %{version}-%{release}

%package mlt
Summary:	Maltese language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-mt = %{version}-%{release}

%package msa
Summary:	Malay language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ms = %{version}-%{release}

%package nld
Summary:	Dutch language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-nl = %{version}-%{release}

%package nor
Summary:	Norwegian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-no = %{version}-%{release}

%package pol
Summary:	Polish language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-pl = %{version}-%{release}

%package por
Summary:	Portuguese language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-pt = %{version}-%{release}

%package ron
Summary:	Romanian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ro = %{version}-%{release}

%package rus
Summary:	Russian Language Data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ru = %{version}-%{release}

%package slk
Summary:	Slovakian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-sk = %{version}-%{release}

%package slv
Summary:	Slovenian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-sl = %{version}-%{release}

%package spa
Summary:	Spanish language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-es = %{version}-%{release}

%package spa_old
Summary:	Spanish (Old) language data for Tesseract
Requires:	%{sname} >= %{version}

%package sqi
Summary:	Albanian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-sq = %{version}-%{release}

%package srp
Summary:	Serbian (Latin) language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-sr = %{version}-%{release}

%package swa
Summary:	Swahili language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-sw = %{version}-%{release}

%package swe
Summary:	Swedish language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-sv = %{version}-%{release}
Obsoletes:	%{name}-swe-frak < 3.02-5

%package tam
Summary:	Tamil language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-ta = %{version}-%{release}

%package tel
Summary:	Telugu language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-te = %{version}-%{release}

%package tgl
Summary:	Tagalog language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-tl = %{version}-%{release}

%package tha
Summary:	Thai language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-th = %{version}-%{release}

%package tur
Summary:	Turkish language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-tr = %{version}-%{release}

%package ukr
Summary:	Ukrainian language data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-uk = %{version}-%{release}

%package vie
Summary:	Vietnamese Language Data for Tesseract
Requires:	%{sname} >= %{version}
Provides:	%{name}-vi = %{version}-%{release}

%description
%description afr
Afrikaans language data for Tesseract
%description ara
Arabic language data for Tesseract
%description aze
Azerbaijani language data for Tesseract
%description bel
Belarusian language data for Tesseract
%description ben
Bengali language data for Tesseract
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
%description chr
Cherokee language data for Tesseract
%description dan
Danish language data for Tesseract
%description deu
German language data for Tesseract
%description ell
Greek language data for Tesseract
%description enm
Middle English (1100-1500) language data for Tesseract
%description epo
Esperanto language data for Tesseract
%description epo_alt
Esperanto alternative language data for Tesseract
%description equ
Math / equation detection module for Tesseract
%description est
Estonian language data for Tesseract
%description eus
Basque language data for Tesseract
%description fin
Finnish language data for Tesseract
%description fra
French language data for Tesseract
%description frk
Frankish language data for Tesseract
%description frm
Middle French (ca. 1400-1600) language data for Tesseract
%description glg
Galician language data for Tesseract
%description grc
Ancient Greek Language data for Tesseract
%description heb
Hebrew language data for Tesseract
%description hin
Hindi language data for Tesseract
%description hrv
Croatian language data for Tesseract
%description hun
Hungarian language data for Tesseract
%description ind
Indonesian language data for Tesseract
%description isl
Icelandic language data for Tesseract
%description ita
Italian language data for Tesseract
%description ita_old
Italian (Old) language data for Tesseract
%description jpn
Japanese language data for Tesseract
%description kan
Kannada language data for Tesseract
%description kor
Korean language data for Tesseract
%description lav
Latvian language data for Tesseract
%description lit
Lithuanian language data for Tesseract
%description mal
Malayalam language data for Tesseract
%description mkd
Macedonian language data for Tesseract
%description mlt
Maltese language data for Tesseract
%description msa
Malay language data for Tesseract
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
Russian Language Data for Tesseract
%description slk
Slovakian language data for Tesseract
%description slv
Slovenian language data for Tesseract
%description spa
Spanish language data for Tesseract
%description spa_old
Spanish (Old) language data for Tesseract
%description sqi
Albanian language data for Tesseract
%description srp
Serbian (Latin) language data for Tesseract
%description swa
Swahili language data for Tesseract
%description swe
Swedish language data for Tesseract
%description tam
Tamil language data for Tesseract
%description tel
Telugu language data for Tesseract
%description tgl
Tagalog language data for Tesseract
%description tha
Thai language data for Tesseract
%description tur
Turkish language data for Tesseract
%description ukr
Ukrainian language data for Tesseract
%description vie
Vietnamese Language Data for Tesseract

%prep
%setup -c -T
for i in %sources;\
		do cp -a $i .;\
done;
for i in *;\
		do tar xvf $i;
done;
rm -rf %{upstreamname}/tessdata/eng.cube.params

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{sname}/tessdata/
install -p -m 644 %{upstreamname}/tessdata/* $RPM_BUILD_ROOT%{_datadir}/%{sname}/tessdata/

%clean
rm -rf $RPM_BUILD_ROOT

%files afr
%{_datadir}/%{sname}/tessdata/afr.traineddata

%files ara
%{_datadir}/%{sname}/tessdata/ara.*

%files aze
%{_datadir}/%{sname}/tessdata/aze.traineddata

%files bel
%{_datadir}/%{sname}/tessdata/bel.traineddata

%files ben
%{_datadir}/%{sname}/tessdata/ben.traineddata

%files bul
%{_datadir}/%{sname}/tessdata/bul.traineddata

%files cat
%{_datadir}/%{sname}/tessdata/cat.traineddata

%files ces
%{_datadir}/%{sname}/tessdata/ces.traineddata

%files chi_sim
%{_datadir}/%{sname}/tessdata/chi_sim.traineddata

%files chi_tra
%{_datadir}/%{sname}/tessdata/chi_tra.traineddata

%files chr
%{_datadir}/%{sname}/tessdata/chr.traineddata

%files dan
%{_datadir}/%{sname}/tessdata/dan.traineddata
%{_datadir}/%{sname}/tessdata/dan-frak.traineddata

%files deu
%{_datadir}/%{sname}/tessdata/deu.traineddata
%{_datadir}/%{sname}/tessdata/deu-frak.traineddata

%files ell
%{_datadir}/%{sname}/tessdata/ell.traineddata

%files enm
%{_datadir}/%{sname}/tessdata/enm.traineddata

%files epo_alt
%{_datadir}/%{sname}/tessdata/epo_alt.traineddata

%files epo
%{_datadir}/%{sname}/tessdata/epo.traineddata

%files equ
%{_datadir}/%{sname}/tessdata/equ.traineddata

%files est
%{_datadir}/%{sname}/tessdata/est.traineddata

%files eus
%{_datadir}/%{sname}/tessdata/eus.traineddata

%files fin
%{_datadir}/%{sname}/tessdata/fin.traineddata

%files fra
%{_datadir}/%{sname}/tessdata/fra.*

%files frk
%{_datadir}/%{sname}/tessdata/frk.traineddata

%files frm
%{_datadir}/%{sname}/tessdata/frm.traineddata

%files glg
%{_datadir}/%{sname}/tessdata/glg.traineddata

%files grc
%{_datadir}/%{sname}/tessdata/grc.traineddata

%files heb
%{_datadir}/%{sname}/tessdata/heb.traineddata

%files hin
%{_datadir}/%{sname}/tessdata/hin.*

%files hrv
%{_datadir}/%{sname}/tessdata/hrv.traineddata

%files hun
%{_datadir}/%{sname}/tessdata/hun.traineddata

%files ind
%{_datadir}/%{sname}/tessdata/ind.traineddata

%files isl
%{_datadir}/%{sname}/tessdata/isl.traineddata

%files ita_old
%{_datadir}/%{sname}/tessdata/ita_old.traineddata

%files ita
%{_datadir}/%{sname}/tessdata/ita.*

%files jpn
%{_datadir}/%{sname}/tessdata/jpn.traineddata

%files kan
%{_datadir}/%{sname}/tessdata/kan.traineddata

%files kor
%{_datadir}/%{sname}/tessdata/kor.traineddata

%files lav
%{_datadir}/%{sname}/tessdata/lav.traineddata

%files lit
%{_datadir}/%{sname}/tessdata/lit.traineddata

%files mal
%{_datadir}/%{sname}/tessdata/mal.traineddata

%files mkd
%{_datadir}/%{sname}/tessdata/mkd.traineddata

%files mlt
%{_datadir}/%{sname}/tessdata/mlt.traineddata

%files msa
%{_datadir}/%{sname}/tessdata/msa.traineddata

%files nld
%{_datadir}/%{sname}/tessdata/nld.traineddata

%files nor
%{_datadir}/%{sname}/tessdata/nor.traineddata

%files pol
%{_datadir}/%{sname}/tessdata/pol.traineddata

%files por
%{_datadir}/%{sname}/tessdata/por.traineddata

%files ron
%{_datadir}/%{sname}/tessdata/ron.traineddata

%files rus
%{_datadir}/%{sname}/tessdata/rus.*

%files slk
%{_datadir}/%{sname}/tessdata/slk.traineddata
%{_datadir}/%{sname}/tessdata/slk-frak.traineddata

%files slv
%{_datadir}/%{sname}/tessdata/slv.traineddata

%files spa_old
%{_datadir}/%{sname}/tessdata/spa_old.traineddata

%files spa
%{_datadir}/%{sname}/tessdata/spa.*

%files sqi
%{_datadir}/%{sname}/tessdata/sqi.traineddata

%files srp
%{_datadir}/%{sname}/tessdata/srp.traineddata

%files swa
%{_datadir}/%{sname}/tessdata/swa.traineddata

%files swe
%{_datadir}/%{sname}/tessdata/swe.traineddata

%files tam
%{_datadir}/%{sname}/tessdata/tam.traineddata

%files tel
%{_datadir}/%{sname}/tessdata/tel.traineddata

%files tgl
%{_datadir}/%{sname}/tessdata/tgl.traineddata

%files tha
%{_datadir}/%{sname}/tessdata/tha.traineddata

%files tur
%{_datadir}/%{sname}/tessdata/tur.traineddata

%files ukr
%{_datadir}/%{sname}/tessdata/ukr.traineddata

%files vie
%{_datadir}/%{sname}/tessdata/vie.traineddata

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.02-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Karol Trzcionka <karlik at fedoraproject.org> - 3.02-6
- Fix typo in -jpn subpackage

* Fri Jun 28 2013 Karol Trzcionka <karlik at fedoraproject.org> - 3.02-5
- Obsolete old langpacks (bz#978706)

* Fri Jun 28 2013 Karol Trzcionka <karlik at fedoraproject.org> - 3.02-4
- Add support for 2-letter iso-codes for langpacks (thanks to Parag Nemade)

* Thu May 09 2013 Karol Trzcionka <karlik at fedoraproject.org> - 3.02-3
- Fix dependencies

* Sun Apr 28 2013 Karol Trzcionka <karlik at fedoraproject.org> - 3.02-2
- Fix path
- Add disttag

* Sat Apr 27 2013 Karol Trzcionka <karlik at fedoraproject.org> - 3.02-1
- Update to v3.02

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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
