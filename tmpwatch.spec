Summary: A utility for removing files based on when they were last accessed
Name: tmpwatch
Version: 2.9.16
Release: 6%{?dist}
URL: https://fedorahosted.org/tmpwatch/
Source0: https://fedorahosted.org/releases/t/m/tmpwatch/tmpwatch-%{version}.tar.bz2
Source1: tmpwatch.daily
Patch0: tmpwatch-2.9.16-fuser.patch
Patch1: tmpwatch-2.9.16-EACCES.patch
License: GPLv2
Group: System Environment/Base
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: psmisc

%description
The tmpwatch utility recursively searches through specified
directories and removes files which have not been accessed in a
specified period of time.  Tmpwatch is normally used to clean up
directories which are used for temporarily holding files (for example,
/tmp).  Tmpwatch ignores symlinks, won't switch filesystems and only
removes empty directories and regular files.

%prep
%setup -q
%patch0 -p1 -b .fuser
%patch1 -p1 -b .EACCES

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make ROOT=%{buildroot} SBINDIR=%{_sbindir} MANDIR=%{_mandir} \
	INSTALL='install -p' install

mkdir -p %{buildroot}%{_bindir}
# The $(...) computes /usr/bin => ../../
ln -s $(echo %{_bindir} |sed 's,/[^/]\+,/..,g; s,^/,,')%{_sbindir}/tmpwatch \
   %{buildroot}%{_bindir}/tmpwatch

mkdir -p %{buildroot}/etc/cron.daily
install -p %{SOURCE1} %{buildroot}/etc/cron.daily/tmpwatch
chmod +x %{buildroot}/etc/cron.daily/tmpwatch

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING ChangeLog NEWS README
%{_bindir}/tmpwatch
%{_sbindir}/tmpwatch
%{_mandir}/man8/tmpwatch.8*
%config(noreplace) /etc/cron.daily/tmpwatch

%changelog
* Fri Nov 6 2015 Miloslav Trmač <mitr@redhat.com> - 2.9.16-6
- Do not remove Python multiprocessing sockets.  Patch by Chris St. Pierre
  <chris.a.st.pierre@gmail.com>.
  Resolves: #1058310

* Wed Oct 14 2015 Miloslav Trmač <mitr@redhat.com> - 2.9.16-5
- Exclude SAP HANA lock files. Patch by Luca Miccini <lmiccini@redhat.com>
  Resolves: #1185244

* Wed Jul 27 2011 Miloslav Trmač <mitr@redhat.com> - 2.9.16-4
- Don't report EACCES errors, they can be routinely returned on FUSE mounts
  Resolves: #722856

* Mon Feb  1 2010 Miloslav Trmač <mitr@redhat.com> - 2.9.16-3
- Ship COPYING
  Resolves: #560690

* Mon Jan  4 2010 Miloslav Trmač <mitr@redhat.com> - 2.9.16-2
- Fix handling of filenames starting with '-' with --fuser
  Resolves: #552291

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.9.16-1.1
- Rebuilt for RHEL 6

* Thu Oct 15 2009 Miloslav Trmač <mitr@redhat.com> - 2.9.16-1
- Update to tmpwatch-2.9.16.
- Exclude /tmp/hsperfdata_*.
  Resolves: #527425
- Preserve timestamps where possible.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Miloslav Trmač <mitr@redhat.com> - 2.9.15-1
- Update to tmpwatch-2.9.15.
- Add a symlink to %%{_bindir}.
  Resolves: #494239

* Mon Mar 23 2009 Miloslav Trmač <mitr@redhat.com> - 2.9.14-1
- Update to tmpwatch-2.9.14.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 23 2008 Miloslav Trmač <mitr@redhat.com> - 2.9.13-2
- Package the new documentation files.

* Sat Feb 23 2008 Miloslav Trmač <mitr@redhat.com> - 2.9.13-1
- New home page at https://fedorahosted.org/tmpwatch/ .
- tmpwatch is now licensed under GPLv2.
- Address issues from reviews by Adel Gadllah and Jason Tibbitts:
  - Run (make) with %%{?_smp_mflags}
  - Add a comment describing the origin of the tarball to the spec file
  - Use a better BuildRoot:

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.9.12-3
- Autorebuild for GCC 4.3

