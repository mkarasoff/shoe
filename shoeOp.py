##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeExpert.py
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
from shoeState import *

class ShoeOp():
    CURRSTATE_CMND='GetCurrentState'
    FMT_LBL_LEN=16
    FMT_TAB_LEN=4

    def __init__(self, shoeSys, dbug=0):
        self.shoeSys=shoeSys
        self.dbug=dbug

        self.svcNames=shoeSys.svcs.keys()

        return

    def _getCurrState(self, svcName):
        currStRtn=self.shoeSys.sendCmnd(self.CURRSTATE_CMND, svcName=svcName)
        if self.dbug > 0:
            print("----------------Current state cmnd return", currStRtn.msgArgs)

        state=ShoeState(
                xmlText=currStRtn.msgArgs['CurrentState'])

        svcState=state.getCfg()
        if self.dbug > 0:
            print("----------------Dev State Rtn", svcState)

        return svcState

    def _fmtOp(self, opData, tab=0):
        fmt= '{0:>%s}{1:%s} : {2:<0}\n'%(tab, self.FMT_LBL_LEN)
        lblessFmt= '{0:>%s}{1:%s}   {2:<0}\n'%(tab, self.FMT_LBL_LEN)
        fmtStr=''

        try:

            for lbl,val in opData.items():
                if type(val) is dict:
                    fmtStr=fmtStr+fmt.format('', str(lbl), '')
                    fmtStr=fmtStr+self._fmtOp(val, tab+self.FMT_TAB_LEN)
                elif type(val) is list:
                    fmtStr=fmt.format('', lbl, '')
                    lstBreak='-'*self.FMT_LBL_LEN
                    fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')
                    for valEl in val:
                        fmtStr=fmtStr+self._fmtOp(valEl, tab+self.FMT_TAB_LEN)
                        fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')
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
        self.shoeSys=ShoeSys(self.host)
        self.op=ShoeOp(self.shoeSys, dbug=2)
        self.cfg=False
        self.httpHandler=TestShoeCurrStHttpHandler
        #This gets config
        self.httpTest()
        return

    def _sendTestMsgs(self):
        rtn=self.cfg
        if self.cfg is False:
            self.shoeSys.getCfg()
            self.cfg=True
        return rtn

class TestShoeOpHttpHandler(TestShoeHttp.TestShoeHttpHandler):
    def do_POST(self):
        self.testSvcs= [ TestActSvc(),
                    TestGroupCtrlSvc(),
                    TestZoneCtrlSvc()]

        headerIn=dict(self.headers)
        self.soapAct=headerIn['SOAPACTION']

        self.postRtn=self._getRtn()

        super().do_POST()
        return

    def _getRtn(self):
        return None

class TestShoeCurrStHttpHandler(TestShoeOpHttpHandler):
    def _getRtn(self):
        testSvcRtn=None

        for testSvc in self.testSvcs:
            if testSvc.getCurrStHdr['SOAPACTION'] == self.soapAct:
                testSvcRtn=testSvc
                break

        return testSvcRtn.getCurrStRtnXml

class TestShoeOpGetCurrSt(TestShoeOp):
    def setUp(self):
        super().setUp()
        #self.testSvcs=[ self.testActSvc,  ]
        self.testSvcs=[ self.testActSvc,
                    self.testGroupCtrlSvc,
                    self.testZoneCtrlSvc]
        return

    def _sendTestMsgs(self):
        if super()._sendTestMsgs():
            self.currSt=self.op._getCurrState(self.svcName)
        return

    def runTest(self):
        for testSvc in self.testSvcs:
            self._testGetCurrSt(testSvc)
            print(self.currSt)
            self.assertCountEqual(self.currSt, self.currStTestRef)

            currStFmt=self.op._fmtOp(self.currSt)
            print(currStFmt)
            self.assertEqual(currStFmt, self.currStFmtTestRef)
        return

    def _testGetCurrSt(self, testSvc):
        self.currStTestRef =testSvc.currSt
        self.currStFmtTestRef =testSvc.currStFmt
        self.postRtn=testSvc.getCurrStRtnXml
        self.svcName=testSvc.name
        self.httpTest()
        return
