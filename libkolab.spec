Summary:	Kolab Object Handling Library
Name:		libkolab
Version:	0.3
Release:	0.1
License:	LGPLv3+
URL:		http://git.kolab.org/libkolab
Source0:	http://git.kolab.org/libkolab/snapshot/%{name}-%{version}.tar.gz
BuildRequires:	curl-devel
BuildRequires:	kde4-kdepimlibs-devel
BuildRequires:	libcalendaring-devel
BuildRequires:	libkolabxml-devel >= 0.7
BuildRequires:	php-devel
BuildRequires:	python-devel
BuildRequires:	qt-devel

%description
The libkolab library is an advanced library to handle Kolab objects.

%package devel
Summary:	Kolab library development headers
BuildRequires:	kde4-kdepimlibs-devel >= 4.8
BuildRequires:	libcalendaring-devel
Requires:	%{name} = %{version}-%{release}
Requires:	libkolabxml-devel >= 0.7
Requires:	php-devel
Requires:	pkgconfig
Requires:	python-devel

%description devel
Development headers for the Kolab object libraries.

%package -n php-kolab
Summary:	PHP Bindings for libkolab
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php(api) = %{php_core_api}
Requires:	php(zend-abi) = %{php_zend_api}

%description -n php-kolab
PHP Bindings for libkolab

%package -n python-kolab
Summary:	Python bindings for libkolab
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-kolab
Python bindings for libkolab

%prep
%setup -q

%build
rm -rf build
mkdir -p build
pushd build
%{cmake} -Wno-fatal-errors -Wno-errors \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
%if 0%{?rhel} < 7 && 0%{?fedora} < 17
	-DUSE_LIBCALENDARING=ON \
%endif
	-DPHP_BINDINGS=ON \
	-DPHP_INSTALL_DIR=%{php_extdir} \
	-DPYTHON_BINDINGS=ON \
	-DPYTHON_INSTALL_DIR=%{py_sitedir} \
	..
%{__make}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
%{__make} install DESTDIR=$RPM_BUILD_ROOT
popd

%check
pushd build/tests
./benchmarktest || :
./calendaringtest || :
./formattest || :
./freebusytest || :
./icalendartest || :
./kcalconversiontest || :
./upgradetest || :
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_libdir}/%{name}.so.0
%{_libdir}/%{name}.so.0.3

%files devel
%defattr(644,root,root,755)
%{_libdir}/%{name}.so
%{_libdir}/cmake/Libkolab
%{_includedir}/kolab

%files -n php-kolab
%defattr(644,root,root,755)
%{php_extdir}/calendaring.php
%{php_extdir}/calendaring.so
%{php_extdir}/icalendar.php
%{php_extdir}/icalendar.so

%files -n python-kolab
%defattr(644,root,root,755)
%{py_sitedir}/_calendaring.so
%{py_sitedir}/calendaring.py*
%{py_sitedir}/_icalendar.so
%{py_sitedir}/icalendar.py*


