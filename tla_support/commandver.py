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


def gettlasyntax():
    global tlasyn, tlaobj
    if tlasyn != None:
        return tlasyn

    verstring = util.getstdoutsafeexec('tla', ['-V'])[0]
    if verstring.find('tla-1.0.') != -1 and \
            verstring.find('+1.1-candidate') == -1:
        tlasyn = '1.0'
        tlaobj = Tla10()
    else:
        tlasyn = '1.1'
        tlaobj = Tla11()
    return tlasyn

class Tla10:
    tagging_method = 'tagging-method'
    add = 'add-tag'
    move = 'move-tag'
    delete = 'delete-tag'
    update = 'update --in-place .'
    replay = 'replay --in-place .'

class Tla11:
    tagging_method = 'id-tagging-method'
    add = 'add'
    move = 'move'
    delete = 'delete'
    update = 'update'
    replay = 'replay'

def cmd():
    global tlaobj
    gettlasyntax()
    return tlaobj
