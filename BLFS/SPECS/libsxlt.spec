Name:           libxslt
Version:        1.1.39
Release:        1%{?dist}
Summary:        libxslt is an XSLT processor based on libxml2.

Vendor:		Malachi Software (a subsidary of Malachi Technologies)
Distribution:	mtOS
     
License:        GPLv3
Source0:   	https://download.gnome.org/sources/libxslt/1.1/libxslt-1.1.39.tar.xz
%description
The libxslt package contains XSLT libraries used for extending libxml2 libraries to support XSLT files.

%prep
%setup -q
sed -i s/3000/5000/ libxslt/transform.c doc/xsltproc.{1,xml}

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name "*.la" -delete

%clean
rm -rf $RPM_BUILD_ROOT


%files
%{_bindir}/*
%{_libdir}/*.so*
%{_libdir}/cmake/libxslt/*
/usr/lib/python*/site-packages/*
%{_libdir}/xsltConf.sh
%doc /usr/share/doc/%{name}/*
#%doc /usr/share/doc/libxslt-python-1.1.39/*
%doc /usr/share/gtk-doc/html/libxslt/*
%doc /usr/share/gtk-doc/html/libexslt/*
%doc /usr/share/man/*/*


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary: Development files for %{name}-%{version}.

%description devel
Development files for %{name}-%{version}.

%files devel
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*.pc

%changelog
*	Sun Dec 09 2018 Samuel Raynor <samuel@samuelraynor.com> 1.1.32-1
-	Initial build.
