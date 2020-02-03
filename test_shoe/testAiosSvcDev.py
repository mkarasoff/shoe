##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testAisoSvcDev.py
# Test data for Aios Svc Device
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
from .testShoeDev import *
from .testGroupCtrlSvc import *
from .testZoneCtrlSvc import *

class TestAiosSvcDev(TestShoeDev):
    ZONE_SVC_CFG={'controlURL': '/upnp/control/AiosServicesDvc/ZoneControl', \
                     'serviceType': 'urn:schemas-denon-com:service:ZoneControl:2', \
                     'serviceId': 'urn:denon-com:serviceId:ZoneControl', \
                     'eventSubURL': '/upnp/event/AiosServicesDvc/ZoneControl', \
                     'SCPDURL': '/upnp/scpd/AiosServicesDvc/ZoneControl.xml'}

    GROUP_SVC_CFG={'controlURL': '/upnp/control/AiosServicesDvc/GroupControl',\
                     'serviceType': 'urn:schemas-denon-com:service:GroupControl:1', \
                     'serviceId': 'urn:denon-com:serviceId:GroupControl', \
                     'eventSubURL': '/upnp/event/AiosServicesDvc/GroupControl', \
                     'SCPDURL': '/upnp/scpd/AiosServicesDvc/GroupControl.xml'}

    ERR_SVC_CFG={'controlURL': '/upnp/control/AiosServicesDvc/ErrorHandler', \
                     'serviceType': 'urn:schemas-denon-com:service:ErrorHandler:1', \
                     'serviceId': 'urn:denon-com:serviceId:ErrorHandler', \
                     'eventSubURL': '/upnp/event/AiosServicesDvc/ErrorHandler', \
                     'SCPDURL': '/upnp/scpd/AiosServicesDvc/ErrorHandler.xml'}

    DEV_CFG={'manufacturerURL': 'http://www.denon.com',\
                'serviceList': {'service': [\
                    ERR_SVC_CFG,\
                    ZONE_SVC_CFG,\
                    GROUP_SVC_CFG]},\
                'modelName': 'HEOS 1', \
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': 'urn:schemas-denon-com:device:AiosServices:1', \
                'friendlyName': 'AiosServices', \
                'UDN': 'uuid:ea6e8c04-2442-11ea-978f-2e728ce88125',\
                'manufacturer': 'Denon'}

    NAME='AiosServices'

    def __init__(self):

        super().__init__(name=self.NAME,
                         udn=self.DEV_CFG['UDN'],
                         urn=self.DEV_CFG['deviceType'],
                         cfg=self.DEV_CFG)

        self.svcs={'GroupControl' : TestGroupCtrlSvc(self.name, self.GROUP_SVC_CFG), \
                   'ZoneControl'  : TestZoneCtrlSvc(self.name, self.ZONE_SVC_CFG)}

        return
