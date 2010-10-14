# compatibility with legacy rpm
%{!?_lib:%define _lib	lib}

%define	__soversion	5.0
%define	_libdb_a	libdb-%{__soversion}.a
%define	_libcxx_a	libdb_cxx-%{__soversion}.a

%define libname_orig	%mklibname db
%define libname		%{libname_orig}%{__soversion}
%define libnamedev	%{libname}-devel
%define libnamestatic	%{libname}-static-devel

%define libdbcxx	%{libname_orig}cxx%{__soversion}
%define libdbtcl	%{libname_orig}tcl%{__soversion}
%define libdbjava	db%{__soversion}

%define libdbnss	%{libname_orig}nss%{__soversion}
%define libdbnssdev	%{libdbnss}-devel

# Define Mandriva Linux version we are building for
%{?!mdkversion:%define mdkversion	%(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandriva-release)}

%ifnarch %mips %arm
%bcond_without java
%define gcj_support 1
%endif

# Define to build a stripped down version to use for nss libraries
%define build_nss	1

# Allow --with[out] nss rpm command line build
%{?_with_nss: %{expand: %%define build_nss 1}}
%{?_without_nss: %{expand: %%define build_nss 0}}

# Define to rename utilities and allow parallel installation
%define build_parallel	0

# Allow --with[out] parallel rpm command line build
%{?_with_parallel: %{expand: %%define build_parallel 1}}
%{?_without_parallel: %{expand: %%define build_parallel 0}}

# mutexes defaults to POSIX/pthreads/library
%define build_asmmutex 0

%{?_with_asmmutex: %global build_asmmutex 1}
%{?_without_asmmutex: %global build_asmmutex 0}

Summary:	The Berkeley DB database library for C
Name:		db50
Version:	5.0.21
Release:	%mkrel 1
Source0:	http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
# statically link db1 library
Patch0:		db-5.0.21-db185.patch
Patch1:		db-4.7.25-fix-format-errors.patch
Patch2:		db-5.0.21-tcl-link.patch
# fedora patches
Patch101:	db-4.7.25-jni-include-dir.patch
URL:		http://www.oracle.com/technology/software/products/berkeley-db/
License:	BSD
Group:		System/Libraries
BuildRequires:	%{!?_without_tcl:tcl-devel} %{!?_without_db1:db1-devel} ed libtool
%if %with java
BuildRequires:	java-rpmbuild
BuildRequires:	sharutils
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%endif
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n	%{libname}
Summary:	The Berkeley DB database library for C
Group:		System/Libraries

