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

class ShoeOp():
    CURRSTATE_CMND='GetCurrentState'
    FMT_LBL_LEN=16
    FMT_TAB_LEN=4

    def __init__(self, shoeRoot, loglvl=0):
        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        self.shoeRoot=shoeRoot
        self.loglvl=loglvl
        return

    def _getCurrState(self, svcName):
        currStRtn=self.shoeRoot.sendCmnd(self.CURRSTATE_CMND, svcName=svcName)
        return currStRtn

    def _fmtOp(self, opData, tab=0):
        fmt= '{0:>%s}{1:%s} : {2:<0}\n'%(tab, self.FMT_LBL_LEN)
        lblessFmt= '{0:>%s}{1:%s}   {2:<0}\n'%(tab, self.FMT_LBL_LEN)
        fmtStr=''

        try:

            for lbl,val in opData.items():
                valType=type(val)
                if valType is dict:
                    fmtStr=fmtStr+fmt.format('', str(lbl), '')
                    fmtStr=fmtStr+self._fmtOp(val, tab+self.FMT_TAB_LEN)
                elif valType is list:
                    fmtStr=fmt.format('', lbl, '')
                    lstBreak='-'*self.FMT_LBL_LEN
                    fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')
                    for valEl in val:
                        fmtStr=fmtStr+self._fmtOp(valEl, tab+self.FMT_TAB_LEN)
                        fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')
                elif valType is bytes:
                    fmtStr=fmtStr+fmt.format('', str(lbl), str(val.decode()))
                else:
                    fmtStr=fmtStr+fmt.format('', str(lbl), str(val))

        except AttributeError:
            fmtSt=fmtStr+lblessFmt.format('', '', str(opData))
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

class TestShoeOpGetCurrSt(TestShoeOp):
    def setUp(self):
        super().setUp()
        self.testSvcs=[ self.testActSvc,
                    self.testGroupCtrlSvc,
                    self.testZoneCtrlSvc]
        return

    def _sendTestMsgs(self):
        self.currSt=self.op._getCurrState(self.testSvc.name)
        return

    def runTest(self):
        for testSvc in self.testSvcs:
            self.testSvc=testSvc
            cmnd=testSvc.cmnds['GetCurrentState']
            self.httpTest(cmnd)

            print("Current state dict******************")
            print(str(self.currSt))

            currStFmt=self.op._fmtOp(self.currSt.args['CurrentState'])
            print("Current state format******************")
            print(currStFmt)

            self.assertEqual(currStFmt, cmnd.fmtOutput)
        return
