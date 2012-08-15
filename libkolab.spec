# TODO
# - pldize this package!
#  - file attrs
#  - pld cmake macros
#  - tests to build, not %check and add bcond
#  - drop rhel/fedora dist macros
Summary:	Kolab Object Handling Library
Name:		libkolab
Version:	0.3.1
Release:	0.1
License:	LGPL v3+
Group:		Libraries
URL:		http://git.kolab.org/libkolab
Source0:	http://mirror.kolabsys.com/pub/releases/%{name}-%{version}.tar.gz
# Source0-md5:	99f2b2c519c3ebaa57f8f520e8880e9a
BuildRequires:	curl-devel
BuildRequires:	kde4-kdepimlibs-devel >= 4.8
BuildRequires:	libcalendaring-devel
BuildRequires:	libcalendaring-devel
BuildRequires:	libkolabxml-devel >= 0.7
BuildRequires:	php-devel >= 4:5.0.4
BuildRequires:	python-devel
BuildRequires:	qt-devel
BuildRequires:	rpmbuild(macros) >= 1.519
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libkolab library is an advanced library to handle Kolab objects.

%package devel
Summary:	Kolab library development headers
Group:		Development/Libraries
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
%{?requires_php_extension}

%description -n php-kolab
PHP Bindings for libkolab.

%package -n python-kolab
Summary:	Python bindings for libkolab
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-kolab
Python bindings for libkolab.

%prep
%setup -q

%build
rm -rf build
install -d build
cd build
%cmake \
	-Wno-fatal-errors -Wno-errors \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
%if 0%{?rhel} < 7 && 0%{?fedora} < 17
	-DUSE_LIBCALENDARING=ON \
%endif
	-DPHP_BINDINGS=ON \
	-DPHP_INSTALL_DIR=%{php_extensiondir} \
	-DPYTHON_BINDINGS=ON \
	-DPYTHON_INSTALL_DIR=%{py_sitedir} \
	..
%{__make}
cd -

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_data_dir}
mv $RPM_BUILD_ROOT{%{php_extensiondir}/*.php,%{php_data_dir}}

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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

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
%{php_data_dir}/calendaring.php
%{php_data_dir}/icalendar.php
%attr(755,root,root) %{php_extensiondir}/calendaring.so
%attr(755,root,root) %{php_extensiondir}/icalendar.so

%files -n python-kolab
%defattr(644,root,root,755)
%{py_sitedir}/_calendaring.so
%{py_sitedir}/calendaring.py[co]
%{py_sitedir}/_icalendar.so
%{py_sitedir}/icalendar.py[co]