* Fri Dec 14 2007 Miloslav Trmač <mitr@redhat.com> - 2.9.12-2
- --atime is -u.  Doh.

* Fri Dec 14 2007 Miloslav Trmač <mitr@redhat.com> - 2.9.12-1
- Fix --nosymlinks description in the man page
- Use the maximum of atime, mtime and ctime when checking whether a file is
  obsolete
  Resolves: #373301

* Tue Oct 16 2007 Miloslav Trmač <mitr@redhat.com> - 2.9.11-2
- Update License:

* Sat Mar 31 2007 Miloslav Trmac <mitr@redhat.com> - 2.9.11-1
- Fix a misleading message in --test
  Resolves: 234596
- Compress the tarball using bzip2
- Move the cron.daily script to a separate source file

* Sun Nov  5 2006 Miloslav Trmac <mitr@redhat.com> - 2.9.10-1
- Reallow --exclude with nonexistent paths
  Resolves: 214034

* Thu Nov  2 2006 Miloslav Trmac <mitr@redhat.com> - 2.9.9-1
- Exclude aquota.group and aquota.user files
  Resolves: 206258
- Don't require the user-specified paths to be absolute

* Wed Nov  1 2006 Miloslav Trmac <mitr@redhat.com> - 2.9.8-1
- Add optional unit suffix to the "hours" (now "time") parameter (original
  patch by Alan J Rosenthal <flaps@dgp.toronto.edu>)
- Fix some format string vs. arguments mismatches
- Fix some rpmlint warnings

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.9.7-1.1
- rebuild

