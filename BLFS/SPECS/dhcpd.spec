Name: 	 dhcpcd
Version: 10.0.2
Release: 1%{?dist}
Summary: dhcpcd is an implementation of the DHCP client specified in RFC2131. A DHCP client is useful for connecting your computer to a network which uses DHCP to assign network addresses. dhcpcd strives to be a fully featured, yet very lightweight DHCP client.
License: ISC License, MPL2.0

Source0: https://github.com/NetworkConfiguration/dhcpcd/releases/download/v10.0.2/dhcpcd-10.0.2.tar.xz

%description

#--------------------------------------
%prep
%setup -q

install  -v -m700 -d /var/lib/dhcpcd &&

groupadd -g 52 dhcpcd        &&
useradd  -c 'dhcpcd PrivSep' \
         -d /var/lib/dhcpcd  \
         -g dhcpcd           \
         -s /bin/false       \
         -u 52 dhcpcd &&
chown    -v dhcpcd:dhcpcd /var/lib/dhcpcd 

./configure --prefix=/usr                \
            --sysconfdir=/etc            \
            --libexecdir=/usr/lib/dhcpcd \
            --dbdir=/var/lib/dhcpcd      \
            --runstatedir=/run           \
            --privsepuser=dhcpcd
make  

#--------------------------------------
%build

%make

#--------------------------------------
make install
#--------------------------------------
%files

# %defattr()
