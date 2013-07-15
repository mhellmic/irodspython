# Copyright (c) 2009, University of Liverpool
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
#
# Author       : Jerome Fuselier
# Creation     : November, 2010

"""Some text parsers (for STC mainly)"""

import re


class PythonParser(object):
    """Some specific parsers for a Python script"""

    def __init__(self):
        self.p_method_name = re.compile('def\s+(\w+)\s*\([\w+,\s]*\)\w*:')

    def find_method_name(self, method_name, text):
        """Return a couple of indices (start and end) of the method_name found
        in the text"""
        p_method_name = re.compile('def\s+(%s)\s*\([\w+,\s]*\)\w*:' %
                                   method_name)
        match = p_method_name.search(text)
        if match:
            return match.span(1)

    def get_method_name(self, line):
        """Return the name of the method found in the line"""
        match = self.p_method_name.search(line)

        if match:
            return match.group(1)
        else:
            return ""
