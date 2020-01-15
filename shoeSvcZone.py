##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeZone.py
#Class impliments ZoneControl service specific functions.
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

class ShoeSvcZone(ShoeSvc):
    DEV_NAME='AiosServices'
    NAME='ZoneControl'

    def __init__(self, host, dbug=0, port=60006):
        super().__init__(host=host,
                         devTag=self.DEV_NAME,
                         svcTag=self.NAME,
                         dbug=dbug,
                         port=port)

        return
