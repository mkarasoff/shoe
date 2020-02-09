#############################################################
# testShoeHttp.py
# This is meant to be a base class for unittest classes that
# will need httpd support.
#
#
##############################################################
import unittest
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from test_shoe import *
import inspect
import os

class TestShoeHttp(unittest.TestCase):
    testRootDev=TestRootDev()
    testActSvc=testRootDev.devs[TestActDev.NAME].svcs['ACT']
    testGroupCtrlSvc=testRootDev.devs[TestAiosSvcDev.NAME].svcs['GroupControl']
    testZoneCtrlSvc=testRootDev.devs[TestAiosSvcDev.NAME].svcs['ZoneControl']

    def setUp(self):
        self.srvPort = 60006
        self.srvHost = '127.0.0.1'
        self.postRtn=None
        self.getRtn=None
        self.noReply=False
        self.rtnCode=200

        self.path=None
        self.cmnd=None
        self.urn=None
        self.args={}
        self.argsCfg={}

        self.testCmnd=None
        self.srvRxMsg=None
        self.srvRxHdr=None
        self.httpHandler=self.TestShoeHttpHandler

        self.sendCnt=0

        self.quiet=False
        self.testCbFunc=self._sendTestMsgs
        return

    #Override This!  Gets called in httpTest() during data transaction.
    def _sendTestMsgs(self, *args):
        reply=None
        return

    #Override This!  Allows final modificaitons to a command before sending.
    def _modTestCmnd(self, testCmnd):
        return testCmnd

    def setTestCmnd(self, cmnd):
        self.postRtn    = cmnd.rtnMsg
        self.noReply    = cmnd.noReply
        self.rtnCode    = cmnd.rtnCode
        self.urn        = cmnd.urn
        self.path       = cmnd.path
        self.cmndName   = cmnd.name
        self.args       = cmnd.args
        self.argsCfg    = cmnd.argsCfg
        self.testCmnd   = cmnd
        return

    def httpTest(self, testCmnd=None, *args):
        if testCmnd is not None:
            self._modTestCmnd(testCmnd)

        if testCmnd is not None:
            self.setTestCmnd(testCmnd)

        self.TestShoeHttpHandler.callObj=self
        self.TestShoeHttpHandler.postRtn=self.postRtn
        self.TestShoeHttpHandler.getRtn=self.getRtn
        self.TestShoeHttpHandler.noReply=self.noReply
        self.TestShoeHttpHandler.rtnCode=self.rtnCode
        self.TestShoeHttpHandler.quiet=self.quiet

        httpd = HTTPServer((self.srvHost, self.srvPort), self.httpHandler)
        httpSrvThread=threading.Thread(target=httpd.serve_forever)
        httpSrvThread.deamon=True

        try:
            httpSrvThread.start()
            self.sendCnt=self.sendCnt+1
            #Customize test messages by overriding
            self.testCbFunc()
        except:
            httpd.shutdown()
            raise

        httpd.shutdown()

        return

    def runTest(self):
        return

    class TestShoeHttpHandler(BaseHTTPRequestHandler):
        #The Python HTTP Server wants to send a 48byte server string
        # maybe can figure out how to solve this?
        postRtn = None
        callObj=None
        rtnCode=200
        noReply=False
        getRtn=None
        quiet=False

        def _dbugPrt(self, *args):
            if self.quiet is False:
                print(*args)

        def do_GET(self):
            self._dbugPrt("@@@@@@@@@@@@@@@@@@@@@@@GET@@@@@@@@@@@@@@@@@@@@@@")
            if self.noReply:
                return

            reqPath = self.path

            testActSvc=TestShoeHttp.testActSvc
            testGroupCtrlSvc=TestShoeHttp.testGroupCtrlSvc
            testZoneCtrlSvc=TestShoeHttp.testZoneCtrlSvc
            testRootDev=TestShoeHttp.testRootDev

            self.send_response(200)
            self.end_headers()

            if self.getRtn:
                rtnMsg=self.getRtn

            elif reqPath == testActSvc.scpdPath:
                rtnMsg=testActSvc.xmlStr

            elif reqPath == testGroupCtrlSvc.scpdPath:
                rtnMsg=testGroupCtrlSvc.xmlStr

            elif reqPath == testZoneCtrlSvc.scpdPath:
                rtnMsg=testZoneCtrlSvc.xmlStr

            elif reqPath == testRootDev.url:
                rtnMsg=testRootDev.xmlStr

            else:
                fileName=os.path.basename(reqPath)
                xmlDev=TestShoeXml(fileName)
                rtnMsg=xmlDev.xmlStr

            self.wfile.write(rtnMsg)
            return

        def do_POST(self):
            if self.noReply:
                return
            self._dbugPrt("@@@@@@@@@@@@@@@@@@@POST@@@@@@@@@@@@@@@@@@@@@@@")

            headersIn=dict(self.headers)
            lengthIn=int(headersIn['CONTENT-LENGTH'])

            if self.callObj is not None:
                self.callObj.srvRxMsg = self.rfile.read(lengthIn).decode()
                self.callObj.srvRxHdr = headersIn

                self._dbugPrt ("POST Req Msg", self.callObj.srvRxMsg)
                self._dbugPrt ("POST Req Hdr", self.callObj.srvRxHdr)

            if self.rtnCode != 200:
                self.send_error(self.rtnCode)
            else:
                msg=self.postRtn
                self.sys_version=''
                self.server_version='LINUX UPnP/1.0 Denon-Heos/147202'
                self.send_response(200)
                self.send_header('Content-type', 'text/xml; charset="utf-8"')
                self.send_header('Content-Length', str(len(msg)))
                self.send_header('Accept-Ranges', 'bytes')

                self._dbugPrt ("POST Reply", msg)

                self.end_headers()
                self.wfile.write(msg.encode('utf-8'))

            return
