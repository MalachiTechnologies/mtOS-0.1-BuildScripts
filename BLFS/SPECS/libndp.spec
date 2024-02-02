Name:           libndp
Version:        1.8
Release:        1%{?dist}
Summary:        The libndp package provides a wrapper for IPv6 Neighbor Discovery Protocol. It also provides a tool named ndptool for sending and receiving NDP messages.
Vendor:		Malachi Software (a subsidary of Malachi Technologies)
Distribution:	mtOS
     
License:        LGPL-2.1
Source0:   	http://libndp.org/files/libndp-1.8.tar.gz
%description


%prep
%setup -q


%build
./configure --prefix=/usr        \
            --sysconfdir=/etc    \
            --localstatedir=/var \
            --disable-static     &&
make

%install
make install

%clean
rm -rf $RPM_BUILD_ROOT


%files


%changelog
