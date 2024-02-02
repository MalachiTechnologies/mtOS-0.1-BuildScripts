Summary: 	Git is a free and open source, distributed version control system designed to handle everything from small to very large projects with speed and efficiency.
Name: 		git
Version: 	2.43.0
Release:	1%{?dist}
License:	GPLv2
Vendor:		Malachi Software (a subsidary of Malachi Technologies)
Distribution:	mtOS
Source0:	https://www.kernel.org/pub/software/scm/git/git-2.43.0.tar.xz

%description

%prep
%setup -q

%build

./configure --prefix=/usr \
            --with-gitconfig=/etc/gitconfig \
            --with-python=python3 &&
make

%install

make perllibdir=/usr/lib/perl5/5.38/site_perl install

%check

%post

%clean

rm -rf %{buildroot}/*

%files

%changelog
*	Thu Jan 18 2024 Malachi Snyder <kmsnyder@malachi.technology>
-	Initial build for mtOS
