##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testGroupCtrlSvc.py
#Class for unittest data generated from GroupControl service SCPD file.
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
from .testShoeSvc import *
from .testShoeEvent import *
from .testShoeCmnd import *
from .testZoneCtrlSvc import *
from collections import OrderedDict

class TestGroupCtrlSvc(TestShoeSvc):
    CFG={'controlURL': '/upnp/control/AiosServicesDvc/GroupControl',\
                     'serviceType': 'urn:schemas-denon-com:service:GroupControl:1', \
                     'serviceId': 'urn:denon-com:serviceId:GroupControl', \
                     'eventSubURL': '/upnp/event/AiosServicesDvc/GroupControl', \
                     'SCPDURL': '/upnp/scpd/AiosServicesDvc/GroupControl.xml'}

    GROUP_UUID='17083c46d003001000800005cdfbb9c6'

    def __init__(self, devName='AiosServices', svcCfg=CFG):
        super().__init__(  xmlFile='GroupControl.xml',
                        md5hex='d2164658e60eedbe0c79090ceb1d904e',
                        devName=devName,
                        svcCfg=svcCfg)

################################################################################
        cmnd=TestShoeCmnd('GetGroupStatus', self.urn, self.cmndPath, self)
        cmnd.argsCfg=  [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID',\
                    'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'}},\
            {'relatedStateVariable': 'GroupStatus', 'direction': 'out', 'name': 'GroupStatus', \
                    'state' : {'dataType': 'string', 'defaultValue': 'NONE', 'name':'GroupStatus',\
                            '@sendEvents': 'no', 'allowedValueList': \
                            {'allowedValue': ['LEADER', 'SLAVE', 'NONE']}}}]

        cmnd.args=OrderedDict([('GroupUUID', self.GROUP_UUID),])
        cmnd.rtn=OrderedDict([('GroupStatus', 'NONE'),])
        cmnd.fmtRtn='GroupStatus      : NONE'

        self.cmnds[cmnd.name]=cmnd

################################################################################
        cmnd=TestShoeCmnd('GetGroupUUID', self.urn, self.cmndPath, self)
        cmnd.argsCfg=  [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'out', 'name': 'GroupUUID',\
                    'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'}},\
            ]

        cmnd.rtn=OrderedDict([('GroupUUID', self.GROUP_UUID),])
        cmnd.fmtRtn='GroupUUID        : %s' % self.GROUP_UUID

        self.cmnds[cmnd.name]=cmnd

