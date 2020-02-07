##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeEvent.py
#Class that parses HEOS event data from "GetCurrentState" command.
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
from shoeSys import *
from collections import OrderedDict

class ShoeEventParser(ShoeCfgXml):

    def __init__(self, xmlText='', loglvl=ConsoleLog.WARNING):
        super().__init__(loglvl=loglvl)

        self.xmlText=xmlText
        self.loglvl=loglvl
        return

    def parse(self):
        try:
            self.xmlText=self.xmlText.encode('utf-8')
        except AttributeError:
            if self.xmlText is None:
                return {}
            else:
                raise
        except:
            raise

        self.xmlDict = self._getXmlDict(self.xmlText)

        return self.xmlDict

    def _getXmlDict(self, xmlText):

        xmlDict=OrderedDict()
        try:
            xmlTreeRoot = self._parseXml(xmlText)
        except etree.XMLSyntaxError:
            return {}
        except:
            raise

        currStDict=self._etreeToDict(xmlTreeRoot)

        for event, eventVal in currStDict['Event'].items():
            xmlDict[event]=self._format(eventVal)

        return xmlDict

    def _format(self, eventVal):
        try:
            eventText=eventVal['@val'].encode('utf-8')
        except AttributeError:
            if eventVal is None:
                return ''
            else:
                raise
        except:
            raise

        try:
            tree=etree.parse(BytesIO(eventText))
        except etree.XMLSyntaxError:
            try:
                return eventText.decode()
            except AttributeError:
                return str(eventText)
            except:
                raise
        except:
            raise

        treeRoot=tree.getroot()
        rtnVal=self._etreeToDict(treeRoot)

        return rtnVal

    def _getHttp(self, path, host, port):
        return None

    def _unEscape(self, xmlStr):
        xmlStr=xmlStr.replace(b'&lt;', b'<')
        xmlStr=xmlStr.replace(b'&gt;', b'>')
        xmlStr=xmlStr.replace(b'&quot;', b'"')
        xmlStr=xmlStr.replace(b'&amp;', b'&')
        return xmlStr

from test_shoe import *
class TestShoeEvent(unittest.TestCase):
    def setUp(self):
        self.testSvcs=[ TestActSvc(), TestGroupCtrlSvc(), TestZoneCtrlSvc()]
        return

    def runTest(self):
        shoeCfg=ShoeCfgXml()

        for svc in self.testSvcs:
            cmnd = svc.cmnds['GetCurrentState']
            rtnMsgBody = cmnd.rtnMsgBody
            xmlTextRoot = shoeCfg._parseXml(rtnMsgBody.encode('utf-8'))
            currStRtn=shoeCfg._etreeToDict(xmlTextRoot)

            shoeSt=ShoeEventParser(
                xmlText=currStRtn['CurrentState'],
                loglvl=logging.DEBUG)

            currSt=shoeSt.parse()

            print(svc.name)
            print("curr st returned", currSt)
            print("curr st expected", cmnd.rtn['CurrentState'])

            self.assertCountEqual(cmnd.rtn['CurrentState'], currSt)
        return
