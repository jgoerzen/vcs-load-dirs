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
    def __init__(self, wcobj, importdir):
        self.wcobj = wcobj
        self.importdir = os.path.abspath(importdir)
        self.actions = {'added': [], 'deleted': [], 'moved': []}

    def updateimportfiles(self):
        self.importfiles = util.maketree(self.importdir)

    def updatewcfiles(self):
        self.wcfiles = self.wcobj.gettree()

    def update(self):
        self.updateimportfiles()
        self.updatewcfiles()
        self.updatechangedfiles()

    def updatechangedfiles(self):
        self.addedfiles = [x for x in self.importfiles if not x in self.wcfiles]
        self.deletedfiles = [x for x in self.wcfiles if not x in self.importfiles]
        

    def main(self):
        while 1:
            self.update()
            if not (len(self.addedfiles) and len(self.deletedfiles)):
                break

            counter = 0
            while counter < max(len(self.addedfiles), len(self.deletedfiles)):
                addfile = ''
                delfile = ''
                if counter < len(self.addedfiles):
                    addfile = self.addedfiles[counter]
                if counter < len(self.deletedfiles):
                    delfile = self.deletedfiles[counter]
                print "%-3x %-35s %-35s" % (counter, delfile, addfile)
                counter += 1
            print "Syntax: (src dest [,src dest [,...]] to move, q to accept:"
            print "Command: ",
            try:
                for command in sys.stdin.readline().strip().split(','):
                    command = command.strip()
                    if command == 'q':
                        break
                    src, dest = command.split(' ')
                    src = int(src, 16)
                    dest = int(dest, 16)
                    self.mv(self.deletedfiles[src], self.addedfiles[dest])
            except:
                raise
                print "Error."

        self.catchup()
        
    def catchup(self):
        self.update()
        for file in self.addedfiles:
            self.addfile(file)
        for file in self.deletedfiles:
            self.delfile(file)

        util.copyfrom(self.importdir, self.wcobj.wcpath)
        self.writelog()
        self.wcobj.commit()

    def writelog(self):
        logfile = self.wcobj.makelog()
        fd = open(logfile, "w")
        fd.write("Summary: Imported %s\n" % self.importdir)
        fd.write("Keywords: \n\n")
        fd.write("Imported %s\ninto %s\n\n" %
                 (self.importdir, self.wcobj.gettreeversion()))
        for action in self.actions:
            if len(self.actions[action]):
                fd.write("To manage the import, the following files were %s:\n" \
                      % action)
                for item in self.actions[action]:
                    if len(item) == 2:
                        fd.write("%s -> %s\n" % (item[0], item[1]))
                    else:
                        fd.write(item[0] + "\n")
                fd.write("\n")
        fd.close()
        

    def addfile(self, file):
        self.wcobj.addtag(file)
        self.actions['added'].append((file,))

    def delfile(self, file):
        self.wcobj.deltag(file)
        self.wcobj.delfile(file)
        self.actions['deleted'].append((file,))
    
        
    def mv(self, src, dest):
        print "%s -> %s" % (src, dest)
        self.wcobj.movefile(src, dest)
        self.wcobj.movetag(src, dest)
        self.actions['moved'].append((src, dest))

        
