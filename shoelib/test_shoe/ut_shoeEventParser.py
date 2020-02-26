##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeEvent.py
#Unit test for shoeEvent module.
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
from .testShoeHttp import *
from shoelib.shoeEventParser import *
import pprint
from console_log import *

class TestShoeEvent(unittest.TestCase):
    def setUp(self):
        self.testSvcs=[ TestActSvc(), TestGroupCtrlSvc(), TestZoneCtrlSvc()]
        return

    def runTest(self):
        log=ConsoleLog(self.__class__.__name__, logging.DEBUG)

        shoeCfg=ShoeCfgXml()

        for svc in self.testSvcs:
            cmnd = svc.cmnds['GetCurrentState']
            rtnMsgBody = cmnd.rtnMsgBody
            xmlTextRoot = shoeCfg._parseXml(rtnMsgBody.encode('utf-8'))
            currStRtn=shoeCfg._etreeToDict(xmlTextRoot)

            shoeSt=ShoeEventParser(
                xmlText=currStRtn['CurrentState'],
                loglvl=logging.DEBUG)

            currSt=shoeSt.parse()

            pp = pprint.PrettyPrinter(indent=2)
            print(svc.name)
            print("Returned")
            pp.pprint(currSt)
            print("Expected")
            pp.pprint(cmnd.rtn['CurrentState'])

            if type(cmnd.rtn['CurrentState']) != dict:
                self.assertEqual(cmnd.rtn['CurrentState'], currSt)
            else:
                self.assertDictEqual(cmnd.rtn['CurrentState'], currSt)
        return
