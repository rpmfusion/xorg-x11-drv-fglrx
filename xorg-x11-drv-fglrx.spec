%define          atilibdir       %{_libdir}/fglrx
%define          ativersion  8.11beta

# Tweak to have debuginfo - part 1/2
%if 0%{?fedora} > 7
%define __debug_install_post %{_builddir}/%{?buildsubdir}/find-debuginfo.sh %{_builddir}/%{?buildsubdir}\
%{nil}
%endif

Name:            xorg-x11-drv-fglrx
Version:         8.543
Release:         0.6.%{ativersion}%{?dist}
Summary:         AMD's proprietary driver for ATI graphic cards
Group:           User Interface/X Hardware Support
License:         BSD/Commercial/GPL/QPL
URL:             http://www.ati.com/support/drivers/linux/radeon-linux.html
#Source0:         https://a248.e.akamai.net/f/674/9206/0/www2.ati.com/drivers/linux/ati-driver-installer-8-10-x86.x86_64.run
Source0:         http://archive.ubuntu.com/ubuntu/pool/multiverse/f/fglrx-installer/fglrx-installer_8.543.orig.tar.gz
Source1:         fglrx-README.Fedora
Source3:         fglrx-config-display
Source4:         fglrx-init
Source5:         amdcccle.desktop
Source6:         fglrx-atieventsd.init
Source7:         fglrx-ati-powermode.sh
Source8:         fglrx-a-ac-aticonfig
Source9:         fglrx-a-lid-aticonfig
Source10:        fglrx.sh
Source11:        fglrx.csh

BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch:   x86_64 i386

Requires:        fglrx-kmod >= %{version}
Requires(post):  fglrx-kmod >= %{version}

# Needed in all nvidia or fglrx driver packages
BuildRequires:   desktop-file-utils
Requires:        livna-config-display >= 0.0.21
Requires:        %{name}-libs = %{version}-%{release}
Requires:        %{atilibdir}/libGL.so.1.2
Requires(post):  livna-config-display
Requires(preun): livna-config-display
Requires(post):  chkconfig
Requires(post):  ldconfig
Requires(preun): chkconfig

Provides:        fglrx-kmod-common = %{version}
Conflicts:       xorg-x11-drv-nvidia
Conflicts:       xorg-x11-drv-nvidia-legacy
Conflicts:       xorg-x11-drv-nvidia-96xx
Obsoletes:       fglrx-kmod < %{version}

# ATI auto-generated RPMs
Conflicts:       ATI-fglrx
Conflicts:       ATI-fglrx-control-panel
Conflicts:       ATI-fglrx-devel
Conflicts:       kernel-module-ATI-fglrx
Conflicts:       ATI-fglrx-IA32-libs

Obsoletes:	ati-x11-drv < %{version}-%{release}
Provides:	ati-x11-drv = %{version}-%{release}

%description
This package provides the most recent proprietary AMD display driver which
allows for hardware accelerated rendering with ATI Mobility, FireGL and
Desktop GPUs. Some of the Desktop and Mobility GPUs supported are the
Radeon 9500 series to the Radeon HD 4800 series.

For the full product support list, please consult the release notes
for release %{version}.


%package devel
Summary:         Development files for %{name}
Group:           Development/Libraries
Requires:        %{name}-libs = %{version}-%{release}
Requires:        %{_includedir}/X11/extensions, %{_includedir}/GL

Obsoletes:	ati-x11-drv-devel < %{version}-%{release}
Provides:       ati-x11-drv-devel = %{version}-%{release}

%description devel
This package provides the development files of the %{name} package,
such as OpenGL headers.


%package libs
Summary:         Libraries for %{name}
Group:           User Interface/X Hardware Support
%ifarch %{ix86}
Provides: %{name}-libs-32bit = %{version}-%{release}
Obsoletes: %{name}-libs-32bit <= %{version}-%{release}
%endif

%description libs
This package provides the shared libraries for %{name}.


%prep
%setup -q -c -T
#sh %{SOURCE0} --extract fglrx
mkdir -p fglrx/common
pushd fglrx
tar xfz %{SOURCE0}
mv etc lib opt usr common
cp common/usr/share/doc/fglrx/ATI_LICENSE.TXT .
popd

