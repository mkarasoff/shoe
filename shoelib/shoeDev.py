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
from .shoeSvc import *
import hashlib

class ShoeDev(ShoeSvc):
    DEVNAME_KEY='deviceType'
    DEVNAME_TAG='device'

    UUID_KEY='UDN'

    def __init__(self,
                cfg=None,
                path=None,
                fileName=None,
                loglvl=ConsoleLog.WARNING,
                host=None,
                port=60006,
                force=False):

        super().__init__(host=host,
                        port=port,
                        cfg=cfg,
                        loglvl=loglvl,
                        fileName=fileName,
                        path=path,
                        force=force)

        self.log.debug("Path %s SelfPath %s", path, self.path)

        self.name=None
        self._svcs=None
        self.uuid=None
        return

    def setUp(self):
        if self.cfg is None:
            errStr="No device configuration for setUp"
            raise ShoeDevErr(errStr)

        self.name= self._getName(self.cfg)

        self.log.debug("Dev Name %s" % self.name)

        try:
            self.uuid=self._getUuid(self.cfg)
        except ShoeDevUnknownParam as e:
            self.log.info("Cannot find UUID for Dev: %s" %
                       self.name)
            self.log.debug(str(e))
            self.uuid=None
        except:
            raise

        self.log.debug("UUID %s" % self.uuid)

        try:
            self._svcs=self._getSvcs(self.cfg)
        except ShoeDevNoSvcs as e:
            self.log.info("No Services for Dev %s" % self.name)
            self.log.debug(str(e))
            self._svcs={}
        except:
            raise

        self.log.debug("%s Services %s" % (self.name, self._svcs))
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
        rtnSvcs=[]
        for svcName, svc in self._svcs.items():
            try:
                cmnds=svc.cmnds
            except ShoeSvcNoTbl:
                self.log.info("Service %s has no cmnd table"
                        % self.svc.name)
                continue
            except:
                raise

            if cmnd in cmnds:
                rtnSvcs.append(svc.name)

        return rtnSvcs

    def getSvc(self, svcName):
        self.log.debug("%s Service Name Req: %s" %(self.name, svcName))
        self.log.debug("%s Services: %s" %(self.name, self._svcs))

        try:
            svc=self._svcs[svcName]
        except TypeError:
            raise ShoeDevErr("Device Not Initialized")
        except KeyError:
            raise ShoeDevErr("Service %s not found on %s" %
                                (svcName, self.name))
        except:
            raise

        return svc

    def _getSvcs(self, cfg):
        svcs={}

        if cfg is None:
            raise ShoeDevErr("No device configuration for service setUp")

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

        for cfg in svcList:
            svc=ShoeSvc(host=self.host,
                        port=self.port,
                        loglvl=self.loglvl,
                        force=self.force,
                        cfg=cfg,
                        devInst=self)

            try:
                svc.setUp()
            except ShoeSvcNoScpd:
                self.log.warning("Service has no SCPD: %s" % svc.name)
                continue
            except:
                raise

            if svc.name == None:
                self.log.warning("No service name.  Setting name to: %s"
                        % unknownSvcIdx)
                svc.name=unkownSvcIdx
                unkownSvcIdx=unkownSvcIdx+1

            svcs[svc.name]=svc

        return svcs

    def _getName(self,
                cfg,
                typeIdKey=DEVNAME_KEY,
                typeIdTag=DEVNAME_TAG ):
        return super()._getName(cfg, typeIdKey, typeIdTag)

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
