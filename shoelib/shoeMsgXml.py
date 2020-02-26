##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeMsgXml.py
#Class impliments and parses xml messages for HEOS.  These
#messages are XML and "soapy"
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
from io import BytesIO
from collections import OrderedDict
from collections import namedtuple
import re
from lxml import etree
from console_log import *

class ShoeMsgXml():
    ENVELOPE_NS_URL=b'http://schemas.xmlsoap.org/soap/envelope/'
    ENVELOPE_STYLE_URL=b'http://schemas.xmlsoap.org/soap/encoding/'
    ENVELOPE= (b'<s:Envelope xmlns:s="%s" s:encodingStyle="%s">'
                b'<s:Body></s:Body>'
                b'</s:Envelope>')

    MSG_INDEX = 0
    BODY_INDEX = 0
    BODY_NS_TAG = 'u'

    ShoeMsgParse = namedtuple('ShoeMsgParse', 'cmnd urn args')

    def __init__(self, cmnd='', urn='', args={}, msgXml=None, loglvl=ConsoleLog.WARNING):
        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        self.cmnd = cmnd
        self.urn = urn
        self.args = args
        self.msgXml=msgXml

        if(msgXml is not None):
            self.setTree(msgXml)
        else:
            self.xmlTree = None

        self._argsXML = None
        return

    #Note that this returns a utf-8 representation of the XML
    def genTree(self):
        self.xmlTree=self._genEnvelope()
        treeRoot=self.xmlTree.getroot()

        msgNsArg="{%s}" % self.urn
        msgNsmap= {ShoeMsgXml.BODY_NS_TAG : self.urn}

        self._genBody(treeRoot, self.cmnd, self.urn, self.args)

        self.msgXml=etree.tostring(treeRoot)

        return self.msgXml

    def parseTree(self):
        self.args = OrderedDict()

        try:
            treeRoot=self.xmlTree.getroot()
        except (AttributeError):
            if self.xmlTree == None:
                raise XMLSyntaxError
            else:
                raise
        except:
            raise

        try:
            msgRoot=treeRoot[ShoeMsgXml.BODY_INDEX][ShoeMsgXml.MSG_INDEX]
        except:
            raise

        self.cmnd = re.sub('{[^}]+}', '', msgRoot.tag)
        self.urn = msgRoot.nsmap[ShoeMsgXml.BODY_NS_TAG]

        for element in msgRoot.iter():
            #lxml
            if element.text is not None:
                self.args[element.tag] = element.text
            else:
                self.args[element.tag] = ''

        #Delete first item in list, it is the body header.
        del self.args[list(self.args.items())[0][0]]

        return ShoeMsgXml.ShoeMsgParse(self.cmnd, self.urn, self.args)

    def setTree(self, xmlTxt=0):
        try:
            self.xmlTree=etree.parse(BytesIO(xmlTxt))
        except:
            raise

        return

    def _genEnvelope(self,
                    ns_url = None,
                    style_url = None):

        if(ns_url is None):
            ns_url=ShoeMsgXml.ENVELOPE_NS_URL
        if(style_url is None):
            style_url=ShoeMsgXml.ENVELOPE_STYLE_URL

        envelopeTxt = ShoeMsgXml.ENVELOPE % (ns_url, style_url)
        envelope=etree.parse(BytesIO(envelopeTxt))

        return envelope

    def _genBody(self, treeRoot, cmnd, urn, args={}):

        self.log.debug("cmnd: %s urn: %s args: %s", cmnd, urn, args)
        msgNsArg="{%s}" % urn
        msgNsmap= {ShoeMsgXml.BODY_NS_TAG : urn}

        bodyRoot=treeRoot[0]

        bodyTree=etree.SubElement(
                bodyRoot,
                msgNsArg + cmnd,
                nsmap=msgNsmap)
        bodyTree.text=''

        for tag, tagText in list(args.items()):
            msgElement=etree.SubElement(
                    bodyTree,
                    str(tag))
            if(tagText is not None):
                msgElement.text=str(tagText)

        return bodyTree
