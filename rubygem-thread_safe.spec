# Generated from thread_safe-0.1.0.gem by gem2rpm -*- rpm-spec -*-
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
%global gem_name thread_safe

# Perl auto-provides would generate a provide for 'package thread_safe;'
%if 0%{?rhel} > 6
%global __provides_filter_from /perl(thread_safe)/
%else
%{?filter_setup:
%filter_from_provides /perl(thread_safe)/d
%filter_setup
}
%endif

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.3.5
Release: 2%{?dist}
Summary: Thread-safe collections and utilities for Ruby
Group: Development/Languages
# jsr166e.LondAdder, jsr166e.Striped64, jsr166e.ConcurrentHashMapV8
# and their Ruby ports are Public Domain
License: ASL 2.0 and Public Domain
URL: https://github.com/ruby-concurrency/thread_safe
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Patch0 sent upstream at
# https://github.com/ruby-concurrency/thread_safe/pull/13
Patch0: rubygem-thread_safe-0.3.5-optional-deps.patch
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
A collection of data structures and utilities to make thread-safe
programming in Ruby easier.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

# Remove dependency on simplecov and coveralls:
%patch0 -p1

# Remove dependency on minitest-reporters:
sed -i -e "/minitest\/reporters/d" test/test_helper.rb
sed -i -e "/Minitest::Reporters/d" test/test_helper.rb

%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd ./%{gem_instdir}
# Skip test_cache_loops.rb for MRI
# Apparantly still an issue on Ruby 2.0.0p247 (2013-06-27 revision 41674)
# http://bugs.ruby-lang.org/issues/8305
#
# Skip test_hash.rb for MRI
# MRI issue/behaviour since thread_safe doesn't really modify MRI's Hash
# https://github.com/headius/thread_safe/issues/10
%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib -e \
  'Dir.glob "./test/test_{array,cache,helper,synchronized_delegator}.rb", &method(:require)'
%{?scl:EOF}

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%exclude %{gem_instdir}/ext
%exclude %{gem_instdir}/.travis.yml

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/examples
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/tasks
%{gem_instdir}/test
%{gem_instdir}/yard-template
%exclude %{gem_instdir}/.yardopts


%changelog
* Fri Jan 22 2016 Dominic Cleal <dcleal@redhat.com> 0.3.5-2
- Rebuild for sclo-ror42 SCL

* Tue Mar 24 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.3.5-1
- Update to 0.3.5
- New upstream URL.
- Remove extraneous BR: ruby. This is covered by BR: ruby(release).
- Patch to make simplecov and coveralls optional dependencies.
- Remove optional minitest/reporters dependency.
- Drop Rakefile shebang removal. This is fixed upstream.

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 0.3.4-3
- Fix provides filtering on RHEL7
  - Related: rhbz#1203138

* Wed Mar 18 2015 Josef Stribny <jstribny@redhat.com> - 0.3.4-2
- Fix: filter perl(thread_safe) provide out
  - Resolves: rhbz#1203138

* Fri Jan 16 2015 Josef Stribny <jstribny@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Tue Feb 04 2014 Josef Stribny <jstribny@redhat.com> - 0.1.3-3
- Add Public Domain to licenses

* Mon Jan 27 2014 Josef Stribny <jstribny@redhat.com> - 0.1.3-2
- Fix license to ASL 2.0
  - Resolves rhbz#1058281

* Wed Oct 30 2013 Josef Stribny <jstribny@redhat.com> - 0.1.3-1
- Update to thread_safe 0.1.3

* Thu Oct 03 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-5
- Fix macros for -doc sub-package

* Thu Oct 03 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-4
- Rebuild for scl

* Tue Jul 30 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-3
- Remove shebang from Rakefile
- Add BR: rubygem(atomic)

* Mon Jul 29 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-2
- Remove JRuby for now

* Fri Jul 26 2013 Josef Stribny <jstribny@redhat.com> - 0.1.2-1
- Update to 0.1.2
- Add JRuby support

* Thu May 09 2013 Josef Stribny <jstribny@redhat.com> - 0.1.0-1
- Initial package
