##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeGroup.py
#Class impliments GroupControl service specific functions.
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
from shoeSvc import *
import copy

class ShoeSvcGroup(ShoeSvc):
    DEV_NAME='AiosServices'
    NAME='GroupControl'

    def __init__(self, host, loglvl=0, port=60006):
        super().__init__(host=host,
                         devTag=self.DEV_NAME,
                         svcTag=self.NAME,
                         loglvl=loglvl,
                         port=port)
        self.log=ConsoleLog(self.__class__.__name__, loglvl)

        return
