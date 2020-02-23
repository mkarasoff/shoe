##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testShoeEvent.py
#Class for unittest of event message parsing commands.  Shoe currently
# does not handle asynchronous events, rather the respose from "GetCurrentState"
# command.  So this is really a command with an "Event" return type.  This
# return type seems to be escaped XML.
#
#This is special because the return message body cannot be derrived simply enough
# from the command return to be suitable for unittesting.  So for this command
# we need to explicity set the return body.
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
from .testShoeCmnd import *
from collections import OrderedDict
import unittest
import re

class TestShoeEvent(TestShoeCmnd):
    def __init__(self, cmndName, urn, path, svcInst):
        super().__init__(cmndName, urn, path, svcInst)
        self.fmtOutput=''
        self.eventRtnMsgBody='<CurrentState></CurrentState>'
        self.rtn=OrderedDict([('CurrentState', None),])

        return

    #This is an intermediate value that is easy to generate from the body
    # useful in only limited cases (maybe only testing ShoeEvent)
    @property
    def msgReplyArgs(self):
        rtnLbl=list(self.rtn.keys())[0]
        msgReplyArgs=OrderedDict()

        msgReplyArgsVal=re.sub('<.+?>', '', self.rtnMsgBody)
        msgReplyArgsVal=msgReplyArgsVal.replace('&quot;', '"')
        msgReplyArgsVal=msgReplyArgsVal.replace('&gt;', '>')
        msgReplyArgsVal=msgReplyArgsVal.replace('&lt;', '<')
        msgReplyArgsVal=msgReplyArgsVal.replace('&amp;', '&')

        msgReplyArgs[rtnLbl]=msgReplyArgsVal

        return msgReplyArgs

    @property
    def rtnMsgBody(self):
        return self.eventRtnMsgBody

    @rtnMsgBody.setter
    def rtnMsgBody(self, msgBody):
        self.eventRtnMsgBody=msgBody

