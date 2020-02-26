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
from .shoeCfgXml import *
from collections import OrderedDict

class ShoeEventParser(ShoeCfgXml):

    def __init__(self, xmlText='', loglvl=ConsoleLog.WARNING):
        super().__init__(loglvl=loglvl)

        self.xmlText=xmlText
        self.loglvl=loglvl
        return

    def parse(self):
        self.log.debug("XmlText %s" % self.xmlText)
        try:
            self.xmlText=self.xmlText.encode()
        except AttributeError:
            if self.xmlText is None:
                return ''
            else:
                raise
        except:
            raise

        self.xmlDict = self._getXmlDict(self.xmlText)

        return self.xmlDict

    def _getXmlDict(self, xmlText):
        self.log.debug("XmlText %s" % xmlText)

        xmlDict=OrderedDict()
        try:
            xmlTreeRoot = self._parseXml(xmlText)
        except etree.XMLSyntaxError:
            return {}
        except:
            raise

        currStDict=self._etreeToDict(xmlTreeRoot)

        self.log.debug("Current State Dict %s" % currStDict)

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

        self.log.debug("Event Val %s" % eventText)

        try:
            tree=etree.parse(BytesIO(eventText))
        except etree.XMLSyntaxError:
            self.log.debug("Syntax Error %s" % eventText)
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

        self.log.debug("Return Val %s" % rtnVal)

        return rtnVal

    def _getHttp(self, path, host, port):
        return None

    def _unEscape(self, xmlStr):
        xmlStr=xmlStr.replace(b'&lt;', b'<')
        xmlStr=xmlStr.replace(b'&gt;', b'>')
        xmlStr=xmlStr.replace(b'&quot;', b'"')
        xmlStr=xmlStr.replace(b'&amp;', b'&')
        return xmlStr
