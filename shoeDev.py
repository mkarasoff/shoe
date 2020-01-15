##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeDev.py
#Class that manages HEOS device configuration.  It automatically
#instantiates and configures services.  It requires an existing device
#configuration, usually gathered from the Aiso XML file grabbed by a
#root device.
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
from shoeCfgXml import *

DEVNAME_KEY='deviceType'
DEVNAME_TAG='device'

SVCNAME_KEY='serviceId'
SVCNAME_TAG='serviceType'

SVC_LIST_KEYS=('serviceList', 'service')

class ShoeDev(ShoeCfgXml):

    UUID_KEY='UDN'

    def __init__(self, devCfg=None, dbug=0, host=None, path='', port=60006):

        super().__init__(host=host,
                        path=path,
                        port=port,
                        dbug=dbug)

        self.cfg=devCfg

        self.name=None

        self.svcs=None
        self.uuid=None
        return

    def init(self):
        if self.cfg is None:
            errStr="No device configuration for init"
            raise ShoeDevErr(errStr)

        try:
            self.name= self._getName()
        except ShoeDevUnkownParam as e:
            print("WARNING: Dev Name not found, setting to 'None'")
            if dbug > 2:
                print(str(e))
            self.name = None
        except:
            raise

        try:
            self.uuid=self._getUuid(self.cfg)
        except ShoeDevUnknownParam as e:
            print("WARNING: Cannot find UUID for Dev",
                    self.name)
            if dbug > 2:
                print(str(e))
            self.uuid=None
        except:
            raise

        try:
            self.svcs=self._getSvcs(self.cfg)
        except ShoeDevNoSvcs as e:
            if dbug > 0:
                print("INFO: No Services for Dev", self.name)
            if dbug > 2:
                print(str(e))
            self.svcs={}
        except:
            raise
       return

    def _getSvcs(self, devCfg):
        svcs={}

        if devCfg is None:
            errStr="No device configuration for service init"
            raise ShoeDevErr(errStr)

        unkownSvcIdx=0

        try:
            svcList=devCfg[self.SVC_LIST_KEYS[0]]\
                        [self.SVC_LIST_KEYS[1]]
        except KeyError:
            try:
                svcList=devCfg[self.SVC_LIST_KEYS[1]]
            except KeyError:
                raise ShoeDevNoSvcs()
            except:
                raise
        except:
            raise

        if not isinstance(svcList, list):
            svcList=[svcList,]

        for svcCfg in svcList:
            svc=shoeSvc(host=host,
                        path=path,
                        port=port,
                        dbug=dbug
                        cfg=svcCfg,
                        devObj=self)

            try:
                svc.init()
            except ShoeSvcNoScpd:
                print("WARNING: Service has no SCPD", svc.name)
                continue
            except:
                raise

            if svc.name == None:
                print("WARNING: No service name.  Setting name to:", unknownSvcIdx)
                svc.name=unkownSvcIdx
                unkownSvcIdx=unkownSvcIdx+1

            svcs[svc.name]=svc

        return svcs

    def _getName(self,
                cfg=self.cfg,
                typeIdKey=self.DEVNAME_KEY,
                typeIdTag=self.DEVNAME_TAG ):

        try:
            l=cfg[typeIdKey].split(':')
        except KeyError:
            errStr="No %s lbl found in devCfg" % typeIdKey
            raise ShoeDevUnknownParam(errStr)
        except:
            raise

        try:
            name=l[l.index(typeIdTag)+1]
        except (ValueError, IndexError):
            errStr="No dev lbl found %s" % l
            raise ShoeDevUnknownParam(errStr)
        except:
            raise

        return name

    def _getUuid(self, devCfg):
        if devCfg is None:
            raise ShoeDevErr("No dev config")

        try:
            udn=devCfg[self.UUID_KEY]
            udn=udn.split(':')
            uuid=udn[-1].replace('-','')
        except KeyError:
            errMsg="Cannot find UUID for dev" % self.devName
            raise ShoeDevUnknownParam(errMsg)
            pass
        except:
            raise

        return uuid

###############################Exceptions#################################
class ShoeDevErr(Exception):
    pass

class ShoeDevUnknownParam(Exception):
    pass

class ShoeDevNoSvcs(Exception):
    pass
###############################Unittests#################################
import unittest
from test_shoe import *
import time
import urllib.parse

class TestShoeDev(unittest.TestCase):
    GROUP_DEV_TAG='AiosServices'
    GROUP_SVC_TAG='GroupControl'

    ZONE_DEV_TAG='AiosServices'
    ZONE_SVC_TAG='ZoneControl'

    ACT_DEV_TAG='ACT-Denon'
    ACT_SVC_TAG='ACT'

    HOST='127.0.0.1'

    def setUp(self):
        testObj=TestAiosDev()
        self.testStr=testObj.xmlStr

        self.testParams=\
            {'group' : \
                    {'devTag': self.GROUP_DEV_TAG,\
                     'test': testObj.groupCtrl},\
             'zone' : \
                    {'devTag': self.ZONE_DEV_TAG,\
                     'test': testObj.zoneCtrl},\
             'act' : \
                    {'devTag': self.ACT_DEV_TAG,\
                     'test': testObj.act}}

        return

    def runTest(self):
        for test,params in list(self.testParams.items()):
            print("@@@@@@@@@@@@@@@@@Cheking zone: %s@@@@@@@@@@@@@@@@@@" % test)

            devTag=params['devTag']
            testParams=params['test']

            shoeDev=ShoeDev(self.HOST, devTag, dbug=10)
            shoeDev._getXmlText=self._getXmlText

            shoeDev.initDev()

            errMsg = "Mismatch for devices %s" % test
            self.assertEqual(testParams['dev'],
                            shoeDev.devCfg,
                            errMsg)

            errMsg = "Mismatch for uuid %s %s %s" % \
                    (test, testParams['uuid'], shoeDev.uuid)
            self.assertEqual(testParams['uuid'],
                            shoeDev.uuid,
                            errMsg)

        return

    def _getXmlText(self):
        return self.testStr
