#!/usr/bin/env python2.3
# arch-tag: tla load dirs main setup script
# Copyright (C) 2003 John Goerzen
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
# END OF COPYRIGHT #

from distutils.core import setup

setup(name = "tla_load_dirs",
      author = 'John Goerzen',
      author_email = 'jgoerzen@complete.org',
      packages = ['tla_support'],
      scripts = ['tla_load_dirs', 'darcs_load_dirs']
      #license = offlineimap.version.copyright + \
      #          ", Licensed under the GPL version 2"
)

