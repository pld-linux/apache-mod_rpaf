%define		mod_name	rpaf
%define 	apxs		%{_sbindir}/apxs
Summary:	Reverse proxy add forward module for Apache2
Summary(pl.UTF-8):	Moduł Apache'a 2 dodający przekazywanie dla odwrotnych proxy
Name:		apache-mod_%{mod_name}
Version:	0.5
Release:	3
License:	Apache
Group:		Networking/Daemons
Source0:	http://stderr.net/apache/rpaf/download/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	471fb059d6223a394f319b7c8ab45c4d
Source1:	%{name}.conf
URL:		http://stderr.net/apache/rpaf/
BuildRequires:	apache-devel >= 2.0.36
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Provides:	apache(mod_rpaf)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
rpaf is for backend Apache servers what mod_proxy_add_forward is for
frontend Apache servers. It does excactly the opposite of
mod_proxy_add_forward written by Ask Bjoern Hansen. It will also work
with mod_proxy that is distributed with Apache2 from version 2.0.36.

%description -l en.UTF-8
rpaf is for backend Apache servers what mod_proxy_add_forward is for
frontend Apache servers. It does excactly the opposite of
mod_proxy_add_forward written by Ask Bjørn Hansen. It will also work
with mod_proxy that is distributed with Apache2 from version 2.0.36.

%description -l pl.UTF-8
rpaf jest dla backendowych serwerów Apache tym, czym
mod_proxy_add_forward jest dla frontendowych. Wykonuje dokładnie
przeciwne operacje do mod_proxy_add_forward napisanego przez Aska
Bjorna Hansena. Będzie także działać z mod_proxy w Apache'u 2
począwszy od wersji 2.0.36.

%prep
%setup -q -n mod_%{mod_name}-%{version}
mv -f mod_%{mod_name}{-2.0,}.c

%build
%{apxs} -S CC="%{__cc}" -c -n mod_%{mod_name}.o mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}
install .libs/mod_rpaf.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/99_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES test.pl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
