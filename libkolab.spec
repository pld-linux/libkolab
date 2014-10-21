#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	php		# PHP bindings
%bcond_without	python		# Python bindings

%define		php_name	php55
Summary:	Kolab Object Handling Library
Name:		libkolab
Version:	0.5.2
Release:	2
License:	LGPL v3+
Group:		Libraries
Source0:	http://mirror.kolabsys.com/pub/releases/%{name}-%{version}.tar.gz
# Source0-md5:	f33fcdc6852b9d045cb2be98ef3907ed
URL:		http://git.kolab.org/libkolab
BuildRequires:	QtCore-devel
BuildRequires:	curl-devel
BuildRequires:	kde4-kdepimlibs-devel >= 4.8
BuildRequires:	libkolabxml-devel >= 1.0
BuildRequires:	qt4-build
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	swig
%if %{with php}
BuildRequires:	%{php_name}-devel
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-program
BuildRequires:	swig-php
%endif
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	swig-python
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libkolab library is an advanced library to handle Kolab objects.

%package devel
Summary:	Kolab library development headers
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
Requires:	libkolabxml-devel >= 1.0

%description devel
Development headers for the Kolab object libraries.

%package -n %{php_name}-kolab
Summary:	PHP Bindings for libkolab
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}

%description -n %{php_name}-kolab
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
install -d build
cd build
%cmake \
	-Wno-fatal-errors -Wno-errors \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DLIB_INSTALL_DIR=%{_libdir} \
%if %{with php}
	-DPHP_BINDINGS=ON \
	-DPHP_INSTALL_DIR=%{php_extensiondir} \
	-DPHP_EXECUTABLE=%{__php} \
%endif
%if %{with python}
	-DPYTHON_BINDINGS=ON \
	-DPYTHON_INSTALL_DIR=%{py_sitedir} \
%endif
	..
%{__make}

%if %{with tests}
cd tests
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

%if %{with php}
install -d $RPM_BUILD_ROOT%{php_data_dir}
mv $RPM_BUILD_ROOT{%{php_extensiondir}/*.php,%{php_data_dir}}
%endif

%if %{with python}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_libdir}/cmake/Libkolab
%{_includedir}/kolab

%if %{with php}
%files -n %{php_name}-kolab
%defattr(644,root,root,755)
%attr(755,root,root) %{php_extensiondir}/kolabcalendaring.so
%attr(755,root,root) %{php_extensiondir}/kolabicalendar.so
%attr(755,root,root) %{php_extensiondir}/kolabobject.so
%attr(755,root,root) %{php_extensiondir}/kolabshared.so
%{php_data_dir}/kolabcalendaring.php
%{php_data_dir}/kolabicalendar.php
%{php_data_dir}/kolabobject.php
%{php_data_dir}/kolabshared.php
%endif

%if %{with python}
%files -n python-kolab
%defattr(644,root,root,755)
%dir %{py_sitedir}/kolab
%attr(755,root,root) %{py_sitedir}/kolab/_calendaring.so
%attr(755,root,root) %{py_sitedir}/kolab/_icalendar.so
%attr(755,root,root) %{py_sitedir}/kolab/_kolabobject.so
%attr(755,root,root) %{py_sitedir}/kolab/_shared.so
%{py_sitedir}/kolab/calendaring.py[co]
%{py_sitedir}/kolab/icalendar.py[co]
%{py_sitedir}/kolab/kolabobject.py[co]
%{py_sitedir}/kolab/shared.py[co]
%endif
