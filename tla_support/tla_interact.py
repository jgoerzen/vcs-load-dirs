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

import sys

class interaction:
    def __init__(self, wcobj, importdir):
        self.wcobj = wcobj
        self.importdir = importdir

    def updateimportfiles(self):
        self.importfiles = util.maketree(importdir)

    def updatewcfiles(self):
        self.wcfiles = wcobj.gettree()

    def update(self):
        self.updateimportfiles(self)
        self.updatewcfiles(self)
        self.updatechangedfiles(self)

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
                print "%-3x %-35s %-35s" % (counter, addfile, delfile)
            print "Syntax: (src dest [,src dest [,...]] to move, q to accept:"
            print "Command: ",
            try:
                for command in sys.stdin.readline().strip().split(','):
                    if command == 'q':
                        break
                    src, dest = command.split(' ')
                    src = int(src, 16)
                    dest = int(dest, 16)
                    self.mv(self.addedfiles[src], self.deletedfiles[dest])
            except:
                print "Error."

        catchup(wcobj, addedfiles, deletedfiles)
        
    def mv(self, src, dest):
        print "Fake mv: %s -> %s" % src, dest
