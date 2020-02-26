##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testRenderDev.py
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
from .testShoeDev import *

class TestRendererDev(TestShoeDev):
    AV_TRANS_SVC_CFG={'controlURL': '/upnp/control/renderer_dvc/AVTransport', \
                     'serviceType': 'urn:schemas-upnp-org:service:AVTransport:1', \
                     'serviceId': 'urn:upnp-org:serviceId:AVTransport', \
                     'eventSubURL': '/upnp/event/renderer_dvc/AVTransport', \
                     'SCPDURL': '/upnp/scpd/renderer_dvc/AVTransport.xml'}

    CONN_MGR_SVC_CFG={'controlURL': '/upnp/control/renderer_dvc/ConnectionManager',\
                     'serviceType': 'urn:schemas-upnp-org:service:ConnectionManager:1',\
                     'serviceId': 'urn:upnp-org:serviceId:ConnectionManager',\
                     'eventSubURL': '/upnp/event/renderer_dvc/ConnectionManager',\
                     'SCPDURL': '/upnp/scpd/renderer_dvc/ConnectionManager.xml'}

    REND_CTRL_SVC_CFG={'controlURL': '/upnp/control/renderer_dvc/RenderingControl',\
                     'serviceType': 'urn:schemas-upnp-org:service:RenderingControl:1',\
                     'serviceId': 'urn:upnp-org:serviceId:RenderingControl',\
                     'eventSubURL': '/upnp/event/renderer_dvc/RenderingControl',\
                     'SCPDURL': '/upnp/scpd/renderer_dvc/RenderingControl.xml'}

    CFG={'manufacturerURL': 'http://www.denon.com',\
                'serviceList': {'service': [\
                    AV_TRANS_SVC_CFG,\
                    CONN_MGR_SVC_CFG,\
                    REND_CTRL_SVC_CFG]},\
                'modelName': 'HEOS 1', \
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': 'urn:schemas-upnp-org:device:MediaRenderer:1', \
                'friendlyName': 'Kitchen', \
                '{http://www.tencent.com}X_QPlay_SoftwareCapability': 'QPlay:1', \
                'UDN': 'uuid:ea6e8aa6-2442-11ea-978f-2e728ce88125',\
                'manufacturer': 'Denon'}

    NAME='MediaRenderer'

    def __init__(self):

        super().__init__(name=self.NAME,
                         udn=self.CFG['UDN'],
                         urn=self.CFG['deviceType'],
                         cfg=self.CFG)

        return
