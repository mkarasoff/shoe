##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeMsg.py
#Class that communicates messages to a HEOS device using HTTP PUT.
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
import http.client, urllib.request, urllib.parse, urllib.error
from http.client import HTTPConnection
from collections import OrderedDict
from shoeMsgXml import *
import re
from lxml import etree
from console_log import *

class ShoeMsg():
    PORT            = 60006

    ACCEPT_RANGES_VAL   = 'bytes'
    CONTENT_TYPE_VAL    = 'text/xml; charset="utf-8"'
    USER_AGENT_VAL      = 'LINUX UPnP/1.0 Denon-Heos/149200'

    def __init__(self,
                    host,
                    path,
                    cmnd,
                    urn,
                    args=OrderedDict(),
                    loglvl=ConsoleLog.WARNING):

        self.log=ConsoleLog(self.__class__.__name__, loglvl)

        self.host=host
        self.path=path
        self.cmnd=cmnd
        self.urn=urn
        self.args=args
        self.reply=None

        self.loglvl=loglvl

        self._msgLen=0
        self._payload=None
        self._soapaction=None
        self._httpReply=None

        return

    def send(self):
        self.log.debug("Cmnd %s, urn %s, args %s",
                        self.cmnd, self.urn, self.args)
        shoexml = ShoeMsgXml(cmnd=self.cmnd,
                            urn=self.urn,
                            args=self.args)

        self._payload = shoexml.genTree()
        self._soapaction='"%s#%s"' % (self.urn, self.cmnd)
        self._msgLen=str(len(self._payload))

        self._post_cmd()

        return

    def parse(self):
        self.reply=''

        self.log.debug("status %s" % self._httpReply.status)

        try:
            status = int(self._httpReply.status)
        except:
            raise ShoeMsgHttpRtnErr("Unknown")

        if(int(status) == 200):
            try:
                self._payloadRtn=self._httpReply.read()
                shoeMsgXml = ShoeMsgXml(msgXml=self._payloadRtn)
                self.reply=shoeMsgXml.parseTree()
            except:
                raise
        else:
            raise ShoeMsgHttpRtnErr(str(status))

        if(self.urn != self.reply.urn):
            errMsg = "HTTP Rtn URN Mismatch %s %s" % (self.urn, self.reply.urn)
            raise ShoeMsgHttpRtnErr(errMsg)

        cmndReply = self.cmnd + "Response"
        if(cmndReply != self.reply.cmnd):
            errMsg = "HTTP Rtn Method Mismatch %s %s" % (cmndReply, self.reply.cmnd)
            raise ShoeMsgHttpRtnErr(errMsg)

        return self.reply

    def _post_cmd(self):

        conn = http.client.HTTPConnection(self.host, ShoeMsg.PORT)

        if self.loglvl <= self.log.DEBUG:
            conn.set_debuglevel(1)
        else:
            conn.set_debuglevel(0)

        conn.putrequest('POST', self.path, skip_host=True, skip_accept_encoding=True)

        host="%s:%s" % (self.host, ShoeMsg.PORT)

        conn.putheader('HOST', host)
        conn.putheader('CONTENT-LENGTH', self._msgLen)
        conn.putheader('Accept-Ranges', ShoeMsg.ACCEPT_RANGES_VAL)
        conn.putheader('CONTENT-TYPE' , ShoeMsg.CONTENT_TYPE_VAL)
        conn.putheader('SOAPACTION' , self._soapaction)
        conn.putheader('USER-AGENT' , ShoeMsg.USER_AGENT_VAL)

        try:
            conn.endheaders(self._payload)
        except Exception as e:
            raise ShoeMsgHttpSendErr("%s %s" % (str(e), host))

        try:
            self._httpReply = conn.getresponse()
        except Exception as e:
            raise ShoeMsgHttpSendErr("%s %s" % (str(e), host))

        conn.close()

        return

#############################EXCEPTIONS#########################################
class ShoeMsgHttpSendErr(Exception):
    pass
class ShoeMsgHttpRtnErr(Exception):
    pass

##############################UNIT TESTS########################################
from test_shoe import *
from random import *
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
        self.shoeMsg = ShoeMsg(self.host, self.path, self.cmndName, self.urn, self.args, 10)
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

        self.assertEqual(reply.cmnd, testCmnd.name + "Response", 'ParseErr: cmnd')
        self.assertEqual(reply.urn, testCmnd.urn, 'ParseErr: urn')
        self.assertDictEqual(reply.args, testCmnd.msgReplyArgs, 'Parse error: args\r %s \r %s' %
                (reply.args, testCmnd.msgReplyArgs) )

        return

class TestShoeMsgBroken(TestShoeMsgCmnds):
    def _checkErr(self, e):
        print("ERROR MESSAGE:", str(e))
        if type(e) is not etree.XMLSyntaxError:
            raise e
        return

    def _modTestCmnd(self, testCmnd):
        idx=randrange(len(testCmnd.rtnMsg)-5)

        testCmnd.rtnMsg=testCmnd.rtnMsg[0:idx]
        return testCmnd

    def runTest(self):
        for testCmnd in self.testCmnds:
            print("@@@@@@@@@@@@@@@@@@@@@@@ %s: Test %s @@@@@@@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, testCmnd.name))
            try:
                self.httpTest(testCmnd)
                raise ValueError("This should throw an error")
            except Exception as e:
                self._checkErr(e)

            print("@@@@@@@@@@@@@@@@@@@@@ %s: Test Done %s @@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, testCmnd.name))

            if self.FAST_TEST>0 and self.sendCnt > self.FAST_TEST:
                 break

        return

class TestShoeMsgBadHost(TestShoeMsgBroken):
    def _checkErr(self, e):
        errMsg=str(e)
        print("ERROR MESSAGE:", errMsg)
        if type(e) is ShoeMsgHttpSendErr:
            errStr=errMsg[:errMsg.find(']')+1]
            if(errStr != "[Errno -2]" and errStr != "[Errno -3]"):
                raise e
        else:
            raise e
        return

    def _modTestCmnd(self, testCmnd):
        self.host = 'ni.shrubbery'
        return testCmnd

class TestShoeMsgBadRequest(TestShoeMsgCmnds):
    def _checkErr(self, e):
        errMsg=str(e)
        print("ERROR MESSAGE:", errMsg, type(e), self.errRtn)
        if type(e) is ShoeMsgHttpRtnErr:
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

class TestShoeMsgBadPort(TestShoeMsgBroken):
    def _checkErr(self, e):
        errMsg = str(e)
        print(errMsg, type(e), self.srvPort)
        if type(e) in (ShoeMsgHttpSendErr,):
            if(errMsg[:errMsg.find(']')+1] == "[Errno 111]"):
                pass
        else:
            raise e
        return

    def _modTestCmnd(self, testCmnd):
        self.srvPort=randrange(1024,65531)
        return testCmnd

class TestShoeMsgNoReply(TestShoeMsgBroken):
    def _checkErr(self, e):
        errMsg = str(e)
        print(errMsg, type(e), self.srvPort)
        if type(e) in (ShoeMsgHttpSendErr,):
            pass
        else:
            raise e
        return

    def _modTestCmnd(self, testCmnd):
        testCmnd.noReply=True
        return testCmnd
