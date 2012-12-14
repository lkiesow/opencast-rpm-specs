Summary: A library of handy utility functions
Name: glib2
Version: 2.32.4
Release: 2%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://www.gtk.org
#VCS: git:git://git.gnome.org/glib
Source: http://download.gnome.org/sources/glib/2.32/glib-%{version}.tar.xz

Patch0: 0001-CVE-2012-3524-Hardening-for-being-run-in-a-setuid-en.patch

BuildRequires: pkgconfig
BuildRequires: gamin-devel
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: libselinux-devel
# for sys/inotify.h
BuildRequires: glibc-devel
BuildRequires: zlib-devel
# for sys/sdt.h
BuildRequires: systemtap-sdt-devel
# Bootstrap build requirements
BuildRequires: automake autoconf libtool
BuildRequires: gtk-doc
BuildRequires: python-devel
BuildRequires: libffi-devel
BuildRequires: elfutils-libelf-devel

# required for GIO content-type support
Requires: shared-mime-info

%description
GLib is the low-level core library that forms the basis for projects
such as GTK+ and GNOME. It provides data structure handling for C,
portability wrappers, and interfaces for such runtime functionality
as an event loop, threads, dynamic loading, and an object system.


%package devel
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for the GLib library.


# anaconda needs static libs, see RH bug #193143
%package static
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The glib2-static package includes static libraries of the GLib library.


%prep
%setup -q -n glib-%{version}
%patch0 -p1

