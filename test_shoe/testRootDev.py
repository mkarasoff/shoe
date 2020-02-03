##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testRootDev.py
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
from .testShoeSvc import *
from .testAiosSvcDev import *
from .testActDev import *
from .testRendererDev import *
from .testMediaSrvDev import *
import copy

class TestRootDev(TestShoeXml):

    def __init__(self):
        xmlFile='aios_device.xml'
        md5hex='59bfffcde20bfc4cf437bdf7676de386'
        urlPath='/upnp/desc/aios_device/'

        self.url='%s%s' % (urlPath, xmlFile)

        super().__init__(xmlFile, md5hex)

        self.devs={ TestActDev.NAME         : TestActDev(),
                    TestAiosSvcDev.NAME     : TestAiosSvcDev(),
                    TestMediaSrvDev.NAME    : TestMediaSrvDev(),
                    TestRendererDev.NAME    : TestRendererDev()}

        self.xmlDict={'root': {'device': \
                {'manufacturerURL': 'http://www.denon.com',\
                'modelName': 'HEOS 1', \
                'deviceList': {'device': [\
                TestRendererDev.DEV_CFG, \
                TestAiosSvcDev.DEV_CFG, \
                TestMediaSrvDev.DEV_CFG, \
                TestActDev.DEV_CFG]}, \
                'serialNumber': 'ACJG9876543210', \
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': 'urn:schemas-denon-com:device:AiosDevice:1', \
                'friendlyName': 'Kitchen', \
                'UDN': 'uuid:ea6e883a-2442-11ea-978f-2e728ce88125',\
                'manufacturer': 'Denon'},\
                'specVersion': \
                    {'major': '1', \
                    'minor': '0'}}}

        return

    @property
    def svcs(self):
        svcs={}
        for dev in self.devs.values():
            svcs.update(dev.svcs)
        return svcs

    @property
    def cmnds(self):
        cmnds=[]
        for dev in self.devs.values():
            cmnds.extend(dev.cmnds)
        return cmnds
