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
import hashlib

class ShoeDev(ShoeCfgXml):
    DEVNAME_KEY='deviceType'
    DEVNAME_TAG='device'

    UUID_KEY='UDN'

    def __init__(self, devCfg=None, loglvl=None, host=None, port=60006):

        super().__init__(host=host,
                        port=port,
                        loglvl=loglvl)

        log=ConsoleLog(self.__class__.__name__, loglvl)

        self.cfg=devCfg
        self.name=None
        self._svcs=None
        self.uuid=None
        return

    def init(self):
        if self.cfg is None:
            errStr="No device configuration for init"
            raise ShoeDevErr(errStr)

        self.name= self._getName(self.cfg)

        try:
            self.uuid=self._getUuid(self.cfg)
        except ShoeDevUnknownParam as e:
            log.info("Cannot find UUID for Dev",
                       self.name)
            log.debug(str(e))
            self.uuid=None
        except:
            raise

        try:
            self._svcs=self._getSvcs(self.cfg)
        except ShoeDevNoSvcs as e:
                log.info("No Services for Dev", self.name)
                log.debug(str(e))
            self._svcs={}
        except:
            raise
        return

    def sendCmnd(self, cmnd, args, svcName=None):
        svc=None

        if svcName is None:
            svcNames=self.findCmnd(cmnd)
            try:
                svcName=svcNames[0]
            except IndexError:
                raise ShoeDevUnknownParam("Cmnd %s not found" % cmnd)
            except:
                raise

        svc = dev.getSvc(svcName)

        return svc.sendCmnd(cmnd, args)

    def findCmnd(self, cmnd):
        svcNames=[]
        for svc in self._svcs:
            try:
                cmnds=svc.cmnds
            except ShoeSvcNoTbl:
                log.info("Service %s has no cmnd table", self.svc.name)
                continue
            except:
                raise

            if cmnd in cmnds:
                rtnSvc.append(svc.name)

        return svcNames

    def getSvc(self, svcName):
        try:
            svc=self._svcs[svcName]
        except TypeError:
            raise ShoeDevErr("Device Not Initialized")
        except KeyError:
            raise ShoeDevErr("Service %s not found on %s" %
                                (svcName, self.name))
        except:
            raise

        return dev

    def _getSvcs(self, cfg):
        svcs={}

        if cfg is None:
            raise ShoeDevErr("No device configuration for service init")

        unkownSvcIdx=0

        try:
            svcList=cfg[self.SVC_LIST_KEYS[0]]\
                        [self.SVC_LIST_KEYS[1]]
        except KeyError:
            try:
                svcList=cfg[self.SVC_LIST_KEYS[1]]
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
                        port=port,
                        loglvl=loglvl,
                        svcCfg=svcCfg,
                        devInst=self)

            try:
                svc.init()
            except ShoeSvcNoScpd:
                log.warning("Service has no SCPD", svc.name)
                continue
            except:
                raise

            if svc.name == None:
                log.warning("No service name.  Setting name to:", unknownSvcIdx)
                svc.name=unkownSvcIdx
                unkownSvcIdx=unkownSvcIdx+1

            svcs[svc.name]=svc

        return svcs

    def _getName(self,
                cfg,
                typeIdKey=DEVNAME_KEY,
                typeIdTag=DEVNAME_TAG ):

        name=None
        cfgLine=[]
        try:
            cfgLine=cfg[typeIdKey].split(':')
        except KeyError:
            log.info("No %s entry found in config" % typeIdKey)
        except:
            raise

        try:
            name=cfgLine[l.index(typeIdTag)+1]
        except (ValueError, IndexError):
            log.info("No dev lbl found on cfg line %s" % cfgLine)
        except:
            raise

        if name is None:
            hashMd5=hashlib.md5(str(cfg).encode('utf-8'))
            name=hashMd5.hexdigest()
            log.warning("Nametag %s not found. Setting to %s" %
                    (typeIdTag, name))

        return name

    def _getUuid(self, cfg):
        try:
            udn=cfg[self.UUID_KEY]
            udn=udn.split(':')
            uuid=udn[-1].replace('-','')
        except KeyError:
            errMsg="Cannot find UUID for %s" % self.name
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

class TestShoeAiosDev(unittest.TestCase):
    HOST='127.0.0.1'

    def setUp(self):
        self.testRoot=TestRootDev()
        self.testDevNames=['AiosServices', 'ACT-Denon']

        return

    def runTest(self):
        for name in self.testDevNames:
            dev=self.testRoot.devs[name]
            self._runTest(dev)
        return

    def _devTest(self, dev):
        print("@@@@@@@@@@@@@@@@@@Dev Test %@@@@@@@@@@@@@@@@@@@@@@@"\
                % dev.name)

        shoeDev=ShoeDev(self.HOST, dev.cfg, loglvl=logging.DEBUG)

        shoeDev.initDev()

        self.assertEqual(dev.cfg, shoeDev.cfg)

        self.assertEqual(dev.uuid, shoeDev.uuid)

        self.assertEqual(dev.name, shoeDev.name)

        return
