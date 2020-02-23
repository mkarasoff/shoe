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
from .shoeMsgXml import *
import re
from lxml import etree
from console_log import *

class ShoeMsg():
    PORT            = 60006

    ACCEPT_RANGES_VAL   = 'bytes'
    CONTENT_TYPE_VAL    = 'text/xml; charset="utf-8"'
    USER_AGENT_VAL      = 'LINUX UPnP/1.0 Denon-Heos/149200'

    def __init__(self,
                    host,
                    path,
                    cmnd,
                    urn,
                    args=OrderedDict(),
                    loglvl=ConsoleLog.WARNING):

        self.log=ConsoleLog(self.__class__.__name__, loglvl)

        self.host=host
        self.path=path
        self.cmnd=cmnd
        self.urn=urn
        self.args=args
        self.reply=None

        self.loglvl=loglvl

        self._msgLen=0
        self._txHttpPayload=None
        self._soapaction=None
        self._httpReply=None

        return

    def send(self):
        self.log.debug("Cmnd %s, urn %s, args %s",
                        self.cmnd, self.urn, self.args)
        shoexml = ShoeMsgXml(cmnd=self.cmnd,
                            urn=self.urn,
                            args=self.args,
                            loglvl=self.loglvl)

        self._txHttpPayload = shoexml.genTree()
        self._soapaction='"%s#%s"' % (self.urn, self.cmnd)
        self._msgLen=str(len(self._txHttpPayload))

        self._post_cmd()

        return

    def parse(self):
        self.reply=''

        self.log.debug("status %s" % self._httpReply.status)
        self.log.debug("httpHeader %s" % str(self._httpReply.getheaders()))

        try:
            status = int(self._httpReply.status)
        except:
            raise ShoeMsgHttpRtnErr("Unknown")

        if(int(status) == 200):
            try:
                self.log.debug("payload %s" % str(self._rxHttpPayload))
                shoeMsgXml = ShoeMsgXml(msgXml=self._rxHttpPayload, loglvl=self.loglvl)
                self.reply=shoeMsgXml.parseTree()
            except:
                raise
        else:
            raise ShoeMsgHttpRtnStatusErr(str(status))

        if(self.urn != self.reply.urn):
            errMsg = "HTTP Rtn URN Mismatch %s %s" % (self.urn, self.reply.urn)
            raise ShoeMsgHttpRtnErr(errMsg)

        cmndReply = self.cmnd + "Response"
        if(cmndReply != self.reply.cmnd):
            errMsg = "HTTP Rtn Method Mismatch %s %s" % (cmndReply, self.reply.cmnd)
            raise ShoeMsgHttpRtnErr(errMsg)

        return self.reply

    def _post_cmd(self):

        conn = http.client.HTTPConnection(self.host, ShoeMsg.PORT)

        if self.loglvl <= self.log.DEBUG:
            conn.set_debuglevel(1)
        else:
            conn.set_debuglevel(0)

        conn.putrequest('POST', self.path, skip_host=True, skip_accept_encoding=True)

        host="%s:%s" % (self.host, ShoeMsg.PORT)

        self.log.debug("Sending Cmnd: Host %s, Path %s" % (host, self.path))

        conn.putheader('HOST', host)
        conn.putheader('CONTENT-LENGTH', self._msgLen)
        conn.putheader('Accept-Ranges', ShoeMsg.ACCEPT_RANGES_VAL)
        conn.putheader('CONTENT-TYPE' , ShoeMsg.CONTENT_TYPE_VAL)
        conn.putheader('SOAPACTION' , self._soapaction)
        conn.putheader('USER-AGENT' , ShoeMsg.USER_AGENT_VAL)

        try:
            conn.endheaders(self._txHttpPayload)
        except Exception as e:
            raise ShoeMsgHttpSendErr("%s %s" % (str(e), host))

        try:
            self._httpReply = conn.getresponse()
        except Exception as e:
            raise ShoeMsgHttpSendErr("%s %s" % (str(e), host))

        self._rxHttpPayload=self._httpReply.read()

        conn.close()

        return

#############################EXCEPTIONS#########################################
class ShoeMsgHttpSendErr(Exception):
    pass
class ShoeMsgHttpRtnErr(Exception):
    pass
class ShoeMsgHttpRtnStatusErr(Exception):
    pass
