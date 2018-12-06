%global goipath         github.com/go-yaml/yaml
# Release 2.2.1
%global commit          5420a8b6744d3b0345ab293f6fcba19c978f1183

%global import_path     gopkg.in/v2/yaml
%global import_path_sec gopkg.in/yaml.v2

%global v1_commit          9f9df34309c04878acc86042b16630b0f696e1de
%global v1_shortcommit     %(c=%{v1_commit}; echo ${c:0:7})
%global v1_import_path     gopkg.in/v1/yaml
%global v1_import_path_sec gopkg.in/yaml.v1

%global devel_main      golang-gopkg-yaml-devel-v2

%gometa

Name:           golang-gopkg-yaml
Version:        1
Release:        25%{?dist}
Summary:        Enables Go programs to comfortably encode and decode YAML values
License:        LGPLv3 with exceptions
URL:            %{gourl}
Source0:        %{gosource}
Source1:        https://%{goipath}/archive/%{v1_commit}/yaml-%{v1_commit}.tar.gz

%description
%{summary}

%package devel
Summary:        Enables Go programs to comfortably encode and decode YAML values
BuildArch:      noarch

BuildRequires:  golang(gopkg.in/check.v1)
Requires:       golang(gopkg.in/check.v1)

%description devel
The yaml package enables Go programs to comfortably encode and decode YAML
values. It was developed within Canonical as part of the juju project, and
is based on a pure Go port of the well-known libyaml C library to parse and
generate YAML data quickly and reliably.

The yaml package is almost compatible with YAML 1.1, including support for
anchors, tags, etc. There are still a few missing bits, such as document
merging, base-60 floats (huh?), and multi-document unmarshalling. These
features are not hard to add, and will be introduced as necessary.

This package contains library source intended for
building other packages which use import path with
%{v1_import_path} prefix.

%package devel-v2
Summary:        Enables Go programs to comfortably encode and decode YAML values
BuildArch:      noarch

%description devel-v2
The yaml package enables Go programs to comfortably encode and decode YAML
values. It was developed within Canonical as part of the juju project, and
is based on a pure Go port of the well-known libyaml C library to parse and
generate YAML data quickly and reliably.

The yaml package supports most of YAML 1.1 and 1.2,
including support for anchors, tags, map merging, etc.
Multi-document unmarshalling is not yet implemented, and base-60 floats
from YAML 1.1 are purposefully not supported since they're a poor design
 and are gone in YAML 1.2.

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%prep
%setup -q -n yaml-%{v1_commit} -T -b 1
%forgesetup

%install
%goinstall
%goinstall -i %{import_path} -o devel.file-list
%goinstall -i %{import_path_sec} -o devel.file-list

cw=$(pwd)
pushd ../yaml-%{v1_commit}
%goinstall -i %{v1_import_path} -o ${cw}/v1_devel.file-list
%goinstall -i %{v1_import_path_sec} -o ${cw}/v1_devel.file-list

# TODO(jchaloup): create rpm macros for this!!!
#github.com/go-yaml/yaml -> gopkg.in/v2/yaml
pushd %{buildroot}/%{gopath}/src/%{import_path}/
sed -i 's/"github\.com\/go-yaml\/yaml/"gopkg\.in\/v2\/yaml/g' \
        $(find . -name '*.go')
#'github.com/go-yaml/yaml -> gopkg.in/yaml.v2
cd %{buildroot}/%{gopath}/src/%{import_path_sec}/
sed -i 's/"github\.com\/go-yaml\/yaml/"gopkg\.in\/yaml\.v2/g' \
        $(find . -name '*.go')
#gopkg.in/v1/yaml -> gopkg.in/yaml.v1
cd %{buildroot}/%{gopath}/src/%{v1_import_path_sec}/
sed -i 's/"gopkg\.in\/v1\/yaml/"gopkg\.in\/yaml\.v1/g' \
        $(find . -name '*.go')
popd

%check
%gochecks
pushd %{buildroot}/%{gopath}/src/%{import_path}/
%gochecks -i %{import_path}
cd %{buildroot}/%{gopath}/src/%{import_path_sec}/
%gochecks
popd

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files devel -f v1_devel.file-list
%license LICENSE LICENSE.libyaml
%doc README.md

%files devel-v2 -f devel.file-list
%license LICENSE LICENSE.libyaml
%doc README.md

%changelog
* Sat Oct 27 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1-25.20181027git5420a8b
- Update to release 2.2.1

* Tue Oct 23 2018 Nicolas Mailhot <nim@fedoraproject.org> - 1-24.gitcd8b52f
- redhat-rpm-config-123 triggers bugs in gosetup, remove it from Go spec files as it’s just an alias
- https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/RWD5YATAYAFWKIDZBB7EB6N5DAO4ZKFM/

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1-23.gitcd8b52f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 30 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1-22.gitcd8b52f
- Fix mixed-up directories
  
* Tue Mar 20 2018 Jan Chaloupka <jchaloup@redhat.com> - 1-21.gitcd8b52f
- Update to spec 3.0
  Bump to cd8b52f8269e0feb286dfeef29f8fe4d5b397e0b

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 22 2017 Jan Chaloupka <jchaloup@redhat.com> - 1-19
- Bump to upstream cd8b52f8269e0feb286dfeef29f8fe4d5b397e0b
  related: #1250524

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 16 2016 Jan Chaloupka <jchaloup@redhat.com> - 1-15
- Polish the spec file
  related: #1250524

* Thu Aug 25 2016 jchaloup <jchaloup@redhat.com> - 1-14
- Enable devel and unit-test for epel7
  related: #1250524

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-13
- https://fedoraproject.org/wiki/Changes/golang1.7

* Sun May 15 2016 jchaloup <jchaloup@redhat.com> - 1-12
- Bump to upstream 53feefa2559fb8dfa8d81baad31be332c97d6c77
  related: #1250524

* Sat Mar 05 2016 jchaloup <jchaloup@redhat.com> - 1-11
- Bump to upstream bef53efd0c76e49e6de55ead051f886bea7e9420
  related: #1250524

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-10
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1-8
- Choose the correct architecture
- Update unit-test subpackage
  related: #1250524

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1-7
- Update spec file to spec-2.0
  resolves: #1250524

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 10 2014 jchaloup <jchaloup@redhat.com> - 1-5
- Update to gopkg.in/check.v2 but still provide gopkg.in/check.v1
  related: #1141875

* Fri Oct 10 2014 jchaloup <jchaloup@redhat.com> - 1-4
- Adding go test and deps on gopkg.in/check.v1
- Adding another Provides

* Mon Sep 15 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1-3
- Resolves: rhbz#1141875 - newpackage
- no debug_package
- preserve timestamps
- do not redefine gopath

* Thu Aug 07 2014 Adam Miller <maxamillion@fedoraproject.org> - 1-2
- Fix import_path

* Tue Aug 05 2014 Adam Miller <maxamillion@fedoraproject.org> - 1-1
- First package for Fedora
