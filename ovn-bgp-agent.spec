%global pypi_name ovn-bgp-agent
%global with_doc 1
%{!?upstream_version: %global ovn-bgp-agent_version %{released_version}%{?milestone}}

Name:           %{pypi_name}
Version:        XXX
Release:        XXX
Summary:        An agent to expose routes to OVN workloads via BGP

License:        ASL 2.0
URL:            https://opendev.org/x/ovn-bgp-agent
Source0:        https://tarballs.opendev.org/x/%{name}/%{name}-%{upstream_version}.tar.gz
Source1:        ovn-bgp-agent.service

BuildArch:      noarch

BuildRequires:  git-core
BuildRequires:  python3-jinja2
BuildRequires:  python3-devel
BuildRequires:  python3-neutron-lib
BuildRequires:  python3-openvswitch
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-service
BuildRequires:  python3-ovsdbapp
BuildRequires:  python3-pbr
BuildRequires:  python3-pyroute2
BuildRequires:  python3-stevedore

Requires:  openvswitch >= 2.8.0
Requires:  python3-jinja2 >= 2.10
Requires:  python3-neutron-lib >= 2.10.1
Requires:  python3-oslo-concurrency >= 3.26.0
Requires:  python3-oslo-config >= 6.1.0
Requires:  python3-oslo-log >= 3.36.0
Requires:  python3-oslo-service => 1.40.2
Requires:  python3-ovsdbapp >= 1.4.0
Requires:  python3-pyroute2 >= 0.6.4
Requires:  python3-stevedore >= 1.20.0
Requires:  python3-openvswitch >= 2.8.0

%description
This package contains the ovn-bgp-agent to expose BGP routes to OVN
workloads.

%if 0%{?with_doc}
%package doc
Summary:    OVN BGP Agent documentation

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%py3_install
mkdir -p %{buildroot}/%{_sysconfdir}/ovn-bgp-agent
mkdir -p %{buildroot}/%{_unitdir}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/ovn-bgp-agent.service

%check
export OS_TEST_PATH='./ovn-bgp-agent/tests/unit'
export PATH=$PATH:%{buildroot}/usr/bin
export PYTHONPATH=$PWD
stestr-3 --test-path $OS_TEST_PATH run

%files
%license LICENSE
%{_bindir}/ovn-bgp-agent
%{_unitdir}/ovn-bgp-agent.service
%{_datadir}/ovn-bgp-agent/systemd/ovn-bgp-agent.service
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{released_version}-py%{python3_version}.egg-info
%{_sysconfdir}/ovn-bgp-agent

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%post
%systemd_post %{pypi_name}

%preun
%systemd_preun %{pypi_name}

%postun
%systemd_postun_with_restart %{pypi_name}

%changelog
