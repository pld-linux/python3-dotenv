#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-dotenv.spec)

%define		module		dotenv
Summary:	Add .env support to your django/flask apps in development and deployments
Summary(pl.UTF-8):	Dodanie obsługi .env do aplikacji django/flaska w trakcie rozwoju i wdrożeń
Name:		python-%{module}
# keep 0.18.x here for python2 support
Version:	0.18.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/python-dotenv/
Source0:	https://files.pythonhosted.org/packages/source/p/python-dotenv/python-dotenv-%{version}.tar.gz
# Source0-md5:	87e2bcc039142b4408337eddb210462a
URL:		https://pypi.org/project/python-dotenv/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-click >= 5.0
BuildRequires:	python-ipython
BuildRequires:	python-mock
BuildRequires:	python-pytest >= 3.9
BuildRequires:	python-pytest-cov
BuildRequires:	python-sh >= 1.09
BuildRequires:	python-typing
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-click >= 5.0
BuildRequires:	python3-ipython < 9
BuildRequires:	python3-mock
BuildRequires:	python3-pytest >= 3.9
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-sh >= 1.09
BuildRequires:	python3-sh < 2
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Add .env support to your django/flask apps in development and
deployments.

%description -l pl.UTF-8
Dodanie obsługi .env do aplikacji django/flaska w trakcie rozwoju i
wdrożeń.

%package -n python3-%{module}
Summary:	Add .env support to your django/flask apps in development and deployments
Summary(pl.UTF-8):	Dodanie obsługi .env do aplikacji django/flaska w trakcie rozwoju i wdrożeń
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-%{module}
Add .env support to your django/flask apps in development and
deployments.

%description -n python3-%{module} -l pl.UTF-8
Dodanie obsługi .env do aplikacji django/flaska w trakcie rozwoju i
wdrożeń.

%prep
%setup -q -n python-dotenv-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
# dotenv entrypoint script stub
install -d build-2/bin
cat >build-2/bin/dotenv <<'EOF'
#!/bin/sh
%{__python} -m dotenv.cli "$@"
EOF
chmod 755 build-2/bin/dotenv

LC_ALL=C.UTF-8 \
PATH=$(pwd)/build-2/bin:$PATH \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# dotenv entrypoint script stub
install -d build-3/bin
cat >build-3/bin/dotenv <<'EOF'
#!/bin/sh
%{__python3} -m dotenv.cli "$@"
EOF
chmod 755 build-3/bin/dotenv

PATH=$(pwd)/build-3/bin:$PATH \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/dotenv{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/dotenv{,-3}
ln -sf dotenv-3 $RPM_BUILD_ROOT%{_bindir}/dotenv
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/dotenv-2
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/python_dotenv-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/dotenv-3
%{_bindir}/dotenv
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/python_dotenv-%{version}-py*.egg-info
%endif
