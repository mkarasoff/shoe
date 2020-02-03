##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeSys.py
#Class that impliments system level configuration and control for HEOS.
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
from shoeSvcAct import *
from shoeSvcGroup import *
from shoeSvcZone import *
from shoeMsg import *
from collections import OrderedDict
import copy
import sys
from collections import defaultdict

class ShoeSys():

    def __init__(self, host, loglvl=0, port=60006):
        self.log=ConsoleLog(self.__class__.__name__, loglvl)

        self.host = host

        self.port = port
        self.loglvl = loglvl

        self.shoeDevRoot=None
        self.devs=None
        return

    def getInfo(self):
        infoDev=self.svcs[ShoeSvcAct.NAME]

        return infoDev._getInfo()

    def init(self):
        self.shoeDevRoot=ShoeDevRoot(self.host, self.loglvl, self.port)
        self.shoeDevRoot.init()

        self.devs=self.shoeDevRoot.devs

        return

    def getArgsCfg(self, cmnd, svc=None):
        if svc is None:
            svc=self.findSvc(cmnd)[0]

        return svc.getCmndArgsCfg(cmnd)

    def getCmnds(self):
        cmndList=defaultdict(list)
        for svcName, svc in self.svcs.items():
            cmndList[svcName]=svc.cmndList

        return cmndList

    def sendCmnd(self, cmnd, argsIn={}, svcName=None):
        if svcName is None:
            svc=self.findSvc(cmnd)[0]
        else:
            svc=self.svcs[svcName]

        return svc.sendCmnd(cmnd, argsIn)

    def findSvcCmnd(self, cmnd):

        if len(rtnDevs) is 0:
            raise ShoeSysErr("%s command not found" % cmnd)

        return rtnDevs

###############################Exceptions#################################
class ShoeSysErr(Exception):
    pass

##############################UNIT TESTS########################################
from test_shoe import *

class TestShoeSys(TestShoeHttp):

    def setUp(self):
        super().setUp()
        self.cmndArgCfg=None
        self.reply=None
        self.port=60006
        self.host='127.0.0.1'
        self.svcName=None
        self.method=None
        return

    def _sendTestMsgs(self):
        self.shoeSys=ShoeSys(self.host)
        self.shoeSys.getCfg()

        if self.method is not None:
            self.cmndArgCfg=self.shoeSys.getArgsCfg(self.method)
            self.reply=self.shoeSys.sendCmnd(self.method, self.msgArgs, self.svcName)
        return

#Check a command within range.
class TestShoeInRange(TestShoeSys):
    def setUp(self):
        super().setUp()

        self.method=self.testActSvc.getNetCfgCmd
        self.msgArgs=OrderedDict()
        self.msgArgs['networkConfigurationId']=1
        self.postRtn=self.testActSvc.getNetCfgRtnXml
        self.argCfg=self.testActSvc.getNetCfgArgs
        return

    def runTest(self):
        print("^^^^^^^^^^^^^^^^TestShoeInRange^^^^^^^^^^^^^^^^^^^^^^")
        self.httpTest()

        self.assertEqual(self.cmndArgCfg,
                            self.argCfg)
        self.assertEqual(self.reply.msgArgs,
                         self.testActSvc.getNetCfgRtn )
        self.assertEqual(self.reply.method,
                         self.method + "Response")
        return

#Fault injection, out of range.
class TestShoeRangeErr(TestShoeInRange):
    def runTest(self):
        print("^^^^^^^^^^^^^^^^TestShoeRangeErr^^^^^^^^^^^^^^^^^^^^^^")
        self.msgArgs['networkConfigurationId']=0

        errMsg=""
        try:
            self.httpTest()
        except ShoeSysErr as e:
            pass
        except:
            raise

        return

#Fault injection, arg type.
class TestShoeTypeErr(TestShoeInRange):
    def runTest(self):
        print("^^^^^^^^^^^^^^^^TestShoeTypeErr^^^^^^^^^^^^^^^^^^^^^^")
        self.msgArgs['networkConfigurationId']='abcd'

        errMsg=""
        try:
            self.httpTest()
        except ShoeSysErr as e:
            pass
        except:
            raise

        return

#Check a command with an allowed arg list
class TestShoeAllowedList(TestShoeSys):
    def setUp(self):
        super().setUp()

        self.method=self.testActSvc.setUpdateActCmnd
        self.msgArgs=OrderedDict()
        self.msgArgs['UpdateAction']='UPDATE_ACTION_NONE'
        self.postRtn=self.testActSvc.setUpdateActRtnXml
        self.argCfg=self.testActSvc.setUpdateActArgs
        return

    def runTest(self):
        print("^^^^^^^^^^^^^^^^TestShoeInRange^^^^^^^^^^^^^^^^^^^^^^")
        self.httpTest()

        self.assertEqual(self.cmndArgCfg,
                            self.argCfg)
        self.assertEqual(self.reply.msgArgs,
                         self.testActSvc.setUpdateActRtn )
        self.assertEqual(self.reply.method,
                         self.method + "Response")

