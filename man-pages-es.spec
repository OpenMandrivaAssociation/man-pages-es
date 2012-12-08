%define LNG es
%define extra_ver 0.8a

Summary: Spanish man (manual) pages from the Linux Documentation Project
Name: man-pages-%LNG
Version: 1.55
Release: %mkrel 8
License: LDP GENERAL PUBLIC LICENSE
Group: System/Internationalization
Source: http://www.ditec.um.es/~piernas/manpages-es/man-pages-es-%{version}.tar.bz2  
Source1: http://www.ditec.um.es/~piernas/manpages-es/man-pages-es-extra-%{extra_ver}.tar.bz2  
URL: http://www.ditec.um.es/~piernas/manpages-es/
#URL: http://www.pameli.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LNG, man => 1.5j-8mdk
Requires(post,preun): sed grep man
Autoreq: false
BuildArch: noarch
Obsoletes: man-%LNG, manpages-%LNG
Provides: man-%LNG, manpages-%LNG
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
        Section 5:  File formats and protocols (e.g., wtmp, %{_sysconfdir}passwd,
                nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)


%prep
%setup -n man-pages-%LNG-%{version} -a1
%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%_mandir/%LNG/man{1,2,3,4,5,6,7,8,9,n}
mkdir -p %{buildroot}/var/catman/%LNG/cat{1,2,3,4,5,6,7,8,9,n}

mv man1/{README,LEAME} .

make MANDIR=%{buildroot}/%_mandir/es allbz

make -C man-pages-es-extra-%{extra_ver} MANDIR=%{buildroot}/%_mandir/es allbz

LANG=%LNG DESTDIR=%{buildroot} %{_sbindir}/makewhatis %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_sbindir}/makewhatis %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG
rm -f %{buildroot}/usr/share/man/es/{LEEME,LEEME.extra,PAQUETES,PROYECTO}

touch %{buildroot}/var/cache/man/%LNG/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LNG, if there isn't any man page
   ## directory /%_mandir/%LNG
   if [ ! -d %_mandir/%LNG ] ; then
       rm -rf /var/catman/%LNG
   fi
fi

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,man,755)
%doc LEEME README man-pages-es-extra-%{extra_ver}/LEEME.extra
%doc man-pages-es-extra-%{extra_ver}/PAQUETES 
%doc man-pages-es-extra-%{extra_ver}/PROYECTO
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%_mandir/%LNG/whatis
%attr(755,root,man) /var/catman/%LNG
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.55-7mdv2011.0
+ Revision: 666368
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.55-6mdv2011.0
+ Revision: 609319
- rebuild
- fix build
- fix typos

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.55-5mdv2011.0
+ Revision: 609212
- fix file list
- fix build
- rebuild
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.55-3mdv2009.1
+ Revision: 351571
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.55-2mdv2009.0
+ Revision: 223172
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tv@mandriva.org> 1.55-1mdv2008.1
+ Revision: 131812
- fix  prereq
- kill re-definition of %%buildroot on Pixel's request
- fix summary-ended-with-dot

* Mon Apr 23 2007 Thierry Vignaud <tv@mandriva.org> 1.55-1mdv2008.0
+ Revision: 17427
- kill icon
- new release ; use mkrel


* Fri Aug 13 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.28-6mdk
- fix description (rafael)

* Fri Aug 13 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.28-5mdk
- rebuild

* Thu Jul 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.28-4mdk
- rebuild

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.28-3mdk
- fix unpackaged files

* Thu May 30 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.28-2mdk
- use new man-pages-LG template
    - don't rebuild whatis on install since
      - we've already build in package
      - cron will rebuild it nightly and so add other package french man pages
    - adapt to new man-pages-LG template
    - requires man => 1.5j-8mdk for new man-pages framework
    - remove old makewhatis.es since default makewhatis is now able to parse
      non english man pages
    - use new std makewhatis to build whatis in spec and in cron entry 
    - whatis db goes into /var/cache/man (so enable ro /usr)
    - standard {Build,}Requires/buildroot/prereq/arc/provides/obsoletes
    - remove translations
- make -C prevent using useless sub shells

* Mon Mar 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.28-1mdk
- fix licence
- new release
- add alternative url

* Thu Mar 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.24-7mdk
- provides manpages-%%LANG 
- don't overwrite crontab if user altered it

* Sun Jul 08 2001 Jesse Kuang <kjx@mandrakesoft.com> 1.24-6mdk
- rebuild on cluster

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.24-5mdk
- BM

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.24-4mdk
- use mandir macro in order to be ok when switching to /usr/share/man as
  following FHS.

* Sat Apr 08 2000 Camille Begnis <camille@mandrakesoft.com> 1.24-3mdk
- spec update
- fix permissions
- fix group

* Fri Nov 19 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- moved makewhatis.es from /usr/local/sbin to /usr/sbin

* Wed Nov 03 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- upgraded to man-pages-es-1.24 & man-pages-es-extra-0.8a

* Tue Jul 20 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- included some nice improvements from man-pages-pl

* Wed Jul 07 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- changed the name from man-es to man-pages-es, to make it consistent
  with the english man pages package (and compatible with the name
  used by Juan Piernas Cánovas)
- merged with the rpm package I mantained before; that is I added an icon,
  the /var/catman/es tree, a makewhatis.es script, and a cron entry to run it

* Sat May 22 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Fix prereqs

* Wed Apr 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Description taken from Juan Piernas Cánovas <piernas@ditec.um.es> package.

* Tue Apr 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Initial version.
- Add a script for /etc/man.config

