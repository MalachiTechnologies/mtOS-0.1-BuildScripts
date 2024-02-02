Name:           cpio
Version:        2.14
Release:        1%{?dist}
Summary:        The cpio package contains tools for archiving.
Vendor:		Malachi Software (a subsidary of Malachi Technologies)
Distribution:	mtOS
     
License:        GNU
Source0:   	https://ftp.gnu.org/gnu/cpio/cpio-2.14.tar.bz2
%description


%prep
%setup -q


%build
./configure --prefix=/usr \
            --enable-mt   \
            --with-rmt=/usr/libexec/rmt &&
make &&
makeinfo --html            -o doc/html      doc/cpio.texi &&
makeinfo --html --no-split -o doc/cpio.html doc/cpio.texi &&
makeinfo --plaintext       -o doc/cpio.txt  doc/cpio.texi

%install
make install &&
install -v -m755 -d /usr/share/doc/cpio-2.14/html &&
install -v -m644    doc/html/* \
                    /usr/share/doc/cpio-2.14/html &&
install -v -m644    doc/cpio.{html,txt} \
                    /usr/share/doc/cpio-2.14

%clean
rm -rf $RPM_BUILD_ROOT


%files


%changelog
