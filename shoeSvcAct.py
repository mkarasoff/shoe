##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeAct.py
#Class impliments ACT service specific functions.
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
from shoeSvc import *
import copy

class ShoeSvcAct(ShoeSvc):
    SVCLIST_KEY='serviceList'
    DEV_NAME='ACT-Denon'
    NAME='ACT'

    def __init__(self, host, dbug=0, port=60006):
        super().__init__(host=host,
                         devTag=self.DEV_NAME,
                         svcTag=self.NAME,
                         dbug=dbug,
                         port=port)

        self.info=None
        return

    def initSvc(self):
        super().initSvc()
        self.info=self._getInfo()
        return

    def _getInfo(self):
        info=copy.deepcopy(self._dev)
        del info[self.SVCLIST_KEY]
        return info

###############################Unittests#################################
import unittest
from test_shoe import *

class TestShoeSvcAct(unittest.TestCase):
    HOST='127.0.0.1'

    def runTest(self):
        testAiosObj=TestAiosDev()
        self.aiosXmlStr=testAiosObj.xmlStr

        testActObj=TestActSvc()
        self.actXmlStr=testActObj.xmlStr

        self.shoeSvcAct=ShoeSvcAct(host=self.HOST)
        self.shoeSvcAct._getXmlText=self._getXmlText

        self.shoeSvcAct.initSvc()

        print("@@@@@@@@@@@@@@@@@@ACT Arg St Table@@@@@@@@@@@@@@@@@@@@@@@")
        print(self.shoeSvcAct._stateVarTbl)

        self.assertEqual(self.shoeSvcAct._stateVarTbl,
                        testActObj._stateVarTbl,
                        "Arg State Table")

        print("@@@@@@@@@@@@@@@@@@ACT Ctrl Command Table@@@@@@@@@@@@@@@@@@@")
        print(self.shoeSvcAct._cmndTbl)

        self.assertEqual(self.shoeSvcAct._cmndTbl,
                        testActObj._cmndTbl,
                        "Command Table")

        print("@@@@@@@@@@@@@@@@@@Info@@@@@@@@@@@@@@@@@@@")
        print(self.shoeSvcAct.info)
        self.assertEqual(self.shoeSvcAct.info,
                        testAiosObj.act['info'],
                        "Info incorrect")

        getCfgTokenArgs=self.shoeSvcAct.getCmndArgsCfg(testActObj.getCfgTokenCmd)
        print("@@@@@@@@@@@@@@@@@@Get Cfg Token Args@@@@@@@@@@@@@@@@@@@")
        print(getCfgTokenArgs)
        print(testActObj.getCfgTokenArgs)
        self.assertEqual(getCfgTokenArgs,
                        testActObj.getCfgTokenArgs,
                        "Cfg Args")

        getAccPtListArgs=self.shoeSvcAct.getCmndArgsCfg(testActObj.getAccPtListCmnd)
        print("@@@@@@@@@@@@@@@@@@Get Access Pt List Args@@@@@@@@@@@@@@@@@@@")
        print(getAccPtListArgs)
        print(testActObj.getAccPtListArgs)
        self.assertEqual(getAccPtListArgs,
                        testActObj.getAccPtListArgs,
                        "Acct Pt Args")

        return

    def _getXmlText(self):
        print("@@@@@@@@@@@@@@@@@@Shoe Cfg Scpd Path@@@@@@@@@@@@@@@@@@@@")
        print(self.shoeSvcAct.path)

        if(self.shoeSvcAct.path == '/upnp/desc/aios_device/aios_device.xml'):
            xmlStr=self.aiosXmlStr

        elif(self.shoeSvcAct.path =='/ACT/SCPD.xml'):
            xmlStr=self.actXmlStr
        else:
            xmlStr = None

        return xmlStr