* Sat May  6 2006 Miloslav Trmac <mitr@redhat.com> - 2.9.7-1
- Add --nosymlinks (#190691)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.9.6-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.9.6-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Miloslav Trmac <mitr@redhat.com> - 2.9.6-1
- Add --exclude-user (original patch by Brett Pemberton)
- Fix too long line in /etc/cron.daily/tmpwatch

* Fri Nov 11 2005 Miloslav Trmac <mitr@redhat.com> - 2.9.5-1
- Fix GPL reference in usage message (#163531, patch by Ville Skyttä)
- Convert changelog to UTF-8

* Mon Jun 20 2005 Miloslav Trmac <mitr@redhat.com> - 2.9.4-1
- Add --dirmtime (#91096)
- Handle fchdir () failures

* Sat Apr 16 2005 Miloslav Trmac <mitr@redhat.com> - 2.9.3-1
- Silently ignore ENOENT if somebody removes files faster than us (#154960)
- Handle failures to exec fuser
- Fix check for negative grace periods

* Sat Mar  5 2005 Miloslav Trmac <mitr@redhat.com> - 2.9.2-2
- Rebuild with gcc 4

* Wed Dec 22 2004 Miloslav Trmac <mitr@redhat.com> - 2.9.2-1
- Mention skipping of lost+found in the man page (#143526)

* Sat Aug 14 2004 Miloslav Trmac <mitr@redhat.com> - 2.9.1-1
- Add --exclude, use it to preserve X socket directories (#107069)
- Allow multiple directory arguments with relative paths (#91097)
- Don't manually strip the binary

* Fri May 30 2003 Mike A. Harris <mharris@redhat.com> 2.9.0-1
- Added Solaris/HPUX support to tmpwatch via patch from Paul Gear (#71288)
- Rebuild in rawhide as 2.9.0-1

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 2.8.4-5
- rebuild

* Fri Feb  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.8.4-2
- rebuild

* Tue Oct  8 2002 Mike A. Harris <mharris@redhat.com> 2.8.4-4
- All-arch rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Mike A. Harris <mharris@redhat.com> 2.8.4-1
- Bump release and rebuild in new environment

* Fri Apr 13 2002 Mike A. Harris <mharris@redhat.com> 2.8.3-1
- Added support for large files with 64bit offsets by adding to CFLAGS
  -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 bug (#56961)

* Sun Jan 27 2002 Mike A. Harris <mharris@redhat.com> 2.8.2-1
- Added newlines to logfile messages as per bug #58912

* Thu Nov  8 2001 Preston Brown <pbrown@redhat.com>
- define default SBINDIR in Makefile
- incorrect boolean comparison fix

* Wed Aug 29 2001 Preston Brown <pbrown@redhat.com>
- cron script fix (#52785)

* Tue Aug 28 2001 Preston Brown <pbrown@redhat.com>
- rebuild for 5.x, 6.x, 7.x errata

* Mon Aug 27 2001 Preston Brown <pbrown@redhat.com>
- noreplace /etc/cron.daily/tmpwatch

* Mon Aug  6 2001 Preston Brown <pbrown@redhat.com> 2.8-1
- added a "nodirs" option which inhibits removal of empty directories.
- Integrated race condition fixes from Martin Macok (#50148)
- do not try to remove ext3 journal files (#50522)

* Tue Jul  3 2001 Preston Brown <pbrown@redhat.com> 2.7.4-1
- fix typo in cron script

* Mon Jul  2 2001 Preston Brown <pbrown@redhat.com>
- better checking for directory existence cleaning man cache dirs (#44117)

* Fri May 11 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Handle directories with large files
- fix some warnings during compilation

* Thu Mar 29 2001 Preston Brown <pbrown@redhat.com>
- fixed longstanding bug where directories removed while in test mode.

* Fri Mar  9 2001 Preston Brown <pbrown@redhat.com>
- Patch from enrico.scholz@informatik.tu-chemnitz.de allows concurrent 
  usage of mtime, ctime, and atime checking (#19550).

* Fri Jan 05 2001 Preston Brown <pbrown@redhat.com>
- increased interval for removal to 30 days for /var/tmp per FHS (#19951)

* Tue Sep 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- use execle() instead of system() to get the correct return code, fixes from
  Jeremy Katz <katzj@linuxpower.org>

* Thu Sep  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- rework to not have to fork() (#17286)
- set utime() after we're done reading a directory

* Sat Jun 17 2000 Matt Wilson <msw@redhat.com>
- defattr

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS compliance

* Thu May 18 2000 Preston Brown <pbrown@redhat.com>
- don't complain about failure to remove non-empty directories.
- fix man page path

* Wed May 17 2000 Preston Brown <pbrown@redhat.com>
- support /var/cache/man and /var/catman (FHS 2.1 compliance).

* Fri May 05 2000 Preston Brown <pbrown@redhat.com>
- support for CTIME from jik@kamens.brookline.ma.us
- fixes for fuser checks from Ian Burrell <iburrell@digital-integrity.com>.
- remove directories when empty without --all flag, to be consistent w/docs.

* Mon Feb 14 2000 Preston Brown <pbrown@redhat.com>
- option to use fuser to see if file in use before removing

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Tue Jan 18 2000 Preston Brown <pbrown@redhat.com>
- null terminal opt struct (#7836)
- test flag implies verbose (#2383)

* Wed Jan 12 2000 Paul Gear <paulgear@bigfoot.com>
- HP-UX port (including doco update)
- Tweaked Makefile to allow installation into different base directory
- Got rid of GETOPT_... defines which didn't do anything, so that short
  equivalents for all long options could be defined.
- Fixed bug in message() where 'where' file handle was set but unused
- Changed most fprintf() calls to message()

* Mon Aug 30 1999 Preston Brown <pbrown@redhat.com>
- skip lost+found directories
- option to use file's atime instead of mtime (# 4178)

* Mon Jun  7 1999 Jeff Johnson <jbj@redhat.com>
- cleanup more man pages, this time adding in cvs (#224).

* Thu Apr 08 1999 Preston Brown <pbrown@redhat.com>
- I am the new maintainer
- fixed cleanup of directories
- added --quiet flag
- freshen manpage
- nice patch from Kevin Vajk <kvajk@ricochet.net> integrated

* Wed Jun 10 1998 Erik Troan <ewt@redhat.com>
- make /etc/cron.daily/tmpwatch executable

* Tue Jan 13 1998 Erik Troan <ewt@redhat.com>
- version 1.5
- fixed flags passing
- cleaned up message()

* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added man page to package
- uses a buildroot and %%attr
- fixed error message generation for directories
- fixed flag propagation

* Mon Mar 24 1997 Erik Troan <ewt@redhat.com>
- Don't follow symlinks which are specified on the command line
- Added a man page

* Sun Mar 09 1997 Erik Troan <ewt@redhat.com>
- Rebuilt to get right permissions on the Alpha (though I have no idea
  how they ended up wrong).
