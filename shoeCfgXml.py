##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeCfgXml.py
#Class that grabs remote XML via HTTP and generates a configuration
#dictionary from it.
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
from lxml import etree
from collections import defaultdict
from io import BytesIO
from consoleLog import *

class ShoeCfgXml():
    def __init__(self, host=None, path='', loglvl=0, port=60006):
        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        self.host = host
        self.port = port
        self.path = path
        self.loglvl=loglvl
        self.xmlDict={}
        return

    def getCfg(self, path=None):
        if path is None:
            path=self.path

        self.xmlText = self._getXmlText(path,
                self.host,
                self.port,
                self.loglvl)

        self.xmlDict = self._getXmlDict(self.xmlText)

        return self.xmlDict

    def _getXmlDict(self, xmlText):
        xmlTreeRoot = self._parseXml(xmlText)
        try:
            xmlDict=self._etreeToDict(xmlTreeRoot)
        except etree.XMLSyntaxError:
            if self.xmlText=='':
                self.xmlDict={}
            else:
                raise
        except:
            raise

        return xmlDict

    def _getXmlText(self, path, host, port, loglvl=None):
        httpRes = self._getHttp(path, host, port, loglvl)
        self.log.debug("status %s", httpRes.status)
        try:
            status = int(httpRes.status)
        except:
            raise ShoeCfgXmlHttpRtnErr("Unknown")

        if(int(status) == 200):
            try:
                xmlText=httpRes.read()
            except:
                raise
        else:
            raise ShoeCfgXmlHttpRtnErr(str(status))

        return xmlText

    def _parseXml(self, xmlText):
        #First pass read to strip default namespace
        try:
            tree=etree.parse(BytesIO(xmlText))
        except:
            raise

        treeRoot=tree.getroot()

        try:
            #This is the default namespace
            dfltNs=treeRoot.nsmap[None]
            #Strip namespace from the text.
            xmlText = xmlText.replace(dfltNs.encode('utf-8'), b'')

        except KeyError:
            pass
        except:
            raise

        #Get tree & root without namespace
        tree=etree.parse(BytesIO(xmlText))
        treeRoot=tree.getroot()

        return treeRoot

    #Converts the a etree root to dictionary
    #Impatiently ripped from stack overflow without shame
    # https://stackoverflow.com/questions/7684333
    def _etreeToDict(self, t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self._etreeToDict, children):
                for k, v in list(dc.items()):
                    dd[k].append(v)
            d = {t.tag: {k: v[0] if len(v) == 1 else v
                         for k, v in list(dd.items())}}
        if t.attrib:
            d[t.tag].update(('@' + k, v)
                            for k, v in list(t.attrib.items()))
        if t.text:
            text = t.text.strip()
            if text is None:
                text=''
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d

    def _getHttp(self, path, host, port, loglvl):
        conn = http.client.HTTPConnection(host, port)

        if loglvl <= self.log.DEBUG:
            conn.set_debuglevel(1)
        else:
            conn.set_debuglevel(0)

        conn.putrequest('GET', path, skip_host=True, skip_accept_encoding=True)

        host="%s:%s" % (host, port)

        conn.putheader('HOST', host)

        try:
            conn.endheaders()
        except Exception as e:
            raise ShoeCfgXmlHttpSendErr(str(e))

        try:
            self.log.debug("Host", host)
            httpRes = conn.getresponse()
        except Exception as e:
            conn.close()
            raise ShoeCfgXmlHttpRtnErr(str(e))

        conn.close()

        return httpRes

###############################Exceptions#################################
class ShoeCfgXmlHttpSendErr(Exception):
    pass
class ShoeCfgXmlHttpRtnErr(Exception):
    pass

###############################Unittests#################################
from test_shoe import *

class TestShoeCfgXml(TestShoeHttp):
    def setUp(self):
        super().setUp()
        self.cmndList=None
        self.cmndArgCfg=None
        self.reply=None
        self.host='127.0.0.1'

        self.testObjs=[
                self.testRootDev,
                self.testActSvc,
                self.testGroupCtrlSvc,
                self.testZoneCtrlSvc]
        return

    def _sendTestMsgs(self):
        shoeCfg=ShoeCfgXml(self.host, self.testFile, loglvl=10)
        self.xmlDict=shoeCfg.getCfg()
        return

class TestShoeCfgXmlDict(TestShoeCfgXml):
    def runTest(self):
        for testObj in self.testObjs:
            self._testXml(testObj)
        return

    def _testXml(self, testObj):
        self.testFile=testObj.fileName
        self.getRtn=testObj.xmlStr

        self.httpTest()

        errMsg = "Shoe cfg: dict not correct: %s." % \
                    testObj.fileName

        self.assertDictEqual(self.xmlDict,
                        testObj.xmlDict,
                        errMsg)

        return
