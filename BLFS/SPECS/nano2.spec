Name: nano
Version: 7.2
Release: 1%{?dist}
Summary: Nano is a small, simple text editor which aims to replace Pico, the default editor in the Pine package
License: GPLv3

Source0: https://www.nano-editor.org/dist/v7/nano-7.2.tar.xz

%description

#--------------------------------------
%prep
%setup -q
./configure --prefix=/usr     \
            --sysconfdir=/etc \
            --enable-utf8     \
            --docdir=/usr/share/doc/nano-7.2

#--------------------------------------
%build

%make

#--------------------------------------
make install && install -v -m644 doc/{nano.html,sample.nanorc} /usr/share/doc/nano-7.2

#--------------------------------------
%files

# %defattr()

