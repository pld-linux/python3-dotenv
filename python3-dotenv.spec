#
# Conditional build:
%bcond_with	doc	# mkdocs based documentation (TODO)
%bcond_without	tests	# unit tests

%define		module		dotenv
Summary:	Add .env support to your django/flask apps in development and deployments
Summary(pl.UTF-8):	Dodanie obsługi .env do aplikacji django/flaska w trakcie rozwoju i wdrożeń
Name:		python3-%{module}
Version:	1.2.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/python-dotenv/
Source0:	https://files.pythonhosted.org/packages/source/p/python-dotenv/python_dotenv-%{version}.tar.gz
# Source0-md5:	72b43685c14b492ced7ed6fb1e3f1d63
URL:		https://pypi.org/project/python-dotenv/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:77.0
%if %{with tests}
BuildRequires:	python3-click >= 5.0
BuildRequires:	python3-ipython
BuildRequires:	python3-pytest >= 3.9
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-sh >= 2
%endif
%if %{with doc}
BuildRequires:	python3-mdx_truly_sane_lists >= 1.3
BuildRequires:	python3-mkdocs >= 1.5.0
BuildRequires:	python3-mkdocs-include-markdown-plugin >= 6.0.0
BuildRequires:	python3-mkdocs-material >= 9.5.0
BuildRequires:	python3-mkdocstrings >= 0.24.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Add .env support to your django/flask apps in development and
deployments.

%description -l pl.UTF-8
Dodanie obsługi .env do aplikacji django/flaska w trakcie rozwoju i
wdrożeń.

%prep
%setup -q -n python_dotenv-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# dotenv entrypoint script stub
install -d build-3/bin
cat >build-3/bin/dotenv <<'EOF'
#!/bin/sh
%{__python3} -m dotenv "$@"
EOF
chmod 755 build-3/bin/dotenv

PATH=$(pwd)/build-3/bin:$PATH \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/dotenv{,-3}
ln -sf dotenv-3 $RPM_BUILD_ROOT%{_bindir}/dotenv

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/dotenv-3
%{_bindir}/dotenv
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/python_dotenv-%{version}.dist-info
