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

class wc:
    """Object for a working copy."""

    def __init__(self, wcpath):
        self.wcpath = os.path.abspath(wcpath)
        if not self.wcverify():
            raise Exception, "%s is not a tla working copy" % self.wcpath

    def wcverify(self):
        try:
            util.chdircmd(self.wcpath, util.silentsafeexec, "tla", ['tree-version'], expected = 0)
        except util.ExecProblem:
            return 0
        return 1

    def gettaggingmethod(self):
        return util.chdircmd(self.wcpath, util.getstdoutsafeexec, "tla",
                             ['tagging-method'])[0].strip()
