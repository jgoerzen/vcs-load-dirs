# arch-tag: tla working copy support 1062530429
# Copyright (C) 2003 John Goerzen
# <jgoerzen@complete.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import util
import os.path
from commandver import cmd, isdarcs, issvk, isgit, tlacmd

class wc:
    """Object for a working copy."""

    def __init__(self, wcpath, verbose = 0):
        self.wcpath = os.path.abspath(wcpath)
        self.verb = verbose
        if not self.wcverify():
            raise Exception, "%s is not a tla working copy" % self.wcpath

    def gettreeversion(self):
        if isdarcs():
            #util.chdircmd(self.wcpath, util.getstdoutsafeexec, "darcs",
            #              ['check'])
            return "Darcs repository"
        elif issvk():
            return "Svk repository"
        elif isgit():
            return "Git repository"
        else:
            return util.chdircmd(self.wcpath, util.getstdoutsafeexec, tlacmd,
                                 ['tree-version'])[0].strip() 

    def wcverify(self):
        try:
            self.gettreeversion()
        except util.ExecProblem:
            return 0
        return 1

    def gettaggingmethod(self):
        if isdarcs() or isgit():
            return 'explicit'
        else:
            return util.chdircmd(self.wcpath, util.getstdoutsafeexec, tlacmd,
                                 [cmd().tagging_method])[0].strip()

    def gettree(self):
        return util.maketree(self.wcpath,
                             ignore = [r'(^(\{arch\}$|,,|\.git|_darcs|\.arch-ids$|\.arch-inventory$|\+\+)|/\.arch-ids/)'])
    
    def addtag(self, file):
        if self.verb:
            print "Adding %s" % file
        if (file[-1] == '/') and \
           (not os.path.exists(os.path.join(self.wcpath,
                                            file[:-1]))):
            try:
                print "addtag: making dir %s" % file[:-1]
                os.makedirs(os.path.join(self.wcpath, file[:-1]))
            except:
                raise
        file = self.slashstrip(file)
        isdir = os.path.isdir(os.path.join(self.wcpath, file))
        if (not isdarcs()) or isdir:
            # Darcs will see adds later, but we need to add dirs
            # now so darcs mv will work.
            util.chdircmd(self.wcpath, util.safeexec, tlacmd,
                          cmd().add + [file])

    def movetag(self, src, dest):
        if self.verb:
            print "Moving %s to %s" % (src, dest)
        if src[-1] == '/' and dest[-1] == '/' and (not isdarcs() and not isgit()):
            # Dir to dir -- mv will catch it already.
            return
        src, dest = self.slashstrip(src, dest)
        util.chdircmd(self.wcpath, util.safeexec, tlacmd,
                      [cmd().move, src, dest])

    def movefile(self, src, dest):
        if self.verb:
            print "Moving file %s to %s" % (src, dest)
        src, dest = self.slashstrip(src, dest)

        def doit():
            destdir = os.path.dirname(dest)
            if (not os.path.exists(destdir)) and destdir != '':
                self.makedirs(destdir)
            if not isdarcs() and not isgit():
                # Darcs and git move it itself
                os.rename(src, dest)

        util.chdircmd(self.wcpath, doit)

    def delfile(self, file):
        if self.verb:
            print "Deleting file %s" % file
        fullfile = os.path.join(self.wcpath, file)
        if os.path.isfile(fullfile):
            os.unlink(fullfile)
        else:
            util.safeexec("rm", ['-rf', fullfile])

    def deltag(self, file):
    	# FXIME: what about git?
        if not isdarcs():
            if self.verb:
                print "Deleting %s" % file
            if os.path.islink(os.path.join(self.wcpath,file)) or os.path.exists(os.path.join(self.wcpath, file)):
                util.chdircmd(self.wcpath, util.safeexec, tlacmd,
                          [cmd().delete, file])

    def makelog(self, summary, logtext):
        self.summary = summary
        self.logtext = logtext
	if isgit():
            logfn = ",,gitlog"
	elif isdarcs():
            logfn = ",,darcslog"
	else:
            logfn =  util.chdircmd(self.wcpath, util.getstdoutsafeexec, tlacmd,
                                   ['make-log'])[0].strip()

        self.logfn = os.path.abspath(logfn)
        
        fd = open(self.logfn, "w")
        if isgit():
            fd.write("%s\n\n" % summary)
        elif not isdarcs():
            fd.write("Summary: %s\n" % summary)
            fd.write("Keywords: \n\n")
        fd.write(logtext)
        print "LOGTEXT", logtext
        fd.close()


    def commit(self):
        if self.verb:
            print "Committing changes"
        if isdarcs():
            util.chdircmd(self.wcpath, util.safeexec, tlacmd,
                          [cmd().commit, "-l", "-a", "-m", self.summary,
                           "--logfile", self.logfn,
                           "--delete-logfile"])
        elif isgit():
            util.chdircmd(self.wcpath, util.safeexec, tlacmd,
                          [cmd().commit, "-a", "-F", self.logfn])
	    os.unlink(self.logfn)
        else:
            if len(util.chdircmd(self.wcpath, util.getstdoutsafeexec, tlacmd, ['logs']))==0:
                util.chdircmd(self.wcpath, util.safeexec, tlacmd, [cmd().importcmd])
            else:
                util.chdircmd(self.wcpath, util.safeexec, tlacmd, [cmd().commit])
        
    def slashstrip(self, *args):
        retval = []
        for item in args:
            if not len(item):
                retval.append(item)
            if item[-1] == '/':
                item = item[:-1]
            retval.append(item)
        if len(args) == 1:
            return retval[0]
        return retval


    def makedirs(self, name, mode=0777):
        """makedirs(path [, mode=0777])

        Super-mkdir; create a leaf directory and all intermediate ones.
        Works like mkdir, except that any intermediate path segment (not
        just the rightmost) will be created if it does not exist.  This is
        recursive.

        (Modified from Python source)

        """
        head, tail = os.path.split(name)
        if not tail:
            head, tail = os.path.split(head)
        if head and tail and not os.path.exists(head):
            self.makedirs(head, mode)
        if self.verb:
            print "Created directory", name
        os.mkdir(name, mode)
        self.addtag(name)
