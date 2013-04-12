
%{!?lsb_release: %global lsb_release %(lsb_release -r | awk {' print $2 '})}
%global rhel_point_release %(echo %{lsb_release} | awk -F . {' print $2 '})

%global contentdir /var/www
# API/ABI Check
%global apiver 20090626
%global zendver 20090626
%global pdover 20080721
# Extension version
%global fileinfover 1.0.5-dev
%global pharver     2.0.1
%global zipver      1.11.0
%global jsonver     1.2.1

%global httpd_mmn %(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%define mysql_config %{_libdir}/mysql/mysql_config

# enabled optional build options
%global _with_milter        1
%global _with_embedded  	1
%global _with_zts       	1
%global _with_litespeed     1

# disabled optional build options
# %%define _with_oci8        1
# %%define _with_interbase   1

# fpm requires a later version of libevent
%if (0%{?rhel} >= 5 && 0%{?rhel_point_release} >= 5)
%global _with_fpm       1
%endif

# fpm should be enabled on EL6
%if (0%{?rhel} >= 6)
%global _with_fpm       1
%endif

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest: %{expand: %%global runselftest 1}}

%if 0%{?_with_oci8}
%global instantclient_ver 10.2.0.3
%endif

%global real_name php
%global name php53u
%global base_ver 5.3

Summary: The PHP HTML-embedded scripting language. (PHP: Hypertext Preprocessor)
Name: %{name}
Version: 5.3.24
Release: 1.ius%{?dist}
License: The PHP License v3.01
Group: Development/Languages
Vendor: IUS Community Project 
URL: http://www.php.net/

Source0: http://www.php.net/distributions/%{real_name}-%{version}.tar.bz2
Source1: php.conf
Source2: php53-ius.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.init
Source7: php-fpm.logrotate

# Ported from Fedora/Redhat
# Build fixes
Patch1: php-5.3.3-gnusrc.patch
Patch2: php-5.3.0-install.patch
Patch3: php-5.2.4-norpath.patch
Patch4: php-5.3.0-phpize64.patch
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
#Patch8: php-5.3.3-aconf26x.patch
Patch9: php-5.3.14-aconf259.patch
Patch10: php-5.3.14-autoconf-milter.patch

# Fixes for extension modules
Patch20: php-4.3.11-shutdown.patch
Patch21: php-5.3.3-macropen.patch

# Functional changes
Patch40: php-5.0.4-dlopen.patch
Patch41: php-5.3.0-easter.patch
Patch42: php-5.3.1-systzdata-v7.patch

# Security patch from upstream SVN
# http://svn.php.net/viewvc?view=revision&revision=306154
#Patch50: php-5.3.4-bug53512.patch

# Fixes for tests
Patch61: php-5.0.4-tests-wddx.patch

# IUS Patches
Patch302: php-5.3.0-oci8-lib64.patch
#Patch316: php-5.3.4-bug53632.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9, db4-devel, expat-devel
BuildRequires: gmp-devel, aspell-devel >= 0.50.0
BuildRequires: httpd-devel >= 2.0.46-1, libjpeg-devel, libpng-devel, pam-devel
BuildRequires: libstdc++-devel, openssl-devel, sqlite-devel >= 3.0.0
BuildRequires: zlib, zlib-devel, smtpdaemon, libedit-devel
BuildRequires: bzip2, fileutils, file >= 3.39, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: apr-devel, elfutils-libelf-devel, apr-util-devel
BuildRequires: t1lib-devel
BuildRequires: libtool-ltdl-devel, e2fsprogs-devel
BuildRequires: redhat-lsb

%if 0%{?_with_milter}
BuildRequires: sendmail-devel
%endif

# Enforce Apache module ABI compatibility
Requires: httpd-mmn = %{httpd_mmn} 
Requires: file >= 3.39
Requires: libxslt >= 1.1.11 
Requires: %{name}-common = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: %{name}-cli = %{version}-%{release}
#Requires: %{name}-pear >= 1:1.8
Requires: t1lib
Requires: libtool-ltdl
Requires: libedit

Provides: mod_php = %{version}-%{release}
Provides: mod_%{name} = %{version}-%{release}
Provides: %{real_name} = %{version}-%{release}
Provides: php53 = %{version}-%{release}

Conflicts: %{real_name} < %{base_ver}
Conflicts: php51, php52

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 

The php package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-cli = %{version}-%{release}
Provides: php53-cli = %{version}-%{release}
Provides: %{name}-cgi = %{version}-%{release}, %{real_name}-cgi = %{version}-%{release}
Provides: php53-cgi = %{version}-%{release}
Provides: %{name}-pcntl, %{name}-readline, %{name}-pcntl 
Provides: php53-pcntl, php53-readline, php53-pcntl 


%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, /usr/bin/php, and the CGI interface.

%package common
Group: Development/Languages
Summary: Common files for PHP
Provides: %{real_name}-common = %{version}-%{release}
Provides: php53-common = %{version}-%{release}
Provides: %{name}-api = %{apiver}, %{name}-zend-abi = %{zendver}
Provides: %{real_name}-api = %{apiver}, %{real_name}-zend-abi = %{zendver}
Provides: php53-api = %{apiver}, php53-zend-abi = %{zendver}
Provides: %{name}(api) = %{apiver}, %{name}(zend-abi) = %{zendver}
Provides: %{real_name}(api) = %{apiver}, %{real_name}(zend-abi) = %{zendver}
Provides: php53(api) = %{apiver}, php53(zend-abi) = %{zendver}

# Provides for all builtin modules for php5x:
Provides: %{name}-bz2, %{name}-calendar, %{name}-ctype, %{name}-curl
Provides: %{name}-date, %{name}-exif, %{name}-ftp, %{name}-gettext
Provides: %{name}-gmp, %{name}-hash, %{name}-iconv, %{name}-libxml
Provides: %{name}-openssl, %{name}-pcre, %{name}-posix
Provides: %{name}-reflection, %{name}-session, %{name}-shmop 
Provides: %{name}-simplexml, %{name}-sockets, %{name}-spl, %{name}-sysvsem
Provides: %{name}-sysvshm, %{name}-sysvmsg, %{name}-tokenizer, %{name}-wddx
Provides: %{name}-zlib, %{name}-json, %{name}-zip
Provides: %{name}-sqlite3

# add for php
Provides: %{real_name}-bz2, %{real_name}-calendar, %{real_name}-ctype
Provides: %{real_name}-curl, %{real_name}-date, %{real_name}-exif 
Provides: %{real_name}-ftp, %{real_name}-gettext, %{real_name}-gmp
Provides: %{real_name}-hash, %{real_name}-iconv, %{real_name}-libxml
Provides: %{real_name}-openssl, %{real_name}-pcre, 
Provides: %{real_name}-posix, %{real_name}-reflection
Provides: %{real_name}-session, %{real_name}-shmop, %{real_name}-simplexml
Provides: %{real_name}-sockets, %{real_name}-spl, %{real_name}-sysvsem
Provides: %{real_name}-sysvshm, %{real_name}-sysvmsg, %{real_name}-tokenizer
Provides: %{real_name}-wddx, %{real_name}-zlib, %{real_name}-json
Provides: %{real_name}-zip
Provides: %{real_name}-sqlite3

