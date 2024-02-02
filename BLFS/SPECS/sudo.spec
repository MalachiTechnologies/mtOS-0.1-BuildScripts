Name: 	 sudo
Version: 1.9.14p3
Release: 1%{?dist}
Summary: The Sudo package allows a system administrator to give certain users (or groups of users) the ability to run some (or all) commands as root or another user while logging the commands and arguments.
License: MIT License

Source0: https://www.sudo.ws/dist/sudo-1.9.14p3.tar.gz

%description

#--------------------------------------
%prep
%setup -q

./configure --prefix=/usr              \
            --libexecdir=/usr/lib      \
            --with-secure-path         \
            --with-all-insults         \
            --with-env-editor          \
            --docdir=/usr/share/doc/sudo-1.9.14p3 \
            --with-passprompt="[sudo] password for %p: " &&
make

#--------------------------------------
%build

%make

#--------------------------------------
make install &&
ln -sfv libsudo_util.so.0.0.0 /usr/lib/sudo/libsudo_util.so.0
#--------------------------------------
%files

# %defattr()
