##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeCfgXml.py
#Unit test for shoeCfgXml module.
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
from shoelib.shoeCfgXml import *

from pprint import pprint
class TestShoeCfgXml(TestShoeHttp):
    def setUp(self):
        super().setUp()
        self.cmndList=None
        self.cmndArgCfg=None
        self.reply=None
        self.host='127.0.0.1'

        self.testObjs=[
                self.testRootDev,
                self.testActSvc,
                self.testGroupCtrlSvc,
                self.testZoneCtrlSvc]
        return

    def _sendTestMsgs(self):
        shoeCfg=ShoeCfgXml(self.host, self.testFile, loglvl=logging.DEBUG)
        self.xmlDict=shoeCfg.getCfg()
        return

class TestShoeCfgXmlDict(TestShoeCfgXml):
    def runTest(self):
        for testObj in self.testObjs:
            print("Testing: ", testObj.name)
            self._testXml(testObj)
        return

    def _testXml(self, testObj):
        self.testFile=testObj.fileName
        self.getRtn=testObj.xmlStr

        self.httpTest()

        errMsg = "Shoe cfg: dict not correct: %s." % \
                    testObj.fileName

        print("Return")
        pprint(self.xmlDict)
        print("Expected")
        pprint(testObj.xmlDict)

        self.assertDictEqual(self.xmlDict,
                        testObj.xmlDict,
                        errMsg)

        return