%description -n	%{libname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n	%{libdbcxx}
Summary:	The Berkeley DB database library for C++
Group:		System/Libraries

%description -n	%{libdbcxx}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build C++ programs which use
Berkeley DB.

%if %with java
%package -n	%{libdbjava}
Summary:	The Berkeley DB database library for C++
Group:		System/Libraries

%description -n	%{libdbjava}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build Java programs which use
Berkeley DB.

%package -n	%{libdbjava}-javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description -n %{libdbjava}-javadoc
Javadoc for %{name}.
%endif

%if %{!?_without_tcl:1}%{?_without_tcl:0}
%package -n	%{libdbtcl}
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

%package	utils
Summary:	Command line tools for managing Berkeley DB databases
Group:		Databases
%if !%{build_parallel}
Conflicts:	db3-utils
Conflicts:	db46-utils
Conflicts:	db47-utils
%endif
Provides:	db5-utils = %{version}-%{release}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains command line tools for managing Berkeley DB databases.

%package -n	%{libnamedev}
Summary:	Development libraries/header files for the Berkeley DB library
Group:		Development/Databases
Requires:	%{libname} = %{version}-%{release}
%if %{!?_without_tcl:1}%{?_without_tcl:0}
Requires:	%{libdbtcl} = %{version}-%{release}
%endif
Requires:	%{libdbcxx} = %{version}-%{release}
Provides:	db%{__soversion}-devel = %{version}-%{release}
Provides:	libdb%{__soversion}-devel = %{version}-%{release}
Conflicts:	db-devel < %{__soversion}
Provides:	db-devel = %{version}-%{release}
Provides:	db5-devel = %{version}-%{release}

%description -n	%{libnamedev}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%package -n	%{libnamestatic}
Summary:	Development static libraries files for the Berkeley DB library
Group:		Development/Databases
Requires:	db%{__soversion}-devel = %{version}-%{release}
Provides:	db%{__soversion}-static-devel = %{version}-%{release}
Provides:	libdb%{__soversion}-static-devel = %{version}-%{release}
Conflicts:	db-static-devel < %{__soversion}
Provides:	db-static-devel = %{version}-%{release}
Provides:	db5-static-devel = %{version}-%{release}

%description -n	%{libnamestatic}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the static libraries for building programs which
use Berkeley DB.

%if %{build_nss}
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

%package -n	%{libdbnssdev}
Summary:	Development libraries/header files for building nss modules with Berkeley DB
Group:		Development/Databases
Requires:	%{libdbnss} = %{version}-%{release}
Provides:	libdbnss-devel = %{version}-%{release}
Provides:	%{_lib}dbnss-devel = %{version}-%{release}
Provides:	db_nss-devel = %{version}-%{release}
Provides:	libdb_nss-devel = %{version}-%{release}
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

%{__rm} -r docs/java
%patch0 -p1 -b .db185~
%patch1 -p1 -b .format~
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
	sed -e 's,="../api_c/,="../../%{name}-devel-%{version}/api_c/,g' \
	    -e 's,="api_c/,="../%{name}-devel-%{version}/api_c/,g' \
	    -e 's,="../api_cxx/,="../../%{name}-devel-%{version}/api_cxx/,g' \
	    -e 's,="api_cxx/,="../%{name}-devel-%{version}/api_cxx/,g' \
	    -e 's,="../api_tcl/,="../../%{name}-devel-%{version}/api_tcl/,g' \
	    -e 's,="api_tcl/,="../%{name}-devel-%{version}/api_tcl/,g' \
	    -e 's,="../java/,="../../%{name}-devel-%{version}/java/,g' \
	    -e 's,="java/,="../%{name}-devel-%{version}/java/,g' \
	    -e 's,="../examples_c/,="../../%{name}-devel-%{version}/examples_c/,g' \
	    -e 's,="examples_c/,="../%{name}-devel-%{version}/examples_c/,g' \
	    -e 's,="../examples_cxx/,="../../%{name}-devel-%{version}/examples_cxx/,g' \
	    -e 's,="examples_cxx/,="../%{name}-devel-%{version}/examples_cxx/,g' \
	    -e 's,="../ref/,="../../%{name}-devel-%{version}/ref/,g' \
	    -e 's,="ref/,="../%{name}-devel-%{version}/ref/,g' \
	    -e 's,="../images/,="../../%{name}-devel-%{version}/images/,g' \
	    -e 's,="images/,="../%{name}-devel-%{version}/images/,g' \
	    -e 's,="../utility/,="../../%{name}-utils-%{version}/utility/,g' \
	    -e 's,="utility/,="../%{name}-utils-%{version}/utility/,g' ${doc} > ${doc}.new
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
CFLAGS="$RPM_OPT_FLAGS"
%ifarch ppc
CFLAGS="$CFLAGS -D_GNU_SOURCE -D_REENTRANT"
%endif
export CFLAGS

%if %with java
export CLASSPATH=
export JAVAC=%{javac}
export JAR=%{jar}
export JAVA=%{java}
export JAVACFLAGS="-nowarn"
JAVA_MAKE="JAR=%{jar} JAVAC=%{javac} JAVACFLAGS="-nowarn" JAVA=%{java}"
%endif

pushd build_unix
CONFIGURE_TOP="../dist" %configure2_5x \
	--enable-shared --enable-static \
%if %{?!_without_db1:1}%{?_without_db1:0}
	--enable-compat185 --enable-dump185 \
%endif
%if %{?!_without_tcl:1}%{?_without_tcl:0}
	--enable-tcl --with-tcl=%{_libdir} --enable-test \
%endif
	--enable-cxx \
%if %with java
	--enable-java \
%endif
%if %{build_asmmutex}
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
%ifarch %{sunsparc}
	--disable-posixmutexes --with-mutex=Sparc/gcc-assembly
%endif
%ifarch %mips
	--disable-posixmutexes --with-mutex=MIPS/gcc-assembly
%endif
%ifarch %arm
	--disable-posixmutexes --with-mutex=ARM/gcc-assembly
%endif
%else
	--with-mutex=POSIX/pthreads/library
%endif

%make $JAVA_MAKE
%if %with java
pushd ../java
%{javadoc} -d ../docs/java `%{_bindir}/find . -name '*.java'`
popd
%endif
popd
%if %{build_nss}
mkdir build_nss
pushd build_nss
CONFIGURE_TOP="../dist" %configure2_5x \
	--enable-shared --disable-static \
	--disable-tcl --disable-cxx --disable-java \
	--with-uniquename=_nss \
	--enable-compat185 \
	--disable-cryptography --disable-queue \
	--disable-replication --disable-verify \
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
%ifarch %{sunsparc}
	--disable-posixmutexes --with-mutex=Sparc/gcc-assembly
%endif
%ifarch %mips
	--disable-posixmutexes --with-mutex=MIPS/gcc-assembly
%endif
%ifarch %arm
	--disable-posixmutexes --with-mutex=ARM/gcc-assembly
%endif

%make libdb_base=libdb_nss libso_target=libdb_nss-%{__soversion}.la libdir=/%{_lib}
popd
%endif

%install
rm -rf %{buildroot}

make -C build_unix install_setup install_include install_lib install_utilities \
	DESTDIR=%{buildroot} includedir=%{_includedir}/db4 \
	emode=755

%if %{build_nss}
make -C build_nss install_include install_lib libdb_base=libdb_nss \
	DESTDIR=%{buildroot} includedir=%{_includedir}/db_nss \
	LIB_INSTALL_FILE_LIST=""

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}/%{_libdir}/libdb_nss-%{__soversion}.so %{buildroot}/%{_lib}
ln -s  /%{_lib}/libdb_nss-%{__soversion}.so %{buildroot}%{_libdir}
%endif

