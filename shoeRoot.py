##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeRootDev.py
#Class that manages HEOS root device configuration.  It automatically
#instantiates other HEOS devices.  It requires an Aiso XML file to work
#will grab it from a HEOS device given by the 'host' variable.
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
##########################################################################
from shoeDev import *

class ShoeRoot(ShoeDev):
    ROOTDEV_KEYS=('root', 'device')
    DEVLIST_KEYS=('deviceList', 'device')
    INFO_EXCLUSION_KEYS=('deviceList', 'deviceType', 'serviceList')

    PREFERRED_DEVS=('ACT-Denon', 'AiosServices')

    AIOS_CFG_PATH='/upnp/desc/aios_device/aios_device.xml'

    def __init__(self,
                    host,
                    aiosCfg=None,
                    loglvl=ConsoleLog.WARNING,
                    port=60006):

        super().__init__(host=host,
                        loglvl=loglvl)

        self.name="root"
        self._devs=None
        self._aiosCfg=aiosCfg
        self.info={}
        return

    def setUp(self):
        if self._aiosCfg is None:
            self._aiosCfg=self.getCfg(self.AIOS_CFG_PATH)

        self.cfg=self._getRootDevCfg(self._aiosCfg)
        self.log.debug2("Root Cfg: %s" % self.cfg)

        super().setUp()

        self._devs=self._getDevs(self.cfg)
        self.log.debug("Devices: %s" % self._devs)

        self.info=self._getInfo(self.cfg, self._devs['ACT-Denon'].cfg)
        self.log.debug("Info: %s", self.info)

        return

    def update(self):
        self._aisoCfg=None
        setUp()
        return

    def getCmndParams(self, cmnd, svcName, devName):
        self.log.debug("cmnd %s, svcName %s, devName %s" %
                (cmnd, svcName, devName))
        dev=self.getDev(devName)
        svc=dev.getSvc(svcName)
        return svc.getCmndArgs(cmnd)

    def sendCmnd(self, cmnd, args=OrderedDict(), svcName=None, devName=None):
        self.log.debug("cmnd %s, args %s, svcName %s, devName %s" %
                (cmnd, args, svcName, devName))

        if args is None:
            args=OrderedDict()

        cmndDevTree=self.findCmnd(cmnd, svcName=svcName, devName=devName)

        if devName is None:
            try:
                devName=list(cmndDevTree.keys())[0]
            except IndexError:
                raise ShoeDevUnknownParam("Cmnd %s not found" % cmnd)

        try:
            svcNames=cmndDevTree[devName]
        except (KeyError):
            raise ShoeDevUnknownParam("Cmnd %s not found" % cmnd)

        if svcName is None:
            try:
                svcName=svcNames[0]
            except IndexError:
                raise ShoeDevUnknownParam("Cmnd %s not found" % cmnd)

        if svcName not in svcNames:
            raise ShoeDevUnknownParam("Cmnd %s not found" % cmnd)

        dev=self.getDev(devName)
        svc=dev.getSvc(svcName)

        return svc.sendCmnd(cmnd, args)

    def getDev(self, devName):
        self.log.debug("devName %s" %
                (devName))
        self.log.debug("devices %s" %
                (self._devs))
        try:
            dev=self._devs[devName]
        except TypeError:
            raise ShoeDevErr("Root Device Not Initialized")
        except KeyError:
            raise ShoeDevErr("Dev %s not found" % devName)
        except:
            raise

        return dev

    def findCmnd(self, cmnd, svcName=None, devName=None):
        devs=OrderedDict()

        self.log.debug("Find command %s devName %s svcName %s host %s",
                    cmnd, devName, svcName, self.host)

        if self._devs is None:
            raise ShoeDevErr("Root Device Not Initialized")

        if devName is None:
            devNames=self.devNames

        else:
            devNames=[devName,]

        self.log.debug("Looking for command %s devs %s",
                    cmnd, devNames)

        for name in devNames:
            self.log.debug("Looking for command %s dev %s",
                    cmnd, name)

            dev=self.getDev(name)
            svcNames=dev.findCmnd(cmnd)

            if len(svcNames) is not 0:
                self.log.debug("Found %s in %s for dev %s",
                        cmnd, svcNames, devName)
                if svcName is None:
                    devs[name]=svcNames
                    self.log.debug("Adding % as candidates for %s",
                            svcNames, cmnd)
                elif svcName in svcNames:
                    devs[name]=[svcName,]
                    self.log.debug("Found %s in %s",
                            svcName, svcNames)
                else:
                    self.log.debug("%s not found in %s",
                            svcName, devName)

        if(len(devs)==0):
            raise ShoeRootDevErr("Cmnd %s Not Found" % cmnd)

        return devs

    def getCmndTree(self):
        cmndTree={}

        if self._devs is None:
            raise ShoeDevErr("Root Device Not Initialized")

        self.log.debug("Devices: %s", self._devs.items())

        for devName,dev in self._devs.items():
            try:
                svcNames=dev._svcs.keys()
            except ValueError:
                raise ShoeDevErr("Device %s not properly initialized" %
                                    devName)
            except:
                raise

            cmndTree[devName]={}

            for svcName in svcNames:
                svc=dev.getSvc(svcName)
                cmndTree[devName][svcName]=svc.cmnds

        return cmndTree

    @property
    def devNames(self):
        return self._devs.keys()

    def _getInfo(self, rootCfg, actDevCfg):
        info=OrderedDict()
        for key, value in rootCfg.items():
            if key not in self.INFO_EXCLUSION_KEYS:
                info[key]=value

        rootCfgKeys=info.keys()

        for key, value in actDevCfg.items():
            if key not in self.INFO_EXCLUSION_KEYS and\
                    key not in rootCfgKeys:
                        info[key]=value
        return info

    def _getRootDevCfg(self, aiosCfg):

        try:
            rootDevCfg=\
                aiosCfg[self.ROOTDEV_KEYS[0]]\
                            [self.ROOTDEV_KEYS[1]]
        except KeyError:
            raise ShoeDevErr("Bad Aios Device XML File")
        except:
            raise

        return rootDevCfg

    def _getDevs(self, rootDevCfg):

        if rootDevCfg is None:
            raise ShoeDevErr("No root configuration")

        try:
            devList=\
                rootDevCfg[self.DEVLIST_KEYS[0]]\
                            [self.DEVLIST_KEYS[1]]
        except KeyError:
            devList=[]
            pass
        except:
            raise

        self.log.debug("Dev List %s", devList)

        #Init devices
        shoeDevs={}
        for devCfg in devList:
            shoeDev=ShoeDev(cfg=devCfg,
                            host=self.host,
                            port=self.port,
                            loglvl=self.loglvl)
            shoeDev.setUp()
            shoeDevs[shoeDev.name]=shoeDev

        #Set Ordering
        rtnDevs=OrderedDict()

        for devName in self.PREFERRED_DEVS:
            rtnDevs[devName]=shoeDevs[devName]

        rtnDevs.update(
                [(devName, shoeDevs[devName]) for devName in shoeDevs.keys()
                    if devName not in self.PREFERRED_DEVS])

        return rtnDevs

    def cmnds(self):
        return self.getCmndTree()

