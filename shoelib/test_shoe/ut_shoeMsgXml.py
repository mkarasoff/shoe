##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeMsgXml.py
#Unit Test for shoeMsgXml module
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
from shoelib.shoeMsgXml import *

class TestShoeMsgXml(unittest.TestCase):
    def setUp(self):
        rootDev=TestRootDev()
        self.testCmnds=rootDev.cmnds

    def genMsg(self, cmnd):
        cmndMsg=cmnd.msg.encode('utf-8')

        shoeXml = ShoeMsgXml(cmnd=cmnd.name, urn=cmnd.urn, args=cmnd.args)
        textRtn = shoeXml.genTree()

        print(' ')
        print('Gen: ')
        print('Gen Text:', shoeXml.msgXml)
        print('Cmp Text:', cmndMsg)

        self.assertEqual(shoeXml.msgXml, cmndMsg, 'GenError: xmlTree')
        self.assertEqual(textRtn, cmndMsg, 'GenErrorRtn: xmlTree')
        return

    def parseMsg(self, cmnd):
        cmndMsg=cmnd.msg.encode('utf-8')

        shoeXml  = ShoeMsgXml(msgXml=cmndMsg)
        parseRtn = shoeXml.parseTree()

        print(' ')
        print('Parse: ')
        print('Cmnd: ', shoeXml.cmnd, 'Cmnd Expected: ', cmnd.name)
        print('URN: ', shoeXml.urn, 'URN Expected: ', cmnd.urn)
        print('ARGs         : ', shoeXml.args)
        print('ARGs Expected: ', cmnd.args)

        self.assertEqual(shoeXml.cmnd, cmnd.name, 'Parse error: cmnd')
        self.assertEqual(shoeXml.urn, cmnd.urn, 'Parse error: urn')

        self.assertEqual(shoeXml.args, cmnd.args, 'Parse error: mesgDataArgs')

        self.assertEqual(parseRtn.cmnd, cmnd.name, 'Parse error rtn: cmnd')
        self.assertEqual(parseRtn.urn, cmnd.urn, 'Parse error rtn: urn')
        self.assertEqual(parseRtn.args, cmnd.args, 'Parse error rtn: mesgDataArgs')

class TestShoeMsgParse(TestShoeMsgXml):
    def runTest(self):
        for testCmnd in self.testCmnds:
            self.parseMsg(testCmnd)
        return

class TestShoeMsgXmlGen(TestShoeMsgXml):
    def runTest(self):
        for testCmnd in self.testCmnds:
            self.genMsg(testCmnd)
        return
