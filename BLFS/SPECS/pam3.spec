Name:           linux-pam
Version:        1.5.3
Release:        2%{?dist}
Summary:        An extensible library which provides authentication for applications
Vendor:			Malachi Software (a subsidary of Malachi Technologies, LLC)
Distribution:	mtOS

Group:          System Security
License:        BSD and GPLv2+
URL:            https://github.com/linux-pam/linux-pam/
	
Source0: https://github.com/linux-pam/linux-pam/releases/download/v%{version}/Linux-PAM-%{version}.tar.xz
Source1: https://github.com/linux-pam/linux-pam/releases/download/v%{version}/Linux-PAM-%{version}.tar.xz.asc
# Source2: https://releases.pagure.org/pam-redhat/pam-redhat-%{pam_redhat_version}.tar.bz2
Source5: other.pamd
Source6: system-auth.pamd
Source7: password-auth.pamd
Source8: fingerprint-auth.pamd
Source9: smartcard-auth.pamd
Source10: config-util.pamd
Source11: dlopen.sh
Source12: system-auth.5
Source13: config-util.5
Source15: pamtmp.conf
Source16: postlogin.pamd
Source17: postlogin.5
Source18: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt      

# BuildRequires:  
# Requires:       

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.
 
%package devel
Summary: Files needed for developing PAM-aware applications and modules for PAM
Requires: pam%{?_isa} = %{version}-%{release}
 
%description devel
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. This package
contains header files used for building both PAM-aware applications
and modules for use with the PAM system.

%prep
%setup -q -n Linux-PAM-%{version} -a 2
perl -pi -e "s/ppc64-\*/ppc64-\* \| ppc64p7-\*/" build-aux/config.sub
perl -pi -e "s/\/lib \/usr\/lib/\/lib \/usr\/lib \/lib64 \/usr\/lib64/" m4/libtool.m4


%build
%configure \
	--disable-rpath \
	--libdir=%{_pamlibdir} \
	--includedir=%{_includedir}/security \
	--disable-selinux \
	--disable-audit \

	--disable-static \
	--disable-prelude
make -C po update-gmo
make



%install
mkdir -p doc/txts
for readme in modules/pam_*/README ; do
	cp -f ${readme} doc/txts/README.`dirname ${readme} | sed -e 's|^modules/||'`
done
 
# Install the binaries, libraries, and modules.
make install DESTDIR=$RPM_BUILD_ROOT LDCONFIG=:
 
# %if %{WITH_SELINUX}
# Temporary compat link
# ln -sf pam_sepermit.so $RPM_BUILD_ROOT%{_moduledir}/pam_selinux_permit.so
# %endif
 
# RPM uses docs from source tree
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/Linux-PAM
# Included in setup package
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/environment
 
# Install default configuration files.
install -d -m 755 $RPM_BUILD_ROOT%{_pamconfdir}
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_pamconfdir}/other
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_pamconfdir}/system-auth
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_pamconfdir}/password-auth
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_pamconfdir}/fingerprint-auth
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_pamconfdir}/smartcard-auth
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_pamconfdir}/config-util
install -m 644 %{SOURCE16} $RPM_BUILD_ROOT%{_pamconfdir}/postlogin
install -m 600 /dev/null $RPM_BUILD_ROOT%{_secconfdir}/opasswd
install -d -m 755 $RPM_BUILD_ROOT/var/log
install -m 600 /dev/null $RPM_BUILD_ROOT/var/log/tallylog
install -d -m 755 $RPM_BUILD_ROOT/var/run/faillock
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/motd.d
install -d -m 755 $RPM_BUILD_ROOT/usr/lib/motd.d
install -d -m 755 $RPM_BUILD_ROOT/run/motd.d
 
# Install man pages.
install -m 644 %{SOURCE12} %{SOURCE13} %{SOURCE17} $RPM_BUILD_ROOT%{_mandir}/man5/
ln -sf system-auth.5 $RPM_BUILD_ROOT%{_mandir}/man5/password-auth.5
ln -sf system-auth.5 $RPM_BUILD_ROOT%{_mandir}/man5/fingerprint-auth.5
ln -sf system-auth.5 $RPM_BUILD_ROOT%{_mandir}/man5/smartcard-auth.5
 
 
for phase in auth acct passwd session ; do
	ln -sf pam_unix.so $RPM_BUILD_ROOT%{_moduledir}/pam_unix_${phase}.so 
