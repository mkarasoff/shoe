#############################################################
# testShoeHttp.py
# This is meant to be a base class for unittest classes that
# will need httpd support.
#
#
##############################################################
import unittest
from threading import Thread
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from .testRootDev import *
import inspect
import os
import time

class TestShoeHttp(unittest.TestCase):
    testRootDev=TestRootDev()
    testActSvc=testRootDev.devs[TestActDev.NAME].svcs['ACT']
    testGroupCtrlSvc=testRootDev.devs[TestAiosSvcDev.NAME].svcs['GroupControl']
    testZoneCtrlSvc=testRootDev.devs[TestAiosSvcDev.NAME].svcs['ZoneControl']

    def setUp(self):
        self.srvPort = 60006
        self.httpSrvData={}
        self.httpSrvData['127.0.0.1'] = self.HandlerData(self)
        self.testCbFunc = self._sendTestMsgs
        self.testCbData = {}

        self.sendCnt    = 0

        self.quiet=False
        return

    #Override This!  Gets called in httpTest() during data transaction.
    def _sendTestMsgs(self, *args):
        reply=None
        return

    #Override This!  Allows final modificaitons to a command before sending.
    def _modTestCmnd(self, testCmnd):
        return testCmnd

    @property
    def httpHandler(self):
        host=list(self.httpSrvData.keys())[0]
        return self.httpSrvData[host].httpHandler

    @httpHandler.setter
    def httpHandler(self, httpHandler):
        host=list(self.httpSrvData.keys())[0]
        self.httpSrvData[host].httpHandler=httpHandler
        return

    @property
    def getRtn(self):
        host=list(self.httpSrvData.keys())[0]
        return self.httpSrvData[host].getRtn

    @getRtn.setter
    def getRtn(self, getRtn):
        host=list(self.httpSrvData.keys())[0]
        self.httpSrvData[host].getRtn=getRtn
        return

    @property
    def srvRxHdr(self):
        host=list(self.httpSrvData.keys())[0]
        return self.httpSrvData[host].srvRx[0]

    @property
    def srvRxMsg(self):
        host=list(self.httpSrvData.keys())[0]
        return self.httpSrvData[host].srvRx[1]

    @property
    def testCmnd(self):
        host=list(self.httpSrvData.keys())[0]
        return self.httpSrvData[host].cmnd

    def getSrvRx(self, host):
        return self.httpSrvData[host].srvRx

    class HandlerData():
        def __init__(self, parent):
            self.getRtn     = None

            self.srvRx      = ('','')
            self.srvRxUrn   = None
            self.srvRxCmnd  = None

            self.httpHandler= parent.TestShoeHttpHandler

            self.postRtn    = None
            self.noReply    = False
            self.rtnCode    = 200
            self.cmnd       = None

        def setTestCmnd(self, cmnd):
            self.postRtn    = cmnd.rtnMsg
            self.noReply    = cmnd.noReply
            self.rtnCode    = cmnd.rtnCode
            self.cmnd       = cmnd
            return

    def setHosts(self, hosts):
        self.httpSrvData={}
        for host in hosts:
            self.httpSrvData[host]=self.HandlerData(self)
        return

    def setHandler(self, handler, host=None):
        if host is None:
            host=list(self.httpSrvData.keys())[0]
        self.httpSrvData[host].httpHandler=handler
        return

    def setGetRtn(self, getRtn, host=None):
        if host is None:
            self.getRtn=getRtn
        else:
            self.httpSrvData[host].getRtn=getRtn
        return

    def setTestCmnd(self, cmnd, hostIp=None):
        if hostIp is not None:
            self.httpSrvData[hostIp].setTestCmnd(cmnd)
        else:
            for hostIp in self.httpSrvData.keys():
                self.httpSrvData[hostIp].setTestCmnd(cmnd)
        return

###################
    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True

    def serveOnPort(self, httpSrv):
        httpSrv.serve_forever()

##################
    def shutDownHttpSrvs(self):
        for  httpSrv in self.httpSrvs:
            ip,port=httpSrv.server_address
            httpSrv.shutdown()
            print("HTTPSrv Stop <<<<<<<<<<<<<<<<<<<<<<<<<", httpSrv, ip)
        del self.httpSrvs
        return

    def httpTest(self, testCmnd=None, host=None):
        if testCmnd is not None:
            self.setTestCmnd(testCmnd, host)

        self.TestShoeHttpHandler.srvData=self.httpSrvData
        self.TestShoeHttpHandler.quiet=self.quiet

        self.httpSrvs=[]

        for hostIp in self.httpSrvData.keys():
            httpSrv = self.ThreadingHTTPServer((hostIp, self.srvPort), self.httpHandler)
            self.httpSrvs.append(httpSrv)
            httpSrvThread=Thread(target=httpSrv.serve_forever)

            try:
                httpSrvThread.start()
            except:
                self.shutDownHttpSrvs()
                raise

            print("HTTPSrv Start >>>>>>>>>>>>>>>>>>>>>>>>>", httpSrv, hostIp)

        try:
            self.sendCnt=self.sendCnt+1
            #Customize test messages by overriding
            self.testCbFunc()

        except:
            self.shutDownHttpSrvs()
            raise

        self.shutDownHttpSrvs()
        time.sleep(.1)
        return

    def runTest(self):
        return

    class TestShoeHttpHandler(BaseHTTPRequestHandler):
        #The Python HTTP Server wants to send a 48byte server string
        # maybe can figure out how to solve this?

        srvData=None
        quiet=False

        def _dbugPrt(self, *args):
            if self.quiet is False:
                print(*args)

        def do_GET(self):
            host,port=self.server.server_address
            self._dbugPrt("@@@@@@@@@@@@@@@@@@@@@@@GET %s@@@@@@@@@@@@@@@@@@@@@@" % host)
            params=self.srvData[host]

            if params.noReply:
                return

            reqPath = self.path

            testActSvc=TestShoeHttp.testActSvc
            testGroupCtrlSvc=TestShoeHttp.testGroupCtrlSvc
            testZoneCtrlSvc=TestShoeHttp.testZoneCtrlSvc
            testRootDev=TestShoeHttp.testRootDev

            self.send_response(200)
            self.end_headers()

            if params.getRtn:
                rtnMsg=params.getRtn

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
            host,port=self.server.server_address
            self._dbugPrt("@@@@@@@@@@@@@@@@@@@POST %s@@@@@@@@@@@@@@@@@@@@@@@" % host)
            params=self.srvData[host]

            if params.noReply:
                return

            headersIn=dict(self.headers)
            lengthIn=int(headersIn['CONTENT-LENGTH'])

            srvRxMsg = self.rfile.read(lengthIn).decode()
            srvRxHdr = headersIn

            params.srvRx = (srvRxHdr, srvRxMsg)

            params.srvRxUrn=None
            params.srvRxCmnd=None

            try:
                soapAct=headersIn['SOAPACTION'].split('#')
                params.srvRxUrn=soapAct[0]
                params.srvRxCmnd=soapAct[1][:-1]

            except (KeyError, IndexError):
                pass

            self._dbugPrt ("POST Req Msg", srvRxMsg)
            self._dbugPrt ("POST Req Hdr", srvRxHdr)

            self.postRtn(params, host)

            return

        def postRtn(self, params, host):
            if params.rtnCode != 200:
                self.send_error(params.rtnCode)
            else:
                msg=params.postRtn
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
