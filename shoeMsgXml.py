##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeGroup.py
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
############################################################################from lxml import etree
from io import BytesIO
from collections import OrderedDict
from collections import namedtuple
import re

class ShoeMsgXml():
    ENVELOPE_NS_URL=b'http://schemas.xmlsoap.org/soap/envelope/'
    ENVELOPE_STYLE_URL=b'http://schemas.xmlsoap.org/soap/encoding/'
    ENVELOPE= (b'<s:Envelope xmlns:s="%s" s:encodingStyle="%s">'
                b'<s:Body></s:Body>'
                b'</s:Envelope>')

    MSG_INDEX = 0
    BODY_INDEX = 0
    BODY_NS_TAG = 'u'

    ShoeMsgParse = namedtuple('ShoeMsgParse', 'method urn msgArgs')

    def __init__(self, method='', urn='', msgArgs={}, xmlText=None, dbug=0):
        self.method = method
        self.urn = urn
        self.msgArgs = msgArgs
        self.xmlTxt=xmlText

        if(xmlText is not None):
            self.setTree(xmlText)
        else:
            self.xmlTree = None

        self._msgArgsXML = None
        return

    def genTree(self):
        self.xmlTree=self._genEnvelope()
        treeRoot=self.xmlTree.getroot()

        msgNsArg="{%s}" % self.urn
        msgNsmap= {ShoeMsgXml.BODY_NS_TAG : self.urn}

        self._genBody(treeRoot, self.method, self.urn, self.msgArgs)

        self.xmlText=etree.tostring(treeRoot)

        return self.xmlText

    def parseTree(self):
        self.msgArgs = OrderedDict()

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

        self.method = re.sub('{[^}]+}', '', msgRoot.tag)
        self.urn = msgRoot.nsmap[ShoeMsgXml.BODY_NS_TAG]

        for element in msgRoot.iter():
            self.msgArgs[element.tag] = element.text

        #Delete first item in list, it is the body header.
        del self.msgArgs[list(self.msgArgs.items())[0][0]]

        return ShoeMsgXml.ShoeMsgParse(self.method, self.urn, self.msgArgs)

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

    def _genBody(self, treeRoot, method, urn, msgArgs={}):

        msgNsArg="{%s}" % urn
        msgNsmap= {ShoeMsgXml.BODY_NS_TAG : urn}

        bodyRoot=treeRoot[0]

        bodyTree=etree.SubElement(
                bodyRoot,
                msgNsArg + method,
                nsmap=msgNsmap)
        bodyTree.text=''

        for tag, tagText in list(msgArgs.items()):
            msgElement=etree.SubElement(
                    bodyTree,
                    str(tag))
            if(tagText is not None):
                msgElement.text=str(tagText)

        return bodyTree

###############################Unittests#################################
import unittest
from test_shoe import *

class TestShoeMsgXml(unittest.TestCase):
    def setUp(self):

        self.method='SetGroupMemberChannel'
        self.urn='urn:schemas-denon-com:service:GroupControl:1'

        self.msgArgs=OrderedDict()
        self.msgArgs['GroupUUID']='17083c46d003001000800005cdfbb9c6'
        self.msgArgs['AudioChannel']='LEFT'

        xmlText=('<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
                   's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
                 '<s:Body>'
                 '<u:%s xmlns:u="%s">'
                 '<%s>%s</%s>'
                 '<%s>%s</%s>'
                 '</u:%s>'
                 '</s:Body>'
                 '</s:Envelope>')

        self.xmlText=xmlText % (self.method, self.urn,
                   list(self.msgArgs.items())[0][0],
                   list(self.msgArgs.items())[0][1],
                   list(self.msgArgs.items())[0][0],
                   list(self.msgArgs.items())[1][0],
                   list(self.msgArgs.items())[1][1],
                   list(self.msgArgs.items())[1][0],
                   self.method)

        self.xmlText=self.xmlText.encode('utf-8')

    def genXml(self):

        shoeXml = ShoeMsgXml(method=self.method, urn=self.urn, msgArgs=self.msgArgs)
        textRtn = shoeXml.genTree()

        print(' ')
        print('Gen: ')
        print('Gen Text:', shoeXml.xmlText)
        print('Cmp Text:', self.xmlText)

        self.assertEqual(shoeXml.xmlText, self.xmlText, 'GenError: xmlTree')
        self.assertEqual(textRtn, self.xmlText, 'GenErrorRtn: xmlTree')
        return

class TestShoeMsgParse(TestShoeMsgXml):
    def runTest(self):
        shoeXml  = ShoeMsgXml(xmlText=self.xmlText)
        parseRtn = shoeXml.parseTree()

        print(' ')
        print('Parse: ')
        print('Method: ', shoeXml.method, 'Method Expected: ', self.method)
        print('URN: ', shoeXml.urn, 'URN Expected: ', self.urn)
        print('ARGs: ', shoeXml.msgArgs, 'ARGs Expected: ', self.msgArgs)

        self.assertEqual(shoeXml.method, self.method, 'Parse error: method')
        self.assertEqual(shoeXml.urn, self.urn, 'Parse error: urn')
        self.assertEqual(shoeXml.msgArgs, self.msgArgs, 'Parse error: mesgDataArgs')

        self.assertEqual(parseRtn.method, self.method, 'Parse error rtn: method')
        self.assertEqual(parseRtn.urn, self.urn, 'Parse error rtn: urn')
        self.assertEqual(parseRtn.msgArgs, self.msgArgs, 'Parse error rtn: mesgDataArgs')

        return

class TestShoeMsgXmlGen(TestShoeMsgXml):
    def runTest(self):
        self.genXml()
        return

class TestShoeMsgXmlGenMt(TestShoeMsgXml):
    def runTest(self):
        self.testObj=TestZoneCtrlSvc()

        self.method=self.testObj.getCurrStCmnd
        self.msgArgs=OrderedDict()
        self.path=self.testObj.urlPath
        self.urn=self.testObj.urn

        self.xmlText=self.testObj.getCurrStCmndXml.encode('utf-8')

        self.genXml()

        return