class TestEvent(unittest.TestCase):
    class CmndTestSvc():
        def __init__(self):
            self.name="testCmnd"
            self.devName="testDevName"

    def setUp(self):
        self.urn='urn:schemas-denon-com:service:ZoneControl:2'
        self.path='/upnp/control/AiosServicesDvc/ZoneControl'
        self.maxDiff=None

        svcInst=self.CmndTestSvc()

        self.cmnd='GetCurrentState'
        self.tEvent=TestShoeEvent(self.cmnd, self.urn, self.path, svcInst)

        self.rtnMsgBody='<CurrentState>&lt;Event xmlns=&quot;urn:schemas-upnp-org:metadata-1-0/ZCS/&quot;&gt;&lt;'\
                'ZoneConnectedList val=&quot;caf7916a94db1a1300800005cdfbb9c6,'\
                'f3ddb59f3e691f1e00800005cdff1706&quot;/&gt;&lt;ZoneFriendlyName val=&quot;Family Room&quot;'\
                '/&gt;&lt;ZoneMemberList val=&quot;caf7916a94db1a1300800005cdfbb9c6,'\
                'f3ddb59f3e691f1e00800005cdff1706&quot;/&gt;&lt;ZoneMemberStatusList val=&quot;'\
                'caf7916a94db1a1300800005cdfbb9c6,ZONE_LEAD,f3ddb59f3e691f1e00800005cdff1706,ZONE_SLAVE&quot;'\
                '/&gt;&lt;ZoneMute val=&quot;0&quot;/&gt;&lt;ZoneStatus val=&quot;ZONE_LEAD&quot;/&gt;&lt;'\
                'ZoneVolume val=&quot;31&quot;/&gt;&lt;ZoneMinimise val=&quot;0&quot;/&gt;&lt;ZoneUUID val=&quot;'\
                '17083c46d003001000800005cdfbb9c6&quot;/&gt;&lt;/Event&gt;</CurrentState>'

        self.tEvent.rtnMsgBody=self.rtnMsgBody

        self.rtn=OrderedDict([('CurrentState',
            OrderedDict([\
                ('ZoneConnectedList',\
                    b'caf7916a94db1a1300800005cdfbb9c6,f3ddb59f3e691f1e00800005cdff1706'),\
                ('ZoneFriendlyName', b'Family Room'), \
                ('ZoneMemberList', \
                    b'caf7916a94db1a1300800005cdfbb9c6,f3ddb59f3e691f1e00800005cdff1706'), \
                ('ZoneMemberStatusList', \
                    b'caf7916a94db1a1300800005cdfbb9c6,ZONE_LEAD,f3ddb59f3e691f1e00800005cdff1706,ZONE_SLAVE'), \
                ('ZoneMute', b'0'), \
                ('ZoneStatus', b'ZONE_LEAD'), \
                ('ZoneVolume', b'31'), \
                ('ZoneMinimise', b'0'), \
                ('ZoneUUID', b'17083c46d003001000800005cdfbb9c6')]))])

        self.tEvent.rtn=self.rtn

        self.fmtOutput=\
            "ZoneConnectedList : b'caf7916a94db1a1300800005cdfbb9c6,f3ddb59f3e691f1e00800005cdff1706'\n"\
            "ZoneFriendlyName : b'Family Room'\n"\
            "ZoneMemberList   : b'caf7916a94db1a1300800005cdfbb9c6,f3ddb59f3e691f1e00800005cdff1706'\n"\
            "ZoneMemberStatusList : "\
            "b'caf7916a94db1a1300800005cdfbb9c6,ZONE_LEAD,f3ddb59f3e691f1e00800005cdff1706,ZONE_SLAVE'\n"\
            "ZoneMute         : b'0'\n"\
            "ZoneStatus       : b'ZONE_LEAD'\n"\
            "ZoneVolume       : b'31'\n"\
            "ZoneMinimise     : b'0'\n"\
            "ZoneUUID         : b'17083c46d003001000800005cdfbb9c6'\n"\

        self.tEvent.fmtOutput=self.fmtOutput

        ##################Done setting up UUT#########################################################
        self.msgReplyArgs=OrderedDict([('CurrentState', \
                '<Event xmlns="urn:schemas-upnp-org:metadata-1-0/ZCS/">'\
                '<ZoneConnectedList val="caf7916a94db1a1300800005cdfbb9c6,'\
                    'f3ddb59f3e691f1e00800005cdff1706"/>'\
                '<ZoneFriendlyName val="Family Room"/>'\
                '<ZoneMemberList val="caf7916a94db1a1300800005cdfbb9c6,'\
                    'f3ddb59f3e691f1e00800005cdff1706"/>'\
                '<ZoneMemberStatusList val="caf7916a94db1a1300800005cdfbb9c6,ZONE_LEAD,'\
                                        'f3ddb59f3e691f1e00800005cdff1706,ZONE_SLAVE"/>'\
                '<ZoneMute val="0"/><ZoneStatus val="ZONE_LEAD"/>'\
                '<ZoneVolume val="31"/><ZoneMinimise val="0"/>'\
                '<ZoneUUID val="17083c46d003001000800005cdfbb9c6"/>'\
                '</Event>')])

        self.hdr={'HOST': '127.0.0.1:60006', \
                            'CONTENT-LENGTH': '247', \
                            'Accept-Ranges': 'bytes', \
                            'CONTENT-TYPE': 'text/xml; charset="utf-8"', \
                            'SOAPACTION': '"urn:schemas-denon-com:service:ZoneControl:2#GetCurrentState"', \
                            'USER-AGENT': 'LINUX UPnP/1.0 Denon-Heos/149200'}

        self.msg= '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                                    's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
                                    '<s:Body>'\
                                    '<u:GetCurrentState xmlns:u="urn:schemas-denon-com:service:ZoneControl:2">'\
                                    '</u:GetCurrentState>'\
                                    '</s:Body>'\
                                    '</s:Envelope>'

        self.rtnMsg='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
                '<s:Body>'\
                    '<u:GetCurrentStateResponse '\
                        'xmlns:u="urn:schemas-denon-com:service:ZoneControl:2">'\
                       '<CurrentState>&lt;Event xmlns=&quot;urn:schemas-upnp-org:metadata-1-0/ZCS/&quot;&gt;&lt;'\
                'ZoneConnectedList val=&quot;caf7916a94db1a1300800005cdfbb9c6,'\
                'f3ddb59f3e691f1e00800005cdff1706&quot;/&gt;&lt;ZoneFriendlyName val=&quot;Family Room&quot;'\
                '/&gt;&lt;ZoneMemberList val=&quot;caf7916a94db1a1300800005cdfbb9c6,'\
                'f3ddb59f3e691f1e00800005cdff1706&quot;/&gt;&lt;ZoneMemberStatusList val=&quot;'\
                'caf7916a94db1a1300800005cdfbb9c6,ZONE_LEAD,f3ddb59f3e691f1e00800005cdff1706,ZONE_SLAVE&quot;'\
                '/&gt;&lt;ZoneMute val=&quot;0&quot;/&gt;&lt;ZoneStatus val=&quot;ZONE_LEAD&quot;/&gt;&lt;'\
                'ZoneVolume val=&quot;31&quot;/&gt;&lt;ZoneMinimise val=&quot;0&quot;/&gt;&lt;ZoneUUID val=&quot;'\
                '17083c46d003001000800005cdfbb9c6&quot;/&gt;&lt;/Event&gt;</CurrentState>'\
                        '</u:GetCurrentStateResponse>'\
                    '</s:Body>'\
                '</s:Envelope>'

    def runTest(self):
        self.assertEqual(self.tEvent.msgReplyArgs, self.msgReplyArgs)
        self.assertEqual(self.tEvent.rtnMsgBody, self.rtnMsgBody)
        self.assertEqual(self.tEvent.rtn, self.rtn)
        self.assertEqual(self.tEvent.fmtOutput, self.fmtOutput)

        self.assertEqual(self.tEvent.hdr, self.hdr)
        self.assertEqual(self.tEvent.msg, self.msg)
        self.assertEqual(self.tEvent.rtnMsg, self.rtnMsg)
