#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testShoeDev.py
# Base class for test services
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
from .testShoeXml import *

class TestShoeSvc(TestShoeXml):
    def __init__(self,
                xmlFile, md5hex,
                devName,
                svcCfg):

        self.devName=devName
        self.cfg=svcCfg

        self.urn=svcCfg['serviceType']
        self.scpdPath=svcCfg['SCPDURL']
        self.cmndPath=svcCfg['controlURL']

        svcId=svcCfg['serviceId'].split(':')
        self.name=svcId[svcId.index('serviceId')+1]

        self.cmnds={}

        super().__init__(xmlFile, md5hex)
        return

    @property
    def xmlText(self):
        return self.xmlStr

    @property
    def svcCfg(self):
        return {}

    @property
    def xmlDict(self):
        return self.scpd

    @property
    def scpd(self):
        return {}

    @property
    def stateVarTbl(self):
        return {}

    @property
    def cmndTbl(self):
        return {}

    @property
    def cmndList(self):
        return list(self.cmndTbl.keys())
