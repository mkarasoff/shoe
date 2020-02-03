##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeInfo.py
#Class that implements "Get Info" CLI functions
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

class ShoeInfo(ShoeOp):
    ACT_FNAME_KEY='friendlyName'
    SVC_NAME_KEY='serviceName'

    def __init__(self, shoeSys, loglvl=0):
        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        super().__init__(shoeSys, loglvl)
        return

    def getInfo(self, extend=False):
        info=self.shoeSys.getInfo()
        info[self.SVC_NAME_KEY]=info[self.ACT_FNAME_KEY]
        del info[self.ACT_FNAME_KEY]

        fmtStr = self._fmtOp(info)
        a=[]
        a.append(fmtStr)
        print(a)
        if extend:
            for svcName in self.svcNames:
                state=self._getCurrState(svcName)
                fmtStr += self._fmtOp(state)

        return fmtStr

##############################UNIT TESTS########################################
from test_shoe import *

class TestShoeInfo(TestShoeHttp):

    def setUp(self):
        super().setUp()
        self.port=60006
        self.host='127.0.0.1'
        self.svcName=None
        self.shoeSys=ShoeSys(self.host, loglvl=logging.DEBUG)
        self.info=ShoeInfo(self.shoeSys, loglvl=logging.DEBUG)
        self.cfg=False
        self.httpHandler=TestShoeCurrStHttpHandler
        #This should run get_cfg()
        self.httpTest()
        return

    def _sendTestMsgs(self):
        rtn=self.cfg
        if self.cfg is False:
            self.shoeSys.getCfg()
            self.cfg=True
        return self.cfg

class TestShoeInfoGetInfo(TestShoeInfo):
    def _sendTestMsgs(self):
        if super()._sendTestMsgs():
            self.infoFmt=self.info.getInfo()
        return

    def runTest(self):
        self.httpTest()
        self.assertEqual(self.infoFmt, self.testAiosDev.infoFmt)
        print(self.infoFmt)
        return

class TestShoeInfoGetInfoExt(TestShoeInfo):
    def _sendTestMsgs(self):
        if super()._sendTestMsgs():
            self.infoFmt=self.info.getInfo(extend=True)
        return

    def runTest(self):
        self.httpTest()
        testRtn=self.testAiosDev.infoFmt + \
                self.testActSvc.currStFmt + \
                self.testGroupCtrlSvc.currStFmt + \
                self.testZoneCtrlSvc.currStFmt

        self.assertEqual(self.infoFmt, testRtn)

        print(self.infoFmt)

        return
