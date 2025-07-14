# TODO
# - broken: https://github.com/gnif/mod_rpaf/issues/27
# or not https://github.com/gnif/mod_rpaf/issues/33#issuecomment-263519703 ?

%define		mod_name	rpaf
%define		apxs		%{_sbindir}/apxs
Summary:	Reverse proxy add forward module for Apache
Summary(pl.UTF-8):	Moduł Apache'a 2 dodający przekazywanie dla odwrotnych proxy
Name:		apache-mod_%{mod_name}
Version:	0.8.4
Release:	3
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/gnif/mod_rpaf/archive/v%{version}/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	8fbd9ee19f8ea4e25ab8414685276105
Source1:	%{name}.conf
Patch0:		git.patch
Patch1:		0.6-compat.patch
URL:		https://github.com/gnif/mod_rpaf/
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Provides:	apache(mod_rpaf)
Conflicts:	apache(mod_extract_forwarded)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
Sets REMOTE_ADDR, HTTPS, and HTTP_PORT to the values provided by an
upstream proxy.

%description -l pl.UTF-8
rpaf jest dla backendowych serwerów Apache tym, czym
mod_proxy_add_forward jest dla frontendowych.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch -P0 -p1
%patch -P1 -p1

%build
%{apxs} -S CC="%{__cc}" -c -n mod_%{mod_name}.o mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
install -p .libs/mod_rpaf.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/99_mod_%{mod_name}.conf

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
%doc README.md CHANGES
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
