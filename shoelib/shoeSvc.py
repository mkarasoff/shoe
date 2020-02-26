##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeSvc.py
#Class that manages HEOS service configuration. It reads SCPD data from an
#host device and configures the sercice accordingly. It requires an existing
#service configuration, usually gathered from the Aiso XML file grabbed
#by a root device.
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
from .shoeCfgXml import *
from .shoeCmnd import *
import copy

class ShoeSvc(ShoeCfgXml):
    ACTTBL_KEYS=('scpd','actionList','action')
    STATEVARTBL_KEYS=('scpd','serviceStateTable','stateVariable')
    ARGLIST_KEYS=('argumentList','argument')
    NAME_KEY='name'
    STATE_KEY='state'
    STATEVAR_KEY='relatedStateVariable'
    SCPD_URL_KEY='SCPDURL'
    SVCNAME_KEY='serviceId'
    SVCNAME_TAG='serviceId'
    SVC_LIST_KEYS=('serviceList', 'service')

    PATH_KEY='controlURL'
    URI_KEY='serviceType'

    def __init__(self,
                    host,
                    cfg,
                    devInst=None,
                    loglvl=ConsoleLog.WARNING,
                    port=60006,
                    scpdCfg=None,
                    fileName=None,
                    path=None,
                    force=False):

        super().__init__(host=host,
                        port=port,
                        loglvl=loglvl,
                        path=path,
                        fileName=fileName)

        self.log.debug("Path %s SelfPath %s", path, self.path)

        self.cfg=cfg
        self._devInst=devInst

        self.devName=None

        self._scpd=scpdCfg
        self._stateVarTbl=None
        self._cmndTbl=None

        self.urn=None

        self.force=force

        self.name=None
        return

    def setUp(self):

        if self._devInst is not None:
            self.devName=self._devInst.name

        self.log.debug("Service Cfg: %s" % self.cfg)

        self.ctrlUrlPath=self.cfg[self.PATH_KEY]

        self.urn=self.cfg[self.URI_KEY]
        self.log.debug("Service Uri: %s" % self.urn)

        self.name= self._getName(self.cfg)
        self.log.debug("Service Name: %s, Dev Name %s" % (self.name, self.devName))

        try:
            if self._scpd is None:
                self._scpd=self._getScpd(self.cfg)
        except KeyError as e:
            log.info("No SCPD for this service %s" % self.name)
            log.debug(str(e))
            raise ShoeSvcNoScpd(errStr)
        except:
            raise

        self.log.debug2("%s SCPD: %s" %
                        (self.name, self._scpd))

        try:
            self._stateVarTbl=self._getStateVarTbl(self._scpd)
        except ShoeSvcNoTbl:
            self._stateVarTbl={}
            log.info("No var table for service %s" % self.name)
        except:
            raise

        self.log.debug2("%s State Var Tbl: %s" %
                        (self.name, self._stateVarTbl))

        try:
            self._cmndTbl=self._getCmndTbl(self._scpd)
        except ShoeSvcNoTbl:
            self._cmndTbl={}
            log.info("No cmnd table for service %s" % self.name)
        except:
            raise

        self.log.debug2("%s Service Commands: %s" %
                        (self.name, self._cmndTbl))

        self.path=self.ctrlUrlPath

        return

    @property
    def cmnds(self):
        self.log.debug2("cmnds: %s", self._cmndTbl)

        if self._cmndTbl is None:
            raise ShoeSvcNoTbl("Service %s not properly initialized" % self.name)
        else:
            return list(self._cmndTbl.keys())

    def getCmndArgs(self, cmnd):
        try:
            argLst=self._cmndTbl[cmnd]
        except (TypeError, KeyError):
            errMsg="%s not an available command" % cmnd
            raise ShoeSvcErr(errMsg)
        except:
            raise

        cmndArgCfg=[]

        for arg in argLst:
            cmndStateVar=copy.deepcopy(arg)

            try:
                stateVarKey=arg[self.STATEVAR_KEY]
            except KeyError:
                stateVarKey=None
            except:
                raise

            try:
                stateVar=self._stateVarTbl[stateVarKey]
            except KeyError:
                stateVar=None
            except:
                raise

            self.log.debug("Service %s Cmnd %s, Arg %s, StateVar %s" %
                    (self.name, cmnd, arg, stateVar))

            cmndStateVar[self.STATE_KEY]=stateVar
            cmndArgCfg.append(cmndStateVar)

        return cmndArgCfg

    def sendCmnd(self, cmnd, args={}):
        self.log.debug("Cmnd %s Args %s", cmnd, args)
        if self.force is True:
            argsCfg={}
        else:
            argsCfg=self.getCmndArgs(cmnd)

        self.log.debug("ArgsCfg %s", argsCfg)

        self.log.debug("Host %s:%s Path %s CmndName %s" %
                        (self.host, self.port, self.path, cmnd))

        shoeCmnd=ShoeCmnd(  host=self.host,
                            path=self.path,
                            urn=self.urn,
                            port=self.port,
                            force=self.force,

                            cmnd=cmnd,
                            argsIn=args,
                            argsCfg=argsCfg,

                            loglvl=self.loglvl)

        shoeCmnd.send()
        return shoeCmnd.parse()

    def _getScpd(self, cfg):
        path=self.path

        self.log.debug("Getting SCPD for service %s" % self.name)
        try:
            path=cfg[self.SCPD_URL_KEY]
        except KeyError:
            raise ShoeSvcNoScpd(errStr)
        except:
            raise

        try:
            scpd=self.getCfg(path=path)
        except:
            self.path=path
            errStr="Service %s has no SCPD" % self.name
            raise ShoeSvcNoScpd(errStr)

        self.path=path
        return scpd

    def _getName(self,
                cfg,
                typeIdKey=SVCNAME_KEY,
                typeIdTag=SVCNAME_TAG ):

        name=None
        cfgLine=[]
        try:
            cfgLine=cfg[typeIdKey].split(':')
        except KeyError:
            self.log.info("No %s entry found in config" % typeIdKey)
        except:
            raise

        try:
            name=cfgLine[cfgLine.index(typeIdTag)+1]
        except (ValueError, IndexError):
            self.log.info("No dev lbl found on cfg line %s" % cfgLine)
        except:
            raise

        if name is None:
            hashMd5=hashlib.md5(str(cfg).encode('utf-8'))
            name=hashMd5.hexdigest()
            self.log.warning("Nametag %s not found. Setting to %s" %
                    (typeIdTag, name))
        return name

    def _getStateVarTbl(self, scpd):
        stateVarTbl={}

        try:
            stateVarXmlTbl=scpd\
                [self.STATEVARTBL_KEYS[0]]\
                [self.STATEVARTBL_KEYS[1]]\
                [self.STATEVARTBL_KEYS[2]]
        except KeyError:
            raise ShoeSvcNoTbl
        except:
            raise

        for stateVar in stateVarXmlTbl:
            stateVarTbl[stateVar[self.NAME_KEY]]=stateVar

        return stateVarTbl

    def _getCmndTbl(self, scpd):
        cmndTbl={}

        try:
            actXmlTbl= scpd\
                  [self.ACTTBL_KEYS[0]]\
                  [self.ACTTBL_KEYS[1]]\
                  [self.ACTTBL_KEYS[2]]
        except KeyError:
            raise shoeSvcNoTbl
        except:
            raise

        for entry in actXmlTbl:
            try:
                argList=entry[self.ARGLIST_KEYS[0]]\
                         [self.ARGLIST_KEYS[1]]
            except KeyError as e:
                #If the only key is 'name', then there are no arguments for the
                if( list(entry.keys()) == ['name',]):
                    argList=[]
                    pass
                else:
                    raise e
            except:
                raise

            if(not isinstance(argList, list)):
                argList=[argList,]

            cmndTbl[entry[self.NAME_KEY]]=argList

        return cmndTbl

    #This should do nothing
    def _initSvcs(self):
        return
###############################Exceptions#################################
class ShoeSvcErr(Exception):
    pass

class ShoeSvcNoScpd(Exception):
    pass

class ShoeSvcNoTbl(Exception):
    pass
