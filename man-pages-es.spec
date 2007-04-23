%define LANG es
%define extra_ver 0.8a

Summary: Spanish man (manual) pages from the Linux Documentation Project.
Name: man-pages-%LANG
Version: 1.55
Release: %mkrel 1
License: LDP GENERAL PUBLIC LICENSE
Group: System/Internationalization
Source: http://www.ditec.um.es/~piernas/manpages-es/man-pages-es-%{version}.tar.bz2  
Source1: http://www.ditec.um.es/~piernas/manpages-es/man-pages-es-extra-%{extra_ver}.tar.bz2  
Icon: books-%LANG.gif
URL: http://www.ditec.um.es/~piernas/manpages-es/
#URL: http://www.pameli.org/
Buildroot: %_tmppath/%name-root
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LANG, man => 1.5j-8mdk
Prereq: sed grep man
Autoreq: false
BuildArch: noarch
Obsoletes: man-%LANG, manpages-%LANG
Provides: man-%LANG, manpages-%LANG
Obsoletes: man-pages-es-extra
Provides: man-pages-es-extra

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to spanish.  The man pages are
organized into the following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, /etc/passwd,
                nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)


%prep
%setup -n man-pages-%LANG-%{version} -a1
%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_mandir/%LANG/man{1,2,3,4,5,6,7,8,9,n}
mkdir -p $RPM_BUILD_ROOT/var/catman/%LANG/cat{1,2,3,4,5,6,7,8,9,n}

mv man1/{README,LEAME} .

make MANDIR=$RPM_BUILD_ROOT/%_mandir/es allbz

make -C man-pages-es-extra-%{extra_ver} MANDIR=$RPM_BUILD_ROOT/%_mandir/es allbz

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG=%LANG /usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG
rm -f $RPM_BUILD_ROOT/usr/share/man/es/{LEEME,LEEME.extra,PAQUETES,PROYECTO}


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LANG, if there isn't any man page
   ## directory /%_mandir/%LANG
   if [ ! -d %_mandir/%LANG ] ; then
       rm -rf /var/catman/%LANG
   fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%doc LEEME README man-pages-es-extra-%{extra_ver}/LEEME.extra
%doc man-pages-es-extra-%{extra_ver}/PAQUETES 
%doc man-pages-es-extra-%{extra_ver}/PROYECTO
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%config(noreplace) /var/cache/man/%LANG/whatis
%_mandir/%LANG/man*
%attr(755,root,man)/var/catman/%LANG
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron

