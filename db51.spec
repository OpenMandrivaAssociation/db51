%define __soversion 5.1
%define _libdb_a libdb-%{__soversion}.a
%define _libcxx_a libdb_cxx-%{__soversion}.a

%define libname_orig %mklibname db
%define libname %{libname_orig}%{__soversion}
%define libnamedev %{libname}-devel
%define libnamestatic %{libname}-static-devel

%define libdbcxx %{libname_orig}cxx%{__soversion}
%define libdbsql %{libname_orig}sql%{__soversion}
%define libdbtcl %{libname_orig}tcl%{__soversion}
%define libdbjava %{libname_orig}java%{__soversion}

%define libdbnss %{libname_orig}nss%{__soversion}
%define libdbnssdev %{libdbnss}-devel

%ifnarch %[mips} %{arm}
%bcond_without java
%define gcj_support 0
%endif

%bcond_without	sql
%bcond_without	tcl
%bcond_without	db1
# Define to build a stripped down version to use for nss libraries
%bcond_without	nss

# Define to rename utilities and allow parallel installation
%bcond_without	parallel

# mutexes defaults to POSIX/pthreads/library
%bcond_with	asmmutex

Summary:	The Berkeley DB database library for C
Name:		db51
Version:	5.1.29
Release:	1
Source0:	http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
# statically link db1 library
Patch0:		db-5.1.19-db185.patch
Patch1:		db-5.1.25-sql_flags.patch
Patch2:		db-5.1.19-tcl-link.patch
# fedora patches
Patch101:	db-4.7.25-jni-include-dir.patch
URL:		https://www.oracle.com/technology/software/products/berkeley-db/
License:	BSD
Group:		System/Libraries
BuildRequires:	systemtap
%if %{with sql}
BuildRequires:	sqlite3-devel
%endif
%if %{with tcl}
BuildRequires:	tcl-devel
%endif
%if %{with db1}
BuildRequires:	db1-devel
%endif
BuildRequires:	ed
BuildRequires:	libtool
%if %{with java}
BuildRequires:	java-rpmbuild
BuildRequires:	sharutils
# required for jni.h
BuildRequires:	libgcj-devel
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%endif
%endif
BuildRoot:	%{_tmppath}/%{name}-%{EVRD}-buildroot

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n %{libname}
Summary:	The Berkeley DB database library for C
Group:		System/Libraries

%description -n	%{libname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n %{libdbcxx}
Summary:	The Berkeley DB database library for C++
Group:		System/Libraries

%description -n	%{libdbcxx}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build C++ programs which use
Berkeley DB.

%if %{with sql}
%package -n %{libdbsql}
Summary:	The Berkeley DB database library for SQL
Group:		System/Libraries

%description -n	%{libdbsql}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build SQL programs which use
Berkeley DB.
%endif

%if %{with java}
%package -n %{libdbjava}
Summary:	The Berkeley DB database library for C++
Group:		System/Libraries
%rename		db%{__soversion}

%description -n	%{libdbjava}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build Java programs which use
Berkeley DB.

%package -n %{libdbjava}-javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description -n %{libdbjava}-javadoc
Javadoc for %{name}.
%endif

%if %{with tcl}
%package -n %{libdbtcl}
Summary:	The Berkeley DB database library for TCL
Group:		System/Libraries

%description -n	%{libdbtcl}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the header files, libraries, and documentation for
building tcl programs which use Berkeley DB.
%endif

%package utils
Summary:	Command line tools for managing Berkeley DB databases
Group:		Databases
%if !%{with parallel}
Conflicts:	db4-utils
Conflicts:	db5-utils < %{__soversion}
Conflicts:	db-utils < %{__soversion}
%endif
Provides:	db5-utils = %{EVRD}
Provides:	db-utils = %{EVRD}
Requires:	%{name}_recover = %{EVRD}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains command line tools for managing Berkeley DB databases.

%package -n %{name}_recover
Summary:	Minimal package with '%{name}_recover' only
Group:		Databases
Provides:	db_recover = %{EVRD}

%description -n	%{name}_recover
This is a minimal package that ships with '%{name}_recover' only as it's
required for using "RPM ACID".

%package -n %{libnamedev}
Summary:	Development libraries/header files for the Berkeley DB library
Group:		Development/Databases
Requires:	%{libname} = %{EVRD}
%if %{with sql}
Requires:	%{libdbsql} = %{EVRD}
%endif
%if %{with tcl}
Requires:	%{libdbtcl} = %{EVRD}
%endif
%if %{with java}
Requires:	%{libdbjava} = %{EVRD}
%endif
Requires:	%{libdbcxx} = %{EVRD}
Provides:	db%{__soversion}-devel = %{EVRD}
Provides:	libdb%{__soversion}-devel = %{EVRD}
Conflicts:	db-devel < %{__soversion}
Conflicts:	db4.8-devel
Conflicts:	db4.7-devel
Conflicts:	db4.6-devel
Conflicts:	db4.5-devel
Conflicts:	db4.4-devel
Conflicts:	db4.3-devel
Conflicts:	db4.2-devel
Provides:	db-devel = %{EVRD}
Provides:	db5-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{libnamedev}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java, Perl and SQL APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%package -n %{libnamestatic}
Summary:	Development static libraries files for the Berkeley DB library
Group:		Development/Databases
Requires:	db%{__soversion}-devel = %{EVRD}
Provides:	db%{__soversion}-static-devel = %{EVRD}
Provides:	libdb%{__soversion}-static-devel = %{EVRD}
Conflicts:	db-static-devel < %{__soversion}
Provides:	db-static-devel = %{EVRD}
Provides:	db5-static-devel = %{EVRD}

%description -n	%{libnamestatic}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the static libraries for building programs which
use Berkeley DB.

%if %{with nss}
%package -n	%{libdbnss}
Summary:	The Berkeley DB database library for NSS modules
Group:		System/Libraries

%description -n	%{libdbnss}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the shared library required by some nss modules
that use Berkeley DB.

%package -n %{libdbnssdev}
Summary:	Development libraries/header files for building nss modules with Berkeley DB
Group:		Development/Databases
Requires:	%{libdbnss} = %{EVRD}
Provides:	libdbnss-devel = %{EVRD}
Provides:	%{_lib}dbnss-devel = %{EVRD}
Provides:	db_nss-devel = %{EVRD}
Provides:	libdb_nss-devel = %{EVRD}
Conflicts:	db_nss-devel < %{__soversion}

%description -n	%{libdbnssdev}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files and libraries for building nss
modules which use Berkeley DB.
%endif

%prep
%setup -q -n db-%{version}

# fix strange attribs
find . -type f -perm 0444 -exec chmod 644 {} \;

rm -r lang/sql/jdbc/doc
%patch0 -p1 -b .db185~
%patch1 -p1 -b .sql_flags~
%patch2 -p1 -b .tcl~

# fedora patches
%patch101 -p1 -b .jni~

pushd dist
libtoolize --copy --force
cat %{_datadir}/aclocal/libtool.m4 >> aclocal.m4
popd

# Remove tags files which we don't need.
find . -name tags | xargs rm -f
# Define a shell function for fixing HREF references in the docs, which
# would otherwise break when we split the docs up into subpackages.
fixup_href() {
    for doc in $@ ; do
	chmod u+w ${doc}
	sed -e 's,="../api_c/,="../../%{name}-devel/api_c/,g' \
	    -e 's,="api_c/,="../%{name}-devel/api_c/,g' \
	    -e 's,="../api_cxx/,="../../%{name}-devel/api_cxx/,g' \
	    -e 's,="api_cxx/,="../%{name}-devel/api_cxx/,g' \
	    -e 's,="../api_tcl/,="../../%{name}-devel/api_tcl/,g' \
	    -e 's,="api_tcl/,="../%{name}-devel/api_tcl/,g' \
	    -e 's,="../java/,="../../%{name}-devel/java/,g' \
	    -e 's,="java/,="../%{name}-devel/java/,g' \
	    -e 's,="../examples_c/,="../../%{name}-devel/examples_c/,g' \
	    -e 's,="examples_c/,="../%{name}-devel/examples_c/,g' \
	    -e 's,="../examples_cxx/,="../../%{name}-devel/examples_cxx/,g' \
	    -e 's,="examples_cxx/,="../%{name}-devel/examples_cxx/,g' \
	    -e 's,="../ref/,="../../%{name}-devel/ref/,g' \
	    -e 's,="ref/,="../%{name}-devel/ref/,g' \
	    -e 's,="../images/,="../../%{name}-devel/images/,g' \
	    -e 's,="images/,="../%{name}-devel/images/,g' \
	    -e 's,="../utility/,="../../%{name}-utils/utility/,g' \
	    -e 's,="utility/,="../%{name}-utils/utility/,g' ${doc} > ${doc}.new
	touch -r ${doc} ${doc}.new
	cat ${doc}.new > ${doc}
	touch -r ${doc}.new ${doc}
	rm -f ${doc}.new
    done
}

set +x	# XXX painful to watch
# Fix all of the HTML files.
fixup_href `find . -name "*.html"`
set -x	# XXX painful to watch

cd dist
./s_config

%build
%ifarch ppc
CFLAGS="$CFLAGS -D_GNU_SOURCE -D_REENTRANT"
%endif
export CFLAGS

%if %{with java}
export CLASSPATH=
export JAVAC=%{javac}
export JAR=%{jar}
export JAVA=%{java}
export JAVACFLAGS="-nowarn"
JAVA_MAKE="JAR=%{jar} JAVAC=%{javac} JAVACFLAGS="-nowarn" JAVA=%{java}"
%endif

pushd build_unix
CONFIGURE_TOP="../dist" \
%configure2_5x	--includedir=%{_includedir}/%{name} \
		--enable-shared --enable-static \
		--enable-dbm \
		--enable-systemtap \
		--enable-o_direct \
%if %{with sql}
		--enable-sql \
%endif
%if %{with db1}
		--enable-compat185 --enable-dump185 \
%endif
%if %{with tcl}
		--enable-tcl --with-tcl=%{_libdir} --enable-test \
%endif
		--enable-cxx \
%if %{with java}
		--enable-java \
%endif
%if %{with asmmutex}
%ifarch %{ix86}
		--disable-posixmutexes --with-mutex=x86/gcc-assembly
%endif
%ifarch x86_64
		--disable-posixmutexes --with-mutex=x86_64/gcc-assembly
%endif
%ifarch alpha
		--disable-posixmutexes --with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
		--disable-posixmutexes --with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
		--disable-posixmutexes --with-mutex=PPC/gcc-assembly
%endif
%ifarch %{sparc}
		--disable-posixmutexes --with-mutex=Sparc/gcc-assembly
%endif
%ifarch %{mips}
		--disable-posixmutexes --with-mutex=MIPS/gcc-assembly
%endif
%ifarch %{arm}
		--disable-posixmutexes --with-mutex=ARM/gcc-assembly
%endif
%else
		--enable-posixmutexes --with-mutex=POSIX/pthreads/library
%endif

%make $JAVA_MAKE
%if %{with java}
pushd ../lang/java
%{javadoc} -d ../sql/jdbc/doc `find . -name '*.java'`
popd
%endif
popd
%if %{with nss}
mkdir build_nss
pushd build_nss
CONFIGURE_TOP="../dist" \
%configure2_5x	--includedir=%{_includedir}/db_nss \
		--enable-shared --disable-static \
		--enable-dbm \
		--enable-systemtap \
		--enable-o_direct \
		--disable-tcl --disable-cxx --disable-java \
		--with-uniquename=_nss \
		--enable-compat185 \
		--disable-cryptography --disable-queue \
		--disable-replication --disable-verify \
%if %{with asmmutex}
%ifarch %{ix86}
		--disable-posixmutexes --with-mutex=x86/gcc-assembly
%endif
%ifarch x86_64
		--disable-posixmutexes --with-mutex=x86_64/gcc-assembly
%endif
%ifarch alpha
		--disable-posixmutexes --with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
		--disable-posixmutexes --with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
		--disable-posixmutexes --with-mutex=PPC/gcc-assembly
%endif
%ifarch %{sparc}
		--disable-posixmutexes --with-mutex=Sparc/gcc-assembly
%endif
%ifarch %{mips}
		--disable-posixmutexes --with-mutex=MIPS/gcc-assembly
%endif
%ifarch %{arm}
		--disable-posixmutexes --with-mutex=ARM/gcc-assembly
%endif
%else
		--enable-posixmutexes --with-mutex=POSIX/pthreads/library
%endif



%make libdb_base=libdb_nss libso_target=libdb_nss-%{__soversion}.la libdir=/%{_lib}
popd
%endif

%install
rm -rf %{buildroot}

make -C build_unix install_setup install_include install_lib install_utilities \
	DESTDIR=%{buildroot} emode=755

%if %{with nss}
make -C build_nss install_include install_lib libdb_base=libdb_nss \
	DESTDIR=%{buildroot} LIB_INSTALL_FILE_LIST=""

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}/%{_libdir}/libdb_nss-%{__soversion}.so %{buildroot}/%{_lib}
ln -s  /%{_lib}/libdb_nss-%{__soversion}.so %{buildroot}%{_libdir}
%endif

