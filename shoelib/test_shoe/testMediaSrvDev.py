##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testMediaSrvDev.py
# Test data for Media Server Device
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

class TestMediaSrvDev(TestShoeDev):
    CONTENT_DIR_SVC_CFG={'controlURL': '/upnp/control/ams_dvc/ContentDirectory', \
                     'serviceType': 'urn:schemas-upnp-org:service:ContentDirectory:1', \
                     'serviceId': 'urn:upnp-org:serviceId:ContentDirectory', \
                     'eventSubURL': '/upnp/event/ams_dvc/ContentDirectory', \
                     'SCPDURL': '/upnp/scpd/ams_dvc/ContentDirectory.xml'}

    CONN_MGR_SVC_CFG={'controlURL': '/upnp/control/ams_dvc/ConnectionManager', \
                     'serviceType': 'urn:schemas-upnp-org:service:ConnectionManager:1',\
                     'serviceId': 'urn:upnp-org:serviceId:ConnectionManager',\
                     'eventSubURL': '/upnp/event/ams_dvc/ConnectionManager',\
                     'SCPDURL': '/upnp/scpd/ams_dvc/ConnectionManager.xml'}

    CFG={'manufacturerURL': 'http://www.denon.com',\
                'serviceList': {'service': [\
                    CONTENT_DIR_SVC_CFG, \
                    CONN_MGR_SVC_CFG]},\
                'modelName': 'HEOS 1', \
                'serialNumber': 'ACJG9876543210', \
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': 'urn:schemas-upnp-org:device:MediaServer:1', \
                'friendlyName': 'Kitchen',\
                'modelDescription': ('Shares User defined folders and files to '
                            'other Universal Plug and Play media devices.'), \
                'UDN': 'uuid:e86e0a10-01ee-9e66-983c-420eb6b2042f', \
                'manufacturer': 'Denon',\
                ('{urn:schemas-avegasystems-com:media-server:metadata-1-0:DIDL-Lite}'
                    'X_VirtualServersSupported'): 'True'}

    NAME='MediaServer'

    def __init__(self):

        super().__init__(name=self.NAME,
                         udn=self.CFG['UDN'],
                         urn=self.CFG['deviceType'],
                         cfg=self.CFG)

        return
