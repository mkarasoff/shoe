##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testShoeDev.py
# Base class for test devices
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

class TestShoeDev():
    def __init__(self, name, urn, udn, cfg):
        self.name=name
        self.urn=urn
        self.udn=udn
        self.uuid=udn.split(':')[-1].replace('-','')
        self.cfg=cfg

        self.svcs={}

        return

    @property
    def cmnds(self):
        cmnds=[]
        for svc in self.svcs.values():
            cmnds.extend(svc.cmnds.values())
        return cmnds