ln -sf %{name}/db.h %{buildroot}%{_includedir}/db.h

# XXX This is needed for parallel install with db4.2
%if %{with parallel}
for F in %{buildroot}%{_bindir}/*db_* ; do
   mv $F `echo $F | sed -e 's,db_,%{name}_,'`
done
%endif

# Move db.jar file to the correct place, and version it
%if %{with java}
mkdir -p %{buildroot}%{_jnidir}
mv %{buildroot}%{_libdir}/db.jar %{buildroot}%{_jnidir}/db%{__soversion}-%{version}.jar
(cd %{buildroot}%{_jnidir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/db%{__soversion}-%{version}
%{__cp} -a lang/sql/jdbc/doc/* %{buildroot}%{_javadocdir}/db%{__soversion}-%{version}
%{__ln_s} db%{__soversion}-%{version} %{buildroot}%{_javadocdir}/db%{__soversion}

%if %{gcj_support}
rm -rf aot-compile-rpm
aot-compile-rpm
%endif
%endif

rm -rf %{buildroot}%{_includedir}/db_nss/db_cxx.h

%clean
rm -rf %{buildroot}

%if %{with java}
%post -n %{libdbjava}
%{update_gcjdb}

%postun -n %{libdbjava}
%{clean_gcjdb}
%endif

%files -n %{libname}
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_libdir}/libdb-%{__soversion}.so

%files -n %{libdbcxx}
%defattr(755,root,root) 
%{_libdir}/libdb_cxx-%{__soversion}.so

%if %{with sql}
%files -n %{libdbsql}
%defattr(755,root,root)
%{_libdir}/libdb_sql-%{__soversion}.so
%endif

%if %{with java}
%files -n %{libdbjava}
%defattr(644,root,root,755)
%doc lang/sql/jdbc/doc/*
%doc examples/java/src
%attr(755,root,root) %{_libdir}/libdb_java-%{__soversion}.so
%attr(755,root,root) %{_libdir}/libdb_java-%{__soversion}_g.so
%{_jnidir}/db%{__soversion}.jar
%{_jnidir}/db%{__soversion}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif

%files -n %{libdbjava}-javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/db%{__soversion}-%{version}
%doc %dir %{_javadocdir}/db%{__soversion}
%endif

%if %{with tcl}
%files -n %{libdbtcl}
%defattr(755,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.so
%endif

%files utils
%defattr(-,root,root)
%doc docs/api_reference/C/db_archive.html
%doc docs/api_reference/C/db_checkpoint.html
%doc docs/api_reference/C/db_deadlock.html
%doc docs/api_reference/C/db_dump.html
%doc docs/api_reference/C/db_load.html
%doc docs/api_reference/C/db_printlog.html
%doc docs/api_reference/C/db_replicate.html
%doc docs/api_reference/C/db_stat.html
%doc docs/api_reference/C/db_upgrade.html
%doc docs/api_reference/C/db_verify.html
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_replicate
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify
%if %{with sql}
%doc docs/api_reference/C/dbsql.html
%{_bindir}/dbsql
%endif

%files -n %{name}_recover
%doc docs/api_reference/C/db_recover.html
%{_bindir}/db*_recover

%files -n %{libnamedev}
%defattr(644,root,root,755)
%doc docs/api_reference
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
%if %{with db1}
%{_includedir}/%{name}/db_185.h
%endif
%{_includedir}/%{name}/db_cxx.h
%if %{with sql}
%{_includedir}/%{name}/dbsql.h
%endif
%{_includedir}/db.h
%{_libdir}/libdb.so
%{_libdir}/libdb-5.so
%{_libdir}/libdb-%{__soversion}.la
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-5.so
%{_libdir}/libdb_cxx-%{__soversion}.la
%if %{with sql}
%{_libdir}/libdb_sql.so
%{_libdir}/libdb_sql-5.so
%{_libdir}/libdb_sql-%{__soversion}.la
%endif
%if %{with tcl}
%{_libdir}/libdb_tcl.so
%{_libdir}/libdb_tcl-5.so
%{_libdir}/libdb_tcl-%{__soversion}.la
%endif
%if %{with java}
%{_libdir}/libdb_java.so
%{_libdir}/libdb_java-5.so
%{_libdir}/libdb_java-%{__soversion}.la
%endif

%files -n %{libnamestatic}
%defattr(644,root,root,755)
%{_libdir}/*.a

%if %{with nss}
%files -n %{libdbnss}
%defattr(755,root,root) 
/%{_lib}/libdb_nss-%{__soversion}.so

%files -n %{libdbnssdev}
%defattr(644,root,root,755)
%dir %{_includedir}/db_nss
%{_includedir}/db_nss/db.h
%if %{with db1}
%{_includedir}/db_nss/db_185.h
%endif
%{_libdir}/libdb_nss.so
%{_libdir}/libdb_nss-5.so
%{_libdir}/libdb_nss-%{__soversion}.la
%{_libdir}/libdb_nss-%{__soversion}.so
%endif


%changelog
* Tue Jul 05 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1.25-5
+ Revision: 688891
- drop old workaround for old gcc 4.6 issues, it'll now even break current build
- add conflicts on more specific db-devel provides as older packages lacks
  canonical one.. :|

* Mon Apr 11 2011 Funda Wang <fwang@mandriva.org> 5.1.25-4
+ Revision: 652438
- fix broken symbolic link on libdbjava

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1.25-3
+ Revision: 649243
- don't disable optimizations on %%{i86}

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1.25-2
+ Revision: 649208
- hastily disable compiler optimizations for %%{ix86} while debugging

* Wed Mar 30 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1.25-1
+ Revision: 649104
- add buildrequires on libgcj-devel
- disable gcj_support
- work around gcc 4.6.0 optimizations that breaks stuff with rpm at least...
- rename db5.1 package to libdbjava5.1
- new version
- enable systemtap per jbj request

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added missing buildrequires for systemtap

* Mon Nov 29 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1.19-5mdv2011.0
+ Revision: 603124
- ship with documentation for utils with them (man page conversion would be nice)
- Enable the O_DIRECT flag for direct I/O.

* Thu Nov 04 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.19-4mdv2011.0
+ Revision: 593334
- rebuild

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - force enabling dbm, otherwise it won't be enabled for some reason with db_nss

* Sun Oct 31 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1.19-3mdv2011.0
+ Revision: 591222
- provide %%{name}-devel
- build nss libs also with posix mutexes
- rename '%%{name}-recover' sub-package to '%%{name}_recover'
- split out db*_recover into a separate sub-package for rpm to require

* Fri Oct 15 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1.19-2mdv2011.0
+ Revision: 585735
- enable build of sql
- fix and do parallel install by default

* Thu Oct 14 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 5.1.19-1mdv2011.0
+ Revision: 585727
- cleanups (wouldn't hurt from aother round of cleanups in addition though...)
- new release: 5.1.20
- imported package db50

