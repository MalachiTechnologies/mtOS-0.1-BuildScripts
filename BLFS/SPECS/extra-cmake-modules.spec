Name:           extra-cmake-modules
Version:        5.109.0
Release:        1%{?dist}
Summary:        The Extra Cmake Modules package contains extra CMake modules used by KDE Frameworks 5 and other packages.

Vendor:		Malachi Software (a subsidary of Malachi Technologies)
Distribution:	mtOS
     
License:        KDE
Source0:   	https://download.kde.org/stable/frameworks/5.109/extra-cmake-modules-5.109.0.tar.xz
%description


%prep
%setup -q

sed -i '/"lib64"/s/64//' kde-modules/KDEInstallDirsCommon.cmake &&

sed -e '/PACKAGE_INIT/i set(SAVE_PACKAGE_PREFIX_DIR "${PACKAGE_PREFIX_DIR}")' \
    -e '/^include/a set(PACKAGE_PREFIX_DIR "${SAVE_PACKAGE_PREFIX_DIR}")' \
    -i ECMConfig.cmake.in &&

mkdir build &&
cd    build &&

cmake -DCMAKE_INSTALL_PREFIX=/usr .. &&
make

# %build

# make

# %install

make install

%clean
rm -rf $RPM_BUILD_ROOT


%files


%changelog