# add for packages expecting php53 from RHEL
Provides: php53-bz2, php53-calendar, php53-ctype
Provides: php53-curl, php53-date, php53-exif
Provides: php53-ftp, php53-gettext, php53-gmp
Provides: php53-hash, php53-iconv, php53-libxml
Provides: php53-openssl, php53-pcre,
Provides: php53-posix, php53-reflection
Provides: php53-session, php53-shmop, php53-simplexml
Provides: php53-sockets, php53-spl, php53-sysvsem
Provides: php53-sysvshm, php53-sysvmsg, php53-tokenizer
Provides: php53-wddx, php53-zlib, php53-json
Provides: php53-zip
Provides: php53-sqlite3

Obsoletes: %{name}-pecl-zip, %{name}-pecl-json, %{name}-json, %{name}-pecl-phar, %{name}-pecl-Fileinfo

# For obsoleted pecl extension - php and php5x
Provides: %{name}-pecl-json = %{jsonver}, %{name}-pecl(json) = %{jsonver}
Provides: %{name}-pecl-zip = %{zipver}, %{name}-pecl(zip) = %{zipver}
Provides: %{name}-pecl-phar = %{pharver}, %{name}-pecl(phar) = %{pharver}
Provides: %{name}-pecl-Fileinfo = %{fileinfover}, %{name}-pecl(Fileinfo) = %{fileinfover}

Provides: %{real_name}-pecl-json = %{jsonver}, %{real_name}-pecl(json) = %{jsonver}
Provides: %{real_name}-pecl-zip = %{zipver}, %{real_name}-pecl(zip) = %{zipver}
Provides: %{real_name}-pecl-phar = %{pharver}, %{real_name}-pecl(phar) = %{pharver}
Provides: %{real_name}-pecl-Fileinfo = %{fileinfover}, %{real_name}-pecl(Fileinfo) = %{fileinfover}

Provides: php53-pecl-json = %{jsonver}, php53-pecl(json) = %{jsonver}
Provides: php53-pecl-zip = %{zipver}, php53-pecl(zip) = %{zipver}
Provides: php53-pecl-phar = %{pharver}, php53-pecl(phar) = %{pharver}
Provides: php53-pecl-Fileinfo = %{fileinfover}, php53-pecl(Fileinfo) = %{fileinfover}

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions.

Requires: %{name} = %{version}-%{release}, autoconf, automake
Provides: %{real_name}-devel = %{version}-%{release}
Provides: php53-devel = %{version}-%{release}

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package imap
Summary: A module for PHP applications that use IMAP.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-imap = %{version}-%{release}
Provides: php53-imap = %{version}-%{release}
BuildRequires: krb5-devel, openssl-devel
BuildRequires: libc-client-devel

%description imap
The php-imap package contains a dynamic shared object (DSO) for the
Apache Web server. When compiled into Apache, the php-imap module will
add IMAP (Internet Message Access Protocol) support to PHP. IMAP is a
protocol for retrieving and uploading e-mail messages on mail
servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package
and the php package.

%package ldap
Summary: A module for PHP applications that use LDAP.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-ldap = %{version}-%{release}
Provides: php53-ldap = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap package is a dynamic shared object (DSO) for the Apache
Web server that adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language. If you need LDAP support for PHP applications, you will
need to install this package in addition to the php package.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-pdo = %{version}-%{release}
Provides: php53-pdo = %{version}-%{release}
Provides: %{name}-pdo-abi = %{pdover}
Provides: %{real_name}-pdo-abi = %{pdover}
Provides: %{real_name}-pdo_sqlite = %{pdover}
Provides: php53-pdo-abi = %{pdover}
Provides: php53-pdo_sqlite = %{pdover}

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other 
databases.

%package mysql
Summary: A module for PHP applications that use MySQL databases.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, %{name}-pdo
Provides: %{real_name}-mysql = %{version}-%{release}
Provides: php53-mysql = %{version}-%{release}
Provides: php_database, %{name}-mysqli, %{real_name}-mysqli
Provides: php53-mysqli
BuildRequires: mysql-devel >= 5.0.45

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

%package pgsql
Summary: A PostgreSQL database module for PHP.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, %{name}-pdo
Provides: %{real_name}-pgsql = %{version}-%{release}
Provides: php53-pgsql = %{version}-%{release}
Provides: php_database
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The php-pgsql package includes a dynamic shared object (DSO) that can
be compiled in to the Apache Web server to add PostgreSQL database
support to PHP. PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package odbc
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, %{name}-pdo
Provides: %{real_name}-odbc = %{version}-%{release}
Provides: php53-odbc = %{version}-%{release}
Summary: A module for PHP applications that use ODBC databases.
Provides: php_database
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, libxml2 >= 2.6.16
Provides: %{real_name}-soap = %{version}-%{release}
Provides: php53-soap = %{version}-%{release}
Summary: A module for PHP applications that use the SOAP protocol
BuildRequires: libxml2-devel >= 2.6.16

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, net-snmp >= 5.1
Provides: %{real_name}-snmp = %{version}-%{release}
Provides: php53-snmp = %{version}-%{release}
BuildRequires: net-snmp-devel >= 5.1

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, libxml2 >= 2.6.16, 
Requires: libxslt >= 1.1.11
Provides: %{real_name}-xml = %{version}-%{release}
Provides: php53-xml = %{version}-%{release}
Provides: %{name}-dom, %{name}-xsl, %{name}-domxml
Provides: %{real_name}-dom, %{real_name}-xsl, %{real_name}-domxml
Provides: php53-dom, php53-xsl, php53-domxml
BuildRequires: libxslt-devel >= 1.1.11, libxml2-devel >= 2.6.16

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Requires: php53-common = %{version}-%{release}
Provides: %{name}-xmlrpc = %{version}-%{release}
BuildRequires: expat-devel

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-mbstring = %{version}-%{release}
Provides: php53-mbstring = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-gd = %{version}-%{release}
Provides: php53-gd = %{version}-%{release}
BuildRequires: gd-devel, freetype-devel

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

This package is built against t1lib adding Postscript Type 1 font support 
to PHP/GD.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-bcmath = %{version}-%{release}
Provides: php53-bcmath = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-dba = %{version}-%{release}
Provides: php53-dba = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%if 0%{?_with_litespeed:1}
%package litespeed
Summary: API for the Litespeed web server
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-litespeed = %{version}-%{release}
Provides: php53-litespeed = %{version}-%{release}

%description litespeed
The php-litespeed package contains the binary used by the Litespeed web server.
%endif

%package tidy
Summary: Utility to clean up and pretty print HTML/XHTML/XML
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-tidy = %{version}-%{release}
Provides: php53-tidy = %{version}-%{release}
Requires: libtidy
BuildRequires: libtidy, libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using libtidy to PHP.

