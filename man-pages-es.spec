%define LNG es
%define extra_ver 0.8a

Summary: Spanish man (manual) pages from the Linux Documentation Project
Name: man-pages-%LNG
Version: 1.55
Release: %mkrel 7
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

mkdir -p  %{buildroot}/var/cache/man/%LNG
rm -f %{buildroot}/usr/share/man/es/{LEEME,LEEME.extra,PAQUETES,PROYECTO}

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LNG, if there isn't any man page
   ## directory /%_mandir/%LNG
   if [ ! -d %_mandir/%LNG ] ; then
       rm -rf /var/catman/%LNG
   fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,man,755)
%doc LEEME README man-pages-es-extra-%{extra_ver}/LEEME.extra
%doc man-pages-es-extra-%{extra_ver}/PAQUETES 
%doc man-pages-es-extra-%{extra_ver}/PROYECTO
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%_mandir/%LNG/man*
%attr(755,root,man) /var/catman/%LNG
