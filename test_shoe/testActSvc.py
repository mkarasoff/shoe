##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testActSvc.py
#Baseclass for unittest data generated from ACT service SCPD file.
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
from .shoeTestXml import *
from collections import OrderedDict

class TestActSvc(ShoeTestXml):
    def __init__(self):
        xmlFile='SCPD.xml'
        md5hex='ff2c1a651e8c18e28ae77a2fe2632994'
        self.urlPath='/ACT/'
        self.urn='urn:schemas-denon-com:service:ACT:1'

        self.url='%s%s' % (self.urlPath, xmlFile)
        self.name='ACT'
        self.devName='ACT-Denon'

        super(TestActSvc, self).__init__(xmlFile, md5hex)
################################################################################
        self.getCurrStCmnd='GetCurrentState'

        self.getCurrStArg= [\
                            {'relatedStateVariable': 'LastChange', 'direction': 'out', 'name': 'CurrentState',\
                             'state' : {'dataType': 'string', '@sendEvents': 'yes', 'name': 'LastChange'}},]

        self.getCurrStHdr={'HOST': '127.0.0.1:60006', \
                            'CONTENT-LENGTH': '239', \
                            'Accept-Ranges': 'bytes', \
                            'CONTENT-TYPE': 'text/xml; charset="utf-8"', \
                            'SOAPACTION': '"urn:schemas-denon-com:service:ACT:1#GetCurrentState"', \
                            'USER-AGENT': 'LINUX UPnP/1.0 Denon-Heos/149200'}

        self.getCurrStCmndXml= '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                                    's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
                                    '<s:Body>'\
                                    '<u:GetCurrentState xmlns:u="urn:schemas-denon-com:service:ACT:1">'\
                                    '</u:GetCurrentState>'\
                                    '</s:Body>'\
                                    '</s:Envelope>'

        self.getCurrStRtnXml='<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '\
                's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
                '<s:Body>'\
                    '<u:GetCurrentStateResponse '\
                        'xmlns:u="urn:schemas-denon-com:service:ACT:1">'\
                        '<CurrentState>%s</CurrentState></u:GetCurrentStateResponse>'\
                    '</s:Body>'\
                '</s:Envelope>' % self.getCurrStRtnBody

#<Event xmlns="urn:schemas-upnp-org:metadata-1-0/ACT/"><ActiveInterface val="1"/><FriendlyName val="Kitchen"/></Event>