%package mcrypt
Summary: A module for PHP applications that use Mcrypt.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, libmcrypt
Provides: %{real_name}-mcrypt = %{version}-%{release}
Provides: php53-mcrypt = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The php-mcrypt package is a dynamic shared object (DSO) for the Apache
Web server that adds Mcrypt support to PHP.

%package mssql
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}, freetds >= 0.64
Requires: %{name}-pdo = %{version}-%{release}
Provides: %{real_name}-mssql = %{version}-%{release}
Provides: php53-mssql = %{version}-%{release}
Summary: A module for PHP applications that use MSSQL databases.
Provides: %{name}_database
BuildRequires: freetds-devel >= 0.64

%description mssql
The mssql package contains a dynamic shared object that will add
support for accessing MSSQL databases to PHP.

%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-pspell = %{version}-%{release}
Provides: php53-pspell = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-recode = %{version}-%{release}
Provides: php53-recode = %{version}-%{release}
Requires: recode
BuildRequires: recode-devel

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-intl = %{version}-%{release}
Provides: php53-intl = %{version}-%{release}
BuildRequires: libicu-devel >= 3.6

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Human Language and Character Encoding Support
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-enchant = %{version}-%{release}
Provides: php53-enchant = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The php-intl package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-process = %{version}-%{release}
Provides: php53-process = %{version}-%{release}
Provides: %{name}-posix, %{name}-sysvsem, %{name}-sysvshm, %{name}-sysvmsg
Provides: %{real_name}-posix, %{real_name}-sysvsem, %{real_name}-sysvshm, %{real_name}-sysvmsg
Provides: php53-posix, php53-sysvsem, php53-sysvshm, php53-sysvmsg

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

# Optional module support

%if 0%{?_with_fpm}
%package fpm
Summary: Alternative PHP FastCGI implementation
Group: Development/Languages
Provides: %{real_name}-fpm = %{version}-%{release}
Provides: php53-fpm = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
BuildRequires: libevent-devel >= 1.4.11

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI 
implementation with some additional features useful for sites 
of any size, especially busier sites.

%endif

%if 0%{?_with_milter}
%package milter
Group: Development/Languages
Summary: Milter SAPI interface for PHP
Requires: %{name}-common = %{version}-%{release}
Provides: php53-miter = %{version}-%{release}
Provides: %{real_name}-milter = %{version}-%{release}
BuildRequires: sendmail-devel

%description milter
The php-milter package contains the milter SAPI interface,
which can be used to write milter plugins using PHP.
%endif

%if 0%{?_with_embedded}
%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: %{name}-embedded-devel = %{version}-%{release}
Provides: %{real_name}-embedded = %{version}-%{release}
Provides: php53-embedded = %{version}-%{release}
Provides: %{real_name}-embedded-devel = %{version}-%{release}
Provides: php53-embedded-devel = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.
%endif

%if 0%{?_with_interbase}
%package interbase
Summary:        A module for PHP applications that use Interbase/Firebird databases
Group:          Development/Languages
BuildRequires:  firebird-devel
Requires:       %{name}-common = %{version}-%{release}, %{name}-pdo
Provides:       %{name}_database, %{name}-firebird, %{name}-pdo_firebird
Provides:       %{real_name}_database, %{real_name}-firebird, %{real_name}-pdo_firebird
Provides:       php53_database, php53-firebird, php53-pdo_firebird

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.
%endif

%if 0%{?_with_oci8}
%package oci8
Summary: A module for PHP applications that connect to Oracle.
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-oci8 = %{version}-%{release}
Provides: php53-oci8 = %{version}-%{release}
Requires: oracle-instantclient-basic >= %{instantclient_ver}
BuildRequires: oracle-instantclient-basic >= %{instantclient_ver}
BuildRequires: oracle-instantclient-devel >= %{instantclient_ver}

%description oci8 
The php-oci8 package is a dynamic shared object (DSO) for the Apache
Web server that adds Oracle support to PHP.
%endif

%if 0%{?_with_zts:1}
%package zts
Group: Development/Languages
Summary: Thread-safe PHP interpreter for use with the Apache HTTP Server
Requires: %{name}-common = %{version}-%{release}
Provides: %{real_name}-zts = %{version}-%{release}
Provides: php53-zts = %{version}-%{release}
Requires: httpd-mmn = %{httpd_mmn}
BuildRequires: libtool-ltdl-devel

%description zts
The php-zts package contains a module for use with the Apache HTTP
Server which can operate under a threaded server processing model.
%endif


%prep
%setup -q -n %{real_name}-%{version} 


%patch1 -p1 -F-1 -b .gnusrc
%patch2 -p1 -F-1 -b .install
%patch3 -p1 -F-1 -b .norpath
%patch4 -p1 -F-1 -b .phpize64
%patch5 -p1 -F-1 -b .includedir
%patch6 -p1 -F-1 -b .embed
%patch7 -p1 -F-1 -b .recode
%patch9 -p1 -F-1 -b .aconf259
%patch10 -p1 -F-1 -b .milter

%patch20 -p1 -F-1 -b .shutdown
%patch21 -p1 -F-1 -b .macropen

%patch40 -p1 -F-1 -b .dlopen
%patch41 -p1 -F-1 -b .easter
%patch42 -p1 -F-1 -b .systzdata

#%patch50 -p4 -b .bug53512
%patch61 -p1 -F-1 -b .tests-wddx

%patch302 -p1 -F-1 -b .oci8-lib64
#%patch316 -p1 -b .bug53632

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/gd/libgd/README gd_README
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT

# Multiple builds for multiple SAPIs 
mkdir build-cgi build-apache build-milter build-embedded build-zts build-litespeed 
%if 0%{?_with_fpm}
mkdir build-fpm
%endif

# Remove bogus test; position of read position after fopen(, "a+")
# is not defined by C standard, so don't presume anything.
rm -f ext/standard/tests/file/bug21131.phpt

# Tests that fail.
rm -f ext/standard/tests/file/bug22414.phpt \
      ext/iconv/tests/bug16069.phpt

# Safety check for API version change.
vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

