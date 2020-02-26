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
from console_log import *

class ShoeCfgXml():
    def __init__(self,
                    host=None,
                    path=None,
                    loglvl=ConsoleLog.WARNING,
                    port=60006,
                    fileName=None):

        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        self.loglvl = loglvl
        self.host = host
        self.port = port
        self.path = path
        self.fileName = fileName
        self.xmlDict={}
        return

    def getCfg(self, path=None, fileName=None):
        self.log.debug("Path %s FileName %s" % (path, fileName))
        if path is None:
            path=self.path
        else:
            self.path=path

        if fileName is None:
            fileName=self.fileName
        else:
            self.fileName=fileName

        self.log.debug("Host %s:%s, Path %s, Filename %s" %
                        (self.host, self.port, self.path, self.fileName))

        if path is None and fileName is None:
            raise ShoeCfgXmlErr("No file or url specified")

        if fileName is None:
            self.xmlText = self._getHttpXmlText(path,
                self.host,
                self.port)
        else:
            self.xmlText = self._getFileXmlText(self.fileName)

        self.log.debug2("XML Test %s" % str(self.xmlText))

        self.xmlDict = self._getXmlDict(self.xmlText)

        self.log.debug("XML Dict %s" % str(self.xmlDict))

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

    def _getFileXmlText(self, fileName):
        f=open(fileName, 'r')
        xmlText=f.read()
        return xmlText.encode()

    def _getHttpXmlText(self, path, host, port):
        httpRes = self._getHttp(path, host, port)
        self.log.debug("status %s", httpRes.status)
        self.log.debug("headers %s", httpRes.headers)
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

        self.log.debug2("HTTP Text %s", xmlText)

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

    def _getHttp(self, path, host, port):
        conn = http.client.HTTPConnection(host, port)

        if self.loglvl <= self.log.DEBUG:
            conn.set_debuglevel(1)
        else:
            conn.set_debuglevel(0)

        self.log.debug("path %s" % path)
        conn.putrequest('GET', path, skip_host=True, skip_accept_encoding=True)

        host="%s:%s" % (host, port)

        conn.putheader('HOST', host)

        try:
            conn.endheaders()
        except Exception as e:
            raise ShoeCfgXmlHttpSendErr(str(e))

        try:
            httpRes = conn.getresponse()
        except Exception as e:
            conn.close()
            raise ShoeCfgXmlHttpRtnErr(str(e))

        conn.close()

        self.log.debug("Host %s" % host)

        return httpRes

###############################Exceptions#################################
class ShoeCfgXmlHttpSendErr(Exception):
    pass
class ShoeCfgXmlHttpRtnErr(Exception):
    pass
class ShoeCfgXmlErr(Exception):
    pass
