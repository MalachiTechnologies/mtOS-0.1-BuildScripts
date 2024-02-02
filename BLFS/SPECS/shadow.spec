Name: 	 shadow
Version: 4.13
Release: 1%{?dist}
Summary: Shadow is an authentication framework for mtOS.
License: GPLv3

Source0: https://github.com/shadow-maint/shadow/releases/download/4.13/shadow-4.13.tar.xz

%description

#--------------------------------------
%prep
%setup -q

sed -i 's/groups$(EXEEXT) //' src/Makefile.in          &&

find man -name Makefile.in -exec sed -i 's/groups\.1 / /'   {} \; &&
find man -name Makefile.in -exec sed -i 's/getspnam\.3 / /' {} \; &&
find man -name Makefile.in -exec sed -i 's/passwd\.5 / /'   {} \; &&

sed -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD YESCRYPT@' \
    -e 's@/var/spool/mail@/var/mail@'                   \
    -e '/PATH=/{s@/sbin:@@;s@/bin:@@}'                  \
    -i etc/login.defs                                   &&

./configure --sysconfdir=/etc               \
            --disable-static                \
            --with-{b,yes}crypt             \
            --with-group-name-max-length=32 &&
make

#--------------------------------------
%build

%make

#--------------------------------------
make exec_prefix=/usr install
#--------------------------------------
%files

# %defattr()
