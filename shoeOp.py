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
