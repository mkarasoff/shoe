##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testZoneCtrlSvc.py
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
from .testShoeCmnd import *
from .testShoeEvent import *

from collections import OrderedDict

class TestZoneCtrlSvc(TestShoeSvc):
    def __init__(self, devName, svcCfg):
        super().__init__(xmlFile='ZoneControl.xml',
                            md5hex='181615f9e5cc9c18f413ba3719afedb6',
                            devName=devName,
                            svcCfg=svcCfg)

################################################################################
        cmnd=TestShoeEvent('GetCurrentState', self.urn, self.cmndPath)

        cmnd.rtnMsgBody='<CurrentState>&lt;Event xmlns=&quot;urn:schemas-upnp-org:metadata-1-0/ZCS/&quot;&gt;&lt;'\
                'ZoneConnectedList val=&quot;caf7916a94db1a1300800005cdfbb9c6,'\
                'f3ddb59f3e691f1e00800005cdff1706&quot;/&gt;&lt;ZoneFriendlyName val=&quot;Family Room&quot;'\
                '/&gt;&lt;ZoneMemberList val=&quot;caf7916a94db1a1300800005cdfbb9c6,'\
                'f3ddb59f3e691f1e00800005cdff1706&quot;/&gt;&lt;ZoneMemberStatusList val=&quot;'\
                'caf7916a94db1a1300800005cdfbb9c6,ZONE_LEAD,f3ddb59f3e691f1e00800005cdff1706,ZONE_SLAVE&quot;'\
                '/&gt;&lt;ZoneMute val=&quot;0&quot;/&gt;&lt;ZoneStatus val=&quot;ZONE_LEAD&quot;/&gt;&lt;'\
                'ZoneVolume val=&quot;31&quot;/&gt;&lt;ZoneMinimise val=&quot;0&quot;/&gt;&lt;ZoneUUID val=&quot;'\
                '17083c46d003001000800005cdfbb9c6&quot;/&gt;&lt;/Event&gt;</CurrentState>'

        cmnd.rtn=OrderedDict([('CurrentState',
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

        cmnd.fmtOutput=\
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

        cmnd.argsCfg= [\
                        {'relatedStateVariable': 'LastChange', 'direction': 'out', 'name': 'CurrentState',\
                           'state' : {'dataType': 'string', '@sendEvents': 'yes', 'name': 'LastChange'}},]

        self.cmnds[cmnd.name]=cmnd

        return
################################################################################
    @property
    def cmndTbl(self):
        cmndTbl ={\
             'DummyAction_ZoneControl': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'A_ARG_TYPE_DummyValueZoneControl', 'direction': 'out', 'name': 'DummyValue'}],\
             'GetZoneMute': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMute', 'direction': 'out', 'name': 'ZoneMute'}],\
             'GetZoneMemberList': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMemberList', 'direction': 'out', 'name': 'ZoneMemberList'}],\
             'GetCurrentState': [\
                {'relatedStateVariable': 'LastChange', 'direction': 'out', 'name': 'CurrentState'}],\
             'TestZoneConnectivity': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneIPList', 'direction': 'in', 'name': 'ZoneIPList'},\
                {'relatedStateVariable': 'A_ARG_TYPE_SupportedGroupList', 'direction': 'out', 'name': 'SupportedGroupList'},\
                {'relatedStateVariable': 'A_ARG_TYPE_SupportedMediaType', 'direction': 'out', 'name': 'SupportedMediaType'}],\
             'GetZoneMinimise': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMinimise', 'direction': 'out', 'name': 'ZoneMinimise'}],\
             'DestroyZone': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'}],\
             'GetZoneUUID': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'out', 'name': 'ZoneUUID'}],\
             'SetZoneMute': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMute', 'direction': 'in', 'name': 'ZoneMute'}],\
             'GetMemberStatus': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMemberStatusList', 'direction': 'out', 'name': 'ZoneMemberStatusList'}],\
             'GetZoneFriendlyName': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneFriendlyName', 'direction': 'out', 'name': 'ZoneFriendlyName'}],\
             'GetZoneConnectedList': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneConnectedList', 'direction': 'out', 'name': 'ZoneConnectedList'}],\
             'RemoveMemberFromZone': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'A_ARG_TYPE_GroupIP', 'direction': 'in', 'name': 'GroupIP'}],\
             'SetZoneFriendlyName': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneFriendlyName', 'direction': 'in', 'name': 'ZoneFriendlyName'}],\
             'SetZoneMinimise': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMinimise', 'direction': 'in', 'name': 'ZoneMinimise'}],\
             'GetZoneStatus': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneStatus', 'direction': 'out', 'name': 'ZoneStatus'}],\
             'GetZoneVolume': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneVolume', 'direction': 'out', 'name': 'ZoneVolume'}],\
             'CreateZone': [\
                {'relatedStateVariable': 'ZoneFriendlyName', 'direction': 'in', 'name': 'ZoneFriendlyName'},\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneIPList', 'direction': 'in', 'name': 'ZoneIPList'},\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'out', 'name': 'ZoneUUID'}],\
             'AddMemberToZone': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'A_ARG_TYPE_GroupIP', 'direction': 'in', 'name': 'GroupIP'}],\
             'SetZoneVolume': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID', 'direction': 'in', 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneVolume', 'direction': 'in', 'name': 'ZoneVolume'}]}
        return cmndTbl

    @property
    def stateVarTbl(self):
        stateVarTbl={\
            'A_ARG_TYPE_ZoneUUID':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_ZoneUUID'},\
            'ZoneVolume':\
                {'dataType': 'ui1', 'defaultValue': '0', 'allowedValueRange':\
                {'step': '1', 'minimum': '0', 'maximum': '100'},\
                    'name': 'ZoneVolume', '@sendEvents': 'no'},\
            'ZoneStatus':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'ZoneStatus'},\
            'ZoneMemberList':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'ZoneMemberList'},\
            'A_ARG_TYPE_SupportedGroupList':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_SupportedGroupList'},\
            'A_ARG_TYPE_DummyValueZoneControl':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_DummyValueZoneControl'},\
            'A_ARG_TYPE_CurrentState_ZoneControl':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_CurrentState_ZoneControl'},\
            'A_ARG_TYPE_SupportedMediaType':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_SupportedMediaType'},\
            'LastChange':\
                {'dataType': 'string', '@sendEvents': 'yes', 'name': 'LastChange'},\
            'ZoneConnectedList':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'ZoneConnectedList'},\
            'ZoneMinimise':\
                {'dataType': 'boolean', 'defaultValue': '0', 'name': 'ZoneMinimise', '@sendEvents': 'no'},\
            'ZoneFriendlyName':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'ZoneFriendlyName'},\
            'A_ARG_TYPE_ZoneIPList':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_ZoneIPList'},\
            'A_ARG_TYPE_GroupIP':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'A_ARG_TYPE_GroupIP'},\
            'ZoneMemberStatusList':\
                {'dataType': 'string', '@sendEvents': 'no', 'name': 'ZoneMemberStatusList'},\
            'ZoneMute':\
                {'dataType': 'boolean', 'defaultValue': '0', 'name': 'ZoneMute', '@sendEvents': 'no'}}
        return stateVarTbl

    @property
    def scpd(self):
        scpd={'scpd': {'actionList': {'action': [\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'A_ARG_TYPE_GroupIP',\
                 'direction': 'in',\
                 'name': 'GroupIP'}]},\
             'name': 'AddMemberToZone'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'ZoneFriendlyName',\
                 'direction': 'in',\
                 'name': 'ZoneFriendlyName'},\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneIPList',\
                 'direction': 'in',\
                 'name': 'ZoneIPList'},\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'out',\
                 'name': 'ZoneUUID'}]},\
             'name': 'CreateZone'},\
            {'argumentList': {'argument':\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'}},\
             'name': 'DestroyZone'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'A_ARG_TYPE_DummyValueZoneControl',\
                 'direction': 'out',\
                 'name': 'DummyValue'}]},\
             'name': 'DummyAction_ZoneControl'},\
            {'argumentList': {'argument':\
                {'relatedStateVariable': 'LastChange',\
                 'direction': 'out',\
                 'name': 'CurrentState'}},\
             'name': 'GetCurrentState'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMemberStatusList',\
                 'direction': 'out',\
                 'name': 'ZoneMemberStatusList'}]},\
             'name': 'GetMemberStatus'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneConnectedList',\
                 'direction': 'out',\
                 'name': 'ZoneConnectedList'}]},\
             'name': 'GetZoneConnectedList'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneFriendlyName',\
                 'direction': 'out',\
                 'name': 'ZoneFriendlyName'}]},\
             'name': 'GetZoneFriendlyName'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMemberList',\
                 'direction': 'out',\
                 'name': 'ZoneMemberList'}]},\
             'name': 'GetZoneMemberList'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMinimise',\
                 'direction': 'out',\
                 'name': 'ZoneMinimise'}]},\
             'name': 'GetZoneMinimise'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMute',\
                 'direction': 'out',\
                 'name': 'ZoneMute'}]},\
             'name': 'GetZoneMute'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneStatus',\
                 'direction': 'out',\
                 'name': 'ZoneStatus'}]},\
             'name': 'GetZoneStatus'},\
            {'argumentList': {'argument':\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'out',\
                 'name': 'ZoneUUID'}},\
             'name': 'GetZoneUUID'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneVolume',\
                 'direction': 'out',\
                 'name': 'ZoneVolume'}]},\
             'name': 'GetZoneVolume'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'A_ARG_TYPE_GroupIP',\
                 'direction': 'in',\
                 'name': 'GroupIP'}]},\
             'name': 'RemoveMemberFromZone'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneFriendlyName',\
                 'direction': 'in',\
                 'name': 'ZoneFriendlyName'}]},\
             'name': 'SetZoneFriendlyName'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMinimise',\
                 'direction': 'in',\
                 'name': 'ZoneMinimise'}]},\
             'name': 'SetZoneMinimise'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneMute',\
                 'direction': 'in',\
                 'name': 'ZoneMute'}]},\
             'name': 'SetZoneMute'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneUUID',\
                 'direction': 'in',\
                 'name': 'ZoneUUID'},\
                {'relatedStateVariable': 'ZoneVolume',\
                 'direction': 'in',\
                 'name': 'ZoneVolume'}]},\
             'name': 'SetZoneVolume'},\
            {'argumentList': {'argument': [\
                {'relatedStateVariable': 'A_ARG_TYPE_ZoneIPList',\
                 'direction': 'in',\
                 'name': 'ZoneIPList'},\
                {'relatedStateVariable': 'A_ARG_TYPE_SupportedGroupList',\
                 'direction': 'out',\
                 'name': 'SupportedGroupList'},\
                {'relatedStateVariable': 'A_ARG_TYPE_SupportedMediaType',\
                 'direction': 'out',\
                 'name': 'SupportedMediaType'}]},\
             'name': 'TestZoneConnectivity'}]},\
             'serviceStateTable': {'stateVariable': [\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'A_ARG_TYPE_CurrentState_ZoneControl'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'A_ARG_TYPE_DummyValueZoneControl'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'A_ARG_TYPE_GroupIP'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'A_ARG_TYPE_SupportedGroupList'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'A_ARG_TYPE_SupportedMediaType'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'A_ARG_TYPE_ZoneIPList'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'A_ARG_TYPE_ZoneUUID'},\
                {'dataType': 'string',\
                 '@sendEvents': 'yes',\
                 'name': 'LastChange'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'ZoneConnectedList'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'ZoneFriendlyName'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'ZoneMemberList'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'ZoneMemberStatusList'},\
                {'dataType': 'boolean',\
                 'defaultValue': '0',\
                 'name': 'ZoneMinimise',\
                 '@sendEvents': 'no'},\
                {'dataType': 'boolean',\
                 'defaultValue': '0',\
                 'name': 'ZoneMute',\
                 '@sendEvents': 'no'},\
                {'dataType': 'string',\
                 '@sendEvents': 'no',\
                 'name': 'ZoneStatus'},\
                {'dataType': 'ui1',\
                 'defaultValue': '0',\
                 'allowedValueRange': {'step': '1',\
                 'minimum': '0',\
                 'maximum': '100'},\
                 'name': 'ZoneVolume',\
                 '@sendEvents': 'no'}]},\
                 'specVersion': {'major': '1',\
                 'minor': '0'}}}

        return scpd
