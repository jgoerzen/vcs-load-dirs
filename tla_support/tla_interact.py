# arch-tag: tla interaction 1062537893
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

import sys, os
import util

class interaction:
    def __init__(self, wcobj, importdir, docommit, log = '', verbose = 0):
        self.wcobj = wcobj
        self.importdir = os.path.abspath(importdir)
        self.log = log
        self.docommit = docommit
        self.verb = verbose

    def updateimportfiles(self):
        if self.verb:
            print "Scanning upstream tree..."
        self.importfiles = util.maketree(self.importdir)

    def updatewcfiles(self):
        if self.verb:
            print "Scanning working copy tree..."
        self.wcfiles = self.wcobj.gettree()

    def update(self):
        self.updatewcfiles()
        self.updatechangedfiles()

    def updatechangedfiles(self):
        if self.verb:
            print "Calculating changes..."
        wcfilehash = {}
        for x in self.wcfiles:
            wcfilehash[x] = 1
        importfilehash = {}
        for x in self.importfiles:
            importfilehash[x] = 1
        
        self.addedfiles = [x for x in self.importfiles if not wcfilehash.has_key(x)]
        self.deletedfiles = [x for x in self.wcfiles if not importfilehash.has_key(x)]
        

    def main(self):
        def readloop():
            for command in sys.stdin.readline().strip().split(','):
                command = command.strip()
                if command == 'q':
                    return 0
                if command == 'r':
                    return 1
                src, dest = command.split(' ')
                src = int(src, 16)
                dest = int(dest, 16)
                self.mv(self.deletedfiles[src], self.addedfiles[dest])
            return 1

        self.updateimportfiles()
        needsupdate = 1
        
        while 1:
            self.update()
            if not (len(self.addedfiles) and len(self.deletedfiles)):
                # Just ran update; don't do it again.
                needsupdate = 0
                break

            counter = 0
            print "%3s %-35s %3s %-35s" % ('Num', 'Source Files', 'Num',
                                             'Destination Files',)
            print "%s %s %s %s" % ("-" * 3, "-" * 35, "-" * 3, "-" * 35)
            while counter < max(len(self.addedfiles), len(self.deletedfiles)):
                addfile = ''
                delfile = ''
                if counter < len(self.addedfiles):
                    addfile = self.addedfiles[counter]
                if counter < len(self.deletedfiles):
                    delfile = self.deletedfiles[counter]
                print "%3x %-35s %3x %-35s" % (counter, delfile, counter, addfile)
                counter += 1
            print "Syntax: src dest [,src dest [,...]] to move, q to accept, r to redraw:"
            sys.stdout.write("Command: ")
            sys.stdout.flush()
            try:
                if not readloop():
                    break
            except ValueError:
                print "Error handling input; please try again."

        self.catchup(needsupdate)
        
    def catchup(self, needsupdate = 1):
        if self.verb:
            print " *** Processing changes."
        if needsupdate:
            self.update()
        if self.verb:
            print "Deleting %d files" % len(self.deletedfiles)
        for file in self.deletedfiles:
            self.delfile(file)

        if self.verb:
            print "Copying upstream directory to working copy..."
        util.copyfrom(self.importdir, self.wcobj.wcpath)

        if self.verb:
            print "Adding %d files" % len(self.addedfiles)
        for file in self.addedfiles:
            self.addfile(file)
        self.writelog()
        if self.docommit:
            self.wcobj.commit()

    def writelog(self):
        logfile = self.wcobj.makelog()
        fd = open(logfile, "w")
        fd.write("Summary: Imported %s\n" % os.path.basename(self.importdir))
        fd.write("Keywords: \n\n")
        fd.write("Imported %s\ninto %s\n\n" %
                 (os.path.basename(self.importdir),
                  self.wcobj.gettreeversion()))
        fd.write(self.log)
        fd.close()
        

    def addfile(self, file):
        self.wcobj.addtag(file)

    def delfile(self, file):
        self.wcobj.deltag(file)
        self.wcobj.delfile(file)
    
        
    def mv(self, src, dest):
        print "%s -> %s" % (src, dest)
        self.wcobj.movefile(src, dest)
        self.wcobj.movetag(src, dest)