ln -sf db4/db.h %{buildroot}%{_includedir}/db.h

# XXX This is needed for parallel install with db4.2
%if %{build_parallel}
for F in %{buildroot}%{_bindir}/*db_* ; do
   mv $F `echo $F | sed -e 's,db_,%{name}_,'`
done
%endif

# Move db.jar file to the correct place, and version it
%if %with java
mkdir -p %{buildroot}%{_jnidir}
mv %{buildroot}%{_libdir}/db.jar %{buildroot}%{_jnidir}/db%{__soversion}-%{version}.jar
(cd %{buildroot}%{_jnidir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/db%{__soversion}-%{version}
%{__cp} -a docs/java/* %{buildroot}%{_javadocdir}/db%{__soversion}-%{version}
%{__ln_s} db%{__soversion}-%{version} %{buildroot}%{_javadocdir}/db%{__soversion}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif
%endif

#symlink the short libdb???.a name
ln -sf %{_libdb_a} %{buildroot}%{_libdir}/libdb.a
ln -sf %{_libcxx_a} %{buildroot}%{_libdir}/libdb_cxx.a
ln -sf libdb_tcl-%{__soversion}.a %{buildroot}%{_libdir}/libdb_tcl.a
ln -sf %{_libdb_a} %{buildroot}%{_libdir}/libdb-5.a
ln -sf %{_libcxx_a} %{buildroot}%{_libdir}/libdb_cxx-5.a
ln -sf libdb_tcl-%{__soversion}.a %{buildroot}%{_libdir}/libdb_tcl-5.a
%if %with java
ln -sf libdb_java-%{__soversion}.a %{buildroot}%{_libdir}/libdb_java.a
ln -sf libdb_java-%{__soversion}.a %{buildroot}%{_libdir}/libdb_java-5.a
%endif

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libdbcxx} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libdbcxx} -p /sbin/ldconfig
%endif

%if %with java
%post -n %{libdbjava}
%{update_gcjdb}

%postun -n %{libdbjava}
%{clean_gcjdb}
%endif

%if %{?!_without_tcl:1}%{?_without_tcl:0} 
%if %mdkversion < 200900
%post -n %{libdbtcl} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libdbtcl} -p /sbin/ldconfig
%endif
%endif

%if %{build_nss}
%if %mdkversion < 200900
%post -n %{libdbnss} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libdbnss} -p /sbin/ldconfig
%endif
%endif

%files -n %{libname}
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_libdir}/libdb-%{__soversion}.so

%files -n %{libdbcxx}
%defattr(755,root,root) 
%{_libdir}/libdb_cxx-%{__soversion}.so

%if %with java
%files -n %{libdbjava}
%defattr(644,root,root,755)
%doc docs/java
%doc examples_java
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

%if %{?!_without_tcl:1}%{?_without_tcl:0} 
%files -n %{libdbtcl}
%defattr(755,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.so
%endif

%files utils
%defattr(-,root,root)
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
#%%{_bindir}/db*_sql
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify

%files -n %{libnamedev}
%defattr(644,root,root,755)
%doc docs/api_reference
%dir %{_includedir}/db4
%{_includedir}/db4/db.h
%if %{?!_without_db1:1}%{?_without_db1:0} 
%{_includedir}/db4/db_185.h
%endif
%{_includedir}/db4/db_cxx.h
%{_includedir}/db.h
%{_libdir}/libdb.so
%{_libdir}/libdb-5.so
%{_libdir}/libdb-%{__soversion}.la
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-5.so
%{_libdir}/libdb_cxx-%{__soversion}.la
%if %{?!_without_tcl:1}%{?_without_tcl:0} 
%{_libdir}/libdb_tcl.so
%{_libdir}/libdb_tcl-5.so
%{_libdir}/libdb_tcl-%{__soversion}.la
%endif
%if %with java
%{_libdir}/libdb_java.so
%{_libdir}/libdb_java-5.so
%{_libdir}/libdb_java-%{__soversion}.la
%endif

%files -n %{libnamestatic}
%defattr(644,root,root,755)
%{_libdir}/*.a

%if %{build_nss}
%files -n %{libdbnss}
%defattr(755,root,root) 
/%{_lib}/libdb_nss-%{__soversion}.so

%files -n %{libdbnssdev}
%defattr(644,root,root,755)
%dir %{_includedir}/db_nss
%{_includedir}/db_nss/db.h
%if %{?!_without_db1:1}%{?_without_db1:0} 
%{_includedir}/db_nss/db_185.h
%endif
%exclude %{_includedir}/db_nss/db_cxx.h
%{_libdir}/libdb_nss.so
%{_libdir}/libdb_nss-5.so
%{_libdir}/libdb_nss-%{__soversion}.la
%{_libdir}/libdb_nss-%{__soversion}.so
%endif



