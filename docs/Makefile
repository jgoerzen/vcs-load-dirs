# arch-tag: documentation build system
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
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

MASTERBASE := tla_load_dirs
TOPNODE := tla_load_dirs
BASICDEPS := $(MASTERBASE).sgml
#DOINDEX := yes
DOINDEX := no
HTMLARGS := -s local
PSARGS := -s local=printlocal

all: ps
ps: $(MASTERBASE).ps
html: html/index.html
text: $(MASTERBASE).txt

manpages: tla_load_dirs.1
%.1: %.sgml
	docbook2man $<

include sgml-common/Makefile.common

realclean: clean
	-rm -rf *.links *.refs *.1
