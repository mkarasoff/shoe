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

class ShoeMsg():
    PORT            = 60006

    ACCEPT_RANGES_VAL   = 'bytes'
    CONTENT_TYPE_VAL    = 'text/xml; charset="utf-8"'
    USER_AGENT_VAL      = 'LINUX UPnP/1.0 Denon-Heos/149200'

    def __init__(self, host, path, method, urn, msgArgs={}, dbug=0):
        self.host=host
        self.path=path
        self.method=method
        self.urn=urn
        self.msgArgs=msgArgs
        self.response=None

        self.dbug=dbug

        self._msgLen=0
        self._payload=None
        self._soapaction=None
        self._httpResp=None

        return

    def send(self):
        shoexml = ShoeMsgXml(method=self.method,
                            urn=self.urn,
                            msgArgs=self.msgArgs)

        self._payload = shoexml.genTree()
        self._soapaction='"%s#%s"' % (self.urn, self.method)
        self._msgLen=str(len(self._payload))

        self._post_cmd()

        return

    def parse(self):
        self.response=''

        if self.dbug > 0:
            print("status", self._httpResp.status)

        try:
            status = int(self._httpResp.status)
        except:
            raise ShoeMsgHttpRtnErr("Unknown")

        if(int(status) == 200):
            try:
                self._payloadRtn=self._httpResp.read()
                shoeMsgXml = ShoeMsgXml(xmlText=self._payloadRtn)
                self.response=shoeMsgXml.parseTree()
            except:
                raise
        else:
            raise ShoeMsgHttpRtnErr(str(status))

        if(self.urn != self.response.urn):
            errMsg = "HTTP Rtn URN Mismatch %s %s" % (self.urn, self.response.urn)
            raise ShoeMsgHttpRtnErr(errMsg)

        methodResp = self.method + "Response"
        if(methodResp != self.response.method):
            errMsg = "HTTP Rtn Method Mismatch %s %s" % (methodResp, self.response.method)
            raise ShoeMsgHttpRtnErr(errMsg)

        return self.response

    def _post_cmd(self):

        conn = http.client.HTTPConnection(self.host, ShoeMsg.PORT)

        conn.set_debuglevel(self.dbug)
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
            raise ShoeMsgHttpSendErr(str(e)) from e

        try:
            self._httpResp = conn.getresponse()
        except Exception as e:
            raise ShoeMsgHttpRtnErr(str(e)) from e

        conn.close()

        return

#############################EXCEPTIONS#########################################
class ShoeMsgHttpSendErr(Exception):
    pass
class ShoeMsgHttpRtnErr(Exception):
    pass

##############################UNIT TESTS########################################
from test_shoe import *

class TestShoeMsg(TestShoeHttp):

    def setUp(self):
        super().setUp()
        self.shoeMsg=None
        self.path=None
        self.method=None
        self.urn=None
        self.msgArgs={}

        self.port=60006
        self.host='127.0.0.1'

        return

    def _sendTestMsgs(self):
        self.shoeMsg = ShoeMsg(self.host, self.path, self.method, self.urn, self.msgArgs, 10)
        self.shoeMsg.send()
        self.shoeMsg.parse()
        return