################################################################################
        cmnd=TestShoeCmnd('DestroyGroup', self.urn, self.cmndPath, self)
        cmnd.argsCfg=  [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID',\
                    'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'}},\
            {'relatedStateVariable': 'PreserveZone', 'direction': 'in', 'name': 'PreserveZone', \
                    'state' : {'dataType': 'boolean', 'defaultValue': '0', 'name': 'PreserveZone',\
                            '@sendEvents': 'no'}}]

        cmnd.args=OrderedDict([('GroupUUID', self.GROUP_UUID), ('PreserveZone', '0')])

        self.cmnds[cmnd.name]=cmnd

################################################################################
        cmnd=TestShoeCmnd('GetGroupMemberChannel', self.urn, self.cmndPath, self)
        cmnd.argsCfg=  [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID',\
                    'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'}},\
            {'relatedStateVariable': 'AudioChannel', 'direction': 'out', 'name': 'AudioChannel',\
                    'state' : {'dataType': 'string', 'defaultValue': 'NORMAL', 'name':'AudioChannel', \
                        '@sendEvents': 'no', 'allowedValueList': {'allowedValue': \
                            ['NORMAL', 'LEFT', 'RIGHT', 'REAR_LEFT', \
                            'REAR_RIGHT', 'LOW_FREQUENCY', 'REAR_STEREO']} }},]

        cmnd.args=OrderedDict([('GroupUUID', self.GROUP_UUID),])
        cmnd.rtn=OrderedDict([('AudioChannel', 'LEFT'),])
        cmnd.fmtRtn='AudioChannel     : LEFT'

        self.cmnds[cmnd.name]=cmnd

################################################################################
        cmnd=TestShoeCmnd('SetGroupMemberChannel', self.urn, self.cmndPath, self)

        cmnd.argsCfg=[\
                {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID',\
                     'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'}},\
                {'relatedStateVariable': 'AudioChannel', 'direction': 'in', 'name': 'AudioChannel',\
                    'state' : {'dataType': 'string', 'defaultValue': 'NORMAL', 'name':'AudioChannel', \
                        '@sendEvents': 'no', 'allowedValueList': {'allowedValue': \
                            ['NORMAL', 'LEFT', 'RIGHT', 'REAR_LEFT', \
                            'REAR_RIGHT', 'LOW_FREQUENCY', 'REAR_STEREO']} }},]

        cmnd.args=OrderedDict()
        cmnd.args['GroupUUID']=self.GROUP_UUID
        cmnd.args['AudioChannel']='LEFT'

        self.cmnds[cmnd.name]=cmnd

################################################################################
        cmnd=TestShoeCmnd('GetGroupVolume', self.urn, self.cmndPath, self)

        cmnd.argsCfg= [\
                    {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID',\
                     'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'}},\
                    {'relatedStateVariable': 'GroupVolume', 'direction': 'out','name': 'GroupVolume',\
                     'state' : {'dataType': 'ui2', 'defaultValue': '0', \
                     'allowedValueRange': {'step': '1', 'minimum': '0', 'maximum': '100'}, \
                     'name': 'GroupVolume', '@sendEvents': 'no' }},]

        cmnd.args=OrderedDict([('GroupUUID', self.GROUP_UUID),])
        cmnd.rtn=OrderedDict([('GroupVolume', 90),])
        cmnd.fmtRtn='GroupVolume      : 90'

        self.cmnds[cmnd.name]=cmnd
################################################################################
        cmnd=TestShoeCmnd('CreateGroup', self.urn, self.cmndPath, self)

        cmnd.argsCfg=  [\
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

        cmnd.args = OrderedDict([ \
                        ('GroupFriendlyName', 'Jam'),\
                        ('GroupMemberUUIDList',TestZoneCtrlSvc.ZONE_MEMBERS),
                        ('GroupMemberChannelList', '')])

        cmnd.rtn=OrderedDict([('GroupUUID', self.GROUP_UUID),])
        cmnd.fmtRtn='GroupUUID        : %s' % self.GROUP_UUID

        self.cmnds[cmnd.name]=cmnd
################################################################################
        cmnd=TestShoeEvent('GetCurrentState', self.urn, self.cmndPath, self)

        cmnd.argsCfg= [\
                    {'relatedStateVariable': 'LastChange', 'direction': 'out', 'name': 'CurrentState',\
                     'state' : {'dataType': 'string', '@sendEvents': 'yes', 'name': 'LastChange'}},]

        cmnd.rtn=OrderedDict([('CurrentState', ''),])
        cmnd.fmtRtn='CurrentState     : '
        self.cmnds[cmnd.name]=cmnd

        return

################################################################################
    @property
    def cmndTbl(self):
        cmndTbl={\
        'GetGroupBalance': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupBalance', 'direction': 'out', 'name': 'GroupBalance'}],\
        'GetGroupTreble': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupTreble', 'direction': 'out', 'name': 'GroupTreble'}],\
        'GetMediaServerUUID': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'MediaServerUUID', 'direction': 'out', 'name': 'MediaServerUUID'}],\
        'GetGroupBass': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupBass', 'direction': 'out', 'name': 'GroupBass'}],\
        'SetGroupMemberChannel': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'AudioChannel', 'direction': 'in', 'name': 'AudioChannel'}],\
        'GetGroupVolume': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupVolume', 'direction': 'out', 'name': 'GroupVolume'}],\
        'GetSignalStrength': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'ExtApSignalStrength', 'direction': 'out', 'name': 'SignalStrength'}],\
        'CreateGroup': [\
            {'relatedStateVariable': 'GroupFriendlyName', 'direction': 'in', 'name': 'GroupFriendlyName'},\
            {'relatedStateVariable': 'GroupMemberUUIDList', 'direction': 'in', 'name': 'GroupMemberUUIDList'},\
            {'relatedStateVariable': 'GroupMemberChannelList', 'direction': 'in', 'name': 'GroupMemberChannelList'},\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'out', 'name': 'GroupUUID'}],\
        'GetGroupStatus': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupStatus', 'direction': 'out', 'name': 'GroupStatus'}],\
        'GetConfigDeviceUUID': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'ConfigDeviceUUID', 'direction': 'out', 'name': 'ConfigDeviceUUID'}],\
        'GetGroupMemberList': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupMemberUUIDList', 'direction': 'out', 'name': 'GroupMemberUUIDList'}],\
        'GetDeviceFriendlyName': [\
            {'relatedStateVariable': 'DeviceFriendlyName', 'direction': 'out', 'name': 'DeviceFriendlyName'}],\
        'AddMembersToGroup': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'A_ARG_TYPE_IPList', 'direction': 'in', 'name': 'GroupMemberIPList'},\
            {'relatedStateVariable': 'GroupMemberUUIDList', 'direction': 'in', 'name': 'GroupMemberUUIDList'},\
            {'relatedStateVariable': 'GroupMemberChannelList', 'direction': 'in', 'name': 'GroupMemberChannelList'},\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'out', 'name': 'GroupUUIDOut'}],\
        'DummyAction_GroupControl': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'A_ARG_TYPE_DummyValueGroupControl', 'direction': 'out', 'name': 'DummyValue'}],\
        'SetGroupMute': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupMute', 'direction': 'in', 'name': 'GroupMute'},\
            {'relatedStateVariable': 'CommandID', 'direction': 'in', 'name': 'CommandID'}],\
        'SetDeviceFriendlyName': [\
            {'relatedStateVariable': 'DeviceFriendlyName', 'direction': 'in', 'name': 'DeviceFriendlyName'}],\
        'GetGroupFriendlyName': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupFriendlyName', 'direction': 'out', 'name': 'GroupFriendlyName'}],\
        'RemoveMembersFromGroup': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupMemberUUIDList', 'direction': 'in', 'name': 'GroupMemberUUIDList'}],\
        'GetCurrentState': [\
            {'relatedStateVariable': 'LastChange', 'direction': 'out', 'name': 'CurrentState'}],\
        'SetGroupBalance': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupBalance', 'direction': 'in', 'name': 'GroupBalance'},\
            {'relatedStateVariable': 'CommandID', 'direction': 'in', 'name': 'CommandID'}],\
        'SetGroupVolume': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupVolume', 'direction': 'in', 'name': 'GroupVolume'},\
            {'relatedStateVariable': 'CommandID', 'direction': 'in', 'name': 'CommandID'}],\
        'GetGroupMemberChannel': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'AudioChannel', 'direction': 'out', 'name': 'AudioChannel'}],\
        'GetGroupUpdating': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupUpdating', 'direction': 'out', 'name': 'GroupUpdating'}],\
        'SetGroupTreble': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupTreble', 'direction': 'in', 'name': 'GroupTreble'}],\
        'SetGroupFriendlyName': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupFriendlyName', 'direction': 'in', 'name': 'GroupFriendlyName'}],\
        'GetGroupMute': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupMute', 'direction': 'out', 'name': 'GroupMute'}],\
        'SetGroupBass': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupBass', 'direction': 'in', 'name': 'GroupBass'}],\
        'DestroyGroup': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'in', 'name': 'GroupUUID'},\
            {'relatedStateVariable': 'PreserveZone', 'direction': 'in', 'name': 'PreserveZone'}],\
        'GetGroupUUID': [\
            {'relatedStateVariable': 'GroupUUID', 'direction': 'out', 'name': 'GroupUUID'}]}

        return cmndTbl

    @property
    def stateVarTbl(self):
        stateVarTbl={\
        'GroupBass': {'dataType': 'ui2', 'defaultValue': '0',\
                    'allowedValueRange': {'step': '1', 'minimum': '0', 'maximum': '10'},\
                    'name': 'GroupBass', '@sendEvents': 'no'},\
        'GroupUpdating': {'dataType': 'boolean', 'defaultValue': '0', 'name': 'GroupUpdating', '@sendEvents': 'no'},\
        'A_ARG_TYPE_IPList': {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_IPList'},\
        'DeviceFriendlyName': {'dataType': 'string', '@sendEvents': 'no', 'name': 'DeviceFriendlyName'},\
        'CommandID': {'dataType': 'string', '@sendEvents': 'no', 'name': 'CommandID'},\
        'GroupMemberUUIDList': {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupMemberUUIDList'},\
        'AudioChannel': {'dataType': 'string', 'defaultValue': 'NORMAL', 'name':'AudioChannel', '@sendEvents': 'no', \
                    'allowedValueList': {'allowedValue': \
                        ['NORMAL', 'LEFT', 'RIGHT', 'REAR_LEFT', 'REAR_RIGHT', 'LOW_FREQUENCY', 'REAR_STEREO']}},\
        'GroupUUID': {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupUUID'},\
        'A_ARG_TYPE_CurrentState_GroupControl': {'dataType': 'string', '@sendEvents': 'no',\
                    'name': 'A_ARG_TYPE_CurrentState_GroupControl'},\
        'PreserveZone': {'dataType': 'boolean', 'defaultValue': '0', 'name': 'PreserveZone', '@sendEvents': 'no'},\
        'GroupFriendlyName': {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupFriendlyName'},\
        'MediaServerUUID': {'dataType': 'string', '@sendEvents': 'no', 'name': 'MediaServerUUID'},\
        'A_ARG_TYPE_DummyValueGroupControl': \
                    {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_DummyValueGroupControl'},\
        'GroupVolume': {'dataType': 'ui2', 'defaultValue': '0', \
                    'allowedValueRange': {'step': '1', 'minimum': '0', 'maximum': '100'},\
                    'name': 'GroupVolume', '@sendEvents': 'no'},\
        'ConfigDeviceUUID': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ConfigDeviceUUID'},\
        'GroupMemberChannelList': {'dataType': 'string', '@sendEvents': 'no', 'name': 'GroupMemberChannelList'},\
        'GroupMute': {'dataType': 'boolean', 'defaultValue': '0', 'name': 'GroupMute', '@sendEvents': 'no'},\
        'ExtApSignalStrength': {'dataType': 'ui2', 'defaultValue': '0', \
                    'allowedValueRange': {'step': '1', 'minimum': '0', 'maximum': '100'},\
                    'name': 'ExtApSignalStrength', '@sendEvents': 'no'},\
        'GroupBalance': {'dataType': 'ui2', 'defaultValue': '50', \
                    'allowedValueRange': {'step': '1', 'minimum': '0', 'maximum': '100'},\
                    'name': 'GroupBalance', '@sendEvents': 'no'},\
        'GroupTreble': {'dataType': 'ui2', 'defaultValue': '0', \
                    'allowedValueRange': {'step': '1', 'minimum': '0', 'maximum': '10'},\
                    'name': 'GroupTreble', '@sendEvents': 'no'},\
        'LastChange': {'dataType': 'string', '@sendEvents': 'yes', 'name': 'LastChange'},\
        'GroupStatus': {'dataType': 'string', 'defaultValue': 'NONE', 'name':'GroupStatus', '@sendEvents': 'no', \
                    'allowedValueList': {'allowedValue': ['LEADER', 'SLAVE', 'NONE']}}}

        return stateVarTbl

    @property
    def scpd(self):
        scpd= {'scpd': {'actionList': {'action': [\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'A_ARG_TYPE_IPList',\
              'direction': 'in',\
              'name': 'GroupMemberIPList'},\
            {'relatedStateVariable': 'GroupMemberUUIDList',\
              'direction': 'in',\
              'name': 'GroupMemberUUIDList'},\
            {'relatedStateVariable': 'GroupMemberChannelList',\
              'direction': 'in',\
              'name': 'GroupMemberChannelList'},\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'out',\
              'name': 'GroupUUIDOut'}]},\
         'name': 'AddMembersToGroup'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupFriendlyName',\
              'direction': 'in',\
              'name': 'GroupFriendlyName'},\
            {'relatedStateVariable': 'GroupMemberUUIDList',\
              'direction': 'in',\
              'name': 'GroupMemberUUIDList'},\
            {'relatedStateVariable': 'GroupMemberChannelList',\
              'direction': 'in',\
              'name': 'GroupMemberChannelList'},\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'out',\
              'name': 'GroupUUID'}]},\
         'name': 'CreateGroup'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'PreserveZone',\
              'direction': 'in',\
              'name': 'PreserveZone'}]},\
         'name': 'DestroyGroup'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'A_ARG_TYPE_DummyValueGroupControl',\
              'direction': 'out',\
              'name': 'DummyValue'}]},\
         'name': 'DummyAction_GroupControl'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'ConfigDeviceUUID',\
              'direction': 'out',\
              'name': 'ConfigDeviceUUID'}]},\
         'name': 'GetConfigDeviceUUID'},\
        {'argumentList': {'argument': \
            {'relatedStateVariable': 'LastChange',\
              'direction': 'out',\
              'name': 'CurrentState'}},\
         'name': 'GetCurrentState'},\
        {'argumentList': {'argument': \
            {'relatedStateVariable': 'DeviceFriendlyName',\
              'direction': 'out',\
              'name': 'DeviceFriendlyName'}},\
              'name': 'GetDeviceFriendlyName'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupBalance',\
              'direction': 'out',\
              'name': 'GroupBalance'}]},\
         'name': 'GetGroupBalance'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupBass',\
              'direction': 'out',\
              'name': 'GroupBass'}]},\
         'name': 'GetGroupBass'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupFriendlyName',\
              'direction': 'out',\
              'name': 'GroupFriendlyName'}]},\
         'name': 'GetGroupFriendlyName'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'AudioChannel',\
              'direction': 'out',\
              'name': 'AudioChannel'}]},\
         'name': 'GetGroupMemberChannel'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupMemberUUIDList',\
              'direction': 'out',\
              'name': 'GroupMemberUUIDList'}]},\
         'name': 'GetGroupMemberList'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupMute',\
              'direction': 'out',\
              'name': 'GroupMute'}]},\
         'name': 'GetGroupMute'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupStatus',\
              'direction': 'out',\
              'name': 'GroupStatus'}]},\
         'name': 'GetGroupStatus'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupTreble',\
              'direction': 'out',\
              'name': 'GroupTreble'}]},\
         'name': 'GetGroupTreble'},\
        {'argumentList': {'argument': \
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'out',\
              'name': 'GroupUUID'}},\
         'name': 'GetGroupUUID'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupUpdating',\
              'direction': 'out',\
              'name': 'GroupUpdating'}]},\
         'name': 'GetGroupUpdating'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupVolume',\
              'direction': 'out',\
              'name': 'GroupVolume'}]},\
         'name': 'GetGroupVolume'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'MediaServerUUID',\
              'direction': 'out',\
              'name': 'MediaServerUUID'}]},\
         'name': 'GetMediaServerUUID'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'ExtApSignalStrength',\
              'direction': 'out',\
              'name': 'SignalStrength'}]},\
         'name': 'GetSignalStrength'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupMemberUUIDList',\
              'direction': 'in',\
              'name': 'GroupMemberUUIDList'}]},\
         'name': 'RemoveMembersFromGroup'},\
        {'argumentList': {'argument': \
            {'relatedStateVariable': 'DeviceFriendlyName',\
              'direction': 'in',\
              'name': 'DeviceFriendlyName'}},\
         'name': 'SetDeviceFriendlyName'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupBalance',\
              'direction': 'in',\
              'name': 'GroupBalance'},\
            {'relatedStateVariable': 'CommandID',\
              'direction': 'in',\
              'name': 'CommandID'}]},\
         'name': 'SetGroupBalance'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupBass',\
              'direction': 'in',\
              'name': 'GroupBass'}]},\
         'name': 'SetGroupBass'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupFriendlyName',\
              'direction': 'in',\
              'name': 'GroupFriendlyName'}]},\
         'name': 'SetGroupFriendlyName'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'AudioChannel',\
              'direction': 'in',\
              'name': 'AudioChannel'}]},\
         'name': 'SetGroupMemberChannel'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupMute',\
              'direction': 'in',\
              'name': 'GroupMute'},\
            {'relatedStateVariable': 'CommandID',\
              'direction': 'in',\
              'name': 'CommandID'}]},\
         'name': 'SetGroupMute'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupTreble',\
              'direction': 'in',\
              'name': 'GroupTreble'}]},\
         'name': 'SetGroupTreble'},\
        {'argumentList': {'argument': [\
            {'relatedStateVariable': 'GroupUUID',\
              'direction': 'in',\
              'name': 'GroupUUID'},\
            {'relatedStateVariable': 'GroupVolume',\
              'direction': 'in',\
              'name': 'GroupVolume'},\
            {'relatedStateVariable': 'CommandID',\
              'direction': 'in',\
              'name': 'CommandID'}]},\
         'name': 'SetGroupVolume'}]},\
        'serviceStateTable': {'stateVariable': [\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'A_ARG_TYPE_CurrentState_GroupControl'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'A_ARG_TYPE_DummyValueGroupControl'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'A_ARG_TYPE_IPList'},\
            {'dataType': 'string',\
              'defaultValue': 'NORMAL',\
              'name': 'AudioChannel',\
              '@sendEvents': 'no',\
              'allowedValueList': {'allowedValue': [\
                  'NORMAL',\
                  'LEFT',\
                  'RIGHT',\
                  'REAR_LEFT',\
                  'REAR_RIGHT',\
                  'LOW_FREQUENCY',\
                  'REAR_STEREO']}},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'CommandID'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'ConfigDeviceUUID'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'DeviceFriendlyName'},\
            {'dataType': 'ui2',\
              'defaultValue': '0',\
              'allowedValueRange': \
                 {'step': '1',\
                  'minimum': '0',\
                  'maximum': '100'},\
                  'name': 'ExtApSignalStrength',\
                  '@sendEvents': 'no'},\
            {'dataType': 'ui2',\
              'defaultValue': '50',\
              'allowedValueRange': \
                 {'step': '1',\
                  'minimum': '0',\
                  'maximum': '100'},\
                  'name': 'GroupBalance',\
                  '@sendEvents': 'no'},\
            {'dataType': 'ui2',\
              'defaultValue': '0',\
              'allowedValueRange': \
                 {'step': '1',\
                  'minimum': '0',\
                  'maximum': '10'},\
                  'name': 'GroupBass',\
                  '@sendEvents': 'no'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'GroupFriendlyName'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'GroupMemberChannelList'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'GroupMemberUUIDList'},\
            {'dataType': 'boolean',\
              'defaultValue': '0',\
              'name': 'GroupMute',\
              '@sendEvents': 'no'},\
            {'dataType': 'string',\
              'defaultValue': 'NONE',\
              'name': 'GroupStatus',\
              '@sendEvents': 'no',\
              'allowedValueList': {\
                  'allowedValue': [\
                  'LEADER',\
                  'SLAVE',\
                  'NONE']}},\
            {'dataType': 'ui2',\
              'defaultValue': '0',\
              'allowedValueRange': \
                  {'step': '1',\
                   'minimum': '0',\
                   'maximum': '10'},\
              'name': 'GroupTreble',\
              '@sendEvents': 'no'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'GroupUUID'},\
            {'dataType': 'boolean',\
              'defaultValue': '0',\
              'name': 'GroupUpdating',\
              '@sendEvents': 'no'},\
            {'dataType': 'ui2',\
              'defaultValue': '0',\
              'allowedValueRange': \
                 {'step': '1',\
                  'minimum': '0',\
                  'maximum': '100'},\
                  'name': 'GroupVolume',\
                  '@sendEvents': 'no'},\
            {'dataType': 'string',\
              '@sendEvents': 'yes',\
              'name': 'LastChange'},\
            {'dataType': 'string',\
              '@sendEvents': 'no',\
              'name': 'MediaServerUUID'},\
            {'dataType': 'boolean',\
              'defaultValue': '0',\
              'name': 'PreserveZone',\
              '@sendEvents': 'no'}]},\
              'specVersion': {'major': '1',\
              'minor': '0'}}}
        return scpd