################################################################################
        self.getAccPtListCmnd='GetAccessPointList'

        self.getAccPtListArgs= [\
                            {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken',\
                             'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_ConfigurationToken'}},\
                            {'relatedStateVariable': 'ARG_AccessPointList', 'direction': 'out', 'name': 'accessPointList',\
                             'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_AccessPointList'}},]

        getAccPtListRtnBody = '<u:GetAccessPointListResponse  xmlns:u="urn:schemas-denon-com:service:ACT:1">'\
                               '<accessPointList>wapname</accessPointList></u:GetAccessPointListResponse>'
        self.getAccPtListRtnXml='%s%s%s' % (self.xmlRtnHead, getAccPtListRtnBody, self.xmlRtnTail)

        self.accPtListRtn=OrderedDict([('accessPointList', 'wapname'),])

################################################################################
        self.getCfgTokenCmd='GetConfigurationToken'
        self.getCfgTokenArgs= [\
                        {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'out', 'name': 'configurationToken',\
                        'state' : {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_ConfigurationToken'}},]

        getCfgTokenRtnBody = '<u:GetConfigurationTokenResponse  xmlns:u="urn:schemas-denon-com:service:ACT:1">'\
                               '<configurationToken>caf7916a94db1</configurationToken></u:GetConfigurationTokenResponse>'
        self.getCfgTokenRtnXml = '%s%s%s' % (self.xmlRtnHead, getCfgTokenRtnBody, self.xmlRtnTail)

        self.getCfgTokenRtn=OrderedDict([('configurationToken', 'caf7916a94db1'),])

################################################################################
        self.setUpdateActCmnd='SetUpdateAction'

        self.setUpdateActArgs=[\
                    {'relatedStateVariable': 'UpdateAction', 'direction': 'in', 'name': 'UpdateAction',\
                    'state' : {'dataType': 'string',\
                                'defaultValue': 'UPDATE_ACTION_NONE',\
                                'name': 'UpdateAction',\
                                '@sendEvents': 'no',\
                                'allowedValueList': {'allowedValue': [\
                                    'UPDATE_ACTION_NONE',\
                                    'UPDATE_ACTION_TONIGHT',\
                                    'UPDATE_ACTION_REMIND',\
                                    'UPDATE_ACTION_SKIP']}}},]

        setUpdateActRtnBody = '<u:SetUpdateActionResponse  xmlns:u="urn:schemas-denon-com:service:ACT:1">'\
                               '</u:SetUpdateActionResponse>'
        self.setUpdateActRtnXml ='%s%s%s' % (self.xmlRtnHead, setUpdateActRtnBody, self.xmlRtnTail)

        self.setUpdateActRtn=OrderedDict()

################################################################################
        self.getNetCfgCmd='GetNetworkConfiguration'

        self.getNetCfgArgs=[\
                {'relatedStateVariable': 'ARG_NetworkConfigurationID', 'direction': 'in', 'name': 'networkConfigurationId',\
                'state': {'dataType': 'ui1', 'defaultValue': '1', \
                            'allowedValueRange': {'step': '1', 'minimum': '1', 'maximum': '255'},\
                            'name': 'ARG_NetworkConfigurationID', '@sendEvents': 'no'},},\
                {'relatedStateVariable': 'ARG_NetworkConfiguration', 'direction': 'out', 'name': 'networkConfiguration',\
                    'state': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_NetworkConfiguration'}}]

        getNetCfgRtnBody = '<u:GetNetworkConfigurationResponse  xmlns:u="urn:schemas-denon-com:service:ACT:1">'\
                               '<networkConfiguration>1</networkConfiguration></u:GetNetworkConfigurationResponse>'
        self.getNetCfgRtnXml ='%s%s%s' % (self.xmlRtnHead, getNetCfgRtnBody, self.xmlRtnTail)

        self.getNetCfgRtn=OrderedDict([('networkConfiguration', '1'),])

################################################################################
        self._cmndTbl={\
            'SetConfigurationStatus': [\
                {'relatedStateVariable': 'ConfigurationStatus', 'direction': 'in', 'name': 'configurationStatus'}],\
            'ReleaseConfigurationToken': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'}],\
            'GetP2PMode': [\
                {'relatedStateVariable': 'ARG_P2pMode', 'direction': 'out', 'name': 'P2PMode'}],\
            'SetSurroundSpeakerConfig': [\
                {'relatedStateVariable': 'SurroundSpeakerConfig', 'direction': 'in', 'name': 'SurroundSpeakerConfig'}],\
            'GetLEDConfig': [\
                {'relatedStateVariable': 'LEDConfig', 'direction': 'out', 'name': 'LEDConfig'}],\
            'GetConfigurationStatus': [\
                {'relatedStateVariable': 'ConfigurationStatus', 'direction': 'out', 'name': 'configurationStatus'}],\
            'GetSupportedLanguageList': [\
                {'relatedStateVariable': 'ARG_SupportedLanguages', 'direction': 'out', 'name': 'languageList'}],\
            'GetUpgradeStatus': [\
                {'relatedStateVariable': 'UpgradeStatus', 'direction': 'out', 'name': 'upgradeStatus'}],\
            'SetWPSPinSSID': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'},\
                {'relatedStateVariable': 'ARG_WPSPinSSID', 'direction': 'in', 'name': 'wpsPinSSID'}],\
            'GetSessionId': [\
                {'relatedStateVariable': 'SessionId', 'direction': 'out', 'name': 'sessionId'}],\
            'SetUpdateLevel': [\
                {'relatedStateVariable': 'UpdateLevel', 'direction': 'in', 'name': 'UpdateLevel'}],\
            'GetTimeZone': [\
                {'relatedStateVariable': 'TimeZone', 'direction': 'out', 'name': 'timeZone'},\
                {'relatedStateVariable': 'IANAName', 'direction': 'out', 'name': 'ianaName'}],\
            'SetDaylightSaving': [\
                {'relatedStateVariable': 'DaylightSaving', 'direction': 'in', 'name': 'daylightSaving'}],\
            'CancelChanges': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'}],\
            'GetDaylightSaving': [\
                {'relatedStateVariable': 'DaylightSaving', 'direction': 'out', 'name': 'daylightSaving'}],\
            'GetAccessPointList': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'},\
                {'relatedStateVariable': 'ARG_AccessPointList', 'direction': 'out', 'name': 'accessPointList'}],\
            'SetCurrentLanguage': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'},\
                {'relatedStateVariable': 'CurrentLanguageLocale', 'direction': 'in', 'name': 'languageLocale'}],\
            'ApplyChanges': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'}],\
            'DeleteNetworkShare': [\
                {'relatedStateVariable': 'id', 'direction': 'in', 'name': 'id'}],\
            'StartInvitation': [\
                {'relatedStateVariable': 'ARG_InvitationConfiguration', 'direction': 'in', 'name': 'InvitationConfiguration'}],\
            'GetSurroundSpeakerConfig': [\
                {'relatedStateVariable': 'SurroundSpeakerConfig', 'direction': 'out', 'name': 'SurroundSpeakerConfig'}],\
            'SetTranscode': [\
                {'relatedStateVariable': 'ARG_Transcode', 'direction': 'in', 'name': 'transcode'}],\
            'StartWifiAp': [\
                {'relatedStateVariable': 'ARG_WifiApConfiguration', 'direction': 'in', 'name': 'WifiApConfiguration'}],\
            'GetActiveInterface': [\
                {'relatedStateVariable': 'ARG_NetworkConfigurationID', 'direction': 'out', 'name': 'networkConfigurationId'}],\
            'SetFriendlyName': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'},\
                {'relatedStateVariable': 'ARG_FriendlyName', 'direction': 'in', 'name': 'friendlyName'}],\
            'GetTranscode': [\
                {'relatedStateVariable': 'ARG_Transcode', 'direction': 'out', 'name': 'transcode'}],\
            'SetVolumeLimit': [\
                {'relatedStateVariable': 'VolumeLimit', 'direction': 'in', 'name': 'VolumeLimit'}],\
            'ReMountNetworkShare': [\
                {'relatedStateVariable': 'id', 'direction': 'in', 'name': 'id'}],\
            'GetCurrentState': [\
                {'relatedStateVariable': 'LastChange', 'direction': 'out', 'name': 'CurrentState'}],\
            'SetNetworkConfiguration': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'},\
                {'relatedStateVariable': 'ARG_NetworkConfiguration', 'direction': 'in', 'name': 'networkConfiguration'}],\
            'GetConfigurationToken': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'out', 'name': 'configurationToken'}],\
            'CheckForFirmwareUpgrade': [],\
            'UpdateFirmware': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'}],\
            'GetCurrentLanguage': [\
                {'relatedStateVariable': 'CurrentLanguageLocale', 'direction': 'out', 'name': 'languageLocale'}],\
            'SetWirelessProfile': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'},\
                {'relatedStateVariable': 'CurrentWirelessProfile', 'direction': 'in', 'name': 'wirelessProfile'}],\
            'RegisterUser': [\
                {'relatedStateVariable': 'ARG_UserInfo', 'direction': 'in', 'name': 'userInfo'}],\
            'SetLEDConfig': [\
                {'relatedStateVariable': 'LEDConfig', 'direction': 'in', 'name': 'LEDConfig'}],\
            'GetBluetoothStatus': [\
                {'relatedStateVariable': 'BTConfig', 'direction': 'out', 'name': 'BTConfig'}],\
            'GetNetworkConfigurationList': [\
                {'relatedStateVariable': 'NetworkConfigurationList', 'direction': 'out', 'name': 'networkConfigurations'}],\
            'StopWifiAp': [\
                {'relatedStateVariable': 'ARG_WifiApConfiguration', 'direction': 'in', 'name': 'WifiApConfiguration'}],\
            'GetWirelessProfile': [\
                {'relatedStateVariable': 'CurrentWirelessProfile', 'direction': 'out', 'name': 'wirelessProfile'}],\
            'SetAudioConfig': [\
                {'relatedStateVariable': 'AudioConfig', 'direction': 'in', 'name': 'AudioConfig'}],\
            'AddNetworkShare': [\
                {'relatedStateVariable': 'name', 'direction': 'in', 'name': 'name'},\
                {'relatedStateVariable': 'path', 'direction': 'in', 'name': 'path'},\
                {'relatedStateVariable': 'user', 'direction': 'in', 'name': 'user'},\
                {'relatedStateVariable': 'pass', 'direction': 'in', 'name': 'pass'}],\
            'GetWirelessStatus': [\
                {'relatedStateVariable': 'wirelessStatus', 'direction': 'out', 'name': 'status'}],\
            'StopInvitation': [\
                {'relatedStateVariable': 'ARG_InvitationConfiguration', 'direction': 'in', 'name': 'InvitationConfiguration'}],\
            'GetAudioConfig': [\
                {'relatedStateVariable': 'AudioConfig', 'direction': 'out', 'name': 'AudioConfig'}],\
            'GetHEOSNetID': [\
                {'relatedStateVariable': 'ARG_HeosNetId', 'direction': 'out', 'name': 'HEOSNetID'}],\
            'SubmitDiagnostics': [\
                {'relatedStateVariable': 'ARG_UserName', 'direction': 'in', 'name': 'UserName'},\
                {'relatedStateVariable': 'ARG_LogId', 'direction': 'in', 'name': 'LogId'}],\
            'GetNetworkConfiguration': [\
                {'relatedStateVariable': 'ARG_NetworkConfigurationID', 'direction': 'in', 'name': 'networkConfigurationId'},\
                {'relatedStateVariable': 'ARG_NetworkConfiguration', 'direction': 'out', 'name': 'networkConfiguration'}],\
            'ReIndexNetworkShare': [\
                {'relatedStateVariable': 'id', 'direction': 'in', 'name': 'id'}],\
            'GetNetworkShares': [\
                {'relatedStateVariable': 'NetworkShareConfig', 'direction': 'out', 'name': 'NetworkShareConfig'}],\
            'GetFriendlyName': [\
                {'relatedStateVariable': 'ARG_FriendlyName', 'direction': 'out', 'name': 'friendlyName'}],\
            'SetBluetoothAction': [\
                {'relatedStateVariable': 'BTAction', 'direction': 'in', 'name': 'BTAction'},\
                {'relatedStateVariable': 'BTIndex', 'direction': 'in', 'name': 'BTIndex'}],\
            'GetUpdateAction': [\
                {'relatedStateVariable': 'UpdateAction', 'direction': 'out', 'name': 'UpdateAction'}],\
            'CancelFirmwareUpgrade': [],\
            'GetVolumeLimit': [\
                {'relatedStateVariable': 'VolumeLimit', 'direction': 'out', 'name': 'VolumeLimit'}],\
            'GetUpgradeProgress': [\
                {'relatedStateVariable': 'UpgradeProgress', 'direction': 'out', 'name': 'upgradeProgress'}],\
            'GetWirelessState': [\
                {'relatedStateVariable': 'WirelessState', 'direction': 'out', 'name': 'wirelessState'}],\
            'SetSessionId': [\
                {'relatedStateVariable': 'SessionId', 'direction': 'in', 'name': 'sessionId'}],\
            'GetUpdateLevel': [\
                {'relatedStateVariable': 'UpdateLevel', 'direction': 'out', 'name': 'UpdateLevel'}],\
            'SetTimeZone': [\
                {'relatedStateVariable': 'TimeZone', 'direction': 'in', 'name': 'timeZone'},\
                {'relatedStateVariable': 'IANAName', 'direction': 'in', 'name': 'ianaName'}],\
            'SetUpdateAction': [\
                {'relatedStateVariable': 'UpdateAction', 'direction': 'in', 'name': 'UpdateAction'}],\
            'SetHEOSNetID': [\
                {'relatedStateVariable': 'ARG_ConfigurationToken', 'direction': 'in', 'name': 'configurationToken'},\
                {'relatedStateVariable': 'ARG_HeosNetId', 'direction': 'in', 'name': 'HEOSNetID'}]}

        self._stateVarTbl = {\
            'pass': {'dataType': 'string', '@sendEvents': 'no', 'name': 'pass'},\
            'LEDConfig': {'dataType': 'string', '@sendEvents': 'no', 'name': 'LEDConfig'},\
            'SessionId': {'dataType': 'string', '@sendEvents': 'no', 'name': 'SessionId'},\
            'ARG_HeosNetId': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_HeosNetId'},\
            'ARG_SupportedLanguages': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_SupportedLanguages'},\
            'TimeZone':  {'dataType': 'string', 'defaultValue': '(GMT-12:00)', 'name': 'TimeZone', '@sendEvents': 'no',\
                'allowedValueList': {'allowedValue': [
                                        '(GMT-12:00)',\
                                        '(GMT-11:00)',\
                                        '(GMT-10:00)',\
                                        '(GMT-9:30)',\
                                        '(GMT-9:00)',\
                                        '(GMT-8:00)',\
                                        '(GMT-7:00)',\
                                        '(GMT-6:00)',\
                                        '(GMT-5:00)',\
                                        '(GMT-4:30)',\
                                        '(GMT-4:00)',\
                                        '(GMT-3:30)',\
                                        '(GMT-3:00)',\
                                        '(GMT-2:00)',\
                                        '(GMT-1:00)',\
                                        '(GMT)',\
                                        '(GMT+1:00)',\
                                        '(GMT+2:00)',\
                                        '(GMT+3:00)',\
                                        '(GMT+3:30)',\
                                        '(GMT+4:00)',\
                                        '(GMT+4:30)',\
                                        '(GMT+5:00)',\
                                        '(GMT+5:30)',\
                                        '(GMT+5:45)',\
                                        '(GMT+6:00)',\
                                        '(GMT+6:30)',\
                                        '(GMT+7:00)',\
                                        '(GMT+8:00)',\
                                        '(GMT+8:30)',\
                                        '(GMT+8:45)',\
                                        '(GMT+9:00)',\
                                        '(GMT+9:30)',\
                                        '(GMT+10:00)',\
                                        '(GMT+10:30)',\
                                        '(GMT+11:00)',\
                                        '(GMT+11:30)',\
                                        '(GMT+12:00)',\
                                        '(GMT+12:45)',\
                                        '(GMT+13:00)',\
                                        '(GMT+14:00)']}},\
            'id': {'dataType': 'string', '@sendEvents': 'no', 'name': 'id'},\
            'ARG_Transcode': {'dataType': 'boolean', 'defaultValue': '0', 'name': 'ARG_Transcode', '@sendEvents': 'no'},\
            'BTAction': {'dataType': 'string', 'defaultValue': 'NONE', 'name': 'BTAction', '@sendEvents': 'no',\
                    'allowedValueList': {'allowedValue': [ \
                                        'NONE',\
                                        'START_PAIRING',\
                                        'CANCEL_PAIRING',\
                                        'CONNECT',\
                                        'DISCONNECT',\
                                        'CLEAR_PAIRED_LIST']}},\
            'UpdateAction': {'dataType': 'string', 'defaultValue': 'UPDATE_ACTION_NONE', 'name': 'UpdateAction', '@sendEvents': 'no',\
                    'allowedValueList': {'allowedValue': [ \
                                        'UPDATE_ACTION_NONE',\
                                        'UPDATE_ACTION_TONIGHT',\
                                        'UPDATE_ACTION_REMIND',\
                                        'UPDATE_ACTION_SKIP']}},\
            'CurrentWirelessProfile': {'dataType': 'string', '@sendEvents': 'no', 'name': 'CurrentWirelessProfile'},\
            'ARG_LastDiscoveredDevice': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_LastDiscoveredDevice'},\
            'ARG_AccessPointList': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_AccessPointList'},\
            'ARG_NetworkConfiguration': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_NetworkConfiguration'},\
            'wirelessStatus': {'dataType': 'string', '@sendEvents': 'no', 'name': 'wirelessStatus'},\
            'ARG_WPSPinSSID': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_WPSPinSSID'},\
            'UpdateLevel': {'dataType': 'ui4', 'defaultValue': '3', 'name': 'UpdateLevel', '@sendEvents': 'no'},\
            'ARG_LogId': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_LogId'},\
            'CurrentLanguageLocale': {'dataType': 'string', 'defaultValue': 'en_US', 'name': 'CurrentLanguageLocale', '@sendEvents': 'no',\
                    'allowedValueList': {'allowedValue': [\
                                         'en_US',\
                                         'ar_SA',\
                                         'pt_BR',\
                                         'fr_CA',\
                                         'cs_CZ',\
                                         'da_DK',\
                                         'de_DE',\
                                         'es_ES',\
                                         'fa_IR',\
                                         'fi_FI',\
                                         'fr_FR',\
                                         'el_GR',\
                                         'iw_IL',\
                                         'hu_HU',\
                                         'id_ID',\
                                         'it_IT',\
                                         'ja_JP',\
                                         'ko_KR',\
                                         'es_AR',\
                                         'nl_NL',\
                                         'no_NO',\
                                         'pl_PL',\
                                         'pt_PT',\
                                         'ro_RO',\
                                         'ru_RU',\
                                         'zh_CN',\
                                         'sv_SE',\
                                         'zh_TW',\
                                         'tr_TR',\
                                         'vi_VN',\
                                         'th_TH']}},\
            'ARG_FriendlyName': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_FriendlyName'},\
            'ARG_ConfigurationToken': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_ConfigurationToken'},\
            'NetworkConfigurationList': {'dataType': 'string', '@sendEvents': 'no', 'name': 'NetworkConfigurationList'},\
            'NetworkShareConfig': {'dataType': 'string', '@sendEvents': 'no', 'name': 'NetworkShareConfig'},\
            'IANAName': {'dataType': 'string', '@sendEvents': 'no', 'name': 'IANAName'},\
            'ARG_P2pMode': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_P2pMode'},\
            'WirelessState': {'dataType': 'string', '@sendEvents': 'no', 'name': 'WirelessState'},\
            'ConfigurationStatus': {'dataType': 'ui4', 'defaultValue': '0', 'name': 'ConfigurationStatus', '@sendEvents': 'no'},\
            'BTConfig': {'dataType': 'string', '@sendEvents': 'no', 'name': 'BTConfig'},\
            'path': {'dataType': 'string', '@sendEvents': 'no', 'name': 'path'},\
            'ARG_NetworkConfigurationID': {'dataType': 'ui1', 'defaultValue': '1', \
                            'allowedValueRange': {'step': '1', 'minimum': '1', 'maximum': '255'},\
                            'name': 'ARG_NetworkConfigurationID', '@sendEvents': 'no'},\
            'VolumeLimit': {'dataType': 'ui1', 'defaultValue': '100', 'name': 'VolumeLimit', '@sendEvents': 'no'},\
            'name': {'dataType': 'string', '@sendEvents': 'no', 'name': 'name'},\
            'SurroundSpeakerConfig': {'dataType': 'string', '@sendEvents': 'no', 'name': 'SurroundSpeakerConfig'},\
            'BTIndex': {'dataType': 'ui4', 'defaultValue': '0', 'name': 'BTIndex', '@sendEvents': 'no'},\
            'ARG_InvitationConfiguration': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_InvitationConfiguration'},\
            'UpgradeProgress': {'dataType': 'ui1', 'defaultValue': '0', 'name': 'UpgradeProgress', '@sendEvents': 'no'},\
            'ARG_UserInfo': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_UserInfo'},\
            'UpgradeStatus': {'dataType': 'string', '@sendEvents': 'no', 'name': 'UpgradeStatus'},\
            'LastChange': {'dataType': 'string', '@sendEvents': 'yes', 'name': 'LastChange'},\
            'ARG_WifiApConfiguration': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_WifiApConfiguration'},\
            'AudioConfig': {'dataType': 'string', '@sendEvents': 'no', 'name': 'AudioConfig'},\
            'DaylightSaving': {'dataType': 'boolean', 'defaultValue': '0', 'name': 'DaylightSaving', '@sendEvents': 'no'},\
            'ARG_UserName': {'dataType': 'string', '@sendEvents': 'no', 'name': 'ARG_UserName'},\
            'user': {'dataType': 'string', '@sendEvents': 'no', 'name': 'user'}}

        self.xmlDict = {'scpd': {'actionList': {'action': [\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'name',\
                  'direction': 'in',\
                  'name': 'name'},\
                 {'relatedStateVariable': 'path',\
                  'direction': 'in',\
                  'name': 'path'},\
                 {'relatedStateVariable': 'user',\
                  'direction': 'in',\
                  'name': 'user'},\
                 {'relatedStateVariable': 'pass',\
                  'direction': 'in',\
                  'name': 'pass'}]},\
              'name': 'AddNetworkShare'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'}},\
              'name': 'ApplyChanges'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'}},\
              'name': 'CancelChanges'},\
             {'name': 'CancelFirmwareUpgrade'},\
             {'name': 'CheckForFirmwareUpgrade'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'id',\
                  'direction': 'in',\
                  'name': 'id'}},\
              'name': 'DeleteNetworkShare'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'},\
                 {'relatedStateVariable': 'ARG_AccessPointList',\
                  'direction': 'out',\
                  'name': 'accessPointList'}]},\
              'name': 'GetAccessPointList'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_NetworkConfigurationID',\
                  'direction': 'out',\
                  'name': 'networkConfigurationId'}},\
              'name': 'GetActiveInterface'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'AudioConfig',\
                  'direction': 'out',\
                  'name': 'AudioConfig'}},\
              'name': 'GetAudioConfig'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'BTConfig',\
                  'direction': 'out',\
                  'name': 'BTConfig'}},\
              'name': 'GetBluetoothStatus'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ConfigurationStatus',\
                  'direction': 'out',\
                  'name': 'configurationStatus'}},\
              'name': 'GetConfigurationStatus'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'out',\
                  'name': 'configurationToken'}},\
              'name': 'GetConfigurationToken'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'CurrentLanguageLocale',\
                  'direction': 'out',\
                  'name': 'languageLocale'}},\
              'name': 'GetCurrentLanguage'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'LastChange',\
                  'direction': 'out',\
                  'name': 'CurrentState'}},\
              'name': 'GetCurrentState'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'DaylightSaving',\
                  'direction': 'out',\
                  'name': 'daylightSaving'}},\
              'name': 'GetDaylightSaving'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_FriendlyName',\
                  'direction': 'out',\
                  'name': 'friendlyName'}},\
              'name': 'GetFriendlyName'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_HeosNetId',\
                  'direction': 'out',\
                  'name': 'HEOSNetID'}},\
              'name': 'GetHEOSNetID'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'LEDConfig',\
                  'direction': 'out',\
                  'name': 'LEDConfig'}},\
              'name': 'GetLEDConfig'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_NetworkConfigurationID',\
                  'direction': 'in',\
                  'name': 'networkConfigurationId'},\
                 {'relatedStateVariable': 'ARG_NetworkConfiguration',\
                  'direction': 'out',\
                  'name': 'networkConfiguration'}]},\
              'name': 'GetNetworkConfiguration'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'NetworkConfigurationList',\
                  'direction': 'out',\
                  'name': 'networkConfigurations'}},\
              'name': 'GetNetworkConfigurationList'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'NetworkShareConfig',\
                  'direction': 'out',\
                  'name': 'NetworkShareConfig'}},\
              'name': 'GetNetworkShares'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_P2pMode',\
                  'direction': 'out',\
                  'name': 'P2PMode'}},\
              'name': 'GetP2PMode'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'SessionId',\
                  'direction': 'out',\
                  'name': 'sessionId'}},\
              'name': 'GetSessionId'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_SupportedLanguages',\
                  'direction': 'out',\
                  'name': 'languageList'}},\
              'name': 'GetSupportedLanguageList'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'SurroundSpeakerConfig',\
                  'direction': 'out',\
                  'name': 'SurroundSpeakerConfig'}},\
              'name': 'GetSurroundSpeakerConfig'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'TimeZone',\
                  'direction': 'out',\
                  'name': 'timeZone'},\
                 {'relatedStateVariable': 'IANAName',\
                  'direction': 'out',\
                  'name': 'ianaName'}]},\
              'name': 'GetTimeZone'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_Transcode',\
                  'direction': 'out',\
                  'name': 'transcode'}},\
              'name': 'GetTranscode'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'UpdateAction',\
                  'direction': 'out',\
                  'name': 'UpdateAction'}},\
              'name': 'GetUpdateAction'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'UpdateLevel',\
                  'direction': 'out',\
                  'name': 'UpdateLevel'}},\
              'name': 'GetUpdateLevel'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'UpgradeProgress',\
                  'direction': 'out',\
                  'name': 'upgradeProgress'}},\
              'name': 'GetUpgradeProgress'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'UpgradeStatus',\
                  'direction': 'out',\
                  'name': 'upgradeStatus'}},\
              'name': 'GetUpgradeStatus'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'VolumeLimit',\
                  'direction': 'out',\
                  'name': 'VolumeLimit'}},\
              'name': 'GetVolumeLimit'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'CurrentWirelessProfile',\
                  'direction': 'out',\
                  'name': 'wirelessProfile'}},\
              'name': 'GetWirelessProfile'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'WirelessState',\
                  'direction': 'out',\
                  'name': 'wirelessState'}},\
              'name': 'GetWirelessState'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'wirelessStatus',\
                  'direction': 'out',\
                  'name': 'status'}},\
              'name': 'GetWirelessStatus'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'id',\
                  'direction': 'in',\
                  'name': 'id'}},\
              'name': 'ReIndexNetworkShare'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'id',\
                  'direction': 'in',\
                  'name': 'id'}},\
              'name': 'ReMountNetworkShare'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_UserInfo',\
                  'direction': 'in',\
                  'name': 'userInfo'}},\
              'name': 'RegisterUser'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'}},\
              'name': 'ReleaseConfigurationToken'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'AudioConfig',\
                  'direction': 'in',\
                  'name': 'AudioConfig'}},\
              'name': 'SetAudioConfig'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'BTAction',\
                  'direction': 'in',\
                  'name': 'BTAction'},\
                 {'relatedStateVariable': 'BTIndex',\
                  'direction': 'in',\
                  'name': 'BTIndex'}]},\
              'name': 'SetBluetoothAction'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ConfigurationStatus',\
                  'direction': 'in',\
                  'name': 'configurationStatus'}},\
              'name': 'SetConfigurationStatus'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'},\
                 {'relatedStateVariable': 'CurrentLanguageLocale',\
                  'direction': 'in',\
                  'name': 'languageLocale'}]},\
              'name': 'SetCurrentLanguage'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'DaylightSaving',\
                  'direction': 'in',\
                  'name': 'daylightSaving'}},\
              'name': 'SetDaylightSaving'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'},\
                 {'relatedStateVariable': 'ARG_FriendlyName',\
                  'direction': 'in',\
                  'name': 'friendlyName'}]},\
              'name': 'SetFriendlyName'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'},\
                 {'relatedStateVariable': 'ARG_HeosNetId',\
                  'direction': 'in',\
                  'name': 'HEOSNetID'}]},\
              'name': 'SetHEOSNetID'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'LEDConfig',\
                  'direction': 'in',\
                  'name': 'LEDConfig'}},\
              'name': 'SetLEDConfig'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'},\
                 {'relatedStateVariable': 'ARG_NetworkConfiguration',\
                  'direction': 'in',\
                  'name': 'networkConfiguration'}]},\
              'name': 'SetNetworkConfiguration'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'SessionId',\
                  'direction': 'in',\
                  'name': 'sessionId'}},\
              'name': 'SetSessionId'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'SurroundSpeakerConfig',\
                  'direction': 'in',\
                  'name': 'SurroundSpeakerConfig'}},\
              'name': 'SetSurroundSpeakerConfig'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'TimeZone',\
                  'direction': 'in',\
                  'name': 'timeZone'},\
                 {'relatedStateVariable': 'IANAName',\
                  'direction': 'in',\
                  'name': 'ianaName'}]},\
              'name': 'SetTimeZone'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_Transcode',\
                  'direction': 'in',\
                  'name': 'transcode'}},\
              'name': 'SetTranscode'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'UpdateAction',\
                  'direction': 'in',\
                  'name': 'UpdateAction'}},\
              'name': 'SetUpdateAction'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'UpdateLevel',\
                  'direction': 'in',\
                  'name': 'UpdateLevel'}},\
              'name': 'SetUpdateLevel'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'VolumeLimit',\
                  'direction': 'in',\
                  'name': 'VolumeLimit'}},\
              'name': 'SetVolumeLimit'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'},\
                 {'relatedStateVariable': 'ARG_WPSPinSSID',\
                  'direction': 'in',\
                  'name': 'wpsPinSSID'}]},\
              'name': 'SetWPSPinSSID'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'},\
                 {'relatedStateVariable': 'CurrentWirelessProfile',\
                  'direction': 'in',\
                  'name': 'wirelessProfile'}]},\
              'name': 'SetWirelessProfile'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_InvitationConfiguration',\
                  'direction': 'in',\
                  'name': 'InvitationConfiguration'}},\
              'name': 'StartInvitation'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_WifiApConfiguration',\
                  'direction': 'in',\
                  'name': 'WifiApConfiguration'}},\
              'name': 'StartWifiAp'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_InvitationConfiguration',\
                  'direction': 'in',\
                  'name': 'InvitationConfiguration'}},\
              'name': 'StopInvitation'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_WifiApConfiguration',\
                  'direction': 'in',\
                  'name': 'WifiApConfiguration'}},\
              'name': 'StopWifiAp'},\
             {'argumentList': {'argument': [\
                 {'relatedStateVariable': 'ARG_UserName',\
                  'direction': 'in',\
                  'name': 'UserName'},\
                 {'relatedStateVariable': 'ARG_LogId',\
                  'direction': 'in',\
                  'name': 'LogId'}]},\
              'name': 'SubmitDiagnostics'},\
             {'argumentList': {'argument':\
                 {'relatedStateVariable': 'ARG_ConfigurationToken',\
                  'direction': 'in',\
                  'name': 'configurationToken'}},\
              'name': 'UpdateFirmware'}]},\
                  'serviceStateTable': {'stateVariable': [\
                 {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_AccessPointList'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_ConfigurationToken'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_FriendlyName'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_HeosNetId'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_InvitationConfiguration'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_LastDiscoveredDevice'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_LogId'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_NetworkConfiguration'},\
             {'dataType': 'ui1',\
                  'defaultValue': '1',\
                  'allowedValueRange': \
                      {'step': '1',\
                       'minimum': '1',\
                       'maximum': '255'},\
                       'name': 'ARG_NetworkConfigurationID',\
                       '@sendEvents': 'no'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_P2pMode'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_SupportedLanguages'},\
             {'dataType': 'boolean',\
                  'defaultValue': '0',\
                  'name': 'ARG_Transcode',\
                  '@sendEvents': 'no'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_UserInfo'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_UserName'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_WPSPinSSID'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'ARG_WifiApConfiguration'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'AudioConfig'},\
             {'dataType': 'string',\
                  'defaultValue': 'NONE',\
                  'name': 'BTAction',\
                  '@sendEvents': 'no',\
                  'allowedValueList': {'allowedValue': [\
                       'NONE',\
                       'START_PAIRING',\
                       'CANCEL_PAIRING',\
                       'CONNECT',\
                       'DISCONNECT',\
                       'CLEAR_PAIRED_LIST']}},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'BTConfig'},\
             {'dataType': 'ui4',\
                  'defaultValue': '0',\
                  'name': 'BTIndex',\
                  '@sendEvents': 'no'},\
             {'dataType': 'ui4',\
                  'defaultValue': '0',\
                  'name': 'ConfigurationStatus',\
                  '@sendEvents': 'no'},\
             {'dataType': 'string',\
                  'defaultValue': 'en_US',\
                  'name': 'CurrentLanguageLocale',\
                  '@sendEvents': 'no',\
                  'allowedValueList': {'allowedValue': [\
                       'en_US',\
                       'ar_SA',\
                       'pt_BR',\
                       'fr_CA',\
                       'cs_CZ',\
                       'da_DK',\
                       'de_DE',\
                       'es_ES',\
                       'fa_IR',\
                       'fi_FI',\
                       'fr_FR',\
                       'el_GR',\
                       'iw_IL',\
                       'hu_HU',\
                       'id_ID',\
                       'it_IT',\
                       'ja_JP',\
                       'ko_KR',\
                       'es_AR',\
                       'nl_NL',\
                       'no_NO',\
                       'pl_PL',\
                       'pt_PT',\
                       'ro_RO',\
                       'ru_RU',\
                       'zh_CN',\
                       'sv_SE',\
                       'zh_TW',\
                       'tr_TR',\
                       'vi_VN',\
                       'th_TH']}},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'CurrentWirelessProfile'},\
             {'dataType': 'boolean',\
                  'defaultValue': '0',\
                  'name': 'DaylightSaving',\
                  '@sendEvents': 'no'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'IANAName'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'LEDConfig'},\
             {'dataType': 'string',\
                  '@sendEvents': 'yes',\
                  'name': 'LastChange'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'NetworkConfigurationList'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'NetworkShareConfig'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'SessionId'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'SurroundSpeakerConfig'},\
             {'dataType': 'string',\
                  'defaultValue': '(GMT-12:00)',\
                  'name': 'TimeZone',\
                  '@sendEvents': 'no',\
                  'allowedValueList': {'allowedValue': [\
                       '(GMT-12:00)',\
                       '(GMT-11:00)',\
                       '(GMT-10:00)',\
                       '(GMT-9:30)',\
                       '(GMT-9:00)',\
                       '(GMT-8:00)',\
                       '(GMT-7:00)',\
                       '(GMT-6:00)',\
                       '(GMT-5:00)',\
                       '(GMT-4:30)',\
                       '(GMT-4:00)',\
                       '(GMT-3:30)',\
                       '(GMT-3:00)',\
                       '(GMT-2:00)',\
                       '(GMT-1:00)',\
                       '(GMT)',\
                       '(GMT+1:00)',\
                       '(GMT+2:00)',\
                       '(GMT+3:00)',\
                       '(GMT+3:30)',\
                       '(GMT+4:00)',\
                       '(GMT+4:30)',\
                       '(GMT+5:00)',\
                       '(GMT+5:30)',\
                       '(GMT+5:45)',\
                       '(GMT+6:00)',\
                       '(GMT+6:30)',\
                       '(GMT+7:00)',\
                       '(GMT+8:00)',\
                       '(GMT+8:30)',\
                       '(GMT+8:45)',\
                       '(GMT+9:00)',\
                       '(GMT+9:30)',\
                       '(GMT+10:00)',\
                       '(GMT+10:30)',\
                       '(GMT+11:00)',\
                       '(GMT+11:30)',\
                       '(GMT+12:00)',\
                       '(GMT+12:45)',\
                       '(GMT+13:00)',\
                       '(GMT+14:00)']}},\
             {'dataType': 'string',\
                  'defaultValue': 'UPDATE_ACTION_NONE',\
                  'name': 'UpdateAction',\
                  '@sendEvents': 'no',\
                  'allowedValueList': {'allowedValue': [\
                       'UPDATE_ACTION_NONE',\
                       'UPDATE_ACTION_TONIGHT',\
                       'UPDATE_ACTION_REMIND',\
                       'UPDATE_ACTION_SKIP']}},\
             {'dataType': 'ui4',\
                  'defaultValue': '3',\
                  'name': 'UpdateLevel',\
                  '@sendEvents': 'no'},\
             {'dataType': 'ui1',\
                  'defaultValue': '0',\
                  'name': 'UpgradeProgress',\
                  '@sendEvents': 'no'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'UpgradeStatus'},\
             {'dataType': 'ui1',\
                  'defaultValue': '100',\
                  'name': 'VolumeLimit',\
                  '@sendEvents': 'no'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'WirelessState'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'id'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'name'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'pass'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'path'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'user'},\
             {'dataType': 'string',\
                  '@sendEvents': 'no',\
                  'name': 'wirelessStatus'}]},\
                  'specVersion': {'major': '1',\
                  'minor': '0'}}}

        return

    @property
    def getCurrStRtn(self):
        currStTxt='<Event xmlns="urn:schemas-upnp-org:metadata-1-0/ACT/">'\
                '<ActiveInterface val="1"/>'\
                '<FriendlyName val="Kitchen"/>'\
                '<HEOSNetId val="DEFAULT-SSID-8e09dfb09df4FBfa996"/>'\
                '<LastDiscoveredDevice val=""/>'\
                '<P2PMode val="NONE"/>'\
                '<Transcode val="1"/>'\
                '<AudioConfig val="'\
                '&lt;AudioConfig&gt;'\
                '&lt;highpass&gt;0'\
                '&lt;/highpass&gt;'\
                '&lt;lowpass&gt;80'\
                '&lt;/lowpass&gt;'\
                '&lt;subwooferEnable&gt;0'\
                '&lt;/subwooferEnable&gt;'\
                '&lt;outputMode&gt;STEREO'\
                '&lt;/outputMode&gt;'\
                '&lt;ampBridged&gt;0'\
                '&lt;/ampBridged&gt;'\
                '&lt;soundMode&gt;STEREO'\
                '&lt;/soundMode&gt;'\
                '&lt;impedance&gt;'\
                '&lt;/impedance&gt;'\
                '&lt;ampPower&gt;1'\
                '&lt;/ampPower&gt;'\
                '&lt;availableSoundModes&gt;MOVIE_NORMAL,MUSIC_NORMAL'\
                '&lt;/availableSoundModes&gt;'\
                '&lt;sourceDirect&gt;0'\
                '&lt;/sourceDirect&gt;'\
                '&lt;bassBoost&gt;0'\
                '&lt;/bassBoost&gt;'\
                '&lt;speakerOption&gt;'\
                '&lt;/speakerOption&gt;'\
                '&lt;/AudioConfig&gt;"/>'\
                '<BTConfig val="'\
                '&lt;BluetoothStatus&gt;'\
                '&lt;connectedStatus&gt;DISCONNECTED'\
                '&lt;/connectedStatus&gt;'\
                '&lt;connectedDevice&gt;'\
                '&lt;/connectedDevice&gt;'\
                '&lt;pairedDevices&gt;'\
                '&lt;/pairedDevices&gt;'\
                '&lt;hasPairedDevices&gt;0'\
                '&lt;/hasPairedDevices&gt;'\
                '&lt;/BluetoothStatus&gt;"/>'\
                '<ConfigurationStatus val="0"/>'\
                '<UpgradeComponentInstallProgress val="0"/>'\
                '<CurrentLanguageLocale val="en_US"/>'\
                '<CurrentWirelessProfile val="'\
                '&lt;wirelessProfile SSID=&quot;DEFAULT-SSID-8e09dfb09df4FBfa996&quot;&gt;'\
                '&lt;wirelessSecurity enabled=&quot;true&quot;&gt;'\
                '&lt;Mode passPhrase=&quot;DEFAULT-PWD-c4E10186eDA2cbfAEB73454E52C09eDFCBEAC50a2fde2460Dd41&quot;&gt;WPA2-AES'\
                '&lt;/Mode&gt;'\
                '&lt;/wirelessSecurity&gt;'\
                '&lt;/wirelessProfile&gt;"/>'\
                '<DaylightSaving val="0"/>'\
                '<IANAName val=""/>'\
                '<LEDConfig val="'\
                '&lt;LEDConfig&gt;'\
                '&lt;led&gt;'\
                '&lt;name&gt;MODE'\
                '&lt;/name&gt;'\
                '&lt;brightness&gt;100'\
                '&lt;/brightness&gt;'\
                '&lt;/led&gt;'\
                '&lt;led&gt;'\
                '&lt;name&gt;NETWORK'\
                '&lt;/name&gt;'\
                '&lt;brightness&gt;100'\
                '&lt;/brightness&gt;'\
                '&lt;/led&gt;'\
                '&lt;led&gt;'\
                '&lt;name&gt;MUTED'\
                '&lt;/name&gt;'\
                '&lt;brightness&gt;100'\
                '&lt;/brightness&gt;'\
                '&lt;/led&gt;'\
                '&lt;led&gt;'\
                '&lt;name&gt;REAR_STATUS'\
                '&lt;/name&gt;'\
                '&lt;brightness&gt;100'\
                '&lt;/brightness&gt;'\
                '&lt;/led&gt;'\
                '&lt;/LEDConfig&gt;"/>'\
                '<NetworkConfigurationList val="'\
                '&lt;listNetworkConfigurations&gt;'\
                '&lt;networkConfiguration id=&quot;1&quot; dhcpOn=&quot;0&quot; enabled=&quot;true&quot;&gt;'\
                '&lt;Name&gt;eth0'\
                '&lt;/Name&gt;'\
                '&lt;Type&gt;LAN'\
                '&lt;/Type&gt;'\
                '&lt;IP&gt;10.42.12.12'\
                '&lt;/IP&gt;'\
                '&lt;Netmask&gt;255.255.255.0'\
                '&lt;/Netmask&gt;'\
                '&lt;Gateway&gt;10.42.12.1'\
                '&lt;/Gateway&gt;'\
                '&lt;DNS1&gt;10.42.12.1'\
                '&lt;/DNS1&gt;'\
                '&lt;DNS2&gt;0.0.0.0'\
                '&lt;/DNS2&gt;'\
                '&lt;DNS3&gt;0.0.0.0'\
                '&lt;/DNS3&gt;'\
                '&lt;gwMac&gt;000000000000'\
                '&lt;/gwMac&gt;'\
                '&lt;/networkConfiguration&gt;'\
                '&lt;networkConfiguration id=&quot;2&quot; dhcpOn=&quot;1&quot; enabled=&quot;true&quot;&gt;'\
                '&lt;Name&gt;wlan0'\
                '&lt;/Name&gt;'\
                '&lt;Type&gt;WLAN'\
                '&lt;/Type&gt;'\
                '&lt;IP&gt;0.0.0.0'\
                '&lt;/IP&gt;'\
                '&lt;Netmask&gt;0.0.0.0'\
                '&lt;/Netmask&gt;'\
                '&lt;Gateway&gt;0.0.0.0'\
                '&lt;/Gateway&gt;'\
                '&lt;DNS1&gt;0.0.0.0'\
                '&lt;/DNS1&gt;'\
                '&lt;DNS2&gt;0.0.0.0'\
                '&lt;/DNS2&gt;'\
                '&lt;DNS3&gt;0.0.0.0'\
                '&lt;/DNS3&gt;'\
                '&lt;gwMac&gt;'\
                '&lt;/gwMac&gt;'\
                '&lt;wirelessProfile SSID=&quot;DEFAULT-SSID-8e09dfb09df4FBfa996&quot;&gt;'\
                '&lt;wirelessSecurity enabled=&quot;true&quot;&gt;'\
                '&lt;Mode passPhrase=&quot;DEFAULT-PWD-c4E10186eDA2cbfAEB73454E52C09eDFCBEAC50a2fde2460Dd41&quot;&gt;WPA2-AES'\
                '&lt;/Mode&gt;'\
                '&lt;/wirelessSecurity&gt;'\
                '&lt;/wirelessProfile&gt;'\
                '&lt;/networkConfiguration&gt;'\
                '&lt;/listNetworkConfigurations&gt;"/>'\
                '<NetworkShareConfig val="&lt;NetworkShareConfig&gt;&lt;/NetworkShareConfig&gt;"/>'\
                '<SessionId val=""/>'\
                '<SurroundSpeakerConfig val="'\
                '&lt;SurroundSpeakerConfig&gt;'\
                '&lt;Front&gt;'\
                '&lt;enabled&gt;1'\
                '&lt;/enabled&gt;'\
                '&lt;crossover&gt;0'\
                '&lt;/crossover&gt;'\
                '&lt;Right&gt;'\
                '&lt;distance&gt;12'\
                '&lt;/distance&gt;'\
                '&lt;level&gt;12'\
                '&lt;/level&gt;'\
                '&lt;test_tone&gt;0'\
                '&lt;/test_tone&gt;'\
                '&lt;/Right&gt;'\
                '&lt;Left&gt;'\
                '&lt;distance&gt;12'\
                '&lt;/distance&gt;'\
                '&lt;level&gt;12'\
                '&lt;/level&gt;'\
                '&lt;test_tone&gt;0'\
                '&lt;/test_tone&gt;'\
                '&lt;/Left&gt;'\
                '&lt;/Front&gt;'\
                '&lt;Center&gt;'\
                '&lt;enabled&gt;0'\
                '&lt;/enabled&gt;'\
                '&lt;crossover&gt;0'\
                '&lt;/crossover&gt;'\
                '&lt;Center&gt;'\
                '&lt;distance&gt;12'\
                '&lt;/distance&gt;'\
                '&lt;level&gt;12'\
                '&lt;/level&gt;'\
                '&lt;test_tone&gt;0'\
                '&lt;/test_tone&gt;'\
                '&lt;/Center&gt;'\
                '&lt;/Center&gt;'\
                '&lt;Subwoofer&gt;'\
                '&lt;enabled&gt;0'\
                '&lt;/enabled&gt;'\
                '&lt;lowpass&gt;250'\
                '&lt;/lowpass&gt;'\
                '&lt;phase&gt;0'\
                '&lt;/phase&gt;'\
                '&lt;Subwoofer&gt;'\
                '&lt;distance&gt;12'\
                '&lt;/distance&gt;'\
                '&lt;level&gt;12'\
                '&lt;/level&gt;'\
                '&lt;test_tone&gt;0'\
                '&lt;/test_tone&gt;'\
                '&lt;/Subwoofer&gt;'\
                '&lt;/Subwoofer&gt;'\
                '&lt;Rear&gt;'\
                '&lt;enabled&gt;0'\
                '&lt;/enabled&gt;'\
                '&lt;crossover&gt;0'\
                '&lt;/crossover&gt;'\
                '&lt;surround_mode&gt;OFF'\
                '&lt;/surround_mode&gt;'\
                '&lt;Right&gt;'\
                '&lt;distance&gt;10'\
                '&lt;/distance&gt;'\
                '&lt;level&gt;12'\
                '&lt;/level&gt;'\
                '&lt;test_tone&gt;0'\
                '&lt;/test_tone&gt;'\
                '&lt;/Right&gt;'\
                '&lt;Left&gt;'\
                '&lt;distance&gt;10'\
                '&lt;/distance&gt;'\
                '&lt;level&gt;12'\
                '&lt;/level&gt;'\
                '&lt;test_tone&gt;0'\
                '&lt;/test_tone&gt;'\
                '&lt;/Left&gt;'\
                '&lt;/Rear&gt;'\
                '&lt;DistUnit&gt;m'\
                '&lt;/DistUnit&gt;'\
                '&lt;/SurroundSpeakerConfig&gt;"/>'\
                '<TimeZone val="(GMT-8:00)"/>'\
                '<UpdateAction val="UPDATE_ACTION_NONE"/>'\
                '<UpdateLevel val="0"/>'\
                '<UpgradeProgress val="0"/>'\
                '<UpgradeStatus val="UPGRADE_CURRENT"/>'\
                '<VolumeLimit val="100"/>'\
                '<WifiApSsid val=""/>'\
                '<WirelessState val="LINK_DOWN"/>'\
                '</Event>'\

        return OrderedDict([('CurrentState', currStTxt)])

    @property
    def getCurrStRtnBody(self):

        rtn = '&lt;Event xmlns=&quot;urn:schemas-upnp-org:metadata-1-0/ACT/&quot;&gt;&lt;ActiveInterface val=&quot;1&quot;/&gt;'\
                '&lt;FriendlyName val=&quot;Kitchen&quot;/&gt;'\
                '&lt;HEOSNetId val=&quot;DEFAULT-SSID-8e09dfb09df4FBfa996&quot;/&gt;'\
                '&lt;LastDiscoveredDevice val=&quot;&quot;/&gt;'\
                '&lt;P2PMode val=&quot;NONE&quot;/&gt;'\
                '&lt;Transcode val=&quot;1&quot;/&gt;'\
                '&lt;AudioConfig val=&quot;&amp;lt;AudioConfig&amp;gt;'\
                '&amp;lt;highpass&amp;gt;0&amp;lt;/highpass&amp;gt;'\
                '&amp;lt;lowpass&amp;gt;80&amp;lt;/lowpass&amp;gt;'\
                '&amp;lt;subwooferEnable&amp;gt;0&amp;lt;/subwooferEnable&amp;gt;'\
                '&amp;lt;outputMode&amp;gt;STEREO&amp;lt;/outputMode&amp;gt;'\
                '&amp;lt;ampBridged&amp;gt;0&amp;lt;/ampBridged&amp;gt;'\
                '&amp;lt;soundMode&amp;gt;STEREO&amp;lt;/soundMode&amp;gt;'\
                '&amp;lt;impedance&amp;gt;'\
                '&amp;lt;/impedance&amp;gt;'\
                '&amp;lt;ampPower&amp;gt;1&amp;lt;/ampPower&amp;gt;'\
                '&amp;lt;availableSoundModes&amp;gt;MOVIE_NORMAL,MUSIC_NORMAL&amp;lt;/availableSoundModes&amp;gt;'\
                '&amp;lt;sourceDirect&amp;gt;0&amp;lt;/sourceDirect&amp;gt;'\
                '&amp;lt;bassBoost&amp;gt;0&amp;lt;/bassBoost&amp;gt;'\
                '&amp;lt;speakerOption&amp;gt;'\
                '&amp;lt;/speakerOption&amp;gt;'\
                '&amp;lt;/AudioConfig&amp;gt;'\
                '&quot;/&gt;&lt;BTConfig val=&quot;&amp;lt;BluetoothStatus&amp;gt;'\
                '&amp;lt;connectedStatus&amp;gt;DISCONNECTED&amp;lt;/connectedStatus&amp;gt;'\
                '&amp;lt;connectedDevice&amp;gt;'\
                '&amp;lt;/connectedDevice&amp;gt;'\
                '&amp;lt;pairedDevices&amp;gt;'\
                '&amp;lt;/pairedDevices&amp;gt;'\
                '&amp;lt;hasPairedDevices&amp;gt;0&amp;lt;/hasPairedDevices&amp;gt;'\
                '&amp;lt;/BluetoothStatus&amp;gt;&quot;/&gt;'\
                '&lt;ConfigurationStatus val=&quot;0&quot;/&gt;'\
                '&lt;UpgradeComponentInstallProgress val=&quot;0&quot;/&gt;'\
                '&lt;CurrentLanguageLocale val=&quot;en_US&quot;/&gt;'\
                '&lt;CurrentWirelessProfile val=&quot;&amp;lt;wirelessProfile SSID=&amp;quot;DEFAULT-SSID-8e09dfb09df4FBfa996&amp;quot;&amp;gt;'\
                '&amp;lt;wirelessSecurity enabled=&amp;quot;true&amp;quot;&amp;gt;'\
                '&amp;lt;Mode passPhrase=&amp;quot;DEFAULT-PWD-c4E10186eDA2cbfAEB73454E52C09eDFCBEAC50a2fde2460Dd41&amp;quot;&amp;gt;WPA2-AES&amp;lt;/Mode&amp;gt;'\
                '&amp;lt;/wirelessSecurity&amp;gt;'\
                '&amp;lt;/wirelessProfile&amp;gt;'\
                '&quot;/&gt;'\
                '&lt;DaylightSaving val=&quot;0&quot;/&gt;'\
                '&lt;IANAName val=&quot;&quot;/&gt;'\
                '&lt;LEDConfig val=&quot;&amp;lt;LEDConfig&amp;gt;'\
                '&amp;lt;led&amp;gt;'\
                '&amp;lt;name&amp;gt;MODE&amp;lt;/name&amp;gt;'\
                '&amp;lt;brightness&amp;gt;100&amp;lt;/brightness&amp;gt;'\
                '&amp;lt;/led&amp;gt;'\
                '&amp;lt;led&amp;gt;'\
                '&amp;lt;name&amp;gt;NETWORK&amp;lt;/name&amp;gt;'\
                '&amp;lt;brightness&amp;gt;100&amp;lt;/brightness&amp;gt;'\
                '&amp;lt;/led&amp;gt;'\
                '&amp;lt;led&amp;gt;'\
                '&amp;lt;name&amp;gt;MUTED&amp;lt;/name&amp;gt;'\
                '&amp;lt;brightness&amp;gt;100&amp;lt;/brightness&amp;gt;'\
                '&amp;lt;/led&amp;gt;'\
                '&amp;lt;led&amp;gt;'\
                '&amp;lt;name&amp;gt;REAR_STATUS&amp;lt;/name&amp;gt;'\
                '&amp;lt;brightness&amp;gt;100&amp;lt;/brightness&amp;gt;'\
                '&amp;lt;/led&amp;gt;'\
                '&amp;lt;/LEDConfig&amp;gt;&quot;/&gt;'\
                '&lt;NetworkConfigurationList val=&quot;&amp;lt;listNetworkConfigurations&amp;gt;'\
                '&amp;lt;networkConfiguration id=&amp;quot;1&amp;quot; dhcpOn=&amp;quot;0&amp;quot; enabled=&amp;quot;true&amp;quot;&amp;gt;'\
                '&amp;lt;Name&amp;gt;eth0&amp;lt;/Name&amp;gt;'\
                '&amp;lt;Type&amp;gt;LAN&amp;lt;/Type&amp;gt;'\
                '&amp;lt;IP&amp;gt;10.42.12.12&amp;lt;/IP&amp;gt;'\
                '&amp;lt;Netmask&amp;gt;255.255.255.0&amp;lt;/Netmask&amp;gt;'\
                '&amp;lt;Gateway&amp;gt;10.42.12.1&amp;lt;/Gateway&amp;gt;'\
                '&amp;lt;DNS1&amp;gt;10.42.12.1&amp;lt;/DNS1&amp;gt;'\
                '&amp;lt;DNS2&amp;gt;0.0.0.0&amp;lt;/DNS2&amp;gt;'\
                '&amp;lt;DNS3&amp;gt;0.0.0.0&amp;lt;/DNS3&amp;gt;'\
                '&amp;lt;gwMac&amp;gt;000000000000&amp;lt;/gwMac&amp;gt;'\
                '&amp;lt;/networkConfiguration&amp;gt;'\
                '&amp;lt;networkConfiguration id=&amp;quot;2&amp;quot; dhcpOn=&amp;quot;1&amp;quot; enabled=&amp;quot;true&amp;quot;&amp;gt;'\
                '&amp;lt;Name&amp;gt;wlan0&amp;lt;/Name&amp;gt;'\
                '&amp;lt;Type&amp;gt;WLAN&amp;lt;/Type&amp;gt;'\
                '&amp;lt;IP&amp;gt;0.0.0.0&amp;lt;/IP&amp;gt;'\
                '&amp;lt;Netmask&amp;gt;0.0.0.0&amp;lt;/Netmask&amp;gt;'\
                '&amp;lt;Gateway&amp;gt;0.0.0.0&amp;lt;/Gateway&amp;gt;'\
                '&amp;lt;DNS1&amp;gt;0.0.0.0&amp;lt;/DNS1&amp;gt;'\
                '&amp;lt;DNS2&amp;gt;0.0.0.0&amp;lt;/DNS2&amp;gt;'\
                '&amp;lt;DNS3&amp;gt;0.0.0.0&amp;lt;/DNS3&amp;gt;'\
                '&amp;lt;gwMac&amp;gt;'\
                '&amp;lt;/gwMac&amp;gt;'\
                '&amp;lt;wirelessProfile SSID=&amp;quot;DEFAULT-SSID-8e09dfb09df4FBfa996&amp;quot;&amp;gt;'\
                '&amp;lt;wirelessSecurity enabled=&amp;quot;true&amp;quot;&amp;gt;'\
                '&amp;lt;Mode passPhrase=&amp;quot;DEFAULT-PWD-c4E10186eDA2cbfAEB73454E52C09eDFCBEAC50a2fde2460Dd41&amp;quot;&amp;gt;WPA2-AES&amp;lt;/Mode&amp;gt;'\
                '&amp;lt;/wirelessSecurity&amp;gt;'\
                '&amp;lt;/wirelessProfile&amp;gt;'\
                '&amp;lt;/networkConfiguration&amp;gt;'\
                '&amp;lt;/listNetworkConfigurations&amp;gt;&quot;/&gt;'\
                '&lt;NetworkShareConfig val=&quot;&amp;lt;NetworkShareConfig&amp;gt;'\
                '&amp;lt;/NetworkShareConfig&amp;gt;&quot;/&gt;'\
                '&lt;SessionId val=&quot;&quot;/&gt;'\
                '&lt;SurroundSpeakerConfig val=&quot;&amp;lt;SurroundSpeakerConfig&amp;gt;'\
                '&amp;lt;Front&amp;gt;'\
                '&amp;lt;enabled&amp;gt;1&amp;lt;/enabled&amp;gt;'\
                '&amp;lt;crossover&amp;gt;0&amp;lt;/crossover&amp;gt;'\
                '&amp;lt;Right&amp;gt;'\
                '&amp;lt;distance&amp;gt;12&amp;lt;/distance&amp;gt;'\
                '&amp;lt;level&amp;gt;12&amp;lt;/level&amp;gt;'\
                '&amp;lt;test_tone&amp;gt;0&amp;lt;/test_tone&amp;gt;'\
                '&amp;lt;/Right&amp;gt;'\
                '&amp;lt;Left&amp;gt;'\
                '&amp;lt;distance&amp;gt;12&amp;lt;/distance&amp;gt;'\
                '&amp;lt;level&amp;gt;12&amp;lt;/level&amp;gt;'\
                '&amp;lt;test_tone&amp;gt;0&amp;lt;/test_tone&amp;gt;'\
                '&amp;lt;/Left&amp;gt;'\
                '&amp;lt;/Front&amp;gt;'\
                '&amp;lt;Center&amp;gt;'\
                '&amp;lt;enabled&amp;gt;0&amp;lt;/enabled&amp;gt;'\
                '&amp;lt;crossover&amp;gt;0&amp;lt;/crossover&amp;gt;'\
                '&amp;lt;Center&amp;gt;'\
                '&amp;lt;distance&amp;gt;12&amp;lt;/distance&amp;gt;'\
                '&amp;lt;level&amp;gt;12&amp;lt;/level&amp;gt;'\
                '&amp;lt;test_tone&amp;gt;0&amp;lt;/test_tone&amp;gt;'\
                '&amp;lt;/Center&amp;gt;'\
                '&amp;lt;/Center&amp;gt;'\
                '&amp;lt;Subwoofer&amp;gt;'\
                '&amp;lt;enabled&amp;gt;0&amp;lt;/enabled&amp;gt;'\
                '&amp;lt;lowpass&amp;gt;250&amp;lt;/lowpass&amp;gt;'\
                '&amp;lt;phase&amp;gt;0&amp;lt;/phase&amp;gt;'\
                '&amp;lt;Subwoofer&amp;gt;'\
                '&amp;lt;distance&amp;gt;12&amp;lt;/distance&amp;gt;'\
                '&amp;lt;level&amp;gt;12&amp;lt;/level&amp;gt;'\
                '&amp;lt;test_tone&amp;gt;0&amp;lt;/test_tone&amp;gt;'\
                '&amp;lt;/Subwoofer&amp;gt;'\
                '&amp;lt;/Subwoofer&amp;gt;'\
                '&amp;lt;Rear&amp;gt;'\
                '&amp;lt;enabled&amp;gt;0&amp;lt;/enabled&amp;gt;'\
                '&amp;lt;crossover&amp;gt;0&amp;lt;/crossover&amp;gt;'\
                '&amp;lt;surround_mode&amp;gt;OFF&amp;lt;/surround_mode&amp;gt;'\
                '&amp;lt;Right&amp;gt;'\
                '&amp;lt;distance&amp;gt;10&amp;lt;/distance&amp;gt;'\
                '&amp;lt;level&amp;gt;12&amp;lt;/level&amp;gt;'\
                '&amp;lt;test_tone&amp;gt;0&amp;lt;/test_tone&amp;gt;'\
                '&amp;lt;/Right&amp;gt;'\
                '&amp;lt;Left&amp;gt;'\
                '&amp;lt;distance&amp;gt;10&amp;lt;/distance&amp;gt;'\
                '&amp;lt;level&amp;gt;12&amp;lt;/level&amp;gt;'\
                '&amp;lt;test_tone&amp;gt;0&amp;lt;/test_tone&amp;gt;'\
                '&amp;lt;/Left&amp;gt;'\
                '&amp;lt;/Rear&amp;gt;'\
                '&amp;lt;DistUnit&amp;gt;m&amp;lt;/DistUnit&amp;gt;'\
                '&amp;lt;/SurroundSpeakerConfig&amp;gt;&quot;/&gt;'\
                '&lt;TimeZone val=&quot;(GMT-8:00)&quot;/&gt;'\
                '&lt;UpdateAction val=&quot;UPDATE_ACTION_NONE&quot;/&gt;'\
                '&lt;UpdateLevel val=&quot;0&quot;/&gt;'\
                '&lt;UpgradeProgress val=&quot;0&quot;/&gt;'\
                '&lt;UpgradeStatus val=&quot;UPGRADE_CURRENT&quot;/&gt;'\
                '&lt;VolumeLimit val=&quot;100&quot;/&gt;'\
                '&lt;WifiApSsid val=&quot;&quot;/&gt;'\
                '&lt;WirelessState val=&quot;LINK_DOWN&quot;/&gt;'\
                '&lt;/Event&gt;'

        return rtn

    @property
    def currSt(self):
        currSt = OrderedDict([\
         ('ActiveInterface', b'1'),\
         ('FriendlyName', b'Kitchen'),\
         ('HEOSNetId', b'DEFAULT-SSID-8e09dfb09df4FBfa996'),\
         ('LastDiscoveredDevice', b''),\
         ('P2PMode', b'NONE'),\
         ('Transcode', b'1'),\
         ('AudioConfig', {'AudioConfig': \
             {'highpass': '0', 'lowpass': '80', 'subwooferEnable': '0', 'outputMode': 'STEREO', 'ampBridged': '0', \
                 'soundMode': 'STEREO', 'impedance': None, 'ampPower': '1', \
                 'availableSoundModes': 'MOVIE_NORMAL,MUSIC_NORMAL', 'sourceDirect': \
                 '0', 'bassBoost': '0', 'speakerOption': None}}),\
         ('BTConfig', {'BluetoothStatus': \
             {'connectedStatus': 'DISCONNECTED', 'connectedDevice': None, 'pairedDevices': None, 'hasPairedDevices': '0'}}),\
         ('ConfigurationStatus', b'0'),\
         ('UpgradeComponentInstallProgress', b'0'),\
         ('CurrentLanguageLocale', b'en_US'),\
         ('CurrentWirelessProfile', \
             {'wirelessProfile': {'wirelessSecurity': {'Mode': \
                 {'@passPhrase': 'DEFAULT-PWD-c4E10186eDA2cbfAEB73454E52C09eDFCBEAC50a2fde2460Dd41', '#text': 'WPA2-AES'},\
                 '@enabled': 'true'}, '@SSID': 'DEFAULT-SSID-8e09dfb09df4FBfa996'}}),\
         ('DaylightSaving', b'0'),\
         ('IANAName', b''),\
         ('LEDConfig', {'LEDConfig': {'led': \
             [{'name': 'MODE', 'brightness': '100'}, \
                 {'name': 'NETWORK', 'brightness': '100'}, \
                 {'name': 'MUTED', 'brightness': '100'}, \
                 {'name': 'REAR_STATUS', 'brightness': '100'}]}}),\
         ('NetworkConfigurationList', {'listNetworkConfigurations': {'networkConfiguration': [\
             {'Name': 'eth0', 'Type': 'LAN', 'IP': '10.42.12.12', 'Netmask': '255.255.255.0', 'Gateway': '10.42.12.1', \
                 'DNS1': '10.42.12.1', 'DNS2': '0.0.0.0', 'DNS3': '0.0.0.0', \
                 'gwMac': '000000000000', '@id': '1', '@dhcpOn': '0', '@enabled': 'true'}, \
             {'Name': 'wlan0', 'Type': 'WLAN', 'IP': '0.0.0.0', 'Netmask': '0.0.0.0', 'Gateway': '0.0.0.0', \
                 'DNS1': '0.0.0.0', 'DNS2': '0.0.0.0', 'DNS3': '0.0.0.0', 'gwMac': None, \
                 'wirelessProfile': {'wirelessSecurity': \
                     {'Mode': {'@passPhrase': 'DEFAULT-PWD-c4E10186eDA2cbfAEB73454E52C09eDFCBEAC50a2fde2460Dd41', '#text': 'WPA2-AES'}, \
                         '@enabled': 'true'}, '@SSID': 'DEFAULT-SSID-8e09dfb09df4FBfa996'}, \
                     '@id': '2', '@dhcpOn': '1', '@enabled': 'true'}]}}),\
         ('NetworkShareConfig', {'NetworkShareConfig': None}),\
         ('SessionId', b''),\
         ('SurroundSpeakerConfig', {'SurroundSpeakerConfig': {'Front': {'enabled': '1', 'crossover': '0', \
             'Right': {'distance': '12', 'level': '12', 'test_tone': '0'}, \
             'Left': {'distance': '12', 'level': '12', 'test_tone': '0'}}, \
             'Center': {'enabled': '0', 'crossover': '0', 'Center': {'distance': '12', 'level': '12', 'test_tone': '0'}}, \
             'Subwoofer': {'enabled': '0', 'lowpass': '250', 'phase': '0', 'Subwoofer': {'distance': '12', 'level': '12', 'test_tone': '0'}}, \
             'Rear': {'enabled': '0', 'crossover': '0', 'surround_mode': 'OFF', \
                 'Right': {'distance': '10', 'level': '12', 'test_tone': '0'}, \
                 'Left': {'distance': '10', 'level': '12', 'test_tone': '0'}}, 'DistUnit': 'm'}}),\
         ('TimeZone', b'(GMT-8:00)'),\
         ('UpdateAction', b'UPDATE_ACTION_NONE'),\
         ('UpdateLevel', b'0'),\
         ('UpgradeProgress', b'0'),\
         ('UpgradeStatus', b'UPGRADE_CURRENT'),\
         ('VolumeLimit', b'100'),\
         ('WifiApSsid', b''),\
         ('WirelessState', b'LINK_DOWN')])

        return currSt

    @property
    def currStFmt(self):

        currStFmtRtn=\
            "ActiveInterface  : b'1'\n"\
            "FriendlyName     : b'Kitchen'\n"\
            "HEOSNetId        : b'DEFAULT-SSID-8e09dfb09df4FBfa996'\n"\
            "LastDiscoveredDevice : b''\n"\
            "P2PMode          : b'NONE'\n"\
            "Transcode        : b'1'\n"\
            "AudioConfig      : \n"\
            "    AudioConfig      : \n"\
            "        highpass         : 0\n"\
            "        lowpass          : 80\n"\
            "        subwooferEnable  : 0\n"\
            "        outputMode       : STEREO\n"\
            "        ampBridged       : 0\n"\
            "        soundMode        : STEREO\n"\
            "        impedance        : None\n"\
            "        ampPower         : 1\n"\
            "        availableSoundModes : MOVIE_NORMAL,MUSIC_NORMAL\n"\
            "        sourceDirect     : 0\n"\
            "        bassBoost        : 0\n"\
            "        speakerOption    : None\n"\
            "BTConfig         : \n"\
            "    BluetoothStatus  : \n"\
            "        connectedStatus  : DISCONNECTED\n"\
            "        connectedDevice  : None\n"\
            "        pairedDevices    : None\n"\
            "        hasPairedDevices : 0\n"\
            "ConfigurationStatus : b'0'\n"\
            "UpgradeComponentInstallProgress : b'0'\n"\
            "CurrentLanguageLocale : b'en_US'\n"\
            "CurrentWirelessProfile : \n"\
            "    wirelessProfile  : \n"\
            "        wirelessSecurity : \n"\
            "            Mode             : \n"\
            "                @passPhrase      : DEFAULT-PWD-c4E10186eDA2cbfAEB73454E52C09eDFCBEAC50a2fde2460Dd41\n"\
            "                #text            : WPA2-AES\n"\
            "            @enabled         : true\n"\
            "        @SSID            : DEFAULT-SSID-8e09dfb09df4FBfa996\n"\
            "DaylightSaving   : b'0'\n"\
            "IANAName         : b''\n"\
            "LEDConfig        : \n"\
            "    LEDConfig        : \n"\
            "        led              : \n"\
            "        ----------------   \n"\
            "            name             : MODE\n"\
            "            brightness       : 100\n"\
            "        ----------------   \n"\
            "            name             : NETWORK\n"\
            "            brightness       : 100\n"\
            "        ----------------   \n"\
            "            name             : MUTED\n"\
            "            brightness       : 100\n"\
            "        ----------------   \n"\
            "            name             : REAR_STATUS\n"\
            "            brightness       : 100\n"\
            "        ----------------   \n"\
            "NetworkConfigurationList : \n"\
            "    listNetworkConfigurations : \n"\
            "        networkConfiguration : \n"\
            "        ----------------   \n"\
            "            Name             : eth0\n"\
            "            Type             : LAN\n"\
            "            IP               : 10.42.12.12\n"\
            "            Netmask          : 255.255.255.0\n"\
            "            Gateway          : 10.42.12.1\n"\
            "            DNS1             : 10.42.12.1\n"\
            "            DNS2             : 0.0.0.0\n"\
            "            DNS3             : 0.0.0.0\n"\
            "            gwMac            : 000000000000\n"\
            "            @id              : 1\n"\
            "            @dhcpOn          : 0\n"\
            "            @enabled         : true\n"\
            "        ----------------   \n"\
            "            Name             : wlan0\n"\
            "            Type             : WLAN\n"\
            "            IP               : 0.0.0.0\n"\
            "            Netmask          : 0.0.0.0\n"\
            "            Gateway          : 0.0.0.0\n"\
            "            DNS1             : 0.0.0.0\n"\
            "            DNS2             : 0.0.0.0\n"\
            "            DNS3             : 0.0.0.0\n"\
            "            gwMac            : None\n"\
            "            wirelessProfile  : \n"\
            "                wirelessSecurity : \n"\
            "                    Mode             : \n"\
            "                        @passPhrase      : DEFAULT-PWD-c4E10186eDA2cbfAEB73454E52C09eDFCBEAC50a2fde2460Dd41\n"\
            "                        #text            : WPA2-AES\n"\
            "                    @enabled         : true\n"\
            "                @SSID            : DEFAULT-SSID-8e09dfb09df4FBfa996\n"\
            "            @id              : 2\n"\
            "            @dhcpOn          : 1\n"\
            "            @enabled         : true\n"\
            "        ----------------   \n"\
            "NetworkShareConfig : \n"\
            "    NetworkShareConfig : None\n"\
            "SessionId        : b''\n"\
            "SurroundSpeakerConfig : \n"\
            "    SurroundSpeakerConfig : \n"\
            "        Front            : \n"\
            "            enabled          : 1\n"\
            "            crossover        : 0\n"\
            "            Right            : \n"\
            "                distance         : 12\n"\
            "                level            : 12\n"\
            "                test_tone        : 0\n"\
            "            Left             : \n"\
            "                distance         : 12\n"\
            "                level            : 12\n"\
            "                test_tone        : 0\n"\
            "        Center           : \n"\
            "            enabled          : 0\n"\
            "            crossover        : 0\n"\
            "            Center           : \n"\
            "                distance         : 12\n"\
            "                level            : 12\n"\
            "                test_tone        : 0\n"\
            "        Subwoofer        : \n"\
            "            enabled          : 0\n"\
            "            lowpass          : 250\n"\
            "            phase            : 0\n"\
            "            Subwoofer        : \n"\
            "                distance         : 12\n"\
            "                level            : 12\n"\
            "                test_tone        : 0\n"\
            "        Rear             : \n"\
            "            enabled          : 0\n"\
            "            crossover        : 0\n"\
            "            surround_mode    : OFF\n"\
            "            Right            : \n"\
            "                distance         : 10\n"\
            "                level            : 12\n"\
            "                test_tone        : 0\n"\
            "            Left             : \n"\
            "                distance         : 10\n"\
            "                level            : 12\n"\
            "                test_tone        : 0\n"\
            "        DistUnit         : m\n"\
            "TimeZone         : b'(GMT-8:00)'\n"\
            "UpdateAction     : b'UPDATE_ACTION_NONE'\n"\
            "UpdateLevel      : b'0'\n"\
            "UpgradeProgress  : b'0'\n"\
            "UpgradeStatus    : b'UPGRADE_CURRENT'\n"\
            "VolumeLimit      : b'100'\n"\
            "WifiApSsid       : b''\n"\
            "WirelessState    : b'LINK_DOWN'\n"\

        return currStFmtRtn

    @property
    def cmndList(self):
        cmndListRtn=\
            ['AddNetworkShare',\
                 'ApplyChanges',\
                 'CancelChanges',\
                 'CancelFirmwareUpgrade',\
                 'CheckForFirmwareUpgrade',\
                 'DeleteNetworkShare',\
                 'GetAccessPointList',\
                 'GetActiveInterface',\
                 'GetAudioConfig',\
                 'GetBluetoothStatus',\
                 'GetConfigurationStatus',\
                 'GetConfigurationToken',\
                 'GetCurrentLanguage',\
                 'GetCurrentState',\
                 'GetDaylightSaving',\
                 'GetFriendlyName',\
                 'GetHEOSNetID',\
                 'GetLEDConfig',\
                 'GetNetworkConfiguration',\
                 'GetNetworkConfigurationList',\
                 'GetNetworkShares',\
                 'GetP2PMode',\
                 'GetSessionId',\
                 'GetSupportedLanguageList',\
                 'GetSurroundSpeakerConfig',\
                 'GetTimeZone',\
                 'GetTranscode',\
                 'GetUpdateAction',\
                 'GetUpdateLevel',\
                 'GetUpgradeProgress',\
                 'GetUpgradeStatus',\
                 'GetVolumeLimit',\
                 'GetWirelessProfile',\
                 'GetWirelessState',\
                 'GetWirelessStatus',\
                 'ReIndexNetworkShare',\
                 'ReMountNetworkShare',\
                 'RegisterUser',\
                 'ReleaseConfigurationToken',\
                 'SetAudioConfig',\
                 'SetBluetoothAction',\
                 'SetConfigurationStatus',\
                 'SetCurrentLanguage',\
                 'SetDaylightSaving',\
                 'SetFriendlyName',\
                 'SetHEOSNetID',\
                 'SetLEDConfig',\
                 'SetNetworkConfiguration',\
                 'SetSessionId',\
                 'SetSurroundSpeakerConfig',\
                 'SetTimeZone',\
                 'SetTranscode',\
                 'SetUpdateAction',\
                 'SetUpdateLevel',\
                 'SetVolumeLimit',\
                 'SetWPSPinSSID',\
                 'SetWirelessProfile',\
                 'StartInvitation',\
                 'StartWifiAp',\
                 'StopInvitation',\
                 'StopWifiAp',\
                 'SubmitDiagnostics',\
                 'UpdateFirmware']

        return cmndListRtn
