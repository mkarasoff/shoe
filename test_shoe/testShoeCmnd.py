##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testShoeCmnd.py
#Class for unittest of messages.
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
from collections import OrderedDict
import unittest

class TestShoeCmnd():
    def __init__(self, cmndName, urn, path, svcInst):
        self.name=cmndName
        self.urn=urn
        self.path=path
        self.svc=svcInst
        self.svcName=svcInst.name
        self.devName=svcInst.devName

        self.args=OrderedDict()

        self.rtn=OrderedDict()

        self.argsCfg=[]

        self._msgEnvHead='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                            's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'

        self._msgEnvTail='</s:Envelope>'

        self.noReply=False
        self.rtnCode=200

        self.rtnMsgOvr=None
        self.msgOvr=None
        self.hdrOvr=None
        self.fmtParams=''
        self.fmtRtn=None
        return

    @property
    def fmtCmndRtn(self):
        if self.fmtRtn is None:
            rtn=\
                '\nCmnd: %sResponse   Service: %s   Device: %s\n' %\
                (self.name, self.svcName, self.devName)

        else:
            rtn=\
                '\nCmnd: %sResponse   Service: %s   Device: %s\n' \
                '%s\n' %\
                (self.name, self.svcName, self.devName, self.fmtRtn)
        return rtn

    @property
    def fmtCmndInfo(self):
        rtn=\
            'Cmnd:    %s \n'\
            'Device:  %s \n'\
            'Service: %s\n'\
            'Parameters       : \n'\
            '%s\n' % \
            (self.name, self.devName, self.svcName, self.fmtParams)

        return rtn

    @property
    def hdr(self):
        if self.hdrOvr is None:
            cmndHdr={'HOST': '127.0.0.1:60006', \
                 'Accept-Ranges': 'bytes', \
                 'CONTENT-TYPE': 'text/xml; charset="utf-8"', \
                 'USER-AGENT': 'LINUX UPnP/1.0 Denon-Heos/149200'}

            cmndHdr['CONTENT-LENGTH'] = str(len(self.msg))
            cmndHdr['SOAPACTION']='"%s#%s"' % (self.urn, self.name)
        else:
            cmndHdr=self.hdrOvr

        return cmndHdr

    @hdr.setter
    def hdr(self, cmndHdr):
        self.hdrOvr=cmndHdr

    @property
    def msg(self):
        if self.msgOvr is None:
            msgBody=''

            for argName, argVal in self.args.items():
                msgBody=msgBody+('<%s>%s</%s>' % (argName, argVal, argName))

            bodyHdr     = '<s:Body><u:%s xmlns:u="%s">' % (self.name, self.urn)
            bodyTail    = '</u:%s></s:Body>' % self.name
            msg ='%s%s%s%s%s' % \
                (self._msgEnvHead, bodyHdr, msgBody, bodyTail, self._msgEnvTail)
        else:
            msg=self.msgOvr
        return msg

    @msg.setter
    def msg(self, msg):
        self.msgOvr=msg

    @property
    def msgReplyArgs(self):
        msgReplyArgs=OrderedDict()
        for arg, val in self.rtn.items():
            msgReplyArgs[arg]=str(val)
        return msgReplyArgs

    @property
    def rtnMsg(self):
        if self.rtnMsgOvr is None:
            bodyHdr     = '<s:Body><u:%sResponse xmlns:u="%s">' % (self.name, self.urn)
            bodyTail    = '</u:%sResponse></s:Body>' % self.name

            msg ='%s%s%s%s%s' % \
                (self._msgEnvHead, bodyHdr, self.rtnMsgBody, bodyTail, self._msgEnvTail)
        else:
            msg=self.rtnMsgOvr
        return msg

    @rtnMsg.setter
    def rtnMsg(self, rtnMsg):
        self.rtnMsgOvr=rtnMsg

    @property
    def rtnMsgBody(self):
        rtnBody=''

        rtnParam="<%s>%s</%s>"
        for param, val in self.rtn.items():
            rtnBody = rtnBody + (rtnParam % (param, str(val), param))
        return rtnBody

