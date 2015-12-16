# Generated from thread_safe-0.1.0.gem by gem2rpm -*- rpm-spec -*-
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}

%global gem_name thread_safe

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.1.3
Release: 2%{?dist}
Summary: Thread-safe collections and utilities for Ruby
Group: Development/Languages
License: ASL 2.0
URL: https://github.com/headius/thread_safe
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(atomic)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(atomic)
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
Documentation for %{pkg_name}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

# No inclusion of pre-built binaries or libraries
# http://fedoraproject.org/wiki/Packaging:Guidelines
rm ./lib/thread_safe/jruby_cache_backend.jar
sed -i 's\, "lib/thread_safe/jruby_cache_backend.jar"\\' %{gem_name}.gemspec

# Remove shebang from non-executable Rakefile
sed -i '1d' Rakefile

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
testrb -Ilib test/test_{array,cache,helper,synchronized_delegator}.rb
%{?scl:EOF}

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/ext

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/examples
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/test



%changelog
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