%build
# Support builds of both git snapshots and tarballs packed with autogoo
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
           --enable-systemtap \
           --enable-static
)

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gio/modules/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_datadir}/glib-2.0/gdb/*.{pyc,pyo}
rm -f $RPM_BUILD_ROOT%{_libdir}/gdbus-codegen/*.{pyc,pyo}

mv  $RPM_BUILD_ROOT%{_bindir}/gio-querymodules $RPM_BUILD_ROOT%{_bindir}/gio-querymodules-%{__isa_bits}

touch $RPM_BUILD_ROOT%{_libdir}/gio/modules/giomodule.cache

%find_lang glib20


%post
/sbin/ldconfig
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules


%postun
/sbin/ldconfig
[ ! -x %{_bindir}/gio-querymodules-%{__isa_bits} ] || \
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules


%files -f glib20.lang
%doc AUTHORS COPYING NEWS README
%{_libdir}/libglib-2.0.so.*
%{_libdir}/libgthread-2.0.so.*
%{_libdir}/libgmodule-2.0.so.*
%{_libdir}/libgobject-2.0.so.*
%{_libdir}/libgio-2.0.so.*
%{_datadir}/bash-completion/completions/gdbus
%{_datadir}/bash-completion/completions/gsettings
%dir %{_datadir}/glib-2.0
%dir %{_datadir}/glib-2.0/schemas
%dir %{_libdir}/gio
%dir %{_libdir}/gio/modules
%ghost %{_libdir}/gio/modules/giomodule.cache
%{_libdir}/gio/modules/libgiofam.so
%{_bindir}/gio-querymodules*
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gdbus
%doc %{_mandir}/man1/gio-querymodules.1.gz
%doc %{_mandir}/man1/glib-compile-schemas.1.gz
%doc %{_mandir}/man1/gsettings.1.gz
%doc %{_mandir}/man1/gdbus.1.gz

%files devel
%{_libdir}/lib*.so
%{_libdir}/glib-2.0
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_datadir}/glib-2.0/gdb
%{_datadir}/glib-2.0/gettext
%{_datadir}/glib-2.0/schemas/gschema.dtd
%{_datadir}/bash-completion/completions/gresource
# %{_datadir}/glib-2.0/gdb/*.pyo
# %{_datadir}/glib-2.0/gdb/*.pyc
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gobject-query
%{_bindir}/gtester
%{_bindir}/gdbus-codegen
%{_bindir}/glib-compile-resources
%{_bindir}/gresource
%{_libdir}/gdbus-2.0/codegen
%attr (0755, root, root) %{_bindir}/gtester-report
%doc %{_datadir}/gtk-doc/html/*
%doc %{_mandir}/man1/glib-genmarshal.1.gz
%doc %{_mandir}/man1/glib-gettextize.1.gz
%doc %{_mandir}/man1/glib-mkenums.1.gz
%doc %{_mandir}/man1/gobject-query.1.gz
%doc %{_mandir}/man1/gtester-report.1.gz
%doc %{_mandir}/man1/gtester.1.gz
%doc %{_mandir}/man1/gdbus-codegen.1.gz
%doc %{_mandir}/man1/glib-compile-resources.1.gz
%doc %{_mandir}/man1/gresource.1.gz
%{_datadir}/gdb/auto-load%{_libdir}/libglib-2.0.so.*-gdb.py*
%{_datadir}/gdb/auto-load%{_libdir}/libgobject-2.0.so.*-gdb.py*
%{_datadir}/systemtap/tapset/*.stp

%files static
%{_libdir}/lib*.a

%changelog
* Thu Sep 13 2012 Colin Walters <walters@verbum.org> - 2.32.4-2
- CVE-2012-3524
- Resolves: #857226

* Sat Jul 14 2012 Matthias Clasen <mclasen@redhat.com> 2.32.4-1
- Update to 2.32.4

* Thu May 17 2012 Kalev Lember <kalevlember@gmail.com> 2.32.3-1
- Update to 2.32.3

* Fri Apr 13 2012 Matthias Clasen <mclasen@redhat.com> 2.32.1-1
- Update to 2.32.1

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> 2.32.0-1
- Update to 2.32.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> 2.31.22-1
- Update to 2.31.22

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> 2.31.20-1
- Update to 2.31.20

* Fri Feb 24 2012 Matthias Clasen <mclasen@redhat.com> 2.31.18-1
- Update to 2.31.18

* Tue Feb 21 2012 Richard Hughes <rhughes@redhat.com> 2.31.16-2
- Add BR: elfutils-libelf-devel for the GResource functionality

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> 2.31.16-1
- Update to 2.31.16
- Drop --with-runtime-libdir, since we have /lib -> /usr/lib now

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> 2.31.12-1
- Update to 2.31.12

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> 2.31.10-2
- Fix a header problem that was causing build failures

* Mon Jan 16 2012 Matthias Clasen <mclasen@redhat.com> - 2.31.10-1
- Update to 2.31.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.2-2
- Fix a GDBus regression leading to segfaults

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Fri Oct 21 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.31.0-1
- Update to 2.31.0

* Fri Oct 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Wed Oct 05 2011 Dan Williams <dcbw@redhat.com> - 2.30.0-2
- Fix signal marshalling on 64-bit big-endian platforms (rh #736489)

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.90-1
- Update to 2.29.90

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.18-1
- Update to 2.29.18

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.16-1
- Update to 2.29.16

* Sat Jul 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.14-1
- Update to 2.29.14

* Tue Jul  5 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.10-1
- Update to 2.29.10

* Tue Jun 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.8-1
- Update to 2.29.8

* Thu Jun  9 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.29.6-4
- Own %%ghost /usr/lib*/gio/modules/giomodule.cache.

* Mon Jun  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.6-3
- Fix a deadlock when finalizing e.g. widgets

* Sun Jun  5 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.6-1
- Update to 2.29.6

* Fri May 27 2011 Colin Walters <walters@verbum.org> - 2.29.4-2
- Remove G_BROKEN_FILENAMES; Closes: #708536

* Fri May  6 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.29.4-1
- Update to 2.29.4

