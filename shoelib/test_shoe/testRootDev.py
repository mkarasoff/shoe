##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#testRootDev.py
#Class for unittest data generated from the aios_device.xml used for the
#root device.
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
from .testAiosSvcDev import *
from .testActDev import *
from .testRendererDev import *
from .testMediaSrvDev import *
import copy

class TestRootDev(TestShoeXml):
    NAME="RootDev"

    def __init__(self):
        self.name=self.NAME
        xmlFile='aios_device.xml'
        md5hex='59bfffcde20bfc4cf437bdf7676de386'
        urlPath='/upnp/desc/aios_device/'

        self.url='%s%s' % (urlPath, xmlFile)

        super().__init__(xmlFile, md5hex)

        self.devs={ TestActDev.NAME         : TestActDev(),
                    TestAiosSvcDev.NAME     : TestAiosSvcDev(),
                    TestMediaSrvDev.NAME    : TestMediaSrvDev(),
                    TestRendererDev.NAME    : TestRendererDev()}

        self.xmlDict={'root': {'device': \
                {'manufacturerURL': 'http://www.denon.com',\
                'modelName': 'HEOS 1', \
                'deviceList': {'device': [\
                TestRendererDev.CFG, \
                TestAiosSvcDev.CFG, \
                TestMediaSrvDev.CFG, \
                TestActDev.CFG]}, \
                'serialNumber': 'ACJG9876543210', \
                'modelNumber': 'DWS-1000 4.0', \
                'deviceType': 'urn:schemas-denon-com:device:AiosDevice:1', \
                'friendlyName': 'Kitchen', \
                'UDN': 'uuid:ea6e883a-2442-11ea-978f-2e728ce88125',\
                'manufacturer': 'Denon'},\
                'specVersion': \
                    {'major': '1', \
                    'minor': '0'}}}

        self.infoDict=\
                {'manufacturerURL'  : 'http://www.denon.com',\
                'modelName'         : 'HEOS 1', \
                'serialNumber'      : 'ACJG9876543210', \
                'modelNumber'       : 'DWS-1000 4.0', \
                'deviceType'        : 'urn:schemas-denon-com:device:AiosDevice:1', \
                'friendlyName'      : 'Kitchen', \
                'UDN'               : 'uuid:ea6e883a-2442-11ea-978f-2e728ce88125',\
                'manufacturer'      : 'Denon',\
                'DeviceID'          : 'AIOS :0001',\
                'firmwareRevision'  : '147202',\
                'firmware_date'     : 'Sun 2019-01-01 00 :00 :00',\
                'firmware_version'  : '1.520.200',\
                'lanMac'            : '00 :05 :CD :00 :00 :01',\
                'locale'            : 'en_NA',\
                'moduleRevision'    : '4',\
                'moduleType'        : 'Aios 4.0',\
                'productRevision'   : '3',\
                'releaseType'       : 'Production',\
                'wlanMac'           : '00 :05 :CD :00 :00 :00'}

        self.infoFmt=\
            'friendlyName     : Kitchen\n'\
            'manufacturer     : Denon\n'\
            'manufacturerURL  : http://www.denon.com\n'\
            'modelName        : HEOS 1\n'\
            'modelNumber      : DWS-1000 4.0\n'\
            'serialNumber     : ACJG9876543210\n'\
            'UDN              : uuid:ea6e883a-2442-11ea-978f-2e728ce88125\n'\
            'DeviceID         : AIOS:0001\n'\
            'firmwareRevision : 147202\n'\
            'firmware_date    : Sun 2019-01-01 00:00:00\n'\
            'firmware_version : 1.520.200\n'\
            'lanMac           : 00:05:CD:00:00:01\n'\
            'locale           : en_NA\n'\
            'moduleRevision   : 4\n'\
            'moduleType       : Aios 4.0\n'\
            'productRevision  : 3\n'\
            'releaseType      : Production\n'\
            'wlanMac          : 00:05:CD:00:00:00\n'

        return

    @property
    def svcs(self):
        svcs={}
        for dev in self.devs.values():
            svcs.update(dev.svcs)
        return svcs

    @property
    def cmnds(self):
        cmnds=[]
        for dev in self.devs.values():
            cmnds.extend(dev.cmnds)
        return cmnds

    @property
    def fmtCmndTreeDflt(self):
        rtnTree=\
            'Device: ACT-Denon : \n'\
            '    Service: ACT     : \n'\
            '    ----------------   \n'\
            '                           AddNetworkShare\n'\
            '                           ApplyChanges\n'\
            '                           CancelChanges\n'\
            '                           CancelFirmwareUpgrade\n'\
            '                           CheckForFirmwareUpgrade\n'\
            '                           DeleteNetworkShare\n'\
            '                           GetAccessPointList\n'\
            '                           GetActiveInterface\n'\
            '                           GetAudioConfig\n'\
            '                           GetBluetoothStatus\n'\
            '                           GetConfigurationStatus\n'\
            '                           GetConfigurationToken\n'\
            '                           GetCurrentLanguage\n'\
            '                           GetCurrentState\n'\
            '                           GetDaylightSaving\n'\
            '                           GetFriendlyName\n'\
            '                           GetHEOSNetID\n'\
            '                           GetLEDConfig\n'\
            '                           GetNetworkConfiguration\n'\
            '                           GetNetworkConfigurationList\n'\
            '                           GetNetworkShares\n'\
            '                           GetP2PMode\n'\
            '                           GetSessionId\n'\
            '                           GetSupportedLanguageList\n'\
            '                           GetSurroundSpeakerConfig\n'\
            '                           GetTimeZone\n'\
            '                           GetTranscode\n'\
            '                           GetUpdateAction\n'\
            '                           GetUpdateLevel\n'\
            '                           GetUpgradeProgress\n'\
            '                           GetUpgradeStatus\n'\
            '                           GetVolumeLimit\n'\
            '                           GetWirelessProfile\n'\
            '                           GetWirelessState\n'\
            '                           GetWirelessStatus\n'\
            '                           ReIndexNetworkShare\n'\
            '                           ReMountNetworkShare\n'\
            '                           RegisterUser\n'\
            '                           ReleaseConfigurationToken\n'\
            '                           SetAudioConfig\n'\
            '                           SetBluetoothAction\n'\
            '                           SetConfigurationStatus\n'\
            '                           SetCurrentLanguage\n'\
            '                           SetDaylightSaving\n'\
            '                           SetFriendlyName\n'\
            '                           SetHEOSNetID\n'\
            '                           SetLEDConfig\n'\
            '                           SetNetworkConfiguration\n'\
            '                           SetSessionId\n'\
            '                           SetSurroundSpeakerConfig\n'\
            '                           SetTimeZone\n'\
            '                           SetTranscode\n'\
            '                           SetUpdateAction\n'\
            '                           SetUpdateLevel\n'\
            '                           SetVolumeLimit\n'\
            '                           SetWPSPinSSID\n'\
            '                           SetWirelessProfile\n'\
            '                           StartInvitation\n'\
            '                           StartWifiAp\n'\
            '                           StopInvitation\n'\
            '                           StopWifiAp\n'\
            '                           SubmitDiagnostics\n'\
            '                           UpdateFirmware\n'\
            '    ----------------   \n'\
            'Device: AiosServices : \n'\
            '    Service: ErrorHandler : \n'\
            '    ----------------   \n'\
            '                           ClearError\n'\
            '                           DummyAction_ErrorHandler\n'\
            '    ----------------   \n'\
            '    Service: ZoneControl : \n'\
            '    ----------------   \n'\
            '                           AddMemberToZone\n'\
            '                           CreateZone\n'\
            '                           DestroyZone\n'\
            '                           DummyAction_ZoneControl\n'\
            '                           GetCurrentState\n'\
            '                           GetMemberStatus\n'\
            '                           GetZoneConnectedList\n'\
            '                           GetZoneFriendlyName\n'\
            '                           GetZoneMemberList\n'\
            '                           GetZoneMinimise\n'\
            '                           GetZoneMute\n'\
            '                           GetZoneStatus\n'\
            '                           GetZoneUUID\n'\
            '                           GetZoneVolume\n'\
            '                           RemoveMemberFromZone\n'\
            '                           SetZoneFriendlyName\n'\
            '                           SetZoneMinimise\n'\
            '                           SetZoneMute\n'\
            '                           SetZoneVolume\n'\
            '                           TestZoneConnectivity\n'\
            '    ----------------   \n'\
            '    Service: GroupControl : \n'\
            '    ----------------   \n'\
            '                           AddMembersToGroup\n'\
            '                           CreateGroup\n'\
            '                           DestroyGroup\n'\
            '                           DummyAction_GroupControl\n'\
            '                           GetConfigDeviceUUID\n'\
            '                           GetCurrentState\n'\
            '                           GetDeviceFriendlyName\n'\
            '                           GetGroupBalance\n'\
            '                           GetGroupBass\n'\
            '                           GetGroupFriendlyName\n'\
            '                           GetGroupMemberChannel\n'\
            '                           GetGroupMemberList\n'\
            '                           GetGroupMute\n'\
            '                           GetGroupStatus\n'\
            '                           GetGroupTreble\n'\
            '                           GetGroupUUID\n'\
            '                           GetGroupUpdating\n'\
            '                           GetGroupVolume\n'\
            '                           GetMediaServerUUID\n'\
            '                           GetSignalStrength\n'\
            '                           RemoveMembersFromGroup\n'\
            '                           SetDeviceFriendlyName\n'\
            '                           SetGroupBalance\n'\
            '                           SetGroupBass\n'\
            '                           SetGroupFriendlyName\n'\
            '                           SetGroupMemberChannel\n'\
            '                           SetGroupMute\n'\
            '                           SetGroupTreble\n'\
            '                           SetGroupVolume\n'\
            '    ----------------   \n'
        return rtnTree

    @property
    def fmtCmndTreeAll(self):
        rtnTree= self.fmtCmndTreeDflt+\
            'Device: MediaRenderer : \n'\
            '    Service: AVTransport : \n'\
            '    ----------------   \n'\
            '                           GetCurrentState\n'\
            '                           GetCurrentTransportActions\n'\
            '                           GetDeviceCapabilities\n'\
            '                           GetMediaInfo\n'\
            '                           GetMediaInfo_Ext\n'\
            '                           GetPositionInfo\n'\
            '                           GetTransportInfo\n'\
            '                           GetTransportSettings\n'\
            '                           Next\n'\
            '                           Pause\n'\
            '                           Play\n'\
            '                           Previous\n'\
            '                           Seek\n'\
            '                           SetAVTransportURI\n'\
            '                           SetNextAVTransportURI\n'\
            '                           SetPlayMode\n'\
            '                           Stop\n'\
            '                           X_SetShuffle\n'\
            '    ----------------   \n'\
            '    Service: ConnectionManager : \n'\
            '    ----------------   \n'\
            '                           ConnectionComplete\n'\
            '                           GetCurrentConnectionIDs\n'\
            '                           GetCurrentConnectionInfo\n'\
            '                           GetCurrentState\n'\
            '                           GetProtocolInfo\n'\
            '                           PrepareForConnection\n'\
            '    ----------------   \n'\
            '    Service: RenderingControl : \n'\
            '    ----------------   \n'\
            '                           GetCurrentState\n'\
            '                           GetMute\n'\
            '                           GetVolume\n'\
            '                           GetVolumeDB\n'\
            '                           ListPresets\n'\
            '                           SelectPreset\n'\
            '                           SetMute\n'\
            '                           SetVolume\n'\
            '                           SetVolumeDB\n'\
            '                           X_GetBalance\n'\
            '                           X_GetBass\n'\
            '                           X_GetPreset\n'\
            '                           X_GetSubwoofer\n'\
            '                           X_GetTreble\n'\
            '                           X_SetBalance\n'\
            '                           X_SetBass\n'\
            '                           X_SetMute\n'\
            '                           X_SetSubwoofer\n'\
            '                           X_SetTreble\n'\
            '                           X_SetVolume\n'\
            '    ----------------   \n'\
            'Device: MediaServer : \n'\
            '    Service: ContentDirectory : \n'\
            '    ----------------   \n'\
            '                           Browse\n'\
            '                           GetSearchCapabilities\n'\
            '                           GetSortCapabilities\n'\
            '                           GetSystemUpdateID\n'\
            '                           Search\n'\
            '                           X_HideItem\n'\
            '                           X_RenameItem\n'\
            '                           X_SetItemInputLevel\n'\
            '    ----------------   \n'\
            '    Service: ConnectionManager : \n'\
            '    ----------------   \n'\
            '                           ConnectionComplete\n'\
            '                           GetCurrentConnectionIDs\n'\
            '                           GetCurrentConnectionInfo\n'\
            '                           GetCurrentState\n'\
            '                           GetProtocolInfo\n'\
            '                           PrepareForConnection\n'\
            '    ----------------   \n'
        return rtnTree
