# arch-tag: tla version-specific command execution
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
tlasyn = None
tlaobj = None
tlacmd = None
darcs = False

def setdarcs(x):
    global darcs, tlacmd
    if (x):
        tlacmd = "darcs"
    else:
        tlacmd = "tla"
    print " TLACMD: ", tlacmd
    darcs = x

def isdarcs():
    global darcs
    return darcs

def gettlasyntax():
    global tlasyn, tlaobj
    if tlasyn != None:
        return tlasyn

    if isdarcs():
        tlasyn = 'darcs'
        tlaobj = Darcs()
    elif util.getstdoutsafeexec('tla', ['-V'])[0].find('tla-1.0.') != -1:
        tlasyn = '1.0'
        tlaobj = Tla10()
    elif util.getstdoutsafeexec('tla', ['-V'])[0].find('tla-1.1.') != -1:
        tlasyn = '1.1'
        tlaobj = Tla11()
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

class Tla11:
    tagging_method = 'id-tagging-method'
    add = ['add']
    move = 'move'
    delete = 'delete'
    update = 'update'
    replay = 'replay'
    commit = 'commit'

class Tla13:
    tagging_method = 'id-tagging-method'
    add = ['add-id']
    move = 'movei-id'
    delete = 'delete-id'
    update = 'update'
    replay = 'replay'
    commit = 'commit'

class Darcs:
    tagging_method = None
    add = ['add', '--case-ok']
    move = 'mv'
    delete = None
    update = 'pull'
    replay = 'pull'
    commit = 'record'

def cmd():
    global tlaobj
    gettlasyntax()
    return tlaobj
