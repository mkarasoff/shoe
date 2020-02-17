##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeExpert.py
#Class that implements "Expert" CLI functions
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
from shoeOp import *
from collections import OrderedDict

class ShoeExpert(ShoeOp):
    def __init__(self, shoeRoot, loglvl=0):
        super().__init__(shoeRoot, loglvl)
        return

    def showCmndTree(self, devName=None, showAll=False):
        cmndTree=self.shoeRoot.getCmndTree()

        showDevs=None
        showTree={}

        if devName is not None:
            showDevs=[devName,]
        elif not showAll:
            showDevs=ShoeRoot.PREFERRED_DEVS

        if showDevs is None:
            showTree=cmndTree
        else:
            self.log.debug(showDevs)
            showTree=OrderedDict([(devName, cmndTree[devName]) for devName in showDevs])

        self.log.debug("ShowTree %s", showTree)

        fmtTree = self._fmtOp(showTree)
        self.log.debug("Fmt Tree:\n %s", fmtTree)
        return fmtTree

    def showCmndInfo(self, cmnd, svcName=None, devName=None):
        cmndLocs=self.shoeRoot.findCmnd(cmnd, svcName, devName)

        cmndInfoStr=""

        self.log.debug2("Cmnd Locs %s" % cmndLocs)
        for devName, svcNames in cmndLocs.items():
            for svcName in svcNames:
                cmndInfoStr += "Cmnd:    %s \nDevice:  %s \nService: %s\n" % \
                                (cmnd, devName, svcName)
                self.log.debug2("Cmnd %s Device: %s Service: %s", cmnd, devName, svcName)
                cmndParams=self.shoeRoot.getCmndParams(cmnd, svcName, devName)

                #Remove redundant info for display
                for cmndParam in cmndParams:
                    try:
                        del cmndParam[ShoeSvc.STATEVAR_KEY]
                    except KeyError:
                        pass

                    try:
                        del cmndParam[ShoeSvc.STATE_KEY][ShoeSvc.NAME_KEY]
                    except KeyError:
                        pass

                fmtParams=self._fmtOp({'Parameters' : cmndParams})
                cmndInfoStr += fmtParams
                cmndInfoStr += "\n"
                self.log.debug2("Command Info:\n %s" % fmtParams)

        return cmndInfoStr

##############################UNIT TESTS########################################
from test_shoe import *

class TestShoeExpert(TestShoeHttp):

    def setUp(self):
        super().setUp()
        self.testActSvc=TestActSvc()
        self.port=60006
        self.host='127.0.0.1'
        self.svcName=None
        self.shoeRoot=ShoeRoot(self.host, loglvl=ConsoleLog.DEBUG)
        self.exp=ShoeExpert(self.shoeRoot, loglvl=ConsoleLog.DEBUG2)
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

class TestShoeExpertTree(TestShoeExpert):
    def runTest(self):
        fmtCmndTree=self.exp.showCmndTree()
        self.assertEqual(fmtCmndTree, self.testRootDev.fmtCmndTreeDflt)
        return

class TestShoeExpertTreeAll(TestShoeExpert):
    def runTest(self):
        fmtCmndTree=self.exp.showCmndTree(showAll=True)
        self.assertEqual(fmtCmndTree, self.testRootDev.fmtCmndTreeAll)
        return

class TestShoeExpertInfo(TestShoeExpert):
    def runTest(self):
        for cmndName,cmnd in self.testActSvc.cmnds.items():
            fmtCmndInfo=self.exp.showCmndInfo(cmndName, cmnd.svcName, cmnd.devName)
            print("Expected %s" % cmnd.fmtCmndInfo)
            print("Recieved %s" % fmtCmndInfo)
            self.assertEqual(fmtCmndInfo, cmnd.fmtCmndInfo)
        return
