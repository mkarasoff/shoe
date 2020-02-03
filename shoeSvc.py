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
from shoeDev import *
import copy
from consoleLog import *

class ShoeSvc(ShoeDev):
    ACTTBL_KEYS=('scpd','actionList','action')
    STATEVARTBL_KEYS=('scpd','serviceStateTable','stateVariable')
    ARGLIST_KEYS=('argumentList','argument')
    SVC_LIST_KEYS=('serviceList', 'service')
    NAME_KEY='name'
    STATEVAR_KEY='relatedStateVariable'
    SCPD_URL_KEY='SCPDURL'
    SVCNAME_KEY='serviceId'
    SVCNAME_TAG='serviceId'

    PATH_KEY='controlURL'
    URI_KEY='serviceType'

    def __init__(self,
                    host,
                    svcCfg,
                    devInst=None,
                    loglvl=0,
                    port=60006,
                    scpdCfg=None):

        super().__init__(host=host,
                        port=port,
                        loglvl=loglvl)

        self.log=ConsoleLog(self.__class__.__name__, loglvl)

        self.cfg=svcCfg
        self._devInst=devInst

        self.devName=None

        self._scpd=scpdCfg
        self._stateVarTbl=None
        self._cmndTbl=None

        self.path=None
        self.uri=None

        self.name=None
        return

    def init(self):
        if self._devInst is not None:
            self.devName=self._devInst.name

        self.path=self.cfg[self.PATH_KEY]
        self.uri=self.cfg[self.URI_KEY]
        self.name= self._getName(self.cfg)

        try:
            if self._scpd is None:
                self._scpd=self._getScpd(self.cfg)
        except KeyError as e:
            log.info("No SCPD for this service", self.name)
            log.debug(str(e))
            raise ShoeSvcNoScpd(errStr)
        except:
            raise

        try:
            self._stateVarTbl=self._getStateVarTbl(self._scpd)
        except ShoeSvcNoTbl:
            self._stateVarTbl={}
            log.info("No var table for service", self.name)
        except:
            raise

        try:
            self._cmndTbl=self._getCmndTbl(self._scpd)
        except ShoeSvcNoTbl:
            self._cmndTbl={}
            log.info("No cmnd table for service", self.name)
        except:
            raise

        return

    @property
    def cmnds(self):
        if self._cmndTbl is None:
            raise ShoeSvcNoTbl("Service not properly initialized")
        else:
            return list(self._cmndTbl.keys())

    def getCmndArgsCfg(self, cmnd):

        try:
            argLst=self._cmndTbl[cmnd]
        except KeyError:
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

            cmndStateVar['state']=stateVar
            cmndArgCfg.append(cmndStateVar)

        return cmndArgCfg

    def sendCmnd(self, cmnd, args={}):
        argsCfg=self.getCmndArgsCfg(cmnd)

        shoeCmnd=ShoeCmnd(  host=self.host,
                            path=self.path,
                            urn=self.urn,
                            port=self.port,

                            cmnd=cmnd,
                            args=args,
                            argsCfg=argsCfg,

                            loglvl=self.loglvl)

        shoeCmnd.send()
        return shoeCmnd.parse()

    def _getScpd(self, svcCfg):
        try:
            path=svcCfg[self.SCPD_URL_KEY]
        except KeyError:
            raise ShoeSvcNoScpd(errStr)
        except:
            raise

        try:
            scpd=self.getCfg(path)
        except:
            errStr="Service %s has no SCPD" % self.name
            raise ShoeSvcNoScpd(errStr)

        return scpd

    def _getName(self,
                cfg,
                typeIdKey=SVCNAME_KEY,
                typeIdTag=SVCNAME_TAG ):

        self.log.debug(cfg)

        return super()._getName(cfg, typeIdKey, typeIdTag)

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

###############################Unittests#################################
import unittest
from test_shoe import *
class TestShoeGroupCtrlSvc(TestShoeHttp):
    HOST='127.0.0.1'
    def setUp(self):
        super().setUp()
        self.shoeMsg=None
        self.path=None
        self.method=None
        self.urn=None
        self.msgArgs={}

        self.port=60006
        self.host='127.0.0.1'

        self.cfg=False

        return

    def _sendTestMsgs(self):
        if self.cfg is False:
            self.shoeSvc.init()
        return

    def runTest(self):
        self._runSvcTest(self.testAiosDev.groupCtrlSvc, self.testGroupCtrlSvc)

        getGroupVolArg=self.shoeSvc.getCmndArgsCfg(self.testGroupCtrlSvc.getGroupVolCmnd)

        print("@@@@@@@@@@@@@@@@@@@Args for Get Group Vol Cmd@@@@@@@@@@@@@@@@@@@")
        print(getGroupVolArg)

        self.assertEqual(getGroupVolArg,
                        self.testGroupCtrlSvc.getGroupVolArg,
                        "Get Group Volume Args")
        return

    def _runSvcTest(self, svcCfg, testSvc):
        class testDev():
            def __init__(self):
                self.name=testSvc.devName
                return

        devInst=testDev()

        self.shoeSvc=ShoeSvc(host=self.HOST,
                            svcCfg=svcCfg,
                            devInst=devInst)

        shoeSvc=self.shoeSvc

        self.httpTest()

        msg="@@@@@@@@@@@@@@@@@@%s Arg St Table@@@@@@@@@@@@@@@@@@@@@@@" % testSvc.name
        print(msg)
        print(shoeSvc._stateVarTbl)

        self.assertEqual(shoeSvc._stateVarTbl,
                        testSvc._stateVarTbl,
                        "Arg State Table")

        msg="@@@@@@@@@@@@@@@@@@%s Command Table@@@@@@@@@@@@@@@@@@@@@@@" % testSvc.name
        print(msg)
        print(self.shoeSvc._cmndTbl)
        self.assertEqual(shoeSvc._cmndTbl,
                        testSvc._cmndTbl,
                        "Command Table")

        msg="@@@@@@@@@@@@@@@@@@%s Command List@@@@@@@@@@@@@@@@@@@@@@@" % testSvc.name
        print(msg)
        print(self.shoeSvc.cmnds)
        self.assertCountEqual(self.shoeSvc.cmnds,
                        testSvc.cmnds,
                        "Command List")

        msg="@@@@@@@@@@@@@@@@@@%s Name@@@@@@@@@@@@@@@@@@@@@@@" % testSvc.name
        print(msg)
        print(self.shoeSvc.name)
        self.assertCountEqual(self.shoeSvc.name,
                        testSvc.name,
                        "Name")

        msg="@@@@@@@@@@@@@@@@@@%s Dev Name@@@@@@@@@@@@@@@@@@@@@@@" % testSvc.name
        print(msg)
        print(self.shoeSvc.devName)
        self.assertCountEqual(self.shoeSvc.devName,
                        testSvc.devName,
                        "Dev Name")

class TestShoeZoneCtrlSvc(TestShoeGroupCtrlSvc):
    def runTest(self):
        self._runSvcTest(self.testAiosDev.zoneCtrlSvc, self.testZoneCtrlSvc)
        return

class TestShoeActSvc(TestShoeGroupCtrlSvc):
    def runTest(self):
        self._runSvcTest(self.testAiosDev.actSvc, self.testActSvc)
        return
