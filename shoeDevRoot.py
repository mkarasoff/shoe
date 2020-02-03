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
############################################################################
from shoeDev import *

class ShoeDevRoot(ShoeDev):

    ROOTDEV_KEYS=('root', 'device')
    DEVLIST_KEYS=('deviceList', 'device')

    AIOS_CFG_PATH='/upnp/desc/aios_device/aios_device.xml'

    def __init__(self, host, aiosCfg=None, loglvl=0, port=60006):

        super().__init__(host=host,
                        path=path,
                        port=port,
                        loglvl=loglvl)

        self._devs=None
        self._aiosCfg=aiosCfg
        return

    def init(self):
        if self.aiosCfg is None:
            self.aiosCfg=self.getCfg(self.AIOS_CFG_PATH)

        self.cfg=self._getRootDevCfg(self.aiosCfg)

        super().init()

        self._devs=self._getDevs(self.cfg)

        try:
            self.sysName=self.cfg[self.SYSNAME_KEYS]
        except KeyError:
            self.sysName = None
            self.log.warning("System name missing from root dev cfg")
        except:
            raise
        return

    def update(self):
        self.aisoCfg=None
        init()
        return

    def sendCmnd(self, cmnd, args, devName=None, svcName=None):
        dev=None
        svc=None

        if devName is None:
            cmndTree=self._findCmnd(cmnd)
            try:
                devName=list(cmndTree.keys())[0]
            except IndexError:
                raise ShoeDevUnknownParam("Cmnd %s not found" % cmnd)

        dev=self.getDev(devName)

        if svcName is None:
            svcNames=dev.findCmnd(cmnd)
            try:
                svcName=svcNames[0]
            except IndexError:
                raise ShoeDevUnknownParam("Cmnd %s not found" % cmnd)
            except:
                raise

        svc=self.getSvc(svcName)

        if svc is None:
            raise ShoeDevErr("No service found for cmnd %s" % cmnd)

        return svc.sendCmnd(cmnd, args)

    def getDev(self, devName):
        try:
            dev=self._devs[devName]
        except TypeError:
            raise ShoeDevErr("Root Device Not Initialized")
        except KeyError:
            raise ShoeDevErr("Dev %s not found" % devName)
        except:
            raise

        return dev

    def findCmnd(self, cmnd):
        devs={}

        if self._devs is None:
            raise ShoeDevErr("Root Device Not Initialized")

        for dev in self._devs.values():
            svcs=dev._findSvc(cmnd)
            if len(svcs) is not 0:
                devs[dev.name]=svcs

        return devs

    def getCmndTree(self):
        cmndTree={}

        if self._devs is None:
            raise ShoeDevErr("Root Device Not Initialized")

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
        devs={}

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

        for devCfg in devList:
            shoeDev=ShoeDev(devCfg=devCfg,
                            host=self.host,
                            port=self.port,
                            loglvl=self.loglvl)
            shoeDev.init()
            devs[shoeDev.name]=shoeDev

        return devs

    def _setSysName(self):
        self.sysName=None
