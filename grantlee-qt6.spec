
%bcond_without	tests		# unit tests

%define		qt_ver		6.6.0
%define		major_ver	5.3

Summary:	Grantlee - set of frameworks for use with Qt 6
Summary(pl.UTF-8):	Grantlee - zbiór szkieletów do wykorzystania z Qt 6
Name:		grantlee-qt6
Version:	5.3.1
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/steveire/grantlee/releases/download/v%{version}/grantlee-%{version}.tar.gz
# Source0-md5:	4ef8eae5dd61e3c7603d76208eb4d922
Patch0:		x87fix.patch
URL:		http://www.grantlee.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Network-devel >= %{qt_ver}
BuildRequires:	Qt6Sql-devel >= %{qt_ver}
BuildRequires:	Qt6Test-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	Qt6Xml-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	qt6-qmake >= %{qt_ver}
BuildRequires:	qt6-linguist >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	Qt6Core >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Obsoletes:	grantlee-qt5 <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Grantlee is a string template engine based on the Django template
system and written using Qt.

%description -l pl.UTF-8
Grantlee to silnik szablonów oparty na systemie szablonów Django i
napisany przy użyciu Qt.

%package devel
Summary:	Header files for grantlee libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek grantlee
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qt_ver}
# only textdocument library
Requires:	Qt6Gui-devel >= %{qt_ver}
Obsoletes:	grantlee-qt5-devel <= %{version}
Conflicts:	grantlee-devel

%description devel
Header files for grantlee libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek grantlee.

%prep
%setup -q -n grantlee-%{version}
%patch0 -p1

%build
%cmake -B build \
	-G Ninja \
	-DGRANTLEE_BUILD_WITH_QT6=ON

%ninja_build -C build

%if %{with tests}
cd build
QT_QPA_PLATFORM=offscreen \
ctest -E '(testinternationalization|htmlbuildertest|plainmarkupbuildertest)' --output-on-failure
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG README.md
%attr(755,root,root) %{_libdir}/libGrantlee_Templates.so.*.*.*
%ghost %{_libdir}/libGrantlee_Templates.so.5
%attr(755,root,root) %{_libdir}/libGrantlee_TextDocument.so.*.*.*
%ghost %{_libdir}/libGrantlee_TextDocument.so.5
%dir %{_libdir}/grantlee
%dir %{_libdir}/grantlee/%{major_ver}
%attr(755,root,root) %{_libdir}/grantlee/%{major_ver}/grantlee_defaultfilters.so
%attr(755,root,root) %{_libdir}/grantlee/%{major_ver}/grantlee_defaulttags.so
%attr(755,root,root) %{_libdir}/grantlee/%{major_ver}/grantlee_i18ntags.so
%attr(755,root,root) %{_libdir}/grantlee/%{major_ver}/grantlee_loadertags.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libGrantlee_Templates.so
%{_libdir}/libGrantlee_TextDocument.so
%{_includedir}/grantlee_templates.h
%{_includedir}/grantlee_textdocument.h
%{_includedir}/grantlee
%{_libdir}/cmake/Grantlee5