tar -cjf fglrx-kmod-data-%{version}.tar.bz2 fglrx/ATI_LICENSE.TXT fglrx/common/*/modules/fglrx/ fglrx/arch/*/*/modules/fglrx/

# Tweak to have debuginfo - part 2/2
%if 0%{?fedora} > 7
cp -p %{_prefix}/lib/rpm/find-debuginfo.sh .
sed -i -e 's|strict=true|strict=false|' find-debuginfo.sh
%endif

mkdir fglrxpkg
%ifarch %{ix86}
#cp -r fglrx/common/* fglrx/x710/* fglrx/arch/x86/* fglrxpkg/
cp -r fglrx/common/* fglrx/x740/* fglrx/arch/x86/* fglrxpkg/
%endif

%ifarch x86_64
echo `pwd`
#cp -r fglrx/common/* fglrx/x710_64a/* fglrx/arch/x86_64/* fglrxpkg/
cp -r fglrx/common/* fglrx/x740_64a/* fglrx/arch/x86_64/* fglrxpkg/
%endif

# fix doc perms
find fglrxpkg/usr/share/doc/fglrx -type f -exec chmod 0644 {} \;

%build


%install
rm -rf $RPM_BUILD_ROOT ./__doc

set +x
for file in $(cd fglrxpkg &> /dev/null; find . -type f | grep -v -e 'amdcccle.kdelnk$' -e 'amdcccle.desktop$' -e 'lib/modules/fglrx$' -e 'fireglcontrolpanel$' -e '/usr/share/doc/fglrx/' -e 'fglrx_panel_sources.tgz$' -e 'amdcccle.*.desktop$' -e 'amdcccle.*.kdelnk' -e 'fglrx_sample_source.tgz$' -e '^./lib/modules/fglrx' -e '/usr/share/icons/ccc_')
do
  if [[ ! "/${file##}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} ./__doc/${file##./usr/share/doc/fglrx/}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/modules/drivers}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_libdir}/xorg/modules/drivers/${file##./usr/X11R6/%{_lib}/modules/drivers}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/modules/dri}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_prefix}/%{_lib}/dri/${file##./usr/X11R6/%{_lib}/modules/dri}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/modules/extensions}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_libdir}/xorg/modules/extensions/fglrx/${file##./usr/X11R6/%{_lib}/modules/extensions}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/modules}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_libdir}/xorg/modules/${file##./usr/X11R6/%{_lib}/modules}
%ifarch %{ix86}
  elif [[ ! "/${file##./usr/X11R6/lib/modules/dri}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_prefix}/lib/dri/${file##./usr/X11R6/lib/modules/dri}
%endif
  elif [[ ! "/${file##./usr/X11R6/include/X11/extensions}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_includedir}/X11/extensions/${file##./usr/X11R6/include/X11/extensions}
  elif [[ ! "/${file##./usr/X11R6/%{_lib}/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{atilibdir}/${file##./usr/X11R6/%{_lib}/}
  #elif [[ ! "/${file##./usr/X11R6/lib/}" = "/${file}" ]]
  #then
  # atilibdir32bit doesn't exist anymore; we do multiarch builds instead (ie "make i386" catches these files)
  #  install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{atilibdir32bit}/${file##./usr/X11R6/lib/}
  #  continue
  elif [[ ! "/${file##./usr/X11R6/bin/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_bindir}/${file##./usr/X11R6/bin/}
  elif [[ ! "/${file##./usr/bin/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_sbindir}/${file##./usr/bin/}
  elif [[ ! "/${file##./usr/sbin/}" = "/${file}" ]]
  then
    install -D -p -m 0755 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_sbindir}/${file##./usr/sbin/}
  elif [[ ! "/${file##./etc/ati/}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/%{_sysconfdir}/ati/${file##./etc/ati/}
  elif [[ ! "/${file##./usr/include/}" = "/${file}" ]] || [[ ! "/${file##./etc/}" = "/${file}" ]] || [[ ! "/${file##./usr/share/man/}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/${file}
  elif [[ ! "/${file##./usr/share/ati/amdcccle}" = "/${file}" ]]
  then
    install -D -p -m 0644 fglrxpkg/${file} $RPM_BUILD_ROOT/${file}
  else
    echo ${file} found -- don\'t know how to handle
    exit 1
  fi
done
set -x

# Change perms on static libs. Can't fathom how to do it nicely above.
find $RPM_BUILD_ROOT/%{atilibdir} -type f -name "*.a" -exec chmod 0644 '{}' \;

# if we want versioned libs, then we need to change this and the loop above
# to install the libs as soname.so.%{version}
ln -s libGL.so.1.2 $RPM_BUILD_ROOT/%{atilibdir}/libGL.so.1
ln -s libfglrx_gamma.so.1.0 $RPM_BUILD_ROOT/%{atilibdir}/libfglrx_gamma.so.1
ln -s libfglrx_dm.so.1.0 $RPM_BUILD_ROOT/%{atilibdir}/libfglrx_dm.so.1
ln -s libfglrx_pp.so.1.0 $RPM_BUILD_ROOT/%{atilibdir}/libfglrx_pp.so.1
ln -s libfglrx_tvout.so.1.0 $RPM_BUILD_ROOT/%{atilibdir}/libfglrx_tvout.so.1

# profile.d files
install -D -p -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/fglrx.sh
install -D -p -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/fglrx.csh

install -D -p -m 0644 fglrxpkg/usr/share/icons/ccc_small.xpm $RPM_BUILD_ROOT/%{_datadir}/icons/ccc_small.xpm
install -D -p -m 0644 fglrxpkg/usr/share/icons/ccc_large.xpm $RPM_BUILD_ROOT/%{_datadir}/icons/ccc_large.xpm
install -D -p -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}/%(basename %{SOURCE3})
install -D -p -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_initrddir}/fglrx
install -D -p -m 0755 %{SOURCE6} $RPM_BUILD_ROOT%{_initrddir}/atieventsd
install -D -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/ati-powermode.sh
install -D -p -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/a-ac-aticonfig.conf
install -D -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/a-lid-aticonfig.conf

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor livna \
    --add-category X-Livna \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    %{SOURCE5}

# Set the correct path for gdm's Xauth file
sed -i 's|GDM_AUTH_FILE=/var/lib/gdm/$1.Xauth|GDM_AUTH_FILE=/var/gdm/$1.Xauth|' fglrxpkg/etc/ati/authatieventsd.sh

# Fix odd perms
find fglrxpkg -type f -perm 0555 -exec chmod 0755 '{}' \;
find fglrxpkg -type f -perm 0744 -exec chmod 0755 '{}' \;
chmod 644 fglrxpkg/usr/src/ati/fglrx_sample_source.tgz
find $RPM_BUILD_ROOT -type f -name '*.a' -exec chmod 0644 '{}' \;
chmod 644 $RPM_BUILD_ROOT/%{_sysconfdir}/ati/*.xbm.example
chmod 755 $RPM_BUILD_ROOT/%{_sysconfdir}/ati/*.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig ||:
if [ "${1}" -eq 1 ]; then
  # Enable fglrx driver when installing
  %{_sbindir}/fglrx-config-display enable &>/dev/null ||:
  # Add init script(s) and start it
  /sbin/chkconfig --add fglrx ||:
  /sbin/chkconfig --add atieventsd ||:
  /etc/init.d/fglrx start &>/dev/null ||:
fi ||:

%post libs -p /sbin/ldconfig

%preun
if [ "${1}" -eq 0 ]; then
  # Disable driver on final removal
  test -f %{_sbindir}/fglrx-config-display && %{_sbindir}/fglrx-config-display disable &>/dev/null ||:
  /etc/init.d/fglrx stop &>/dev/null ||:
  /sbin/chkconfig --del fglrx ||:
  /sbin/chkconfig --del atieventsd ||:
fi ||:

%postun -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc fglrxpkg/usr/share/doc/fglrx/*
%dir %{_sysconfdir}/ati/
%{_sysconfdir}/ati/authatieventsd.sh
%{_sysconfdir}/ati/signature
%{_sysconfdir}/acpi/actions/ati-powermode.sh
%config %{_sysconfdir}/ati/atiogl.xml
%config %{_sysconfdir}/ati/logo.xbm.example
%config %{_sysconfdir}/ati/logo_mask.xbm.example
%config %{_sysconfdir}/ati/control
%config %{_sysconfdir}/ati/amdpcsdb.default
%config(noreplace) %{_sysconfdir}/acpi/events/*aticonfig.conf
%config(noreplace)%{_sysconfdir}/profile.d/fglrx.*
%{_initrddir}/*
%{_sbindir}/*
%{_bindir}/*
# Xorg libs that do not need to be multilib
%{_libdir}/xorg/modules/drivers/fglrx_drv.so
%{_libdir}/xorg/modules/linux/libfglrxdrm.so
#/no_multilib
%{_datadir}/applications/*amdcccle.desktop
%{_datadir}/ati/amdcccle/*
%{_datadir}/icons/*
%{_mandir}/man[1-9]/atieventsd.*
%{_libdir}/xorg/modules/extensions/fglrx/
%{_libdir}/xorg/modules/*.so

%files libs
%defattr(-,root,root,-)
%dir %{atilibdir}
%{atilibdir}/*.so*
# FIXME: This file is recognized as "data" - figure out how to move it later
%{atilibdir}/libAMDXvBA.cap
%{_libdir}/dri/

%files devel
%defattr(-,root,root,-)
%doc fglrxpkg/usr/src/ati/fglrx_sample_source.tgz
%{atilibdir}/*.a
%{_libdir}/xorg/modules/*.a
%{_includedir}/GL/
%{_includedir}/X11/extensions/*.h

%changelog
* Mon Nov 3 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.6.8.11beta
- Fix upgrade path for FreshRPMs users

* Sat Oct 25 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.5.8.11beta
- Remove the libs subpackage's dependency on main package
  
* Thu Oct 23 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.4.8.11beta
- Don't place Xorg modules in -libs
- Let RPM detect dependency on libstdc

* Mon Oct 20 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.3.8.11beta
- Move libdri to the extensions/fglrx directory to prevent conflicts
- Require livna-config-display >= 0.0.21

* Sat Oct 18 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.2.8.11beta
- Change dependency of main package to libs subpackage in devel subpackage to
  fix multiarch repo push
  
* Thu Oct 16 2008 Stewart Adam <s.adam at diffingo.com> - 8.543-0.1.8.11beta
- Update to 8.11 beta (8.54.3)

* Thu Oct 16 2008 Stewart Adam <s.adam at diffingo.com> - 8.542-1.8.10
- Update to 8.10

* Sat Sep 21 2008 Stewart Adam <s.adam at diffingo.com> - 8.532-1.8.09
- Update to 8.09

* Wed Sep 3 2008 Stewart Adam <s.adam at diffingo.com> - 8.522-2.8.08
- Fix x86 %%files

* Thu Aug 21 2008 Stewart Adam <s.adam at diffingo.com> - 8.522-1.8.08
- Update to 8.08
- Update description
- Update the install grep loop and remove duplicate 'fglrx_sample_source.tgz$'

* Thu Jul 24 2008 Stewart Adam <s.adam at diffingo.com> - 8.512-1.8.07
- Update to 8.07

* Wed Jun 18 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.501-1.8.06
- Update to 8.06
- Don't remove python-devel BR (I think this was a glitch in RPM pre-F9 rawhide)

* Thu May 22 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.493-1.8.05
- Update to 8.05
- Update debuginfo fix

* Fri Apr 18 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.476-1.8.04
- Update to 8.04
- Call ldconfig in post, postun for libs and main package

* Wed Mar 5 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.471-1.8.03
- Update to 8.03

* Wed Feb 13 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.455.2-1.8.02
- Update to 8.02

* Sat Feb 2 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.452.1-3.8.01
- Port kwizart's changes to nvidia in devel:
- Remove ldconfig call on the main package 
- Remove some old Obsoletes/Provides
- Move the xorg modules to the main package (not needed for multilib)
- Add Requires libGL.so from the right path

* Sun Jan 27 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.452.1-2.8.01
- Main package requires %%{name}-libs
- Fix -libs description

* Sat Jan 19 2008 Stewart Adam <s.adam AT diffingo DOT com> - 8.452.1-1.8.01
- Update to Catalyst 8.01
- %%config(noreplace) the acpi configuration files
- No shebangs in files that are to be sourced
- Provides ati-fglrx since we obsolete it

* Wed Dec 26 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.443.1-2.7.12
- Split up libraries
- Remove libs-32bit package
- Don't use %%dir and file listing, just use directoryname/ to grab the dir
  and all files in it
- Add empty build section
- Fix License tag
- Provide proper libraries

* Thu Dec 20 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.443.1-1.7.12
- Update to Catalyst 7.12
- Don't overwrite LD_LIBRARY_PATH for now

* Wed Nov 21 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.43-1.7.11
- Update to Catalyst 7.11

* Mon Nov 5 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.42.3-7.1
- Fix typo in initscript

* Thu Nov 1 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.42.3-7
- Initscript improvements
- Minor bugfixes with scriptlets (don't echo "already disabled" type messages)
- config(noreplace) the profile.d scripts

* Sat Oct 27 2007 Stewart Adam <s.adam AT diffingo DOT com> 8.42.3-6
- Modify profile.d scripts so that we find fglrx's libGL.so.1

* Thu Oct 25 2007 kwizart < kwizart at gmail.com > 8.42.3-5
- Strip binaries and libs even if no debuginfo is made
- Fix some doc perms.

* Thu Oct 25 2007 kwizart < kwizart at gmail.com > 8.42.3-4
- Fix Deletion of static libs until we support them on x86_64
- Fix post ldconfig on libs-32bit
- Create symlinks for linker.

* Wed Oct 24 2007 kwizart < kwizart at gmail.com > 8.42.3-3
- Fix x86_64 build (Remove 32bit static lib and use fglrx/arch/x86/* in
  fglrxpkg/
- Add postun script for 32bit package

* Wed Oct 24 2007 Stewart Adam <s.adam AT diffingo DOT com> 8.42.3-2
- BR: python-devel to fix "python: command not found" errors during build

* Tue Oct 23 2007 Stewart Adam <s.adam AT diffingo DOT com> 8.42.3-1
- Update to 8.42.3
- Change fglrx-config-display to leave AIGLX on by default now that it is
  supported by the drivers

* Sun Oct 07 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> 8.40.4-3
- Disable debuginfo generation to avoid "no build id" errors

* Sun Aug 19 2007 Stewart Adam <s.adam AT diffingo DOT com> 8.40.4-2
- Add /etc/ati/signature

* Tue Aug 16 2007 Stewart Adam <s.adam AT diffingo DOT com> 8.40.4-1
- Update to 8.40.4

* Sun Jul 23 2007 Stewart Adam <s.adam AT diffingo DOT com> 8.39.4-2
- Update ATI's fixed 8.39.4

* Thu Jul 19 2007 Stewart Adam <s.adam AT diffingo DOT com> 8.39.4-1
- Update to 8.39.4

* Thu Jul 05 2007 Niko Mirthes <nmirthes AT gmail DOT com> - 8.38.7-3
- make fglrx-config-display add/remove the OpenGLOverlay X option. This
  is aticonfig's default behavior

* Sun Jul 1 2007 Stewart Adam <s.adam AT diffingo DOT com> 8.38.7-2
- Bump

* Sat Jun 30 2007 Niko Mirthes <nmirthes AT gmail DOT com> - 8.38.7-1
- Update to 8.38.7
- Whitespace alignment
- Install the .desktop file more 'correctly'

* Mon Jun 25 2007 Niko Mirthes <nmirthes AT gmail DOT com> - 8.38.6-1
- Update to 8.38.6
- fglrx remains broken on Fedora 7
- removed remaining build requirements for old control panel

* Sun Jun 03 2007 Niko Mirthes <nmirthes AT gmail DOT com> - 8.37.6-3
- Further 'fixed' fglrx.csh. Hope it doesn't suck too badly. It seems
  to work, but someone with more C shell experience should fix it up.
- Tweaked .desktop file (remove empty and unneeded entries, added 3 new
  languages).
- Minor whitespace adjustments to the .spec
- Remove build requirement qt-devel. CCC is binary only. We should look
  at the other build requirements as well since we no longer actually
  compile anything.

* Sun Jun 3 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.37.6-2
- forgot to mention in 8.36.7-1 that atieventsd is now added
- Fix fglrx.csh

* Thu May 31 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.37.6-1
- Update to 8.37.6
- Add ||: to _all_ commands in pre/post scriptlets so they don't block the
  scriptlet if they fail to execute
- New profile.d scripts, remove old /etc/profile.d script
- Package our own desktop file

* Sat Apr 28 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.36.5-3
- Fixes in the config-display (vendor > majorVendor)

* Sun Apr 22 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.36.5-2
- fglrx-config-display updates

* Wed Apr 18 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.36.5-1
- Update to new 8.36.5 release

* Fri Mar 30 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.35.5-1
- Update to 8.35.5
- Update sources
- Remove uneeded patch for the control panel sources

* Sun Mar 25 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.34.8-10
- Sync devel with FC-6
- Fix up initscript a little
- Update README

* Fri Mar 9 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.34.8-9
- Fix up scriptlets a little so that 'Driver already enabled|disabled'
  doesn't always appear on install or remove
- Update *-config-display files for majorVendor and not plain vendor

* Fri Mar 2 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-8
- New config-display
- New initscript
- Bump to -8

* Mon Feb 26 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-6
- Remove broken symlink atiogl_a_dri.so
- It's AMD not ATI's driver now!

* Sat Feb 24 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.34.8-5
- Bump for new tag

* Sat Feb 24 2007 Stewart Adam < <s.adam AT diffingo DOT com> - 8.34.8-4
- Standardize all summaries and descriptions with other nvidia and fglrx
  packages
- Standardize initscript and *config-display with other nvidia and fglrx
  packages
- Start merge with livna-config-display
- No more ghost!

* Thu Feb 22 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-3
- Add the profile.d script back, it was used for something else then
  workaround for the RH bug

* Wed Feb 21 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-2
- Seems I can't overwrite a tag.. Bump I go!
- Fix changelog date for 8.34.8-1

* Wed Feb 21 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.34.8-1
- Update to 8.34.8
- Move paths and names to plain fglrx, not ati-fglrx, the driver's name's
  long changed!
- Don't own /usr/X11R6... It's part of the standard hierarchy!
- Fix funny permissions on /etc/ files
- Mark config files as %%config

* Sun Feb 18 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-4
- Fix %%post, make it %%postun for libs-32bit

* Sat Feb 17 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-3
- Change descriptions to more informative, easy-to-understand ones
- Requires pyxf86config

* Fri Jan 12 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-2
- ldconfig in %%postun for 32-bit libs, too!

* Fri Jan 12 2007 Stewart Adam <s.adam AT diffingo DOT com> - 8.33.6-1
- Update to 8.33.6
- ldconfig in %%post for 32-bit libs

* Tue Nov 27 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.31.5-3
- re-add workaround -- seems some machines still search in /usr/X11R6 for dri
  files

* Mon Nov 27 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.31.5-2
- add modified version of a patch from Stewart Adam to put the DRI .so files
  to the right spot and remove the old workaround

* Fri Nov 17 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.31.5-1
- Update to 8.31.5, patch from Edgan in #livna

* Sat Oct 14 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.29.6-1
- Update to 8.29.6 (needed for 2.6.18 suppport/FC6)

* Fri Aug 18 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.28.8-1
- Update to 8.28.4
- refactored %%prep now that ATi's installer has merged arches

* Fri Aug 18 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-4
- updated/improved atieventsd init script
- removed remove excess tabs/whitespace from fglrx-config-display
- make tar quiet when creating the kmod tarball

* Sat Aug 05 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-3
- don't try to use '*.sh' in the for loop
- tone down the rant in ati-fglrx.profile.d

* Tue Aug 01 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-2
- fix perms on static libs
- added powerplay acpi bits
- made authatieventsd actually do something. Thorsten's for loop hurts little children
- rearranged files sections somewhat
- move all *.a files to devel package
- make the package actually build (file libaticonfig.a dropped upstream)

* Sun Jul 30 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.27.10-1
- Update to 8.27.10
- minor changes to spacing, removal of random tabs, re-arrangements

* Tue Jun 27 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.26.18-1
- Update to 8.26.18

* Fri Jun 02 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.25.18-2
- Fix 32bit libs

* Wed May 24 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.25.18-1
- Update to 8.25.18

* Fri May 19 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.24.8-3
- Change security context in %%post until #191054 is fixed
- conflict with nvidia packages

* Sun May 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 8.24.8-2
- Require fglrx-kmod instead of kmod-fglrx, obsolete incompatible kmods (#970).

* Sat Apr 15 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.24.8-1
- Update to 8.24.8

* Sun Apr 02 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-6
- Fix a "lib != %%{_lib}"

* Wed Mar 29 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 8.23.7-5
- fix perms on the headers
- tweak nvidia-settings' desktop file slightly

* Sun Mar 26 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-4
- fix another stupid oddity of fglrx with modular X

* Sun Mar 26 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-3
- fix deps in devel
- separate package for 32bit libs
- some cleanups from straw
- always activate driver
- try to unload drm and radeon in profile.d script

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-2
- update fglrx-config-display
- packge /usr/lib/xorg/modules/dri/fglrx_dri.so for now

* Sat Mar 18 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.23.7-1
- drop 0.lvn
- update to 8.23.7
- ExclusiveArch i386 and not %%{ix86} -- we don't want to build for athlon&co
- package some links that ldconfig normally would create

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Jan 30 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.1
- split into packages for userland and kmod
- rename to xorg-x11-drv-fglrx; yum/rpm should use mesa-libGL{,-devel} then in
  the future when seaching for libGL.so{,.1}
- remove kernel-module part
- remove old cruft

* Mon Dec 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.3
- Add patch for kernel 2.6.15

* Tue Dec 13 2005 Dams <anvil[AT]livna.org> - 8.20.8.1-0.lvn.2
- Really dropped Epoch

* Sat Dec 10 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.20.8.1-0.lvn.1
- Update to 8.20.8-1
- Drop Epoch

* Sun Nov 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 8.19.10.1-0.lvn.2
- Patch for 2.6.14 still needed on x86_64 (thx Ryo Dairiki for noticing)

* Sat Nov 12 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.19.10.1-0.lvn.1
- Update to 8.19.10-1
- Remove patches for 2.6.14
- Add fresh translation to desktop-file

* Wed Nov 09 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.18.6.1-0.lvn.2
- Patch kernel-module source to compile with 2.6.14

* Thu Oct 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.18.6.1-0.lvn.1
- Update to 8.18.6-1
- Conflict with nvidia-glx{,-legacy) (#627)
- Fix moduleline.split in fglrx-config-display (#582)
- Unload drm in fglrx-config-display, too
- Only ship self compiled fireglcontrolpanel

* Fri Aug 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.16.20.1-0.lvn.1
- Update to 8.16.20-1
- Update patch1, fireglcontrol.desktop
- Don't strip kernel-module for now

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.5
- Update fglrx-2.6.12-inter_module_get.patch (thx to Mike Duigou)

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.4
- Add patches from http://ati.cchtml.com/show_bug.cgi?id=136 and some tricks
  to built with 2.6.12 -- fixes building for FC4

* Tue Jun 07 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.3
- Missed one thing during reword of kernel-module-build-stuff
- Both x86_64 and x86 in the same package now

* Sun Jun 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.2
- Fix thinko

* Sun Jun 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.14.13.1-0.lvn.1
- Rework kernel-module-build-stuff for FC3 kmd and FC4 and new livna scheme
- Simplify the install; Lowers risk to miss files and is easier to maintain
- Remove dep on fedora-rpmdevtools
- Use modules and userland rpmbuild parameter to not build kernel- or driver-package

* Wed May 04 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.12.10.1-0.lvn.2
- Add fix for kernel 2.6.11

* Fri Apr 08 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.12.10.1-0.lvn.1
- Update to 8.12.10-1
- mod 0755 dri.so to let rpm detect require libstdc++.so.5

* Thu Mar 06 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.10.19.1-0.lvn.2
- Add patch for via agpgart (#355)

* Thu Feb 17 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.10.19.1-0.lvn.1
- Update to 8.10.19-1
- Remove patch for 2.6.10 kernel
- require libstdc++.so.5

* Wed Jan 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.4
- fix x86-64 in spec-file and in fglrx-config-display
- Fix by Ville Skyttä: ldconfig on upgrades

* Wed Jan 19 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.3
- Package library links

* Wed Jan 19 2005 Dams <anvil[AT]livna.org> - 0:8.8.25.1-0.lvn.2
- Urlized ati rpm source

* Sat Jan 15 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:8.8.25.1-0.lvn.1
- Update to 8.8.25
- Remove workaround from last version
- Remove special drm includes
- Prepare package for 64-bit version; But untested ATM
- Update patches

* Tue Jan 11 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.3
- add patch10 -- allows building on 2.6.10; Found:
  http://www.rage3d.com/board/showthread.php?t=33798874&highlight=2.6.10
- update drm-includes
- temporary for kernel-module:  Requires: ati-fglrx >= %%{epoch}:%%{version}-0.lvn.2
  so we don't have to rebuild the driver package

* Sun Nov 21 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.2
- Use kernelp and driverp rpmbuild parameter to not build kernel- or
  driver-package
- Trim doc in header

* Fri Nov 04 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.6-0.lvn.1
- Update to 3.14.6

* Fri Nov 04 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.7
- Build per default without kmoddev
- Rename --without tools to --without dirverp
- Update dri-headers to 2.6.9 version
- update building documentation in header

* Fri Oct 22 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.6
- Some small cleanups to various parts of the package as suggested by Dams

* Fri Oct 22 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.5
- Enhance makefile patch so building with different uname should work correctly
- Build verbose

* Thu Oct 21 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.4
- Update fedora-unrpm usage to work with newer version
- Update one para in README and fglrx-config-display output

* Fri Oct 15 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.3
- Change the enabling/disabling methode again -- driver is changed now
  directly. DRI is enabled when fglrx is enabled, but try to unload/warn if
  radeon kernel-module is loaded. DRI will be disabled and reenabled on the
  when next restart when disableing fglrx driver.
- Update README.fglrx.Fedora

* Mon Oct 11 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.2
- Let new version of ati-flrx-config-display change default depth to 24
- Updated Spec-File bits: fedora-kmodhelper usage and building description

* Thu Sep 30 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.14.1-0.lvn.1
- Update to 3.14.1
- In expectation of missing kernel-sourcecode package in FC3 remove the BR
  on it and include the neccessary header-files in the package. Will
  integrate more packages if there are API changes. But for now I
  think this is the easiest methode.
- Let ati-flrx-config-display handle /etc/ld.so.conf.d/ati-fglrx.conf
- Update ati-flrx-config-display; it adds a VideoOverlay Option now
  so xv works out of the box
- Don't (de)activate driver if DRI-Kernel-Modules are loaded; Let the
  init script to that during restart
- Update README.fglrx.Fedora

* Wed Sep 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.12.0-0.lvn.2
- Allow rpm to strip the kernel module.
- Fix shared library permissions.
- Split Requires(post,postun) to two to work around a bug in rpm.
- Fix -devel dependencies and kernel module package provisions.
- Improve summary and description, remove misleading comments.

* Sat Sep 11 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.12.0-0.lvn.1
- Update to 3.12.0
- Fix some fedora-kmodhelper/kernel-module related bits in spec
- Clean up install part a bit more

* Sun Sep 05 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.6
- Add stupid ati-fglrx.profile.d workaround for systems that had the
  original fglrx drivers installed before
- Conflict with fglrx -- the package should be removed so it can clean up
  the mess it did itself.
- Clean up desktop file

* Tue Aug 24 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.5
- Add ifdefs so building tools and kernel-module can be separated
- BuildRequire kernel-sourcecode kverrel, not kernel

* Wed Aug 17 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.4
- Fixed double release in Requires of devel-package
- Building against custom kernels now should work using rhkernel-macro
- Updated fedora-kmodhelper to 0.9.10
- Add 'include ld.so.conf.d/*.conf' before /usr/lib/X11 in /etc/ld.so.conf if
  it does not exists

* Wed Aug 10 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.3
- small fixes for dump issues

* Thu Aug 09 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.2
- BuildRequire fedora-rpmdevtools
- Use KERNEL_PATH correctly, needs updated patch1

* Sat Aug 07 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.11.1-0.lvn.1
- Update to 3.11.1
- Minor fixes

* Fri Aug  6 2004 Dams <anvil[AT]livna.org> 0:3.9.0-0.lvn.4
- .a files are 0644 moded. tgz files too.
- Added missing BuildReq: desktop-file-utils, qt-devel, fedora-rpmdevtools

* Mon Jul 19 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.3
- Update Patches to a working solution
- Modify start-script-- fglrx can also work without kernel-module (no DRI then)

* Sun Jul 18 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.2
- intergrate Readme, init-script and fglrx-config-display (stolen from
  nvidia package)

* Sat Jul 17 2004 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:3.9.0-0.lvn.1
- Initial RPM release.