done
 
# Remove .la files and make new .so links -- this depends on the value
# of _libdir not changing, and *not* being /usr/lib.
for lib in libpam libpamc libpam_misc ; do
rm -f $RPM_BUILD_ROOT%{_pamlibdir}/${lib}.la
done
rm -f $RPM_BUILD_ROOT%{_moduledir}/*.la
 
%if "%{_pamlibdir}" != "%{_libdir}"
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}
for lib in libpam libpamc libpam_misc ; do
pushd $RPM_BUILD_ROOT%{_libdir}
ln -sf %{_pamlibdir}/${lib}.so.*.* ${lib}.so
popd
rm -f $RPM_BUILD_ROOT%{_pamlibdir}/${lib}.so
done
%endif
 
# Duplicate doc file sets.
rm -fr $RPM_BUILD_ROOT/usr/share/doc/pam
 
# Install the file for autocreation of /var/run subdirectories on boot
install -m644 -D %{SOURCE15} $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/pam.conf
 
%find_lang Linux-PAM

	
%check
# Make sure every module subdirectory gave us a module.  Yes, this is hackish.
for dir in modules/pam_* ; do
if [ -d ${dir} ] ; then
# %if ! %{WITH_SELINUX}
# 	[ ${dir} = "modules/pam_selinux" ] && continue
# 	[ ${dir} = "modules/pam_sepermit" ] && continue
# %endif
# %if ! %{WITH_AUDIT}
# 	[ ${dir} = "modules/pam_tty_audit" ] && continue
# %endif
	[ ${dir} = "modules/pam_tally" ] && continue
	[ ${dir} = "modules/pam_tally2" ] && continue
	if ! ls -1 $RPM_BUILD_ROOT%{_moduledir}/`basename ${dir}`*.so ; then
		echo ERROR `basename ${dir}` did not build a module.
		exit 1
	fi
fi
done
 
# Check for module problems.  Specifically, check that every module we just
# installed can actually be loaded by a minimal PAM-aware application.
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_pamlibdir}
for module in $RPM_BUILD_ROOT%{_moduledir}/pam*.so ; do
	if ! env LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_pamlibdir} \
		 %{SOURCE11} -ldl -lpam -L$RPM_BUILD_ROOT%{_libdir} ${module} ; then
		echo ERROR module: ${module} cannot be loaded.
		exit 1
	fi
done

	
%ldconfig_scriptlets

%files -f Linux-PAM.lang
%dir %{_pamconfdir}
%config(noreplace) %{_pamconfdir}/other
%config(noreplace) %{_pamconfdir}/system-auth
%config(noreplace) %{_pamconfdir}/password-auth
%config(noreplace) %{_pamconfdir}/fingerprint-auth
%config(noreplace) %{_pamconfdir}/smartcard-auth
%config(noreplace) %{_pamconfdir}/config-util
%config(noreplace) %{_pamconfdir}/postlogin
%{!?_licensedir:%global license %%doc}
%license Copyright
%license gpl-2.0.txt
%doc doc/txts
%doc doc/sag/*.txt doc/sag/html
%{_pamlibdir}/libpam.so.*
%{_pamlibdir}/libpamc.so.*
%{_pamlibdir}/libpam_misc.so.*
%{_sbindir}/pam_console_apply
%{_sbindir}/faillock
%attr(4755,root,root) %{_sbindir}/pam_timestamp_check
%attr(4755,root,root) %{_sbindir}/unix_chkpwd
%attr(0700,root,root) %{_sbindir}/unix_update
%attr(0755,root,root) %{_sbindir}/mkhomedir_helper
%attr(0755,root,root) %{_sbindir}/pwhistory_helper
%dir %{_moduledir}
%{_moduledir}/pam_access.so
%{_moduledir}/pam_chroot.so
%{_moduledir}/pam_console.so
%{_moduledir}/pam_cracklib.so
%{_moduledir}/pam_debug.so
%{_moduledir}/pam_deny.so
%{_moduledir}/pam_echo.so
%{_moduledir}/pam_env.so
%{_moduledir}/pam_exec.so
%{_moduledir}/pam_faildelay.so
%{_moduledir}/pam_faillock.so
%{_moduledir}/pam_filter.so
%{_moduledir}/pam_ftp.so
%{_moduledir}/pam_group.so
%{_moduledir}/pam_issue.so
%{_moduledir}/pam_keyinit.so
%{_moduledir}/pam_lastlog.so
%{_moduledir}/pam_limits.so
%{_moduledir}/pam_listfile.so
%{_moduledir}/pam_localuser.so
%{_moduledir}/pam_loginuid.so
%{_moduledir}/pam_mail.so
%{_moduledir}/pam_mkhomedir.so
%{_moduledir}/pam_motd.so
%{_moduledir}/pam_namespace.so
%{_moduledir}/pam_nologin.so
%{_moduledir}/pam_permit.so
%{_moduledir}/pam_postgresok.so
%{_moduledir}/pam_pwhistory.so
%{_moduledir}/pam_rhosts.so
%{_moduledir}/pam_rootok.so
# %if %{WITH_SELINUX}
# %{_moduledir}/pam_selinux.so
# %{_moduledir}/pam_selinux_permit.so
# %{_moduledir}/pam_sepermit.so
# %endif
%{_moduledir}/pam_securetty.so
%{_moduledir}/pam_shells.so
%{_moduledir}/pam_stress.so
%{_moduledir}/pam_succeed_if.so
%{_moduledir}/pam_time.so
%{_moduledir}/pam_timestamp.so
# %if %{WITH_AUDIT}
# %{_moduledir}/pam_tty_audit.so
# %endif
%{_moduledir}/pam_umask.so
%{_moduledir}/pam_unix.so
%{_moduledir}/pam_unix_acct.so
%{_moduledir}/pam_unix_auth.so
%{_moduledir}/pam_unix_passwd.so
%{_moduledir}/pam_unix_session.so
%{_moduledir}/pam_userdb.so
%{_moduledir}/pam_warn.so
%{_moduledir}/pam_wheel.so
%{_moduledir}/pam_xauth.so
%{_moduledir}/pam_filter
%dir %{_secconfdir}
%config(noreplace) %{_secconfdir}/access.conf
%config(noreplace) %{_secconfdir}/chroot.conf
%config %{_secconfdir}/console.perms
%config(noreplace) %{_secconfdir}/console.handlers
%config(noreplace) %{_secconfdir}/group.conf
%config(noreplace) %{_secconfdir}/limits.conf
%dir %{_secconfdir}/limits.d
%config(noreplace) %{_secconfdir}/namespace.conf
%dir %{_secconfdir}/namespace.d
%attr(755,root,root) %config(noreplace) %{_secconfdir}/namespace.init
%config(noreplace) %{_secconfdir}/pam_env.conf
%config(noreplace) %{_secconfdir}/time.conf
%config(noreplace) %{_secconfdir}/opasswd
%dir %{_secconfdir}/console.apps
%dir %{_secconfdir}/console.perms.d
%dir /var/run/console
# %if %{WITH_SELINUX}
# %config(noreplace) %{_secconfdir}/sepermit.conf
# %dir /var/run/sepermit
# %endif
%ghost %verify(not md5 size mtime) /var/log/tallylog
%dir /var/run/faillock
%dir %{_sysconfdir}/motd.d
%dir /run/motd.d
%dir /usr/lib/motd.d
%{_prefix}/lib/tmpfiles.d/pam.conf
%{_mandir}/man5/*
%{_mandir}/man8/*
 
%files devel
%{_includedir}/security
%{_mandir}/man3/*
%{_libdir}/libpam.so
%{_libdir}/libpamc.so
%{_libdir}/libpam_misc.so
%doc doc/mwg/*.txt doc/mwg/html
%doc doc/adg/*.txt doc/adg/html
%doc doc/specs/rfc86.0.txt



%changelog