class CmndTest(unittest.TestCase):
    class CmndTestSvc():
        def __init__(self):
            self.name="testCmnd"
            self.devName="testDevName"

    def setUp(self):
        svcInst=self.CmndTestSvc()
        self.maxDiff=None

        self.cmnd='CreateGroup'
        self.urn='urn:schemas-denon-com:service:GroupControl:1'
        self.path='/upnp/control/AiosServicesDvc/GroupControl'

        self.shoeCmnd=TestShoeCmnd(self.cmnd, self.urn, self.path, svcInst)

        self.shoeCmnd.args = OrderedDict([ \
                        ('GroupFriendlyName', 'Jam'),\
                        ('GroupMemberUUIDList',\
                          'caf7916a94db1a1300800005cdfbb9c6,f3ddb59f3e691f1e00800005cdff1706'),\
                        ('GroupMemberChannelList', '')])

        self.shoeCmnd.rtn=OrderedDict([('GroupUUID', '17083c46d003001000800005cdfbb9c6'),])

        self.shoeCmnd.argsCfg=  [\
                {'relatedStateVariable': 'GroupFriendlyName','direction': 'in',\
                  'name': 'GroupFriendlyName',\
                  'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupFriendlyName'}},\
                {'relatedStateVariable': 'GroupMemberUUIDList', 'direction': 'in',\
                  'name': 'GroupMemberUUIDList',\
                  'state' :{'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupMemberUUIDList'}},\
                {'relatedStateVariable': 'GroupMemberChannelList', 'direction': 'in', \
                  'name': 'GroupMemberChannelList',\
                  'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupMemberChannelList'}},\
                {'relatedStateVariable': 'GroupUUID', 'direction': 'out', \
                   'name': 'GroupUUID',\
                   'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'}},]

        self.msg = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                    's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
                                    '<s:Body>'\
                                    '<u:CreateGroup xmlns:u="urn:schemas-denon-com:service:GroupControl:1">'\
                                        '<GroupFriendlyName>Jam</GroupFriendlyName>'\
                                        '<GroupMemberUUIDList>caf7916a94db1a1300800005cdfbb9c6,'\
                                           'f3ddb59f3e691f1e00800005cdff1706</GroupMemberUUIDList>'\
                                        '<GroupMemberChannelList></GroupMemberChannelList>'\
                                    '</u:CreateGroup>'\
                                    '</s:Body>'\
                                    '</s:Envelope>'

        self.rtnMsgBody='<GroupUUID>17083c46d003001000800005cdfbb9c6</GroupUUID>'

        self.rtnMsg='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                    's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
                                    '<s:Body>'\
                    '<u:CreateGroupResponse xmlns:u="urn:schemas-denon-com:service:GroupControl:1">'\
                               '<GroupUUID>17083c46d003001000800005cdfbb9c6</GroupUUID></u:CreateGroupResponse>'\
                               '</s:Body></s:Envelope>'

        self.hdr={'HOST': '127.0.0.1:60006', \
                  'CONTENT-LENGTH': '439', \
                  'Accept-Ranges': 'bytes', \
                  'CONTENT-TYPE': 'text/xml; charset="utf-8"', \
                  'SOAPACTION': '"urn:schemas-denon-com:service:GroupControl:1#CreateGroup"', \
                  'USER-AGENT': 'LINUX UPnP/1.0 Denon-Heos/149200'}

    def runTest(self):
        self.assertEqual(self.shoeCmnd.msg, self.msg)
        self.assertEqual(self.shoeCmnd.rtnMsg, self.rtnMsg)
        self.assertEqual(self.shoeCmnd.rtnMsgBody, self.rtnMsgBody)
        self.assertDictEqual(self.shoeCmnd.hdr, self.hdr)

class CmndTestGetVol(CmndTest):
    def setUp(self):
        self.maxDiff=None
        svcInst=self.CmndTestSvc()

        self.cmnd='GetGroupVolume'
        self.urn='urn:schemas-denon-com:service:GroupControl:1'
        self.path='/upnp/control/AiosServicesDvc/GroupControl'
        self.shoeCmnd=TestShoeCmnd(self.cmnd, self.urn, self.path, svcInst)

        self.shoeCmnd.argsCfg= [\
                            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID',\
                             'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'}},\
                            {'relatedStateVariable': 'GroupVolume', 'direction': 'out','name': 'GroupVolume',\
                             'state' : {'dataType': 'ui2', 'defaultValue': '0', \
                             'allowedValueRange': {'step': '1', 'minimum': '0', 'maximum': '100'}, \
                             'name': 'GroupVolume', '@sendEvents': 'no'}},]

        self.shoeCmnd.args=OrderedDict([('GroupUUID', '17083c46d003001000800005cdfbb9c6'),])

        self.shoeCmnd.rtn=OrderedDict([('GroupVolume', 90),])

        self.rtnMsgBody = '<GroupVolume>90</GroupVolume>'

        self.rtnMsg='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                    's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>'\
                    '<u:GetGroupVolumeResponse xmlns:u="urn:schemas-denon-com:service:GroupControl:1">'\
                    '<GroupVolume>90</GroupVolume></u:GetGroupVolumeResponse>'\
                    '</s:Body></s:Envelope>'

        self.hdr={'HOST': '127.0.0.1:60006', \
                  'CONTENT-LENGTH': '301', \
                  'Accept-Ranges': 'bytes', \
                  'CONTENT-TYPE': 'text/xml; charset="utf-8"', \
                  'SOAPACTION': '"urn:schemas-denon-com:service:GroupControl:1#GetGroupVolume"', \
                  'USER-AGENT': 'LINUX UPnP/1.0 Denon-Heos/149200'}

        self.msg='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                    's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
                    '<s:Body><u:GetGroupVolume '\
                    'xmlns:u="urn:schemas-denon-com:service:GroupControl:1">'\
                    '<GroupUUID>17083c46d003001000800005cdfbb9c6</GroupUUID>'\
                    '</u:GetGroupVolume></s:Body></s:Envelope>'
