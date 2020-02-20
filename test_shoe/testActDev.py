##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testActDev.py
# Test data for Act Device
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
from .testActSvc import *
from .testShoeDev import *

class TestActDev(TestShoeDev):
    CFG={'manufacturerURL': 'http://www.denon.com', \
                'modelName': 'HEOS 1', \
                'lanMac': '00:05:CD:00:00:01', \
                'locale': 'en_NA',\
                'serialNumber': 'ACJG9876543210', \
                'releaseType': 'Production',\
                'firmware_date': 'Sun 2019-01-01 00:00:00', \
                'moduleRevision': '4',\
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': 'urn:schemas-denon-com:device:ACT-Denon:1', \
                'productRevision': '3',\
                'wlanMac': '00:05:CD:00:00:00', \
                'friendlyName': 'ACT-Kitchen',\
                'firmwareRevision': '147202', \
                'firmware_version': '1.520.200',\
                'manufacturer': 'Denon', \
                'UDN': 'uuid:ea6e8d44-2442-11ea-978f-2e728ce88125',\
                'moduleType': 'Aios 4.0', \
                'DeviceID': 'AIOS:0001',
                'serviceList' : {'service': TestActSvc.CFG}}

    NAME='ACT-Denon'

    def __init__(self):

        super().__init__(name=self.NAME,
                         udn=self.CFG['UDN'],
                         urn=self.CFG['deviceType'],
                         cfg=self.CFG)

        self.svcs={'ACT' : TestActSvc(self.name)}

        return