* Thu Apr 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.6-2
- Include byte-compiled files, it seems to be required (#670861)

* Thu Apr 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.6-1
- Update to 2.28.6

* Fri Apr  1 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.5-1
- Update to 2.28.5

* Tue Mar 29 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.4-2
- Fix some introspection annotations

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.4-1
- Update to 2.28.4

* Fri Mar 18 2011 Colin Walters <walters@verbum.org> - 2.28.3-2
- Rebuild to hopefully pick up new systemtap mark ABI
  The current version doesn't seem to be triggering the stock
  marks; a local rebuild of the RPM does, so let's do a rebuild
  here.

* Mon Mar 14 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.3-1
- Update to 2.28.3

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Fri Feb 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1
- Drop another space-saving hack from the spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Sat Jan 29 2011 Matthias Clasen <mclasen@redhat.com> - 2.27.93-1
- Update to 2.27.93

* Mon Jan 24 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.27.92-2
- Don't run gio-querymodules* in %%postun if it no longer exists.

* Sat Jan 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92
- Drop update-gio-modules wrapper

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Thu Jan  6 2011 Matthias Clasen <mclasen@redhat.com> - 2.27.90-1
- Update to 2.27.90

* Wed Dec  1 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Wed Sep 29 2010 jkeating - 2.27.0-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Matthias Clasen <mclasen@redhat.com> - 2.27.0-2
- Make /usr/bin/update-gio-modules executable
- Make /etc/bash_completion.d/*.sh not executable

* Mon Sep 20 2010 Matthias Clasen <mclasen@redhat.com> - 2.27.0-1
- Update to 2.27.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.15-1
- Update to 2.25.15

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.14-2
- Fix a PolicyKit problem

* Tue Aug 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.14-1
- Update to 2.25.14

* Mon Aug  9 2010 Colin Walters <walters@verbum.org> - 2.25.13-2
- Add patch from mjw to enable systemtap
  For background, see: https://bugzilla.gnome.org/show_bug.cgi?id=606044

* Fri Aug  6 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.13-1
- Update to 2.25.13

* Mon Aug  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.12-1
- Update to 2.25.12

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.11-1
- Update to 2.25.11

* Tue Jun 29 2010 Colin Walters <walters@verbum.org> - 2.25.10-4
- Include gsettings bash completion

* Mon Jun 28 2010 Colin Walters <walters@verbum.org> - 2.25.10-3
- Revert rpath change; Fedora's libtool is supposed to not generate
  them for system paths.
- Add changes to spec file to support being built from snapshot as
  well as "make dist"-ball.  This includes BuildRequires and autogen.sh
  handling, and gtk-doc enabling if we're bootstrapping.

* Sun Jun 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.10-2
- Fix an evince crash

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.10-1
- Update to 2.25.10

* Wed Jun 23 2010 Colin Walters <walters@verbum.org> - 2.25.9-3
- Only strip rpath at install time, not before build.  Neutering
  libtool sabotages gtk-doc, since it needs those rpaths to run
  an in-tree binary.

* Tue Jun 22 2010 Richard Hughes <rhughes@redhat.com> - 2.25.9-2
- Backport a patch from git master to avoid a segfault when doing the
  schema file check for several GNOME projects.

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.9-1
- Update to 2.25.9

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.8-1
- Update to 2.25.8

* Tue May 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.7-2 
- Require shared-mime-info

* Mon May 24 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.7-1
- Update to 2.25.7

* Wed May 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.6-1
- Update to 2.25.6
- Simplify gio-querymodules handling

* Mon May 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.5-2
- Remove an erroneous removal

* Fri May 14 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.5-1
- Update to 2.25.5

* Fri Apr 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.3-1
- Update to 2.25.3
- Move schema compiler to the main package, since it is
  needed by other rpm's %%post at runtime
- Split up man pages to go along with their binaries

* Mon Apr 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.1-2
- Add a multilib wrapper for gio-querymodules

* Mon Apr 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Sun Mar 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Mar 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Wed Mar 10 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.5-2
- Fix some rpmlint complaints

* Tue Mar  9 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Sun Feb 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Thu Feb 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Mon Jan 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.2-3
- Actually apply the patch, too

* Mon Jan 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.2-2
- Drop the dependency on a GLIBC_PRIVATE symbol

* Mon Jan 25 2010 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Mon Dec 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Mon Nov 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.23.0-1
- Update to 2.23.0

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.22.0-4
- Avoid multilib conflicts even harder

* Thu Sep 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.22.0-3
- Avoid multilib conflicts (#525213)

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.22.0-2
- Fix location of gdb macros

* Tue Sep 22 2009 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Fri Sep  4 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.6-1
- Update to 2.21.6

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Sun Aug  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.4-3
- Save some space

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Mon Jul  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.3-2
- Use --with-runtime-libdir

* Mon Jul  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Mon Jun 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Fri May 29 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Fri May 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.21.0-1
- Update to 2.21.0

* Thu Apr  9 2009 Matthias Clasen <mclasen@redhat.com> - 2.20.1-1
- Update to 2.20.1
- See http://download.gnome.org/sources/glib/2.20/glib-2.20.1.news

* Fri Mar 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Thu Mar 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.10-2
- Fix integer overflows in the base64 handling functions. CVE-2008-4316

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.10-1
- Update to 2.19.10

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.8-1
- Update to 2.19.8
- Drop atomic patch, since we are building for i586 now

* Mon Feb 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.7-1
- Update to 2.19.7

* Mon Feb  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Mon Jan  5 2009 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Mon Dec 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Tue Dec  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.19.2-2
- Rebuild

* Mon Dec  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Mon Dec  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.19.1-2
- Update to 2.19.1

* Mon Oct 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.18.2-3
- Use asm implementation for atomic ops on x86

* Fri Oct 24 2008 Alexander Larsson <alexl@redhat.com> - 2.18.2-2
- Don't return generic fallback icons for files,
  as this means custom mimetypes don't work (from svn)

* Thu Oct 16 2008 Matthias Clasen <mclasen@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Wed Oct  1 2008 David Zeuthen <davidz@redhat.com> - 2.18.1-2
- Update the patch to always pass FUSE POSIX URI's

* Wed Sep 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.7-1
- Update to 2.17.7

* Thu Jul 24 2008 David Zeuthen <davidz@redhat.com> - 2.17.4-5
- rebuild

* Thu Jul 24 2008 David Zeuthen <davidz@redhat.com> - 2.17.4-4
- autoreconf

* Thu Jul 24 2008 David Zeuthen <davidz@redhat.com> - 2.17.4-3
- Backport patch for g_mount_guess_content_type_sync

* Mon Jul 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.4-2
- Fix statfs configure check

* Mon Jul 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Thu Jul  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.3-3
- Fix a stupid crash

* Wed Jul  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3

* Mon Jun 16 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.2-2
- Fix a directory ownership oversight

* Thu Jun 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1
- Update to 2.17.2

* Tue May 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.17.0-1
- Update to 2.17.0

* Thu Apr 24 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.16.3-5
- Add support for GIO to set selinux attributes (gnome #529694)

* Thu Apr 17 2008 David Zeuthen <davidz@redhat.com> - 2.16.3-4
- Only pass URI's for gio apps (#442835)

* Sun Apr 13 2008 Dan Williams <dcbw@redhat.com> - 2.16.3-3
- Revert upstream changes to g_static_mutex_get_mutex_impl_shortcut that broke
    users of GMutex and GStaticMutex (bgo#316221)

* Wed Apr  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.3-2
- Fix a possible crash in application launching (bgo#527132)

* Tue Apr  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.3-1
- Update to 2.16.3

* Thu Apr  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.2-2
- Fix occasional misbehaviour of g_timeout_add_seconds

* Tue Apr  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.2-1
- Update to 2.16.2

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1
- Update to 2.16.0

* Mon Mar  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.6-2
- Fix inline support

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.6-1
- Update to 2.15.6

* Mon Feb 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.5-1
- Update to 2.15.5

* Thu Feb  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.4-2
- Update PCRE to 7.6

* Mon Jan 28 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Mon Jan 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.3-1
- Update to 2.15.3

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.2

* Tue Jan  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- 2.15.1
- add new BuildRequires
- 
* Sat Dec 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-4
- Another attempt

* Sat Dec 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-3
- Fix some errors in desktop files handling

* Fri Dec 21 2007 Caolan McNamara <caolanm@redhat.com> - 2.15.0-2
- add jakubs patch in so xulrunner will build and so gcc too

* Thu Dec 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.15.0-1
- Update to 2.15.0

* Sat Nov 24 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.4-1
- Update to 2.14.4

* Wed Nov  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.3-1
- Update to 2.14.3, including a new version of PCRE that
  fixes several vulnerabilities

* Tue Oct 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.2-1
- Update to 2.14.2 (bug fixes)

* Sun Sep 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.1-1
- Update to 2.14.1

* Sat Aug  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Thu Aug  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-3
- Update License field
- Don't ship ChangeLog

* Thu Jul 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-2
- Fix build issues on ppc

* Thu Jul 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.7-1
- Update to 2.13.7

* Fri Jun 29 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.6-1
- Update to 2.13.6
- Drop an ancient Conflict

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.5-1
- Update to 2.13.5

* Wed Jun  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.4-1
- Update to 2.13.4

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.3-1
- Update to 2.13.3

* Wed May 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.2-1
- Update to 2.13.2

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.1-1
- Update to 2.13.1

* Fri Mar  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.11-1
- Update to 2.12.11

* Wed Mar  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.10-1
- Update to 2.12.10

* Fri Feb  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-4
- More package review demands:
 * keep all -devel content in /usr/lib

* Sun Feb  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-3
- More package review feedback:
 * install /etc/profile.d snipplets as 644
 * explain Conflict with libgnomeui
 * remove stale Conflict with glib-devel
 
* Sat Feb  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-2
- Incorporate package review feedback:
 * drop an obsolete Provides:
 * add a -static subpackage
 * explain %%check ppc exception
 * align summaries
 
* Tue Jan 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.9-1
- Update to 2.12.9

* Mon Jan 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.8-1
- Update to 2.12.8

* Thu Jan  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.12.7-1
- Update to 2.12.7
- Fix bit-test on x86-64

* Wed Dec 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.6-1
- Update to 2.12.6

* Mon Dec 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.5-2
- Fix the configure check for broken poll

* Mon Dec 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.5-1
- Update to 2.12.5

* Sun Oct 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.4-1
- Update to 2.12.4

* Wed Aug 30 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.3-1.fc6
- Update to 2.12.3
- Drop upstreamed patch

* Sun Aug 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.2-2.fc6
- Use Posix monotonic timers for GTimer

* Tue Aug 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.2-1.fc6
- Update to 2.12.2

* Sat Jul 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.1-1
- Update to 2.12.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.12.0-1.1
- rebuild

* Sun Jul  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Jun 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.4-1
- Update to 2.11.4

* Mon Jun 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.3-1
- Update to 2.11.3

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.2-1
- Update to 2.11.2

* Thu Jun  1 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-6
- Rebuild

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-5
- Fix some fallout

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-4
- Include static libraries, since anaconda needs them (#193143)

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-3
- Keep glibconfig.h in /usr/lib

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-2
- Move glib to /lib

* Mon May 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to 2.11.1

* Tue May 2 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.0-1
- Update to 2.11.0

* Fri Apr 7 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.2-2
- Update to 2.10.2

* Tue Mar 7 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Fri Feb 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1
- Update to 2.10.0

* Sat Feb 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.6-1
- Update to 2.9.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.9.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.9.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.5-1
- Update to 2.9.5

* Wed Jan 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.4-1
- Update to 2.9.4

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.3-1
- Update to 2.9.3

* Fri Jan  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.9.2-2
- Update to 2.9.2

* Sun Dec 11 2005 Matthias Clasen <mclasen@redhat.com>
- Specfile cosmetics

* Sat Dec 10 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.1-1
- New upstream version

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.0-1
- New upstream version

* Tue Nov 15 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.4-1
- New upstream version

* Mon Oct  3 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.3-1
- New upstream version

* Mon Sep 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.2-1
- New upstream version

* Sat Aug 23 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.1-1
- New upstream version
- Drop patches

* Sat Aug 13 2005 Matthias Clasen <mclasen@redhat.com> - 2.8.0-1
- New stable upstream version
- Drop patches

* Fri Aug  5 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-3
- Fix C++ guards in gstdio.h

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-2
- Another attempt to fix atomic ops on s390

* Tue Aug  3 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.6-1
- Update to 2.7.6

* Tue Aug  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.5-1
- Update to 2.7.5

* Fri Jul 22 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Fri Jul 15 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Fri Jul  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.2-1
- Update to 2.7.2

* Fri Jul  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Mon Jun 13 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.0-1
- Update to 2.7.0

* Wed Apr  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.4-1
- Update to 2.6.4
- Drop upstreamed patches

* Fri Mar 11 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-4
- Fix #150817

* Wed Mar  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-3
- Rebuild

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-2
- Rebuild with gcc4

* Mon Feb 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.3-1
- Upgrade to 2.6.3

* Fri Feb  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.2-1
- Upgrade to 2.6.2

* Mon Jan 10 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.1-1
- Upgrade to 2.6.1

* Mon Dec 21 2004 Matthias Clasen <mclasen@redhat.com> - 2.6.0-1
- Upgrade to 2.6.0
 
* Mon Dec 06 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.8-1
- Upgrade to 2.4.8
 
* Wed Oct 13 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.7-1
- Upgrade to 2.4.7
 
* Fri Aug 13 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.6-1
- Update to 2.4.6

* Sun Aug 1 2004 ALan Cox <alan@redhat.com> - 2.4.5-2
- Fixed BuildRoot to use % macro not hardcode /var/tmp

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.5-1
- Update to 2.4.5
- Escape macros in changelog section

* Fri Jul 09 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.4-1
- Update to 2.4.4

* Mon Jun 21 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.2-1
- Require gettext at build time  (#125320)
- Update to 2.4.2 (#125736)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 19 2004 Matthias Clasen <mclasen@redhat.com> 2.4.1-1
- Update to 2.4.1

* Tue Mar 16 2004 Owen Taylor <otaylor@redhat.com> 2.4.0-1
- Update to 2.4.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.3.6-1
- Update to 2.3.6
- Remove gatomic build fix

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Mark McLoughlin <markmc@redhat.com> 2.3.5-1
- Update to 2.3.5
- Fix build on ppc64
- Disable make check on s390 as well - test-thread failing

* Wed Feb 25 2004 Mark McLoughlin <markmc@redhat.com> 2.3.3-1
- Update to 2.3.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Jonathan Blandford <jrb@redhat.com> 2.3.2-1
- new version
- remove 'make check' temporarily

* Mon Sep  8 2003 Owen Taylor <otaylor@redhat.com> 2.2.3-2.0
- Conflict with libgnomeui <= 2.2.0 (#83581, Göran Uddeborg)

* Tue Aug 26 2003 Owen Taylor <otaylor@redhat.com> 2.2.3-1.1
- Version 2.2.3

* Tue Jul  8 2003 Owen Taylor <otaylor@redhat.com> 2.2.2-2.0
- Bump for rebuild

* Sun Jun  8 2003 Owen Taylor <otaylor@redhat.com>
- Version 2.2.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Sun Feb  2 2003 Owen Taylor <otaylor@redhat.com>
- Version 2.2.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Owen Taylor <otaylor@redhat.com>
- Add static libraries to build (#78685, Bernd Kischnick)
- Bump-and-rebuild for new redhat-rpm-config

* Fri Dec 20 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.2.0
- Add make check to the build process

* Mon Dec 16 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.5

* Wed Dec 11 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.4

* Mon Dec  2 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.1.3

* Mon Oct 07 2002 Havoc Pennington <hp@redhat.com>
- Try rebuilding with new arches

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- install glib2.sh and glib2.csh to set G_BROKEN_FILENAMES
- blow away unpackaged files in install

* Thu Aug  8 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.6
- Remove fixed-ltmain.sh; shouldn't be needed any more.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.4

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 24 2002 Havoc Pennington <hp@redhat.com>
 - rebuild in different environment

* Mon Apr 15 2002 Owen Taylor <otaylor@redhat.com>
- Fix missing .po files (#63336)

* Wed Apr  3 2002 Alex Larsson <alexl@redhat.com>
- Update to version 2.0.1

* Fri Mar  8 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.0

* Mon Feb 25 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.3.15

* Thu Feb 21 2002 Alex Larsson <alexl@redhat.com>
- Bump for rebuild

* Mon Feb 18 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.3.14

* Fri Feb 15 2002 Havoc Pennington <hp@redhat.com>
- add horrible buildrequires hack

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.3.13.91 cvs snap

* Mon Feb 11 2002 Matt Wilson <msw@redhat.com>
- rebuild from CVS snapshot
- use setup -q

* Thu Jan 31 2002 Jeremy Katz <katzj@redhat.com>
- rebuild

* Tue Jan 29 2002 Owen Taylor <otaylor@redhat.com>
- 1.3.13

* Tue Jan 22 2002 Havoc Pennington <hp@redhat.com>
- attempting rebuild in rawhide

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- remove 64-bit patch now upstream, 1.3.12.90

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- add some missing files to file list, langify

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- add temporary patch to fix GTypeFundamentals on 64-bit

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- Version 1.3.11

* Thu Oct 25 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.10

* Tue Sep 25 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.9

* Wed Sep 19 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.3.8

* Fri Jul 20 2001 Owen Taylor <otaylor@redhat.com>
- Make -devel package require main package (#45388)
- Fix description and summary
- Configure with --disable-gtk-doc

* Wed Jun 20 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add some portability fixes needed at least on s390
- copy config.{guess,sub} instead of calling libtoolize

* Wed Jun 13 2001 Havoc Pennington <hp@redhat.com>
- try a new glib tarball with Makefile changes to work around
  libtool linking to installed .la files
- make -devel require pkgconfig

* Tue Jun 12 2001 Havoc Pennington <hp@redhat.com>
- either libtool or the bad libtool hacks caused link 
  against glib-gobject 1.3.2, rebuild

* Tue Jun 12 2001 Havoc Pennington <hp@redhat.com>
- 1.3.6
- bad libtool workarounds

* Fri May 04 2001 Owen Taylor <otaylor@redhat.com>
- 1.3.5, rename to glib2

* Fri Nov 17 2000 Owen Taylor <otaylor@redhat.com>
- Final 1.3.2

* Mon Nov 13 2000 Owen Taylor <otaylor@redhat.com>
- Version 1.3.2pre1
- Remove pkgconfig

* Sun Aug 13 2000 Owen Taylor <otaylor@redhat.com>
- Call 1.3.1b instead of snap... the snap* naming doesn't
  order correctly.

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- new snapshot with fixed .pc files

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- include .pc files in file list

* Thu Aug 10 2000 Havoc Pennington <hp@redhat.com>
- Include pkg-config
- Upgrade to a glib CVS snapshot

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Fri Jul 14 2000 Owen Taylor <otaylor@redhat.com>
- Remove glib-config.1 manpage from build since
  it conflicts with glib-devel. When we go to 
  glib glib1.2 setup, we should add it back

* Fri Jul 07 2000 Owen Taylor <otaylor@redhat.com>
- Version 1.3.1
- Move back to standard %%{prefix}

* Thu Jun 8 2000 Owen Taylor <otaylor@redhat.com>
- Rebuild in /opt/gtk-beta

* Tue May 30 2000 Owen Taylor <otaylor@redhat.com>
- New version (adds gobject)

* Wed Apr 25 2000 Owen Taylor <otaylor@redhat.com>
- Don't blow away /etc/ld.so.conf (sorry!)

* Tue Apr 24 2000 Owen Taylor <otaylor@redhat.com>
- Snapshot RPM for Pango testing

* Fri Feb 04 2000 Owen Taylor <otaylor@redhat.com>
- Added fixes from stable branch of CVS

* Thu Oct 7  1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.6

* Fri Sep 24 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.5

* Fri Sep 17 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.4

* Mon Jun 7 1999 Owen Taylor <otaylor@redhat.com>
- version 1.2.3

* Thu Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.1

* Fri Feb 26 1999 Michael Fulbright <drmike@redhat.com>
- Version 1.2

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- version 1.2.0pre1

* Tue Feb 23 1999 Cristian Gafton <gafton@redhat.com>
- new description tags 

* Sun Feb 21 1999 Michael Fulbright <drmike@redhat.com>
- removed libtoolize from %%build

* Thu Feb 11 1999 Michael Fulbright <drmike@redhat.com>
- added libgthread to file list

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.15

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.14

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.13

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- version 1.1.12

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated in preparation for the GNOME freeze

* Mon Apr 13 1998 Marc Ewing <marc@redhat.com>
- Split out glib package

