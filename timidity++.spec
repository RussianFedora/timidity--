Summary: A software wavetable MIDI synthesizer
Name: timidity++
Version: 2.13.2
Release: 4%{?dist}
Group: Applications/Multimedia
Source: TiMidity++-%{version}.tar.bz2
Source1: instruments.tar.bz2
Source2: timidity.cfg
Source3: britepno.pat.bz2
Source4: pistol.pat.bz2
Source5: fedora-timidity.desktop
URL: http://timidity.sourceforge.net
Patch: TiMidity++-2.13.0-redhat.patch
Patch3: TiMidity++-2.13.0-detect.patch
Patch5: TiMidity++-2.13.0-64bit.patch
Patch6: TiMidity++-2.13.0-warnings.patch
License: GPLv2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: timidity++-X11
BuildRequires: arts-devel esound-devel alsa-lib-devel ncurses-devel gtk2-devel
BuildRequires: desktop-file-utils
Requires: %{name}-patches = %{version}-%{release}, hicolor-icon-theme

%description
TiMidity++ is a MIDI format to wave table format converter and
player. Install timidity++ if you'd like to play MIDI files and your
sound card does not natively support wave table format.


%package        patches
Summary:        Instrument (patch) files for %{name}
Group:          Applications/Multimedia

%description    patches
This package contains samples of instruments (called patches) for use in
wavetable midi synthesizers like %{name}. These patches are in the Gravis
Ultasound .pat format and can be used by any wavetable midi synthesizer which
understands this format.


%prep
%setup -q -n TiMidity++-%{version}
# Put config files etc. to sane locations
%patch -p1 -b .redhat
# Autodetect whether we should use aRts, esd, or neither
%patch3 -p1 -b .detect
# fix for x86_64 and s390x
%patch5 -p1 -b .64bit
%patch6 -p1 -b .warnings


%build
export EXTRACFLAGS="$RPM_OPT_FLAGS"
%configure --enable-dynamic --disable-dependency-tracking \
	--enable-interface=ncurses,slang,vt100,alsaseq,server,network,gtk \
	--enable-audio=oss,arts,alsa,esd,vorbis \
	--enable-gtk
make


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/timidity $RPM_BUILD_ROOT/etc
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/timidity.cfg
ln -s /etc/timidity.cfg $RPM_BUILD_ROOT%{_datadir}/timidity/timidity.cfg
pushd $RPM_BUILD_ROOT%{_datadir}/timidity
tar xvjf %{SOURCE1}
bzip2 -dck %{SOURCE3} >instruments/britepno.pat
bzip2 -dck %{SOURCE4} >instruments/pistol.pat
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora              \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
  %{SOURCE5}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
install -m 644 interface/pixmaps/timidity.xpm \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/timidity.xpm


%clean
rm -rf $RPM_BUILD_ROOT


%post
# update icon themes
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
# update icon themes
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/applications/fedora-timidity.desktop
%{_datadir}/icons/hicolor/48x48/apps/timidity.xpm

%files patches
%defattr(-,root,root,-)
%config(noreplace) /etc/timidity.cfg
%{_datadir}/timidity


%changelog
* Sat Oct 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.13.2-4
- Split the patches of into a seperate sub package so that they can be used
  by other wavetable midi synthesizers, without dragging in a bunch of unwanted
  dependencies (bz 250735)
- There is no reason to install the icon in /usr/share/pixmaps if it also gets
  installed under /usr/share/icons
- Rewrite autodetection of wether to use esd, aRts or alsa as output patch,
  so that it actually works (bz 200688)

* Thu Oct 11 2007 Jindrich Novy <jnovy@redhat.com> 2.13.2-3
- fix typo in package description (#185328) 
- use RPM_OPT_FLAGS, make debuginfo package usable (#249968),
  thanks to Ville Skitta
- compile with GTK interface (#231745), thanks to Brian Jedsen
  
* Mon Sep 24 2007 Jindrich Novy <jnovy@redhat.com> 2.13.2-2
- spec/license fixes
  
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.13.2-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.2-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.2-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Aug 26 2004 Thomas Woerner <twoerner@redhat.com> 2.13.0-3
- fixed esd output plugin to not output to stderr on fault (#130633)

* Mon Jul  5 2004 Thomas Woerner <twoerner@redhat.com> 2.13.0-2
- fixed configure options (#127190)

* Thu Jul  1 2004 Thomas Woerner <twoerner@redhat.com> 2.13.0-1
- new version 2.13.0
  - with alsa support (#117024, #123327)
  - working default output (#124774)
  - working ogg output (#124776)
- spec file fixes
- fixed some configure options
- added BuildRequires for ncurses-devel (#125028)

* Sat Jun 19 2004 Alan Cox <alan@redhat.com>
- fixed compiler reported bugs 

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Oct 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add %%clean specfile target

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 11 2003 Thomas Woerner <twoerner@redhat.com> 2.11.3-7
- fix for x86_64 and s390x

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec  9 2002 Thomas Woerner <twoerner@redhat.com> 2.11.3-5
- fixed dependency for autoconf

* Mon Jul 22 2002 Than Ngo <than@redhat.com> 2.11.3-4
- build against current libvorbis

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.11.3-1
- Update to 2.11.3
- Extend the aRts output plugin to support KDE 3.x features
- Fix the dependency mess

* Wed Aug 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.10.4-2
- Finally managed to locate free versions of britepno.pat and pistol.pat
  (#50982)

* Sat Apr 14 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.10.4

* Fri Feb 23 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Change timidity.cfg to work perfectly with both the real
  TiMidity++ and the timidity version used in kmidi
- Fix a typo in the GUS drumset #0

* Mon Jan  8 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Autodetect whether the aRts, esd or dsp backend should
  be used

* Thu Dec  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add aRts (KDE 2.x) backend (Patches #1 and #2)

* Mon Nov 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.10.3a2
- Move the config file to the FHSly correct place, /etc/timidity.cfg
- Enable ogg/vorbis support, now that we're shipping it

* Thu Aug 3 2000 Tim Powers <timp@redhat.com>
- rebuilt against libpng-1.0.8

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move instrument files to /usr/share/timidity, where it's actually looking
  for them (Bug #13932)
- 2.9.5 (bugfix release)

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jun 28 2000 Than Ngo <than@redhat.de>
- FHS fixes
- clean up specfile
- use RPM macros

* Sat Jun 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.4

* Wed Jan 19 2000 Tim Powoers <timp@redhat.com>
- bzipped source to conserve space

* Sat Aug 14 1999 Bill Nottingham <notting@redhat.com>
- add a changelog
- strip binaries
