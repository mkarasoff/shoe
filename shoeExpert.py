##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeExpert.py
#Class that implements "Expert" CLI functions
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
from shoeOp import *

class ShoeExpert(ShoeOp):
    def __init__(self, shoeSys, loglvl=0):
        super().__init__(shoeSys, loglvl)
        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        return

    def getCmnds(self):
        svcCmnds=self.shoeSys.getCmnds()

        for svcName, cmnds in svcCmnds.items():
            self.log.debug("Device: ", svcName)
            for cmndName in cmnds:
                if len(self.shoeSys.findDev()) > 1:
                    cmndName="%s.%s" % (svcName, cmndName)
                self.log.debug("  ",cmndName)
            self.log.debug("\r\r")
        return
