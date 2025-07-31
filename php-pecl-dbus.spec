%define		php_name	php%{?php_suffix}
%define		modname	dbus
%define		snap	20250731
Summary:	Extension for interaction with DBUS busses
Name:		%{php_name}-pecl-%{modname}
Version:	0.1.2
Release:	1.%{snap}.1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://github.com/derickr/pecl-dbus/archive/master/%{name}-%{version}.tar.gz
# Source0-md5:	a2e2e90fc8e35a99d4f9200f1c2aaee4
URL:		https://github.com/derickr/pecl-dbus
BuildRequires:	%{php_name}-devel >= 4:5.2.0
BuildRequires:	dbus-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(dbus)
Obsoletes:	php-pecl-dbus < 0.1.1-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allows you to talk to DBUS services on a system, and
also act as a DBUS service.

%prep
%setup -qc
mv pecl-%{modname}-*/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
