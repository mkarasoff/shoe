##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeMsg.py
#Unit test for shoeMsg module.
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
from shoelib.shoeMsg import *
from lxml import etree

class TestShoeMsg(TestShoeHttp):
    #Set to 0 to do the long test.  Set to a number N>0 to itereate N
    FAST_TEST=1

    def setUp(self):
        super().setUp()

        self.port=60006
        self.host='127.0.0.1'
        self.testRootDev=TestRootDev()
        self.testCmnds=self.testRootDev.cmnds
        return

    def _sendTestMsgs(self):
        self.shoeMsg = ShoeMsg(self.host,
                                self.testCmnd.path,
                                self.testCmnd.name,
                                self.testCmnd.urn,
                                self.testCmnd.args,
                                10)
        self.shoeMsg.send()
        self.shoeMsg.parse()
        self._checkMsg(self.testCmnd)
        return

class TestShoeMsgCmnds(TestShoeMsg):
    def runTest(self):
        for testCmnd in self.testCmnds:
            print("@@@@@@@@@@@@@@@@@@@@@@@ %s: Test %s @@@@@@@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, testCmnd.name))
            self.httpTest(testCmnd)
            print("@@@@@@@@@@@@@@@@@@@@@ %s: Test Done %s @@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, testCmnd.name))

            if self.FAST_TEST>0 and self.sendCnt > self.FAST_TEST:
                    break

        return

    def _checkMsg(self, testCmnd):
        self.assertEqual(self.shoeMsg.cmnd, testCmnd.name, 'Parse error: cmnd')
        self.assertEqual(self.shoeMsg.urn, testCmnd.urn, 'Parse error: urn')
        self.assertEqual(self.shoeMsg.args, testCmnd.args, 'Parse error: urn')
        self.assertEqual(self.srvRxMsg, testCmnd.msg)
        self.assertEqual(self.srvRxHdr, testCmnd.hdr)

        reply=self.shoeMsg.reply

        self.assertEqual(reply.cmnd, testCmnd.name +
                            "Response", 'ParseErr: cmnd')
        self.assertEqual(reply.urn, testCmnd.urn,
                            'ParseErr: urn')
        self.assertDictEqual(reply.args, testCmnd.msgReplyArgs,
                            'Parse error: args\r %s \r %s' %
                            (reply.args, testCmnd.msgReplyArgs) )

        return

#This broke when impliemented test for dual HTTP servers.
#class TestShoeMsgBroken(TestShoeMsgCmnds):
#    def _checkErr(self, e):
#        print("ERROR MESSAGE:", str(e))
#        if type(e) is not etree.XMLSyntaxError:
#            raise e
#        return
#
#    def _modTestCmnd(self, testCmnd):
#        idx=randrange(len(testCmnd.rtnMsg)-5)
#
#        testCmnd.rtnMsg=testCmnd.rtnMsg[0:idx]
#        return testCmnd
#
#    def runTest(self):
#        for testCmnd in self.testCmnds:
#            print("@@@@@@@@@@@@@@@@@@@@@@@ %s: Test %s @@@@@@@@@@@@@@@@@@@@@@@@@@@@@"\
#                    % (self.__class__.__name__, testCmnd.name))
#            try:
#                self.httpTest(testCmnd)
#                raise ValueError("This should throw an error")
#            except Exception as e:
#                self._checkErr(e)
#
#            print("@@@@@@@@@@@@@@@@@@@@@ %s: Test Done %s @@@@@@@@@@@@@@@@@@@@@@@@"\
#                    % (self.__class__.__name__, testCmnd.name))
#
#            if self.FAST_TEST>0 and self.sendCnt > self.FAST_TEST:
#                 break
#
#        return
#

#For a network connected computer, this runs slow.
#class TestShoeMsgBadHost(TestShoeMsgBroken):
#    def _checkErr(self, e):
#        errMsg=str(e)
#        print("ERROR MESSAGE:", errMsg)
#        if type(e) is ShoeMsgHttpSendErr:
#            errStr=errMsg[:errMsg.find(']')+1]
#            if(errStr != "[Errno -2]" and errStr != "[Errno -3]"):
#                raise e
#        else:
#            raise e
#        return
#
#    def _modTestCmnd(self, testCmnd):
#        self.host = 'ni.shrubbery'
#        return testCmnd

class TestShoeMsgBadRequest(TestShoeMsgCmnds):
    def _checkErr(self, e):
        errMsg=str(e)
        print("ERROR MESSAGE:", errMsg, type(e), self.errRtn)
        if type(e) is ShoeMsgHttpRtnStatusErr:
            if(int(errMsg) != self.errRtn):
                raise e
        elif type(e) is ShoeMsgHttpSendErr:
            pass
        else:
            raise e
        return

    def runTest(self):

        rtnCodes=(400, 401, 403, 404, 405, 406, 407, 408, 409, 410, \
                100, 101, 102, 103, \
                201, 202, 203, 204, 205, 206, 207, 208, 226,\
                300, 301, 302, 303, 304, 307, 308,\
                411, 412, 413, 414, 415, 416, 417, 418, \
                421, 422, 423, 425, 428, 429, 431, 451,\
                500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511)

        for rtnCode in rtnCodes:
            self.errRtn=rtnCode
            testCmnd=self.testCmnds[self.sendCnt%len(self.testCmnds)]
            testCmnd.rtnCode=self.errRtn
            try:
                self.httpTest(testCmnd)
            except Exception as e:
                self._checkErr(e)

            if self.FAST_TEST>0 and self.sendCnt > self.FAST_TEST:
                 break

        return

#This broke when impliemented test for dual HTTP servers.
#class TestShoeMsgBadPort(TestShoeMsgBroken):
#    def _checkErr(self, e):
#        errMsg = str(e)
#        print(errMsg, type(e), self.srvPort)
#        if type(e) in (ShoeMsgHttpSendErr,):
#            if(errMsg[:errMsg.find(']')+1] == "[Errno 111]"):
#                pass
#        else:
#            raise e
#        return
#
#    def _modTestCmnd(self, testCmnd):
#        self.srvPort=randrange(1024,65531)
#        return testCmnd
#

#This broke when impliemented test for dual HTTP servers.
#class TestShoeMsgNoReply(TestShoeMsgBroken):
#    def _checkErr(self, e):
#        errMsg = str(e)
#        print(errMsg, type(e), self.port)
#        if type(e) in (ShoeMsgHttpSendErr,):
#            pass
#        else:
#            raise e
#        return
#
#    def _modTestCmnd(self, testCmnd):
#        testCmnd.noReply=True
#        return testCmnd
#
#
#
