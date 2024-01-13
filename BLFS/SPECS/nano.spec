Summary:         A small text editor
Name:            nano
Version:         7.2
Release:         1%{?dist}
License:         GPL-3.0-or-later
URL:             https://www.nano-editor.org
 
Source0:         https://www.nano-editor.org/dist/latest/%{name}-%{version}.tar.xz
Source1:         https://www.nano-editor.org/dist/latest/%{name}-%{version}.tar.xz.asc
# gpg --keyserver keyserver.ubuntu.com --recv-key 168E6F4297BFD7A79AFD4496514BBE2EB8E1961F
# gpg --output bensberg.pgp --armor --export bensberg@telfort.nl
Source2:         bensberg.pgp
 
# Additional sources
Source3:         nanorc
 
# Shell snippets for default-editor setup
Source11:        nano-default-editor.sh
Source12:        nano-default-editor.csh
Source13:        nano-default-editor.fish
 
BuildRequires:   file-devel
BuildRequires:   gettext-devel
BuildRequires:   gcc
BuildRequires:   git
BuildRequires:   gnupg2
BuildRequires:   groff
BuildRequires:   make
BuildRequires:   ncurses-devel
BuildRequires:   sed
BuildRequires:   texinfo
Conflicts:       filesystem < 3
 
%description
GNU nano is a small and friendly text editor.
 
%if %{with default_editor}
%package default-editor
Summary:         Sets GNU nano as the default editor
Requires:        nano = %{version}-%{release}
# Ensure that only one package with this capability is installed
Provides:        system-default-editor
Conflicts:       system-default-editor
BuildArch:       noarch
 
%description default-editor
This package ensures the EDITOR shell variable
is set in common shells to GNU nano.
 
%package -n default-editor
Summary:         Metapackage for DNF group
Recommends:      nano-default-editor
Requires:        system-default-editor
BuildArch:       noarch
 
%description -n default-editor
The package acts as a placeholder in DNF group 'Standard', which will
install nano-default-editor on fresh installs and it will not block users
who don't have nano as a default editor during upgrade.
%endif
 
%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -S git
 
%build
mkdir build
cd build
%global _configure ../configure
%configure
%make_build
# generate default /etc/nanorc
# - set hunspell as the default spell-checker
# - enable syntax highlighting by default (#1270712)
sed -e 's/^#.*set speller.*$/set speller "hunspell"/' \
    -e 's|^# \(include "/usr/share/nano/\*.nanorc"\)|\1|' \
    %{SOURCE3} doc/sample.nanorc > ./nanorc
 
%install
cd build
%make_install
rm -f %{buildroot}%{_infodir}/dir
 
# remove installed HTML documentation
rm -f %{buildroot}%{_docdir}/nano/{nano,nano.1,nanorc.5,rnano.1}.html
 
# install default /etc/nanorc
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 ./nanorc %{buildroot}%{_sysconfdir}/nanorc
 
# enable all extra syntax highlighting files by default
mv %{buildroot}%{_datadir}/nano/extra/* %{buildroot}%{_datadir}/nano
rm -rf %{buildroot}%{_datadir}/nano/extra
 
%find_lang %{name}
 
%if %{with default_editor}
# install nano-default-editor snippets
install -Dpm 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/profile.d/%{basename:%{S:11}}
install -Dpm 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/profile.d/%{basename:%{S:12}}
install -Dpm 0644 %{SOURCE13} %{buildroot}%{_datadir}/fish/vendor_conf.d/%{basename:%{S:13}}
%endif
 
%files -f build/%{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%doc build/doc/sample.nanorc
%doc doc/{faq,nano}.html
%{_bindir}/{,r}nano
%config(noreplace) %{_sysconfdir}/nanorc
%{_mandir}/man1/{,r}nano.1*
%{_mandir}/man5/nanorc.5*
%{_infodir}/nano.info*
%{_datadir}/nano
 
%if %{with default_editor}
%files default-editor
%dir %{_sysconfdir}/profile.d
%config(noreplace) %{_sysconfdir}/profile.d/nano-default-editor.*
%dir %{_datadir}/fish/vendor_conf.d
%{_datadir}/fish/vendor_conf.d/nano-default-editor.fish
 
%files -n default-editor
%endif
 
 
%changelog
