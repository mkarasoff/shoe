##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testAiosDev.py
#Class for unittest data generated from the aios_device.xml used for the
#root device.
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
from .shoeTestXml import *
import copy

class TestAiosDev(ShoeTestXml):
    def __init__(self):
        xmlFile='aios_device.xml'
        md5hex='59bfffcde20bfc4cf437bdf7676de386'
        urlPath='/upnp/desc/aios_device/'

        self.url='%s%s' % (urlPath, xmlFile)

        super(TestAiosDev, self).__init__(xmlFile, md5hex)

        name='Kitchen'

        zoneCtrlSvc={'controlURL': '/upnp/control/AiosServicesDvc/ZoneControl', \
                     'serviceType': 'urn:schemas-denon-com:service:ZoneControl:2', \
                     'serviceId': 'urn:denon-com:serviceId:ZoneControl', \
                     'eventSubURL': '/upnp/event/AiosServicesDvc/ZoneControl', \
                     'SCPDURL': '/upnp/scpd/AiosServicesDvc/ZoneControl.xml'}

        groupCtrlSvc={'controlURL': '/upnp/control/AiosServicesDvc/GroupControl',\
                     'serviceType': 'urn:schemas-denon-com:service:GroupControl:1', \
                     'serviceId': 'urn:denon-com:serviceId:GroupControl', \
                     'eventSubURL': '/upnp/event/AiosServicesDvc/GroupControl', \
                     'SCPDURL': '/upnp/scpd/AiosServicesDvc/GroupControl.xml'}

        actSvc={'controlURL': '/ACT/control', \
                    'serviceType': 'urn:schemas-denon-com:service:ACT:1', \
                    'serviceId': 'urn:denon-com:serviceId:ACT', \
                    'eventSubURL': '/ACT/event',\
                    'SCPDURL': '/ACT/SCPD.xml'}

        devTags = { 'act'      : 'ACT-Denon',
                    'aios'     : 'AiosServices',
                    'mediaSrv' : 'MediaServer',
                    'renderer' : 'MediaRenderer',
                    'root'     : 'AiosDevice'
                    }

        self.act={}
        self.act['urn']='urn:schemas-denon-com:device:ACT-Denon:1'
        self.act['name']='ACT-Kitchen'
        self.act['udn']='uuid:ea6e8d44-2442-11ea-978f-2e728ce88125'
        self.act['uuid']='ea6e8d44244211ea978f2e728ce88125'
        self.act['svc']=actSvc
        self.act['sysName']=name

        self.act['info']={'manufacturerURL': 'http://www.denon.com', \
                'modelName': 'HEOS 1', \
                'lanMac': '00:05:CD:00:00:01', \
                'locale': 'en_NA',\
                'serialNumber': 'ACJG9876543210', \
                'releaseType': 'Production',\
                'firmware_date': 'Sun 2019-01-01 00:00:00', \
                'moduleRevision': '4',\
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': self.act['urn'], \
                'productRevision': '3',\
                'wlanMac': '00:05:CD:00:00:00', \
                'friendlyName': self.act['name'],\
                'firmwareRevision': '147202', \
                'firmware_version': '1.520.200',\
                'manufacturer': 'Denon', \
                'UDN': self.act['udn'],\
                'moduleType': 'Aios 4.0', \
                'DeviceID': 'AIOS:0001'}

        self.act['dev']=copy.deepcopy(self.act['info'])
        self.act['dev']['serviceList'] = {'service': actSvc}

        self.aios={}
        self.aios['urn']='urn:schemas-denon-com:device:AiosServices:1'
        self.aios['name']='AiosServices'
        self.aios['udn']='uuid:ea6e8c04-2442-11ea-978f-2e728ce88125'
        self.aios['uuid']='ea6e8c04244211ea978f2e728ce88125'
        self.aios['sysName']=name
        self.aios['dev']={'manufacturerURL': 'http://www.denon.com',\
                'serviceList': {'service': [\
                    {'controlURL': '/upnp/control/AiosServicesDvc/ErrorHandler', \
                     'serviceType': 'urn:schemas-denon-com:service:ErrorHandler:1', \
                     'serviceId': 'urn:denon-com:serviceId:ErrorHandler', \
                     'eventSubURL': '/upnp/event/AiosServicesDvc/ErrorHandler', \
                     'SCPDURL': '/upnp/scpd/AiosServicesDvc/ErrorHandler.xml'},\
                    zoneCtrlSvc,\
                    groupCtrlSvc]},\
                'modelName': 'HEOS 1', \
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': self.aios['urn'], \
                'friendlyName': self.aios['name'], \
                'UDN': self.aios['udn'],\
                'manufacturer': 'Denon'}

        self.groupCtrl=copy.deepcopy(self.aios)
        self.groupCtrl['svc']=groupCtrlSvc
        self.zoneCtrl=copy.deepcopy(self.aios)
        self.zoneCtrl['svc']=zoneCtrlSvc

        self.mediaSrv={}
        self.mediaSrv['sysName']=name
        self.mediaSrv['dev']={'manufacturerURL': 'http://www.denon.com',\
                'serviceList': {'service': [\
                    {'controlURL': '/upnp/control/ams_dvc/ContentDirectory', \
                     'serviceType': 'urn:schemas-upnp-org:service:ContentDirectory:1', \
                     'serviceId': 'urn:upnp-org:serviceId:ContentDirectory', \
                     'eventSubURL': '/upnp/event/ams_dvc/ContentDirectory', \
                     'SCPDURL': '/upnp/scpd/ams_dvc/ContentDirectory.xml'}, \
                    {'controlURL': '/upnp/control/ams_dvc/ConnectionManager', \
                     'serviceType': 'urn:schemas-upnp-org:service:ConnectionManager:1',\
                     'serviceId': 'urn:upnp-org:serviceId:ConnectionManager',\
                     'eventSubURL': '/upnp/event/ams_dvc/ConnectionManager',\
                     'SCPDURL': '/upnp/scpd/ams_dvc/ConnectionManager.xml'}]},\
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

        self.renderer={}
        self.renderer['sysName']=name
        self.renderer['dev']={'manufacturerURL': 'http://www.denon.com',\
                'serviceList': {'service': [\
                    {'controlURL': '/upnp/control/renderer_dvc/AVTransport', \
                     'serviceType': 'urn:schemas-upnp-org:service:AVTransport:1', \
                     'serviceId': 'urn:upnp-org:serviceId:AVTransport', \
                     'eventSubURL': '/upnp/event/renderer_dvc/AVTransport', \
                     'SCPDURL': '/upnp/scpd/renderer_dvc/AVTransport.xml'},\
                    {'controlURL': '/upnp/control/renderer_dvc/ConnectionManager',\
                     'serviceType': 'urn:schemas-upnp-org:service:ConnectionManager:1',\
                     'serviceId': 'urn:upnp-org:serviceId:ConnectionManager',\
                     'eventSubURL': '/upnp/event/renderer_dvc/ConnectionManager',\
                     'SCPDURL': '/upnp/scpd/renderer_dvc/ConnectionManager.xml'},\
                    {'controlURL': '/upnp/control/renderer_dvc/RenderingControl',\
                     'serviceType': 'urn:schemas-upnp-org:service:RenderingControl:1',\
                     'serviceId': 'urn:upnp-org:serviceId:RenderingControl',\
                     'eventSubURL': '/upnp/event/renderer_dvc/RenderingControl',\
                     'SCPDURL': '/upnp/scpd/renderer_dvc/RenderingControl.xml'}]},\
                'modelName': 'HEOS 1', \
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': 'urn:schemas-upnp-org:device:MediaRenderer:1', \
                'friendlyName': 'Kitchen', \
                '{http://www.tencent.com}X_QPlay_SoftwareCapability': 'QPlay:1', \
                'UDN': 'uuid:ea6e8aa6-2442-11ea-978f-2e728ce88125',\
                'manufacturer': 'Denon'}

        self.xmlDict={'root': {'device': \
                {'manufacturerURL': 'http://www.denon.com',\
                'modelName': 'HEOS 1', \
                'deviceList': {'device': [\
                self.renderer['dev'], \
                self.aios['dev'], \
                self.mediaSrv['dev'], \
                self.act['dev']]}, \
                'serialNumber': 'ACJG9876543210', \
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': 'urn:schemas-denon-com:device:AiosDevice:1', \
                'friendlyName': name, \
                'UDN': 'uuid:ea6e883a-2442-11ea-978f-2e728ce88125',\
                'manufacturer': 'Denon'},\
                'specVersion': \
                    {'major': '1', \
                    'minor': '0'}}}

        self.infoFmt=\
            "deviceType       : urn:schemas-denon-com:device:ACT-Denon:1\n"\
            "manufacturer     : Denon\n"\
            "manufacturerURL  : http://www.denon.com\n"\
            "modelName        : HEOS 1\n"\
            "modelNumber      : DWS-1000 4.0\n"\
            "serialNumber     : ACJG9876543210\n"\
            "UDN              : uuid:ea6e8d44-2442-11ea-978f-2e728ce88125\n"\
            "DeviceID         : AIOS:0001\n"\
            "firmwareRevision : 147202\n"\
            "firmware_date    : Sun 2019-01-01 00:00:00\n"\
            "firmware_version : 1.520.200\n"\
            "lanMac           : 00:05:CD:00:00:01\n"\
            "locale           : en_NA\n"\
            "moduleRevision   : 4\n"\
            "moduleType       : Aios 4.0\n"\
            "productRevision  : 3\n"\
            "releaseType      : Production\n"\
            "wlanMac          : 00:05:CD:00:00:00\n"\
            "devName          : ACT-Kitchen\n"\

        return