# Check for some extension version
ver=$(sed -n '/#define PHP_FILEINFO_VERSION /{s/.* "//;s/".*$//;p}' ext/fileinfo/php_fileinfo.h)
if test "$ver" != "%{fileinfover}"; then
   : Error: Upstream FILEINFO version is now ${ver}, expecting %{fileinfover}.
   : Update the fileinfover macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_PHAR_VERSION /{s/.* "//;s/".*$//;p}' ext/phar/php_phar.h)
if test "$ver" != "%{pharver}"; then
   : Error: Upstream PHAR version is now ${ver}, expecting %{pharver}.
   : Update the pharver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_ZIP_VERSION_STRING /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the zipver macro and rebuild.
   exit 1
fi
ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the jsonver macro and rebuild.
   exit 1
fi

%build
%if 0%{?rhel} >= 6
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:                                                         
libtoolize --force --copy                                                              
%if 0%{?rhel} >= 6
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4                             
%endif

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.

build() {
# bison-1.875-2 seems to produce a broken parser; workaround.
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
ln -sf ../configure
%configure \
        --cache-file=../config.cache \
        --with-libdir=%{_lib} \
        --with-config-file-path=%{_sysconfdir} \
        --with-config-file-scan-dir=%{_sysconfdir}/php.d \
        --disable-debug \
        --with-pic \
        --disable-rpath \
        --without-pear \
        --with-bz2 \
        --with-exec-dir=%{_bindir} \
        --with-freetype-dir=%{_prefix} \
        --with-png-dir=%{_prefix} \
        --with-xpm-dir=%{_prefix} \
        --enable-gd-native-ttf \
        --with-t1lib=%{_prefix} \
        --without-gdbm \
        --with-gettext \
        --with-gmp \
        --with-iconv \
        --with-jpeg-dir=%{_prefix} \
        --with-openssl \
        --with-pcre-regex \
        --with-zlib \
        --with-layout=GNU \
        --enable-exif \
        --enable-ftp \
        --enable-magic-quotes \
        --enable-sockets \
        --enable-sysvsem --enable-sysvshm --enable-sysvmsg \
        --with-kerberos \
        --enable-ucd-snmp-hack \
        --enable-shmop \
        --enable-calendar \
        --without-mime-magic \
        --without-sqlite \
        --with-libxml-dir=%{_prefix} \
        --with-xml \
        --with-system-tzdata \
        $* 
if test $? != 0; then 
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and all the shared extensions
pushd build-cgi
build --enable-force-cgi-redirect \
      --enable-pcntl \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-gd=shared \
      --enable-bcmath=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-fastcgi \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,%{mysql_config} \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
      --enable-json=shared \
      --enable-zip=shared \
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --with-mssql=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
      %{?_with_interbase:--with-interbase=shared,%{_libdir}/firebird} \
      %{?_with_interbase:--with-pdo-firebird=shared,%{_libdir}/firebird} \
      %{?_with_oci8:--with-oci8=shared,instantclient,%{_libdir}/oracle/%{instantclient_ver}/client/lib}
popd

without_shared="--without-mysql --without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-pdo --disable-xmlreader --disable-xmlwriter \
      --disable-phar --disable-fileinfo \
      --disable-json --without-pspell --disable-wddx \
      --without-curl --disable-posix \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_sbindir}/apxs ${without_shared}
popd

%if 0%{?_with_fpm}
#build fpm
pushd build-fpm
build --enable-fpm ${without_shared}
popd
%endif

%if 0%{?_with_milter:1}
# Build milter SAPI
# /usr/lib[64]/libphp5.so
pushd build-milter
build --with-milter ${without_shared}
popd
%endif

%if 0%{?_with_embedded:1}
# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed ${without_shared}
popd
%endif

%if 0%{?_with_litespeed:1}
# Build litespeed module
pushd build-litespeed
build --with-litespeed ${without_shared}
popd
%endif

%if 0%{?_with_zts:1}
# Build a special thread-safe Apache SAPI
pushd build-zts
EXTENSION_DIR=%{_libdir}/php/modules-zts
build --with-apxs2=%{_sbindir}/apxs ${without_shared} \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d
popd
%endif

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.

%check
%if %runselftest
cd build-apache
# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in `find .. -name \*.diff -type f -print`; do
    echo "TEST FAILURE: $f --"
    cat "$f"
    echo "-- $f result ends."
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if 0%{?_with_fpm}
# Install the php-fpm binary
make -C build-fpm install-fpm INSTALL_ROOT=%{buildroot}
%endif

# Install the version for milter SAPI
%if 0%{?_with_milter}
make -C build-milter install-sapi install-headers INSTALL_ROOT=%{buildroot}
%endif

# Install the version for embedded script language in applications + php_embed.h
%if 0%{?_with_embedded}
make -C build-embedded install-sapi install-headers INSTALL_ROOT=%{buildroot}
%endif

# Install everything from the CGI SAPI build
pushd build-cgi
make install INSTALL_ROOT=%{buildroot} 
popd

# Install the Apache module
pushd build-apache
make install-sapi INSTALL_ROOT=%{buildroot}
popd

# Install the default configuration file and icons
install -m 755 -d %{buildroot}%{_sysconfdir}/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/php.ini
install -m 755 -d %{buildroot}%{contentdir}/icons
install -m 644 *.gif %{buildroot}%{contentdir}/icons/

mkdir -p %{buildroot}%{_sysconfdir}/rpm

# Use correct libdir
sed -i -e 's|%{_prefix}/lib|%{_libdir}|' %{buildroot}%{_sysconfdir}/php.ini

# install the DSO
install -m 755 -d %{buildroot}%{_libdir}/httpd/modules
install -m 755 build-apache/libs/libphp5.so %{buildroot}%{_libdir}/httpd/modules

%if 0%{?_with_zts:1}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp5.so %{buildroot}%{_libdir}/httpd/modules/libphp5-zts.so
%endif

%if 0%{?_with_litespeed:1}
# install the php litespeed binary
install -m 755 build-litespeed/sapi/litespeed/php %{buildroot}%{_bindir}/php-ls
%endif

# Apache config fragment
install -m 755 -d %{buildroot}/etc/httpd/conf.d
install -m 644 %{SOURCE1} %{buildroot}/etc/httpd/conf.d

install -m 755 -d %{buildroot}%{_sysconfdir}/php.d
install -m 755 -d %{buildroot}%{_localstatedir}/lib/php
install -m 700 -d %{buildroot}%{_localstatedir}/lib/php/session

%if 0%{?_with_fpm}
# PHP-FPM stuff
# Log
install -m 755 -d %{buildroot}%{_localstatedir}/log/php-fpm
install -m 755 -d %{buildroot}%{_localstatedir}/run/php-fpm
# Config
install -m 755 -d %{buildroot}%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/php-fpm.d/www.conf
mv %{buildroot}%{_sysconfdir}/php-fpm.conf.default .
# Service
install -m 755 -d %{buildroot}%{_initrddir}
install -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/php-fpm
# LogRotate
install -m 755 -d %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/php-fpm
%endif

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql mysql mysqli odbc ldap snmp xmlrpc imap \
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    pdo pdo_mysql pdo_pgsql pdo_odbc pdo_sqlite json zip \
    enchant phar mcrypt mssql tidy fileinfo intl \
    pdo_dblib pspell curl wddx posix sysvshm sysvsem sysvmsg \
    recode \
    %{?_with_interbase:interbase pdo_firebird} %{?_with_oci8:oci8} tidy ; do
    cat > %{buildroot}%{_sysconfdir}/php.d/${mod}.ini <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${mod}.ini
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx > files.xml

# The mysql and mysqli modules are both packaged in php-mysql
cat files.mysqli >> files.mysql

# Split out the PDO modules
cat files.pdo_dblib >> files.mssql
cat files.pdo_mysql >> files.mysql
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
%if 0%{?_with_interbase}
cat files.pdo_firebird >> files.interbase
%endif

# sysv* and posix in packaged in php-process
cat files.sysv* files.posix > files.process

# Package pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo

# Package json and zip in -common.
cat files.json files.zip files.curl files.phar files.fileinfo > files.common

# Install the macros file:
install -d %{buildroot}%{_sysconfdir}/rpm
sed -e "s/@PHP_APIVER@/%{apiver}/;s/@PHP_ZENDVER@/%{zendver}/;s/@PHP_PDOVER@/%{pdover}/" \
    < %{SOURCE3} > macros.php
install -m 644 -c macros.php \
           %{buildroot}%{_sysconfdir}/rpm/macros.php


# Remove unpackaged files
rm -rf %{buildroot}%{_libdir}/php/modules/*.a \
       %{buildroot}%{_bindir}/{phptar} \
       %{buildroot}%{_datadir}/pear \
       %{buildroot}%{_libdir}/libphp5.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

# Fix the link
(cd %{buildroot}%{_bindir}; ln -sfn phar.phar phar)

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
rm files.* macros.php

%if 0%{?_with_milter}
%post milter -p /sbin/ldconfig
%postun milter -p /sbin/ldconfig
%endif

%if 0%{?_with_embedded}
%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig
%endif

%if 0%{?_with_fpm}
%post fpm
/sbin/chkconfig --add php-fpm

%preun fpm
if [ "$1" = 0 ] ; then
    /sbin/service php-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del php-fpm
fi
%endif


%files
%defattr(-,root,root)
%{_libdir}/httpd/modules/libphp5.so
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%config %{_sysconfdir}/httpd/conf.d/php.conf
%{contentdir}/icons/php.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_* TSRM_LICENSE 
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%dir %{_localstatedir}/lib/php

%files cli
%defattr(-,root,root)
%doc sapi/cgi/README* sapi/cli/README
%{_bindir}/php
%{_bindir}/phar*
%{_bindir}/php-cgi
%{_mandir}/man1/php.1*
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/phpize.1*

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%{_mandir}/man1/php-config.1*
%config %{_sysconfdir}/rpm/macros.php

%if 0%{?_with_fpm}
%files fpm
%defattr(-,root,root)
%doc php-fpm.conf.default
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%{_sbindir}/php-fpm
%{_initrddir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,apache) %dir %{_localstatedir}/log/php-fpm
%dir %{_localstatedir}/run/php-fpm
%{_mandir}/man8/php-fpm.8.gz
%{_datadir}/fpm/status.html
%endif

%files pgsql -f files.pgsql
%files mysql -f files.mysql
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%files gd -f files.gd
%doc gd_README
%files soap -f files.soap
%files bcmath -f files.bcmath
%files dba -f files.dba
%files pdo -f files.pdo
%files tidy -f files.tidy
%files mcrypt -f files.mcrypt
%files mssql -f files.mssql
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%files enchant -f files.enchant

# Files for conditional Module Support
%if 0%{?_with_oci8}
%files oci8 -f files.oci8
%endif

%if 0%{?_with_zts}
%files zts
%defattr(-,root,root)
%{_libdir}/httpd/modules/libphp5-zts.so
%endif

%if 0%{?_with_litespeed}
%files litespeed
%defattr(-,root,root)
%{_bindir}/php-ls
%endif

%if 0%{?_with_milter}
%files milter
%defattr(-,root,root)
%{_bindir}/php-milter
%endif

%if 0%{?_with_embedded}
%files embedded
%defattr(-,root,root,-)
%{_libdir}/libphp5.so
%{_libdir}/libphp5-%{version}.so
%endif

%if 0%{?_with_interbase}
%defattr(-,root,root,-)
%files interbase -f files.interbase
%endif

%changelog
* Fri Apr 12 2013 Ben Harper <ben.harper@rackspace.com> - 5.2.24-1.ius
- Latest source from upstream
	
* Fri Mar 15 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.23-1.ius
- Latest source from upstream

* Thu Mar 07 2013 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.22-4.ius
- Removing custom find-requires in place of building for CentOS
  in IUS Community.

* Tue Mar 05 2013 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.22-3.ius
- Left over from debugging, this was causing strange requires to be added:
  http://packagetester.iuscommunity.org/package/26639/

* Thu Feb 28 2013 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.22-2.ius
- Provide a custom find-requires that excludes 'LIBJPEG_6.2'.
- libjpeg-turbo which replaced libjpeg in EL 6.4 provides
  libjpeg.so.62(LIBJPEG_6.2) where as libjpeg did not,
  find-requires is linking against this and will break pre 6.4 users,
  we will exlude that link using a custom find-requires.

* Fri Feb 22 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.22-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.22

* Thu Jan 17 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.21-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.21
  
* Mon Jan 14 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.20-2.ius
- added pdo requirement for mssql per
  https://bugs.launchpad.net/ius/+bug/1099138

* Thu Dec 20 2012 Ben Harper <ben.harper@rackspace.com> - 5.3.20-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.20

* Mon Nov 26 2012 Ben Harper <ben.harper@rackspace.com> - 5.3.19-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.19

* Thu Oct 18 2012 Ben Harper <ben.harper@rackspace.com> - 5.3.18-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.18
- Patch for FPM issue removed, addressed upstream

* Mon Sep 27 2012 Ben Harper <ben.harper@rackspace.com> - 5.3.17-2.ius
- Patch for FPM issue see: http://bugs.php.net/bug.php?id=62886

* Mon Sep 17 2012 Ben Harper <ben.harper@rackspace.com> - 5.3.17-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.17

* Mon Aug 20 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.16-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.16

* Mon Jul 23 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.15-1.ius
- Latest sources
- Fixes CVE-2012-2688
- Updating zipver macro to 1.11.0

* Mon Jul 09 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.14-3.ius
- Global misspelled

* Thu Jun 22 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.14-2.ius
- Adding support for milter per Lars request in 
  https://bugs.launchpad.net/ius/+bug/1020087

* Thu Jun 21 2012 Dustin Offutt <dustin.offutt@rackspace.com> - 5.3.14-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.14
- Address CVE-2012-2143
- Altered patch-5.3.7-aconf259.patch to patch-5.3.14-aconf259.patch

* Mon May 08 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.13-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.13
- Address CVE-2012-2311

* Mon May 07 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.12-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.12
- Address CVE-2012-1823

* Mon Apr 30 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.11-1.ius
- Latest source from upstream http://www.php.net/ChangeLog-5.php#5.3.11
- Address CVE-2012-1172

* Tue Apr 10 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.10-2.ius
- Removing old psa-compat package

* Thu Feb 02 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.10-1.ius
- Latest sources from upstream http://www.php.net/ChangeLog-5.php#5.3.10
- Addresses CVE-2012-0830

* Wed Jan 11 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.9-1.ius
- Latest sources from upstream http://www.php.net/ChangeLog-5.php#5.3.9
- New file added to fpm package '/usr/share/fpm/status.html'

* Thu Dec 01 2011 Jeffrey Ness <wdierkes@rackspace.com> - 5.3.8-4.ius
- Adding in Litespeed package per Launchpad Request
  https://bugs.launchpad.net/ius/+bug/898674

* Thu Oct 20 2011 BJ Dierkes <wdierkes@rackspace.com> - 5.3.8-3.ius
- Adding in needed provides of php53 

* Tue Aug 23 2011 BJ Dierkes <wdierkes@rackspace.com> - 5.3.8-2.ius
- touch configure.in before running buildconf to force rebuild (necesary
  due to patches)

* Tue Aug 23 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.8-1.ius
- Latest sources form upstream
  http://us.php.net/ChangeLog-5.php

* Fri Aug 19 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.7-1.ius
- Latest Sources
  http://www.php.net/archive/2011.php#id2011-08-18-1
- Removing Patch8 in place of Patch9

* Fri Aug 12 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.6-4.ius
- Enable FPM on EL6 or greater

* Wed Aug 10 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.6-3.ius
- Adding -F -1 to all %%patch as EL6 set patch fuzz to 0 
  from -1 in EL5 and has caused issues
- Adding aconf and libtool fixes for EL6

* Thu May 05 2011 BJ Dierkes <wdierkes@rackspace.com> - 5.3.6-2.ius
- Remove 'Requires: php53u' (base package) as the -common subpackage
  does not necessarily need base... and php53u-cli doesn't need the 
  added deps of the base package (httpd, etc).
 
* Thu Mar 17 2011 Jeffrey Ness <jefrey.ness@rackspace.com> - 5.3.6-1.ius
- Latest source from upstream, full changelog available from:
  http://php.net/ChangeLog-5.php#5.3.6
- CVEs addressed: CVE-2011-1153, CVE-2011-1092, CVE-2011-0708, CVE-2011-0421
- Removed: php-5.3.4-bug53512.patch, fixed upstream
- Removed --without-sqlite3 from without_shared, this module is now built
  in and no longer shared

* Mon Feb 21 2011 BJ Dierkes <wdierkes@rackspace.com> - 5.3.5-4.ius
- Add 'Provides: php53u-sqlite3' under -common sub package. 
  Resolves LP#722648

* Tue Feb 01 2011 BJ Dierkes <wdierkes@rackspace.com> - 5.3.5-3.ius
- Remove the associated commented with the obsoletes removed in last
  update

* Tue Feb 01 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.5-2.ius
- Removed Obsoletes: php53*

* Tue Jan 11 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.5-1.ius
- Latest source form upstream. Full changelog available at:
  http://www.php.net/ChangeLog-5.php#5.3.5
- Building PCRE provided from PHP Source:
  Removed BuildRequires pcre-devel >= 6.6
  Changed Configure line to --with-pcre-regex 
- Removed Patch316: php-5.3.4-bug53632.patch, applied by upstream
- Ported the following changes from Fedora midstream:
  use mysql_config in libdir directly to avoid biarch build failures 

* Wed Jan 05 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.4-3.ius
- Added Patch316: php-5.3.4-bug53632.patch,
  Resolves PHP Bug #53632 http://bugs.php.net/bug.php?id=53632

* Fri Dec 17 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.4-2.ius
- Name change to php53u based on the fact that RHEL 5.6 includes 
  php53 packages.  Resolves LP#691755
- Obsoletes: php53 < 5.3.4 (This needs to be removed before RHEL
  5.6 is GA).  All subpackages obsolete their respective counterparts
  as well.

* Thu Dec 16 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.4-1.ius
- Latest sources from upstream.  Full changelog available at:
  http://www.php.net/ChangeLog-5.php#5.3.4
  Resolves: CVE-2010-4150, CVE-2010-3709, CVE-2010-3436, 
  CVE-2010-2950, CVE-2010-3710, CVE-2010-3870, CVE-2010-4409,
  CVE-2010-4156
- Added Patch50: php-5.3.4-bug53512.path
- Move phpize under -cli subpackage (see BZ#657812)
- No longer Require: php53-pear.  Resolves LP#682259
- BuildRequires: redhat-lsb.  Use lsb_release to determine rhel point 
  release.  Fixes build issues on CentOS

* Fri Aug 20 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.3-4.ius
- Removed Source4 (macros.pear)
- Source5 becomes Source301 (oci8)
- Ported Source4, Source5, Source6, Source7 (FPM support) from 
  Remi's php repo
- Fixed broken %%{without_shared} macro to be proper bash variable.
  Resolves LP #620636 (Thank you to Remi for help with that)
- php-fpm BR: libevent >= 1.4.11 explicitly
- Added without_shared bash var to fpm build
- Stop php-fpm in preun script

* Thu Aug 19 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.3-3.ius
- Porting changes from Fedora upstream
- Added Patch3: php-5.2.4-norpath.patch
- Added Patch4: php-5.3.0-phpize64.patch (replaces Patch310)
- Added Patch5: php-5.2.0-includedir.patch
- Added Patch8: php-5.3.3-aconf26x.patch
- Added Patch20: php-4.3.11-shutdown.patch
- Added Patch21: php-5.3.3-macropen.patch
- Added Patch61: php-5.0.4-tests-wddx.patch


* Wed Aug 11 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.3-2.ius
- Build -fpm support if rhel_point_release >= 5.5

* Fri Jun 23 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.3-1.ius
- Latest sources from upstream.  Full changelog available at:
  http://www.php.net/ChangeLog-5.php#5.3.3
- Removed Patch9: php-5.3.2-phar.patch (applied upstream)
- Removed Patch314: php-5.2.13-bug51263.patch (applied upstream) 
- Removed Patch315: php-5.3.2-bug51192.patch (applied upstream)
- Merged LP#29926, Resolves LP#591609 PHP-FPM Support (disabled
  by default)

* Tue Jun 15 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.2-6.ius
- Rebuild for 5.x (EUS) repos

* Thu May 20 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.2-5.ius
- Added -psa-compat subpackage which adds Plesk (psa) compatibility
  Resolves LP#583485.

* Thu May 13 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.2-4.ius
- Set error_reporting = E_ALL & ~E_NOTICE | E_DEPRECATED.  Resolves 
  RS #585 (internal)
 
* Tue Apr 06 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.2-3.ius
- Added Patch314: php-5.2.13-bug51263.patch resolves Bug 51263 imagettftext
  and rotated text uses wrong baseline (regression).  Resolves LP #551189.
- Added Patch315: php-5.3.2-bug51192.patch resolves Bug 51192
  FILTER_VALIDATE_URL will invalidate a hostname that includes '-'.  Resolves
  LP #548985.

* Thu Mar 18 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.2-2.ius
- Add Requires: recode for -recode package
- Fixed httpd_mmn macro bug for -zts package

* Thu Mar 04 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.2-1.ius
- Latest sources from upstream.
- Removed Patch9: php-5.3.0-libedit.patch (applied upstream)
- Added Patch9: php-5.3.2-phar.patch (http://bugs.php.net/50578).  Reusing
  patch number 9 to follow upstream (Fedora) patch numbers.
- Updated Patch2: php-5.3.2-install.patch
- add runselftest option to allow build without test suite
- Added provides for all inherited pecl modules

* Wed Feb 10 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.1-2.ius
- Porting a lot of changes from Fedora 12
- Added optional zts module build.  Resolves LP#519548
- Added optional interbase support (requires firebird)
- Added optional embedded support 
- Added sysvshm, sysvsem, sysvmsg, posix into php-process
- Added recode support, -recode subpackage 
- Added modules enchant, phar, fileinfo, intl, pspell, 
- Added wddx to php-xml 
- Added curl shared in php-common
- Added -Wno-pointer-sign to CFLAGS
- Added SASL support to php-ldap
- Added t1lib and xpm support to GD 
- Added --with-system-tzdata
- Added READMEs for php-cli
- Added Patch6: php-5.2.4-embed.patch
- Added Patch7: php-5.3.0-recode.patch
- Added Patch9: php-5.3.0-libedit.patch
- Enable pdo_dblib driver in php-mssql
- Build with libedit support in place of readline
- Requires: php53-pear (not php-pear18)
- Adjust php.conf to use -zts SAPI build for worker MPM
- Remove legacy pear stuff
- Trim changelog to changes >= 5.2.0
- Drop mime_magic provides (legacy)
- Define php_extdir in macros.php
- Removed legacy hacks for php4->5 upgrades
- split pspell extension out into php-pspell 
- drop extension_dir from default php.ini, rely on hard-coded
  default, to make php-common multilib-safe 
- Removed el3/4 hacks
- Synced php.ini inline with upstream and Fedora
- Set short_open_tag = Off in php.ini
- Set memory_limit = 128M
- Set error_reporting = E_ALL & ~E_DEPRECATED
- Set variables_order = "GPCS"
- Set enable_dl = Off
- Set mail.add_x_header = On Resolves LP#491114
- Set session.bug_compat_warn = Off

* Fri Nov 20 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.1-1.ius
- Latest sources from upstream.
- Removed Patch313: php-5.3.0-error_log-bug49627.patch (applied upstream)
- Removed Patch309: php-5.3.0-bug447752.patch (applied upstream)
- Removed Patch312: php-5.3.0-bug462057.patch (applied upstream)

* Wed Nov 11 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-8.ius
- Added: Patch313: php-5.3.0-error_log-bug49627.patch

* Tue Oct 27 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-7.ius
- Added Patch312: php-5.3.0-bug462057.patch - Resolves LaunchPad
  Bug 462057 PHP 'posix_mkfifo()' 'open_basedir' Restriction Bypass
  Vulnerability

* Thu Oct 22 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-6.1.ius
- php53-mysql Requires: php53-common (not php-common)
- Remove Obscoletes from all subpackages.

* Fri Oct 16 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-6.ius
- Requires: php-pear18 >= 1:1.8. Resolves LP #452720.
- Added Patch310: php-5.3.0-phpize.patch

* Sat Oct 10 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-5.ius
- Only install /etc/rpm/macros.pear if building with pear.  Resolves
  LaunchPad Bug #448260.
- Added Patch309: php-5.3.0-bug447752.patch resolves LaunchPad Bug
  447752, Security Focus Bugtraq ID 36555 PHP tempname() safe_mode 
  Restriction-Bypass Vulnerability

* Thu Sep 03 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-4.ius
- MySQL subpackage provides %{real_name}-mysql

* Mon Aug 03 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-3.ius
- Set mysql.allow_persistent = Off in php.ini.  Resolves internal
  Rackspace tracker [#1402].

* Fri Jul 31 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-2.ius
- Requires: php-pear >= 1.8 (provided by php-pear18 in IUS)

* Wed Jul 22 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.3.0-1.ius
- Renamed package as php53
- Conflicts: php51, php52
- Latest sources, 5.3 branch.
- Removed mhash and ncurses sub packages (per changelog mhash was removed
  and ncurses was moved to PECL).

* Wed Apr 29 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.2.10-1.1.ius
- Rebuilding for IUS.
- Changed name to php52
- Require/BuildRequire: mhash rather than libmhash (EPEL)

* Mon Apr 27 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.2.9-2.rs
- Only build php-pear for el3/4 
- BuildRequires e2fsprogs-devel on el5

* Fri Feb 27 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.2.9-1.rs
- Latest sources from upstream.
- Removed Patch307: php-5.2.8-timelib_no_clone.patch (applied upstream)
- Removed Patch308: php-5.2.8-array.patch (applied upstream)

* Mon Jan 26 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.2.8-3.1.rs
- Adding Vendor tag.

* Tue Jan 06 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.2.8-3.rs
- Adding macros.pear
- Provides php(api), php(zend-abi)

* Tue Dec 23 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.2.8-2.rs
- Added Patch307: php-5.2.8-timelib_no_clone.patch 
  (resolves PHP Bug #46889)
- Added Patch308: php-5.2.8-array.patch (resolves PHP Bug #46893)

* Tue Dec 09 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.2.8-1.rs
- Latest sources
- Replaces Patch350: php-5.2.4-dashn.patch with 
  Patch350: php-5.2.8-dashn.patch
- Replaced Patch302: php-5.2.6-oci8-lib64.patch with 
  Patch302: php-5.2.8-oci8-lib64.patch
- Removed Patch303: php-5.2.6-CVE-2008-3658.patch (applied upstream)
- Removed Patch304: php-5.2.6-CVE-2008-3659.patch (applied upstream)
- Removed Patch305: php-5.2.6-CVE-2008-3660.patch (applied upstream)
- Removed Patch306: php-5.2.6-CVE-2008-2829.patch (applied upstream)

* Thu Nov 20 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.2.6-4.rs
- Added Patch306: php-5.2.6-CVE-2008-2829.patch which backports 
  fixes for PHP Bug #45460

* Wed Oct 22 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.2.6-3.rs
- Added Patch303: php-5.2.6-CVE-2008-3658.patch
- Added Patch304: php-5.2.6-CVE-2008-3659.patch
- Added Patch305: php-5.2.6-CVE-2008-3660.patch
- BuildRequires: zlib

* Fri May 16 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.2.6-2.rs
- php-mysql requires mysqlclient15 on el3 and el4. Resolves Rackspace
  Bug [#486].
- Requires libxslt under main php, Resolves Rackspace Bug [#487].

* Mon May 05 2008 Shawn Ashlee <shawn.ashlee@rackspace.com> 5.2.6-1.rs
- latest sources from upstream
- replaced (Patch302) php-5.2.3-oci8-lib64.patch with php-5.2.6-oci8-lib64.patch

* Thu Apr 03 2008 Shawn Ashlee <shawn.ashlee@rackspace.com> 5.2.5-3.rs
- add tidy module

* Fri Jan 01 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.2.5-2.1.rs
- Requires: libtool-ltdl on el5 (as well)

* Thu Dec 13 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.2.5-2.rs
- BuildRequires: mysql-devel >= 5.0.22 (el5 compatible)
- BuildRequires: libtool-ltdl-devel on el5

* Mon Nov 19 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.2.5-1.rs
- Latest sources.

* Tue Oct 23 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.2.4-2.1.rs
- Disable allow_url_fopen in php.ini
- BuildRequires: mysql-devel >= 5.0.45, Requires mysqlclient15 

* Sun Sep 02 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.2.4-1.1.rs
- Fixed %pre/post common scripts to properly organize php.ini if 
  the current version of php is < 5.

* Fri Aug 31 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.2.4-1.rs
- Latest sources from upstream.
- Replaces Patch1: Patch1: php-5.1.4-gnusrc.patch with
  Patch1: php-5.2.4-gnusrc.patch
- Replaced Patch3: php-5.0.4-norpath.patch with 
  Patch3: php-5.2.4-norpath.patch
- Replaced Patch31: php-5.0.0-easter.patch with
  Patch31: php-5.2.4-easter.patch
- Replaced Patch350: php-5.2.2-tests-dashn.patch with
  Patch350: php-5.2.4-dashn.patch
- Removed Patch21: php-4.3.1-odbc.patch (modified upstream)

* Mon Jul 23 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.2.3-4.rs
- Re-Marking php.ini as noreplace (upgrades for non major versions
  break customer configs).  There is a prein script to move php.ini out
  of the way if the php major version is 4 before upgrade.
- Remove post script that warned about ioncube loader.  Our ioncube
  loader package has a triggerin script that reconfigs after php
  upgrade.
- php.ini pre script goes under the common package

* Thu Jul 12 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.2.3-3.1.rs
- Adding conditional t1lib support, not enabled by default

* Mon Jul 09 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.3-3.rs
- Adding Patch302: php-5.2.3-oci8-lib64.patch (Bug #41941)

* Fri Jun 29 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.3-2.rs
- Making spec 'Mock' compatible.
- Adding oci8 module by default
- 'rhelX' vars become 'elX' vars.

* Fri Jun 01 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.3-1.rs
- Latest sources
- Removing Patch301: php-5.2.2-http_raw_post_data.patch (applied upstream)
- Removed workaround for installing CLI as /usr/bin/php .... PHP now installs
  the CLI by default.

* Tue May 08 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.2-2.rs
- Adding Patch301: php-5.2.2-http_raw_post_data.patch (PHP BugID: 41293)

* Fri May 03 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.2-1.rs
- Latest sources
- Replaced Patch50: php-5.0.4-tests-dashn.patch with Patch350: php-5.2.2-tests-dashn.patch
- Removed Patch79: php-5.2.1-CVE-2007-1285.patch (applied upstream)
- Removed Patch80: php-5.1.6-CVE-2007-1583.patch (applied upstream)
- Removed Patch81: php-5.1.6-CVE-2007-0455.patch (applied upstream)
- Removed Patch82: php-5.1.6-CVE-2007-1001.patch (applied upstream)
- Removed Patch83: php-5.1.6-CVE-2007-1718.patch (applied upstream)

* Fri Apr 20 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.1-5.1.rs
- BuildRequires: apr-devel, elfutils-libelf-devel, apr-util-devel

* Mon Apr 16 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.1-5.rs
- Security updates.
- Added Patch79: php-5.2.1-CVE-2007-1285.patch
- Added Patch80: php-5.1.6-CVE-2007-1583.patch
- Added Patch81: php-5.1.6-CVE-2007-0455.patch
- Added Patch82: php-5.1.6-CVE-2007-1001.patch
- Added Patch83: php-5.1.6-CVE-2007-1718.patch

* Tue Mar 27 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.1-4.rs
- Adding optional support for Oracle (oci8) additional module
- Requires/BuildRequires oracle-instantclient-{basic,devel} >= 10.2.0.3

* Fri Feb 23 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.1-3.2.rs
- Obsoletes any-php-sqlite2
- Add %post script to detect /etc/php.d/ioncube-loader.ini, and if so
  warn installer to verify it's configuration

* Thu Feb 22 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.1-3.1.rs
- Obsoletes php-sqlite2 

* Tue Feb 13 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.1-3.rs
- Bring Additional Module definitions in house (set in spec, not at command line)
- Being back mssql support (Requires/BuildRequires freetds/freetds-devel) 
  built in by default

* Fri Feb 09 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.1-2.rs
- Adding Patch300: php-5.2.1-PQfreemem.patch (PQfreemem requires
  postgresql > 7.4)
 
* Thu Feb 08 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.1-1.rs
- Latest sources add many features, and improve stability.  The official
  release announcement can be found here: http://www.php.net/releases/5_2_1.php
- Requires libxslt >= 1.1.11, BuildRequires libxslt-devel >= 1.1.11
- Add a -e check on /etc/php.ini in %pre script
- Requires mysqlclient14 on rhel3
- Removed Patch6: php-5.1.6-curl716.patch (applied upstream)
- Removed Patch7: php-5.2.0-filterm4.patch (applied upstream)

* Fri Jan 12 2007 BJ Dierkes <wdierkes@rackspace.com> 5.2.0-9.rs
- Removed '-Wno-pointer-sign' from CFLAGS
- Modified BuildRequires file >= 4.0 to 3.39 (rhel3 savvy, builds fine)
- Modified BuildRequires for imap package to do conditional requires for
  rhel3 (imap-devel) and rhel4 (libc-client-devel)
- Added a %pre script to check for php < 5 php.ini and move it out of the way if it isn't
  (i.e. allow the new php.ini to install to /etc/php.ini)
- Requires/BuildRequires: libxml2 and libxml2-devel >= 2.6.16
- Add conditional change - Use internal pcre on rhel3
- Requires/BuildRequires net-snmp and net-snmp-devel >= 5.1
- Added php-pear back in as a subpackage
- Adding conditional support for Mhash and Mcrypt

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 5.2.0-8
- fix filter.h installation path
- fix php-zend-abi version (Remi Collet, #212804)

* Tue Nov 28 2006 Joe Orton <jorton@redhat.com> 5.2.0-7
- rebuild again

* Tue Nov 28 2006 Joe Orton <jorton@redhat.com> 5.2.0-6
- rebuild for net-snmp soname bump

* Mon Nov 27 2006 Joe Orton <jorton@redhat.com> 5.2.0-5
- build json and zip shared, in -common (Remi Collet, #215966)
- obsolete php-json and php-pecl-zip
- build readline extension into /usr/bin/php* (#210585)
- change module subpackages to require php-common not php (#177821)

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 5.2.0-4
- provide php-zend-abi (#212804)
- add /etc/rpm/macros.php exporting interface versions
- synch with upstream recommended php.ini

* Wed Nov 15 2006 Joe Orton <jorton@redhat.com> 5.2.0-3
- update to 5.2.0 (#213837)
- php-xml provides php-domxml (#215656)
- fix php-pdo-abi provide (#214281)

