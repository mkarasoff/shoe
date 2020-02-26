##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeTestXml.py
#Class for XML unit data.
#
#
##########################################################################
#GPLv.3 License
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

from hashlib import md5
from collections import OrderedDict

class TestShoeXml(object):
    def __init__(self, xmlFile, md5hex=None, testPath='./test_shoe/xml_files/'):
        self.testPath=testPath
        self.xmlFile=xmlFile

        if (md5hex is not None):
            self._checkTestFile(md5hex)
        else:
            print("Warning: No MD5 sum given for the xml file.")
            print("If xml file was modified, it is undetected.")

        f=open(self.fileName, 'r')
        self.xmlStr=f.read().encode('utf-8')
        return

    def _checkTestFile(self, md5hex):
        md5obj=md5()
        f=open(self.fileName)
        md5obj.update(f.read().encode('utf-8'))
        digest=md5obj.hexdigest()
        if(md5hex != digest):
            errMsg=('Md5 sum mismatch for file %s'
                    '\ncalculated %s'
                    '\nexpected %s') % \
                        (self.fileName, digest, md5hex)
            raise TextXmlMd5Err(errMsg)
        return

    @property
    def fileName(self):
        return "%s%s" % (self.testPath, self.xmlFile)

class TextXmlMd5Err(Exception):
    pass
