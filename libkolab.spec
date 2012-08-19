%bcond_without	tests
Summary:	Kolab Object Handling Library
Name:		libkolab
Version:	0.3.1
Release:	1
License:	LGPL v3+
Group:		Libraries
URL:		http://git.kolab.org/libkolab
Source0:	http://mirror.kolabsys.com/pub/releases/%{name}-%{version}.tar.gz
# Source0-md5:	99f2b2c519c3ebaa57f8f520e8880e9a
Patch0:		0001-Fix-kolab-errorhandler.h-kolabformat-errorhandler.h.patch
BuildRequires:	QtCore-devel
BuildRequires:	curl-devel
BuildRequires:	kde4-kdepimlibs-devel >= 4.8
BuildRequires:	libkolabxml-devel >= 0.8
BuildRequires:	php-devel >= 4:5.0.4
BuildRequires:	python-devel
BuildRequires:	qt4-build
BuildRequires:	rpmbuild(macros) >= 1.519
BuildRequires:	swig
BuildRequires:	swig-php
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libkolab library is an advanced library to handle Kolab objects.

%package devel
Summary:	Kolab library development headers
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libkolabxml-devel >= 0.8
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
%patch0 -p1

%build
rm -rf build
install -d build
cd build
%cmake \
	-Wno-fatal-errors -Wno-errors \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DPHP_BINDINGS=ON \
	-DPHP_INSTALL_DIR=%{php_extensiondir} \
	-DPYTHON_BINDINGS=ON \
	-DPYTHON_INSTALL_DIR=%{py_sitedir} \
	..
%{__make}
cd -

%if %{with tests}
cd build/tests
./benchmarktest || :
./calendaringtest || :
./formattest || :
./freebusytest || :
./icalendartest || :
./kcalconversiontest || :
./upgradetest || :
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_data_dir}
mv $RPM_BUILD_ROOT{%{php_extensiondir}/*.php,%{php_data_dir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.0
%attr(755,root,root) %{_libdir}/%{name}.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_libdir}/cmake/Libkolab
%{_includedir}/kolab

%files -n php-kolab
%defattr(644,root,root,755)
%{php_data_dir}/kolabcalendaring.php
%{php_data_dir}/kolabicalendar.php
%{php_data_dir}/kolabshared.php
%attr(755,root,root) %{php_extensiondir}/kolabcalendaring.so
%attr(755,root,root) %{php_extensiondir}/kolabicalendar.so
%attr(755,root,root) %{php_extensiondir}/kolabshared.so

%files -n python-kolab
%defattr(644,root,root,755)
%dir %{py_sitedir}/kolab
%attr(755,root,root) %{py_sitedir}/kolab/_calendaring.so
%{py_sitedir}/kolab/calendaring.py*
%attr(755,root,root) %{py_sitedir}/kolab/_icalendar.so
%{py_sitedir}/kolab/icalendar.py*
%attr(755,root,root) %{py_sitedir}/kolab/_shared.so
%{py_sitedir}/kolab/shared.py*