class TestShoeMsgCreateGroup(TestShoeMsg):
    def setUp(self):
        super().setUp()
        print("@@@@@@@@@@@@@@@@@@@@@@Test Create Group@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        self.method='CreateGroup'

        self.msgArgs=OrderedDict()
        self.msgArgs['GroupFriendlyName']='Jam'
        self.msgArgs['GroupMemberUUIDList']=\
                'caf7916a94db1a1300800005cdfbb9c6,f3ddb59f3e691f1e00800005cdff1706'
        self.msgArgs['GroupMemberChannelList']=''
        self.path='/upnp/control/AiosServicesDvc/GroupControl'
        self.urn='urn:schemas-denon-com:service:GroupControl:1'

        self.testObj=self.testGroupCtrlSvc

        self.path=self.testObj.urlPath
        self.urn=self.testObj.urn

        self.srvRxMsg=None
        self.testRxMsg=self.testObj.createGroupCmndXml.encode('utf-8')

        self.srvRxHdr=None
        self.testRxHdr=self.testObj.createGroupHdr

    def runTest(self):
        self.postRtn=self.testObj.createGroupRtnXml
        self.httpTest()

        self.assertEqual(self.shoeMsg.method, self.method, 'Parse error: method')
        self.assertEqual(self.shoeMsg.urn, self.urn, 'Parse error: urn')
        self.assertEqual(self.shoeMsg.msgArgs, self.msgArgs, 'Parse error: urn')

        self.assertEqual(self.srvRxMsg, self.testRxMsg)
        self.assertEqual(self.srvRxHdr, self.testRxHdr)

        return

class TestShoeMsgBroken(TestShoeMsgCreateGroup):
    def runTest(self):
        self.testRes=self.TestResponse()
        self.shoeMsg = ShoeMsg(self.host, self.path, self.method, self.urn, self.msgArgs, 10)
        self.shoeMsg._httpResp=self.testRes
        try:
            self.shoeMsg.parse()
        except etree.XMLSyntaxError:
            pass
        except:
            raise

        return

    class TestResponse():
        def __init__(self):
            self.status=200

        def read(self):
            response=(
                    's:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
                    's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">')

            return response.encode('utf-8')

class TestShoeMsgParse(TestShoeMsgCreateGroup):
    def runTest(self):
        self.method='CreateGroup'
        self.msgArgs=OrderedDict()
        self.msgArgs['GroupUUID']='17083c46d003001000800005cdfbb9c6'

        responseTemp=(
                '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
                's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
                '<s:Body>'
                '<u:%s xmlns:u="%s">'
                '<%s>%s</%s>'
                '</u:%s>'
                '</s:Body>'
                '</s:Envelope>')

        response=responseTemp % (
                self.method + "Response",
                self.urn,
                list(self.msgArgs.items())[0][0],
                list(self.msgArgs.items())[0][1],
                list(self.msgArgs.items())[0][0],
                self.method + "Response")

        self.shoeMsg = ShoeMsg(self.host, self.path, self.method, self.urn, self.msgArgs, 10)
        self.shoeMsg._httpResp=self.TestResponse(response)
        response = self.shoeMsg.parse()

        self.assertEqual(response.method, self.method + "Response", 'ParseErr: method')
        self.assertEqual(response.urn, self.urn, 'ParseErr: urn')
        self.assertEqual(response.msgArgs, self.msgArgs, 'Parse error: args')
        return

    class TestResponse():
        def __init__(self, response):
            self.status=200
            self.response=response
        def read(self):
            return self.response.encode('utf-8')

class TestShoeMsgBadHost(TestShoeMsgCreateGroup):
    def runTest(self):
        self.host = 'ni.shrubbery'
        try:
            self.httpTest()
            raise ValueError("This should throw an error")

        except ShoeMsgHttpSendErr as e:
            errMsg = str(e)
            print(errMsg)
            if(errMsg[:errMsg.find(']')+1] == "[Errno -3]"):
                pass
            else:
                raise
        except:
            raise

        return

class TestShoeMsgBadRequest(TestShoeMsgCreateGroup):
    def runTest(self):
        self.rtnCode=400

        try:
            self.httpTest()
            raise ValueError("This should throw an error")

        except ShoeMsgHttpRtnErr as e:
            if(str(e)=="400"):
                pass
            else:
                raise
        except:
            raise

        return

class TestShoeMsgBadPort(TestShoeMsgCreateGroup):
    def runTest(self):
        self.srvPort=24242
        try:
            self.httpTest()
            raise ValueError("This should throw an error")

        except ShoeMsgHttpSendErr as e:
            errMsg = str(e)
            print(errMsg)
            if(errMsg[:errMsg.find(']')+1] == "[Errno 111]"):
                pass
            else:
                raise
        except:
            raise

        return

class TestShoeMsgNoReply(TestShoeMsgCreateGroup):
    def runTest(self):
        self.noResp=True
        try:
            self.httpTest()
            raise ValueError("This should throw an error")

        except ShoeMsgHttpRtnErr as e:
            pass

        except:
            raise

        return

class TestShoeMsgActGetState(TestShoeMsg):

    def runTest(self):
        print("@@@@@@@@@@@@@@@@@Act Get State@@@@@@@@@@@@@@@@@@@@@@@@@")
        self.testObj=self.testActSvc

        self.method=self.testObj.getCurrStCmnd
        self.msgArgs=OrderedDict()
        self.urn=self.testObj.urn

        self.testRxMsg=self.testObj.getCurrStCmndXml.encode('utf-8')
        self.testRxHdr=self.testObj.getCurrStHdr
        self.postRtn=self.testObj.getCurrStRtnXml

        self.httpTest()

        return

class TestShoeMsgZoneGetState(TestShoeMsg):

    def runTest(self):
        print("@@@@@@@@@@@@@@@@@Zone Get State@@@@@@@@@@@@@@@@@@@@@@@@@")
        self.testObj=self.testZoneCtrlSvc
        self.method=self.testObj.getCurrStCmnd
        self.msgArgs=OrderedDict()
        self.urn=self.testObj.urn

        self.testRxMsg=self.testObj.getCurrStCmndXml.encode('utf-8')
        self.testRxHdr=self.testObj.getCurrStHdr
        self.postRtn=self.testObj.getCurrStRtnXml

        self.httpTest()
        return
