##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeOp.py
#Base class for CLI functions
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
from console_log import *
from shoeRoot import *
from collections.abc import Iterable
from collections import OrderedDict

class ShoeOp():
    CURRSTATE_CMND='GetCurrentState'
    FMT_LBL_LEN=16
    FMT_TAB_LEN=4

    def __init__(self, shoeRoot, loglvl=0):
        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        self.shoeRoot=shoeRoot
        self.loglvl=loglvl
        return

    def getInfo(self):
        infoFmt=self._fmtOp(self.shoeRoot.info)
        return infoFmt

    def runCmnd(self, cmnd, args, svcName=None, devName=None):
        cmndRtn=self.shoeRoot.sendCmnd(cmnd, args, svcName, devName)
        self.log.debug("Command Return:\n%s" % str(cmndRtn))
        cmndRtnStr = "%s\n" % cmndRtn.cmnd
        cmndRtnStr += self._fmtOp(cmndRtn.args)
        self.log.debug("Cmnd Return String:\n%s" % cmndRtnStr)
        return cmndRtnStr

    def getCurrState(self, svcName):
        currStFmt=self.runCmnd(self.CURRSTATE_CMND, svcName=svcName)
        return currStFmt

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

    def _fmtOp(self, opData, tab=0):
        fmt= '{0:>%s}{1:%s} : {2:<0}\n'%(tab, self.FMT_LBL_LEN)
        lblessFmt= '{0:>%s}{1:%s}   {2:<0}\n'%(tab, self.FMT_LBL_LEN)
        fmtStr=''

        try:
            self.log.debug2("OpData %s", opData)

            for lbl,val in opData.items():
                self.log.debug2("OpData Value [lbl]: %s [val]: %s [type]: %s",
                        lbl, val, type(val))
                valType=type(val)
                if valType is dict or valType is OrderedDict:
                    fmtStr=fmtStr+fmt.format('', str(lbl), '')
                    fmtStr=fmtStr+self._fmtOp(val, tab+self.FMT_TAB_LEN)
                elif valType is list:
                    fmtStr=fmtStr+fmt.format('', lbl, '')
                    lstBreak='-'*self.FMT_LBL_LEN
                    fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')
                    first=True
                    for valEl in val:
                        if first:
                            first=False
                        else:
                            if isinstance(valEl, Iterable) and type(valEl) != str:
                                fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')

                        self.log.debug2("List Element %s", valEl)
                        listElStr=self._fmtOp(valEl, tab+self.FMT_TAB_LEN)
                        self.log.debug2("List Element String %s", listElStr)
                        fmtStr=fmtStr+listElStr
                    fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')
                elif valType is bytes:
                    fmtStr=fmtStr+fmt.format('', str(lbl), str(val.decode()))
                else:
                    fmtStr=fmtStr+fmt.format('', str(lbl), str(val))

        except AttributeError:
            self.log.debug2("OpData Not Iterable %s", opData)
            fmtStr=fmtStr+lblessFmt.format('', '', str(opData))
            pass

        except:
            raise

        return fmtStr

##############################UNIT TESTS########################################
from test_shoe import *

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

class TestShoeOpInfo(TestShoeOp):
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
