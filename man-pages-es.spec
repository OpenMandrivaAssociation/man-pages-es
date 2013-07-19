%define LNG es
%define extra_ver 0.8a

Summary:	Spanish man (manual) pages from the Linux Documentation Project
Name:		man-pages-%{LNG}
Version:	1.55
Release:	9
License:	LDP GENERAL PUBLIC LICENSE
Group:		System/Internationalization
#Url:		http://www.pameli.org/
Url:		http://www.ditec.um.es/~piernas/manpages-es/
Source0:	http://www.ditec.um.es/~piernas/manpages-es/man-pages-es-%{version}.tar.bz2  
Source1:	http://www.ditec.um.es/~piernas/manpages-es/man-pages-es-extra-%{extra_ver}.tar.bz2  
BuildArch:	noarch
BuildRequires:	man
Requires:	locales-%{LNG}
Requires:	man
Requires(post,preun):	sed grep man
Autoreq:	false

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
%setup -n man-pages-%{LNG}-%{version} -a1
%build

%install
mkdir -p %{buildroot}/%{_mandir}/%{LNG}/man{1,2,3,4,5,6,7,8,9,n}
mkdir -p %{buildroot}/var/catman/%{LNG}/cat{1,2,3,4,5,6,7,8,9,n}

mv man1/{README,LEAME} .

make MANDIR=%{buildroot}/%{_mandir}/es allbz

make -C man-pages-es-extra-%{extra_ver} MANDIR=%{buildroot}/%{_mandir}/es allbz

LANG=%{LNG} DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%{_mandir}/%{LNG}

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron << EOF
#!/bin/bash
LANG=%{LNG} %{_bindir}/mandb %{_mandir}/%{LNG}
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LNG}
rm -f %{buildroot}/usr/share/man/es/{LEEME,LEEME.extra,PAQUETES,PROYECTO}

touch %{buildroot}/var/cache/man/%{LNG}/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%{LNG}, if there isn't any man page
   ## directory /%{_mandir}/%{LNG}
   if [ ! -d %{_mandir}/%{LNG} ] ; then
       rm -rf /var/catman/%{LNG}
   fi
fi

%post
%create_ghostfile /var/cache/man/%{LNG}/whatis root root 644

%files
%doc LEEME README man-pages-es-extra-%{extra_ver}/LEEME.extra
%doc man-pages-es-extra-%{extra_ver}/PAQUETES 
%doc man-pages-es-extra-%{extra_ver}/PROYECTO
%dir %{_mandir}/%{LNG}
%dir /var/cache/man/%{LNG}
%ghost %config(noreplace) /var/cache/man/%{LNG}/whatis
%{_mandir}/%{LNG}/man*
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/CACHEDIR.TAG*
%{_mandir}/%{LNG}/index.db*
%attr(755,root,man) /var/catman/%{LNG}
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

