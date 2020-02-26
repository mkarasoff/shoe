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
###############################Unittests#################################
from .testShoeHttp import *
from shoelib.shoeSvc import *

class TestShoeCtrlSvc(TestShoeHttp):
    HOST='127.0.0.1'
    def setUp(self):
        super().setUp()
        self.shoeMsg=None
        self.path=None
        self.method=None
        self.msgArgs={}

        self.port=60006
        self.host='127.0.0.1'

        self.cfg=False

        self.testSvcs=[ self.testGroupCtrlSvc,
                        self.testZoneCtrlSvc,
                        self.testActSvc ]

        return

    def _sendTestMsgs(self):
        if self.cfg is False:
            self.shoeSvc.setUp()
        return

    def runTest(self):
        for svc in self.testSvcs:
            self._runSvcTest(svc)
        return

    def _runSvcTest(self, testSvc):
        class testDev():
            def __init__(self):
                self.name=testSvc.devName
                return

        self.devInst=testDev()

        self.shoeSvc=ShoeSvc(host=self.HOST,
                            cfg=testSvc.cfg,
                            devInst=self.devInst)

        self.httpTest()

        msg="@@@@@@@@@@@@@@@@@@%s Arg St Table@@@@@@@@@@@@@@@@@@@@@@@" % testSvc.name
        print(msg)
        print(self.shoeSvc._stateVarTbl)

        self.assertEqual(self.shoeSvc._stateVarTbl,
                        testSvc.stateVarTbl,
                        "Arg State Table")

        msg="@@@@@@@@@@@@@@@@@@%s Command Table@@@@@@@@@@@@@@@@@@@@@@@" % testSvc.name
        print(msg)
        print(self.shoeSvc._cmndTbl)
        self.assertEqual(self.shoeSvc._cmndTbl,
                        testSvc.cmndTbl,
                        "Command Table")

        msg="@@@@@@@@@@@@@@@@@@%s Command List@@@@@@@@@@@@@@@@@@@@@@@" % testSvc.name
        print(msg)
        print(self.shoeSvc.cmnds)
        self.assertCountEqual(self.shoeSvc.cmnds,
                        testSvc.cmndTbl.keys(),
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

class TestShoeCtrlSvcArgs(TestShoeCtrlSvc):
    def runTest(self):
        for testSvc in self.testSvcs:
            self._getArgsTest(testSvc)
        return

    def _getArgsTest(self, testSvc):
        class testDev():
            def __init__(self):
                self.name=testSvc.devName
                return

        self.devInst=testDev()

        cmndNames=testSvc.cmnds.keys()

        self.shoeSvc=ShoeSvc(host=self.HOST,
                            cfg=testSvc.cfg,
                            devInst=self.devInst)
        self.maxDiff=None

        self.httpTest()

        for cmndName in cmndNames:
            cmndArgsCfg=self.shoeSvc.getCmndArgs(cmndName)

            self.assertEqual(testSvc.cmnds[cmndName].argsCfg,
                                    cmndArgsCfg)
