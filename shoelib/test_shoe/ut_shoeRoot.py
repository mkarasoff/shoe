##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeRoot.py
#Unit test for shoeRoot module.
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
##########################################################################
##############################UNIT TESTS##################################
from .testShoeHttp import *
from shoelib.shoeRoot import *

class TestShoeRoot(TestShoeHttp):

    def setUp(self):
        super().setUp()
        self.reply=None
        self.port=60006
        self.host='127.0.0.1'
        self.rootDev=ShoeRoot(host=self.host, port=self.port, loglvl=logging.DEBUG)
        self.testCbFunc=self._setUp
        self.httpTest()
        self.testCbFunc=self._sendTestMsgs
        return

    def _setUp(self):
        self.rootDev.setUp()
        return

    def _sendTestMsgs(self):
        cmnd = self.cmnd
        print("Cmnd %s" % self.cmnd)
        self.reply=self.rootDev.sendCmnd(cmnd.name, cmnd.args, cmnd.svcName, cmnd.devName)
        return

#Check a command within range.
class TestShoeRootCmnds(TestShoeRoot):
    def runTest(self):
        for cmnd in self.testRootDev.cmnds:
            print("^^^^^^^^TestShoeInRange %s %s %s^^^^^^^^" %
                    (cmnd.svcName, cmnd.devName, cmnd))
            self.cmnd=cmnd
            self.httpTest(cmnd)

            self.assertEqual(self.reply.args,
                            cmnd.rtn)

            #self.assertEqual(self.reply.cmnd,
            #             cmnd.name + "Response")
        return
