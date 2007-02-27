# arch-tag: tla version-specific command execution
# Copyright (C) 2003-2006 John Goerzen
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
tlasyn = None
tlaobj = None
tlacmd = None
darcs = False
svk = False
git = False

def setscm(x):
    global darcs, svk, git, tlacmd
    if (x == "darcs"):
        tlacmd = "darcs"
        darcs = True
    elif (x == "baz"):
        tlacmd = "baz"
    elif (x == "tla"):
        tlacmd = "tla"
    elif (x == "git"):
        tlacmd = "git"
        git = True
    else:
        tlacmd = "svk"
        svk = True
    print " TLACMD: ", tlacmd

def isdarcs():
    global darcs
    return darcs

def issvk():
    global svk
    return svk

def isgit():
    global git
    return git

def gettlasyntax():
    global tlasyn, tlaobj
    if tlasyn != None:
        return tlasyn

    if isdarcs():
        tlasyn = 'darcs'
        tlaobj = Darcs()
    elif isgit():
        tlasyn = 'Git'
        tlaobj = Git()
    elif util.getstdoutsafeexec(tlacmd, ['-V'])[0].find('tla-1.0.') != -1:
        tlasyn = '1.0'
        tlaobj = Tla10()
    elif util.getstdoutsafeexec(tlacmd, ['-V'])[0].find('tla-1.1.') != -1:
        tlasyn = '1.1'
        tlaobj = Tla11()
    elif util.getstdoutsafeexec(tlacmd, ['-V'])[0].find('tla-1.3.') != -1:
        tlasyn = '1.3'
        tlaobj = Tla13()
    elif util.getstdoutsafeexec(tlacmd, ['-V'])[0].find('baz Bazaar version 1.4.') != -1:
        tlasyn = 'baz1.4'
        tlaobj = Baz14()        
    elif util.getstdoutsafeexec(tlacmd, ['-V'])[0].find('This is svk') != -1:
        tlasyn = 'svk'
        tlaobj = Svk()
    else:
        tlasyn = '1.3'
        tlaobj = Tla13()
    return tlasyn

class Tla10:
    tagging_method = 'tagging-method'
    add = ['add-tag']
    move = 'move-tag'
    delete = 'delete-tag'
    update = 'update --in-place .'
    replay = 'replay --in-place .'
    commit = 'commit'
    importcmd = 'import'

class Tla11:
    tagging_method = 'id-tagging-method'
    add = ['add']
    move = 'move'
    delete = 'delete'
    update = 'update'
    replay = 'replay'
    commit = 'commit'
    importcmd = 'import'

class Tla13:
    tagging_method = 'id-tagging-method'
    add = ['add-id']
    move = 'move-id'
    delete = 'delete-id'
    update = 'update'
    replay = 'replay'
    commit = 'commit'
    importcmd = 'import'

class Baz14:
    tagging_method = 'id-tagging-method'
    add = ['add-id']
    move = 'move-id'
    delete = 'delete-id'
    update = 'update'
    replay = 'replay'
    commit = 'commit'    
    importcmd = 'import'

class Darcs:
    tagging_method = None
    add = ['add', '--case-ok']
    move = 'mv'
    delete = None
    update = 'pull'
    replay = 'pull'
    commit = 'record'

class Git:
    tagging_method = None
    add = ['add']
    move = 'mv'
    delete = 'rm'
    update = 'checkout'
    replay = None 
    commit = 'commit'

class Svk:
	tagging_method = None
	add = ['add']
	move = 'mv'
	delete = 'rm'
	update = 'pull'
	replay = 'pull'
	commit = 'commit'

def cmd():
    global tlaobj
    gettlasyntax()
    return tlaobj