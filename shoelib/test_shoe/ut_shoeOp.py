##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeOp.py
#Unit Test for ShoeOp.py
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
##############################UNIT TESTS########################################
from .testShoeHttp import *
from shoelib.shoeRoot import *
from shoelib.shoeOp import *

class TestShoeOp(TestShoeHttp):

    def setUp(self):
        super().setUp()
        self.port=60006
        self.host='127.0.0.1'
        self.svcName=None
        self.shoeRoot=ShoeRoot(self.host, loglvl=logging.DEBUG)
        self.op=ShoeOp(self.shoeRoot, loglvl=logging.DEBUG)
        self.cfg=False
        self.testCbFunc=self._setUp
        self.httpTest()
        self.testCbFunc=self._sendTestMsgs
        return

    def _setUp(self):
        self.shoeRoot.setUp()
        return

    def _sendTestMsgs(self):
        return

class TestShoeOpTree(TestShoeOp):
    def runTest(self):
        fmtCmndTree=self.op.showCmndTree()
        self.assertEqual(fmtCmndTree, self.testRootDev.fmtCmndTreeDflt)
        return

class TestShoeOpTreeAll(TestShoeOp):
    def runTest(self):
        fmtCmndTree=self.op.showCmndTree(showAll=True)
        self.assertEqual(fmtCmndTree, self.testRootDev.fmtCmndTreeAll)
        return

class TestShoeOpCmndInfo(TestShoeOp):
    def runTest(self):
        for cmndName,cmnd in self.testActSvc.cmnds.items():
            fmtCmndInfo=self.op.showCmndInfo(cmndName, cmnd.svcName, cmnd.devName)
            print("Expected %s" % cmnd.fmtCmndInfo)
            print("Recieved %s" % fmtCmndInfo)
            self.assertEqual(fmtCmndInfo, cmnd.fmtCmndInfo)
        return

class TestShoeOpGetInfo(TestShoeOp):
    def setUp(self):
        super().setUp()
        return

    def runTest(self):
        self.maxDiff=None
        rootDev=TestRootDev()
        self.infoFmt=self.op.getInfo()
        print(self.infoFmt)
        self.assertEqual(self.infoFmt, rootDev.infoFmt)
        return

class TestShoeOpRunCmnd(TestShoeOp):
    def setUp(self):
        super().setUp()
        self.testSvcs=[ self.testActSvc,
                    self.testGroupCtrlSvc,
                    self.testZoneCtrlSvc]
        return

    def _sendTestMsgs(self):
        cmnd=self.cmnd
        self.fmtCmndRtn=self.op.runCmnd(cmnd.name, cmnd.args, cmnd.svcName, cmnd.devName)
        return

    def runTest(self):
        self.maxDiff=None
        for testSvc in self.testSvcs:
            for cmndName, cmnd in testSvc.cmnds.items():
                self.cmnd = cmnd
                self.httpTest(cmnd)

                print("Expected*********************")
                print(cmnd.fmtCmndRtn)

                print("Current state format******************")
                print(self.fmtCmndRtn)

                self.assertEqual(self.fmtCmndRtn, cmnd.fmtCmndRtn)
        return