###############################Exceptions#################################
class ShoeRootDevErr(Exception):
    pass

##############################UNIT TESTS########################################
from test_shoe import *

class TestShoeRoot(TestShoeHttp):

    def setUp(self):
        super().setUp()
        self.reply=None
        self.port=60006
        self.host='127.0.0.1'
        self.rootDev=ShoeRoot(host=self.host, port=self.port, loglvl=logging.DEBUG)
        self.testCbFunc=self._setUp
        self.httpTest()
        self.testCbFunc=self._sendTestMsgs
        return

    def _setUp(self):
        self.rootDev.setUp()
        return

    def _sendTestMsgs(self):
        cmnd = self.cmnd
        print("Cmnd %s" % self.cmnd)
        self.reply=self.rootDev.sendCmnd(cmnd.name, cmnd.args, cmnd.svcName, cmnd.devName)
        return

#Check a command within range.
class TestShoeRootCmnds(TestShoeRoot):
    def runTest(self):
        for cmnd in self.testRootDev.cmnds:
            print("^^^^^^^^TestShoeInRange %s %s %s^^^^^^^^" %
                    (cmnd.svcName, cmnd.devName, cmnd))
            self.cmnd=cmnd
            self.httpTest(cmnd)

            self.assertEqual(self.reply.args,
                            cmnd.rtn)

            #self.assertEqual(self.reply.cmnd,
            #             cmnd.name + "Response")
        return