#Fault Injuction, not on allowed command arg list
class TestShoeAllowedErr(TestShoeAllowedList):
    def runTest(self):
        print("^^^^^^^^^^^^^^^^TestShoeTypeErr^^^^^^^^^^^^^^^^^^^^^^")
        self.msgArgs['UpdateAction']='UPDATE_ACTION'

        errMsg=""
        try:
            self.httpTest()
        except ShoeSysErr as e:
            print(str(e))
            pass
        except:
            raise

        return

#Simple command test 1
class TestShoeSysGetAccessPtList(TestShoeSys):
    def setUp(self):
        super().setUp()

        self.method=self.testActSvc.getAccPtListCmnd
        self.msgArgs=OrderedDict()
        self.msgArgs['configurationToken']='caf7916a94db1'
        self.postRtn=self.testActSvc.getAccPtListRtnXml
        self.argCfg=self.testActSvc.getAccPtListArgs
        return

    def runTest(self):
        print("^^^^^^^^^^^^^^^^TestShoeGetAccessPtList^^^^^^^^^^^^^^^^^^^^^^")
        self.httpTest()

        self.assertEqual(self.cmndArgCfg,
                            self.argCfg)

        self.assertEqual(self.reply.msgArgs,
                         self.testActSvc.accPtListRtn )

        self.assertEqual(self.reply.method,
                         self.method + "Response")
        return

#Simple command test
class TestShoeSysGetGroupVol(TestShoeSys):
    def setUp(self):
        super().setUp()
        self.method=self.testGroupCtrlSvc.getGroupVolCmnd
        self.msgArgs=OrderedDict()
        self.msgArgs['GroupUUID']=\
                'caf7916a94db1a1300800005cdfbb9c6,f3ddb59f3e691f1e00800005cdff1706'
        self.postRtn=self.testGroupCtrlSvc.getGroupVolRtnXml

        self.argCfg=self.testGroupCtrlSvc.getGroupVolArg
        return

    def runTest(self):
        print("^^^^^^^^^^^^^^^^TestShoeSysGetGroup^^^^^^^^^^^^^^^^^^^^^^")
        self.httpTest()

        self.assertEqual(self.cmndArgCfg,
                            self.argCfg)

        self.assertEqual(self.reply.msgArgs,
                         self.testGroupCtrlSvc.getGroupVolRtn)

        self.assertEqual(self.reply.method,
                         self.method + "Response")

        print("^^^^^^^^^^^^^^^^TestShoeSysGetGroup Done^^^^^^^^^^^^^^^^^^^^^^")
        return

#Large return arg value - embedded,escaped XML.
class TestShoeSysGetCurrStAct(TestShoeSys):
    def setUp(self):
        super().setUp()
        self.testObj=self.testActSvc
        print("^^^^^^^^^^^^^^^^Current State ACT^^^^^^^^^^^^^^^^^^^^^^")
        return

    def runTest(self):
        self.svcName=self.testObj.name
        self.method=self.testObj.getCurrStCmnd
        self.msgArgs=OrderedDict()
        self.postRtn=self.testObj.getCurrStRtnXml
        self.argCfg=self.testObj.getCurrStArg

        self.httpTest()

        self.assertEqual(self.cmndArgCfg,
                            self.argCfg)

        self.assertEqual(self.reply.msgArgs,
                         self.testObj.getCurrStRtn)

        self.assertEqual(self.reply.method,
                         self.method + "Response")

        return

#Empty return arg value
class TestShoeSysGetCurrStGroup(TestShoeSysGetCurrStAct):
    def setUp(self):
        super().setUp()
        self.testObj=self.testGroupCtrlSvc
        print("^^^^^^^^^^^^^^^^Current State Group^^^^^^^^^^^^^^^^^^^^^^")
        return

#Get Info
class TestShoeSysGetInfo(TestShoeSys):
    def setUp(self):
        #This will just run a getCfg.
        super().setUp()
        self.method=None
        self.httpTest()
        self.testObj=self.testAiosDev

        self.testCmnds={
                self.testGroupCtrlSvc.name : self.testGroupCtrlSvc.cmndList,
                self.testZoneCtrlSvc.name : self.testZoneCtrlSvc.cmndList,
                self.testActSvc.name : self.testActSvc.cmndList}

    def runTest(self):

        info=self.shoeSys.getInfo()

        self.assertCountEqual(info,
                self.testObj.act['info'])

        return

#Get Commands
class TestShoeSysGetCmnds(TestShoeSysGetInfo):
    def runTest(self):
        cmnds=self.shoeSys.getCmnds()

        self.assertCountEqual(cmnds, self.testCmnds)

        return
