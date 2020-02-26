##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeCmnd.py
#Unit test for shoeCmnd.py module.
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
##############################UNIT TESTS####################################
from .testShoeHttp import *
from shoelib.shoeCmnd import *

class TestShoeCmnd(TestShoeHttp):
    #Set to 0 to do the long test.  Set to a number N>0 to itereate N
    FAST_TEST=0

    def setUp(self):
        super().setUp()

        self.port=60006
        self.host='127.0.0.1'
        self.testRootDev=TestRootDev()
        self.cmnds=self.testRootDev.cmnds
        self.cmnd = None
        return

    def _sendTestMsgs(self):
        self.shoeCmnd = ShoeCmnd(host=self.host,
                                path=self.cmnd.path,
                                urn=self.cmnd.urn,
                                cmnd=self.cmnd.name,
                                argsIn=self.cmnd.args,
                                argsCfg=self.cmnd.argsCfg,
                                loglvl=logging.DEBUG)
        self.shoeCmnd.send()
        self.shoeCmnd.parse()
        self._checkMsg(self.cmnd)
        return

class TestShoeCmnds(TestShoeCmnd):
    def runTest(self):
        for cmnd in self.cmnds:
            self.cmnd = cmnd
            print("@@@@@@@@@@@@@@@@@@@@@@@ %s: Test %s @@@@@@@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, cmnd.name))
            self.httpTest(cmnd)
            print("@@@@@@@@@@@@@@@@@@@@@ %s: Test Done %s @@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, cmnd.name))

            if self.FAST_TEST>0 and self.sendCnt > self.FAST_TEST:
                    break

        return

    def _checkMsg(self, cmnd):

        self.assertEqual(self.shoeCmnd.cmnd, cmnd.name, 'Parse error: cmnd')
        self.assertEqual(self.shoeCmnd.urn, cmnd.urn, 'Parse error: urn')
        self.assertDictEqual(self.shoeCmnd.args, cmnd.args)
        self.assertEqual(self.srvRxMsg, cmnd.msg)
        self.assertEqual(self.srvRxHdr, cmnd.hdr)

        reply=self.shoeCmnd.cmndReply

        print("reply", reply.args)
        print("expected", cmnd.rtn)

        self.assertEqual(reply.cmnd, cmnd.name + "Response", 'ParseErr: cmnd')
        self.assertEqual(reply.urn, cmnd.urn, 'ParseErr: urn')
        self.assertDictEqual(reply.args, cmnd.rtn)
        #self.assertDictEqual(reply.args, cmnd.msgReplyArgs, 'Parse error: args\r %s \r %s' %
        #        (reply.args, cmnd.msgReplyArgs) )

        return
