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

class TestShoeHttp(unittest.TestCase):
    testActSvc=TestActSvc()
    testGroupCtrlSvc=TestGroupCtrlSvc()
    testZoneCtrlSvc=TestZoneCtrlSvc()
    testAiosDev=TestAiosDev()

    def setUp(self):
        self.srvPort = 60006
        self.srvHost = '127.0.0.1'
        self.postRtn=None
        self.getRtn=None
        self.noResp=False
        self.rtnCode=200

        self.srvRxMsg=None
        self.srvRxHdr=None
        self.httpHandler=self.TestShoeHttpHandler
        return

    #Override This!  Gets called in httpTest() during data transaction.
    def _sendTestMsgs(self):
        reply=None
        return

    def httpTest(self):
        self.TestShoeHttpHandler.callObj=self
        self.TestShoeHttpHandler.postRtn=self.postRtn
        self.TestShoeHttpHandler.getRtn=self.getRtn
        self.TestShoeHttpHandler.noResp=self.noResp
        self.TestShoeHttpHandler.rtnCode=self.rtnCode

        httpd = HTTPServer((self.srvHost, self.srvPort), self.httpHandler)
        httpSrvThread=threading.Thread(target=httpd.serve_forever)
        httpSrvThread.deamon=True

        try:
            httpSrvThread.start()
            #Customize test messages by overriding
            self._sendTestMsgs()

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
        noResp=False
        getRtn=None

        def do_GET(self):
            print("@@@@@@@@@@@@@@@@@@@@@@@GET@@@@@@@@@@@@@@@@@@@@@@")
            if self.noResp:
                return

            reqPath = self.path

            testActSvc=TestShoeHttp.testActSvc
            testGroupCtrlSvc=TestShoeHttp.testGroupCtrlSvc
            testZoneCtrlSvc=TestShoeHttp.testZoneCtrlSvc
            testAiosDev=TestShoeHttp.testAiosDev

            self.send_response(200)
            self.end_headers()

            if self.getRtn:
                rtnMsg=self.getRtn

            elif reqPath == testActSvc.url:
                rtnMsg=testActSvc.xmlStr

            elif reqPath == testGroupCtrlSvc.url:
                rtnMsg=testGroupCtrlSvc.xmlStr

            elif reqPath == testZoneCtrlSvc.url:
                rtnMsg=testZoneCtrlSvc.xmlStr

            elif reqPath == testAiosDev.url:
                rtnMsg=testAiosDev.xmlStr

            else:
                raise ValueError(reqPath)

            self.wfile.write(rtnMsg)
            return

        def do_POST(self):
            print("@@@@@@@@@@@@@@@@@@@POST@@@@@@@@@@@@@@@@@@@@@@@")
            if self.noResp:
                return

            headersIn=dict(self.headers)
            lengthIn=int(headersIn['CONTENT-LENGTH'])

            if self.callObj is not None:
                self.callObj.srvRxMsg = self.rfile.read(lengthIn)
                self.callObj.srvRxHdr = headersIn
                print ("POST Req Msg", self.callObj.srvRxMsg)
                print ("POST Req Hdr", self.callObj.srvRxHdr)

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

                print ("POST Reply", msg)

                self.end_headers()
                self.wfile.write(msg.encode('utf-8'))

            return
