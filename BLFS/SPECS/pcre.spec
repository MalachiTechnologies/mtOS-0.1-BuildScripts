Name: 	 pcre2
Version: 10.42
Release: 1%{?dist}
Summary: The PCRE2 package contains a new generation of the Perl Compatible Regular Expression libraries. These are useful for implementing regular expression pattern matching using the same syntax and semantics as Perl.
License: PCRE2 License

Source0: https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.42/pcre2-10.42.tar.bz2

%description

#--------------------------------------
%prep
%setup -q

./configure --prefix=/usr                       \
            --docdir=/usr/share/doc/pcre2-10.42 \
            --enable-unicode                    \
            --enable-jit                        \
            --enable-pcre2-16                   \
            --enable-pcre2-32                   \
            --enable-pcre2grep-libz             \
            --enable-pcre2grep-libbz2           \
            --enable-pcre2test-libreadline      \
            --disable-static                    &&
make


#--------------------------------------
%build

%make

#--------------------------------------
make install
#--------------------------------------
%files

# %defattr()
