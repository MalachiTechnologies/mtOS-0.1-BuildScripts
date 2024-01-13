Name:           wget
Version:        1.21.4
Release:        1%{?dist}
Summary:        The Wget package contains a utility useful for non-interactive downloading of files from the Web.
Vendor:		Malachi Software (a subsidary of Malachi Technologies)
Distribution:	mtOS
Group:          Applications/System
License:        GPLv3
URL:            https://www.gnu.org/software/wget/
Source0:        ftp://ftp.gnu.org/gnu/wget/wget-1.21.4.tar.gz

%description
GNU Wget is a free utility for non-interactive download of files from
the Web.  It supports HTTP, HTTPS, and FTP protocols, as well as
retrieval through HTTP proxies.

%prep
%define _unpackaged_files_terminate_build 0
%setup -q


%build
%configure --with-ssl=openssl
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%config(noreplace) /etc/wgetrc
%{_bindir}/*
%{_datadir}/locale*
%{_mandir}/*/*
%{_infodir}/wget.info.gz



%changelog
