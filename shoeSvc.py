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

class ShoeSvc(ShoeDev):
    ACTTBL_KEYS=('scpd','actionList','action')
    STATEVARTBL_KEYS=('scpd','serviceStateTable','stateVariable')
    ARGLIST_KEYS=('argumentList','argument')
    NAME_KEY='name'
    STATEVAR_KEY='relatedStateVariable'

    URL_KEY='SCPDURL'

    def __init__(self, host, svcCfg, devObj, dbug=0, port=60006, scpdCfg=None):
        super().__init__(host=host,
                         devTag=devTag,
                         dbug=dbug,
                         port=port)

        self.cfg=svcCfg
        self._devObj=devObj

        self.devName=None

        self._scpd=scpdCfg
        self._stateVarTbl=None
        self._cmndTbl=None

        return

    def init(self):
        self.devName=self._devObj.name

        try:
            self.name= self._getName()
        except ShoeDevUnkownParam as e:
            print("WARNING: Svc Name not found, setting to 'None'")
            if dbug > 0:
                print(str(e))
            self.name = None
        except:
            raise

        try:
            if self._scpd is None:
                self._scpd=self._getScpd(self.cfg)
        except KeyError as e:
            print("INFO: No SCPD for this service", self.name)
            if dbug > 0:
                print(str(e))
            raise ShoeSvcNoScpd(errStr)
        except:
            raise

        try:
            self._stateVarTbl=self._getStateVarTbl(self.scpd)
        except ShoeSvcNoTbl:
            self._stateVarTbl={}
            if dbug > 0:
                print("INFO: No var table for service", self.name)
        except:
            raise

        try:
            self._cmndTbl=self._getCmndTbl(self.scpd)
        except ShoeSvcNoTbl:
            self._cmndTbl={}
            if dbug > 0:
                print("INFO: No cmnd table for service", self.name)
        except:
            raise

        return

    def _getScpd(self, svcCfg):
        try:
            path=svcCfg[self.URL_KEY]
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
                cfg=self.cfg,
                typeIdKey=self.SVCNAME_KEY,
                typeIdTag=self.SVCNAME_TAG ):
        return super()._getName(cfg, typeIdKey, typeIdTag)

    @property
    def cmndList(self):
        if self._cmndTbl is None:
            raise ShoeSvcErr("uninitialized")
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

class TestShoeSvc(unittest.TestCase):
    GROUP_DEV_TAG='AiosServices'
    GROUP_SVC_TAG='GroupControl'

    HOST='127.0.0.1'

    def setUp(self):
      return

    def runTest(self):

        testObj=TestGroupCtrlSvc()
        self.xmlStr=testObj.xmlStr

        self.shoeSvc=ShoeSvc(self.HOST,
                    self.GROUP_DEV_TAG,
                    self.GROUP_SVC_TAG,
                    dbug=10)

        self.shoeSvc._getXmlText=self._getXmlText

        self.shoeSvc.initSvc()

        print("@@@@@@@@@@@@@@@@@@Group Arg St Table@@@@@@@@@@@@@@@@@@@@@@@")
        print(self.shoeSvc._stateVarTbl)

        self.assertEqual(self.shoeSvc._stateVarTbl,
                        testObj._stateVarTbl,
                        "Arg State Table")

        print("@@@@@@@@@@@@@@@@@@Group Ctrl Command Table@@@@@@@@@@@@@@@@@@@")
        print(self.shoeSvc._cmndTbl)
        self.assertEqual(self.shoeSvc._cmndTbl,
                        testObj._cmndTbl,
                        "Command Table")

        print("@@@@@@@@@@@@@@@@@Group Ctrl Command List@@@@@@@@@@@@@@@@@@@@@@@")
        print(self.shoeSvc.cmndList)
        self.assertCountEqual(self.shoeSvc.cmndList,
                        testObj.cmndList,
                        "Command List")

        getGroupVolArg=self.shoeSvc.getCmndArgsCfg(testObj.getGroupVolCmnd)

        print("@@@@@@@@@@@@@@@@@@@Args for Get Group Vol Cmd@@@@@@@@@@@@@@@@@@@")
        print(getGroupVolArg)

        self.assertEqual(getGroupVolArg,
                        testObj.getGroupVolArg,
                        "Get Group Volume Args")

        return

    def _getXmlText(self):
        print("@@@@@@@@@@@@@@@@@@Shoe Cfg Scpd Path@@@@@@@@@@@@@@@@@@@@")
        print(self.shoeSvc.path)

        if(self.shoeSvc.path ==
                '/upnp/desc/aios_device/aios_device.xml'):
            aiosDevObj=TestAiosDev()
            xmlStr=aiosDevObj.xmlStr

        else:
            xmlStr=self.xmlStr

        return xmlStr
