##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeBond.py
#Class for bonding functions
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
from shoeOp import *
import time

class ShoeBond(ShoeOp):
    ZONE_UUID_ARG='ZoneUUID'

    CREATE_ZONE_CMND    = 'CreateZone'
    ZONE_CONN_LIST_CMND = 'GetZoneConnectedList'
    CREATE_GROUP_CMND   = 'CreateGroup'
    GROUP_STATUS_CMND   = 'GetGroupStatus'
    ZONE_UUID_CMND      = 'GetZoneUUID'
    GROUP_UUID_CMND     = 'GetGroupUUID'
    GROUP_DEL_CMND      = 'DestroyGroup'
    GET_CHAN_CMND       = 'GetGroupMemberChannel'
    SET_CHAN_CMND       = 'SetGroupMemberChannel'
    ZONE_DEL_CMND       = 'DestroyZone'

    ZONE_IPLIST_ARG='ZoneIPList'
    ZONE_NAME_ARG='ZoneFriendlyName'

    ZONE_CONN_LIST_ARG='ZoneConnectedList'

    GROUP_NAME_ARG='GroupFriendlyName'
    GROUP_MEMBER_ARG='GroupMemberUUIDList'
    GROUP_CHANLIST_ARG='GroupMemberChannelList'

    GROUP_STATUS_ARG='GroupStatus'

    GROUP_UUID_ARG='GroupUUID'

    GROUP_LEAD=['GROUP_LEAD', 'LEADER']

    GROUP_PRESERVE_ZONE_ARG='PreserveZone'

    MT_UUIDS=['', '00000000000000000000000000000000']

    CHAN_ARG='AudioChannel'

    BOND_DEV='AiosServices'
    ZONE_SVC='ZoneControl'
    GROUP_SVC='GroupControl'

    def __init__(self, spkrRoots=[], loglvl=ConsoleLog.WARNING):
        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        self.spkrRoots=spkrRoots
        return

    def bondSpkrs(self, name):
        self.log.debug("Bond Spkrs Name %s" % name)
        otherIps=[spkrRoot.host for spkrRoot in self.spkrRoots]
        del otherIps[0]
        leadSpkrRoot=self.spkrRoots[0]

        zoneUuid=self._createZone(leadSpkrRoot, otherIps, name)
        zoneConnList=self._getZoneConnectList(leadSpkrRoot, zoneUuid)
        self.log.debug("Zone Connect List %s", zoneConnList)

        args=OrderedDict()

        args=OrderedDict()
        args[self.GROUP_NAME_ARG]=name
        args[self.GROUP_MEMBER_ARG]=zoneConnList
        args[self.GROUP_CHANLIST_ARG]=''

        cmndRtnStr=self.runCmnd(leadSpkrRoot, self.CREATE_GROUP_CMND, args)

        return cmndRtnStr

    def swapStereoSpkrs(self):
        groupUuid=self._getGroupUuid(self.spkrRoots[0])

        swapChan={'RIGHT':'LEFT', 'LEFT':'RIGHT'}
        spkrCmndRtn={}

        cmndRtnStr=''

        for spkrRoot in self.spkrRoots:
            chan=self._getSpkrChannel(spkrRoot, groupUuid)

            try:
                chan=swapChan[chan]
            except KeyError:
                continue

            cmndRtnStr+="Host %s\n" % spkrRoot.host
            cmndRtnStr+=self.setSpkrChan(spkrRoot, groupUuid, chan)
            cmndRtnStr+='\n'

        return cmndRtnStr

    def setSpkrChan(self, spkrRoot, groupUuid, chan):
        args=OrderedDict()
        args[self.GROUP_UUID_ARG]=groupUuid
        args[self.CHAN_ARG]=chan
        cmndRtnStr=self.runCmnd(spkrRoot, self.SET_CHAN_CMND, args)
        return cmndRtnStr

    def unbondSpkrs(self):
        groupUuid=self._getGroupUuid(self.spkrRoots[0])
        leadSpkrRoot=self._getGroupLead(groupUuid)
        args=OrderedDict()
        args[self.GROUP_UUID_ARG]=groupUuid
        args[self.GROUP_PRESERVE_ZONE_ARG]=False

        cmndRtnStr=self.runCmnd(leadSpkrRoot, self.GROUP_DEL_CMND, args)

        if self._getGroupUuid(leadSpkrRoot) not in self.MT_UUIDS:
            raise ShoeBondGroupErr("Group Not Deleted")

        return cmndRtnStr

    def runCmnd(self, spkrRoot, cmnd, args):
        cmndStrRtn=super().runCmnd(cmnd,
                        args,
                        devName=self.BOND_DEV,
                        svcName=None,
                        shoeRoot=spkrRoot)
        return cmndStrRtn

    def _getGroupUuid(self, spkrRoot):
        cmndRtn=self._rootCmnd(spkrRoot, self.GROUP_UUID_CMND)
        return cmndRtn.args[self.GROUP_UUID_ARG]

    def _getSpkrChannel(self,spkrRoot, groupUuid):
        args=OrderedDict()
        args[self.GROUP_UUID_ARG]=groupUuid

        cmndRtn=self._rootCmnd(spkrRoot, self.GET_CHAN_CMND, args)
        return cmndRtn.args[self.CHAN_ARG]

    def _getGroupLead(self, groupUuid):
        args=OrderedDict()
        args[self.GROUP_UUID_ARG]=groupUuid

        rtnDev=None

        for spkrRoot in self.spkrRoots:
            cmndRtn=self._rootCmnd(spkrRoot, self.GROUP_STATUS_CMND, args)
            self.log.debug("lead seek %s %s", spkrRoot.host, cmndRtn)
            if cmndRtn.args[self.GROUP_STATUS_ARG] in self.GROUP_LEAD:
                rtnDev=spkrRoot
                break

        if rtnDev is None:
            raise ShoeBondGroupErr("Group Lead Not Found")

        return rtnDev

    def _createZone(self, leadSpkrRoot, otherIps, name):
        self.log.debug("Create Zone %s %s", leadSpkrRoot.host, otherIps)

        args=OrderedDict()

        zoneUuid=self._getZoneUUID(leadSpkrRoot)

        self.log.debug("Init Zone UUID %s", zoneUuid)

        #If zone exists, delete.
        if zoneUuid not in self.MT_UUIDS:
            self._deleteZone(leadSpkrRoot, zoneUuid)

        otherIpsVal=''
        first=True
        for otherIp in otherIps:
            if first:
                otherIpsVal=str(otherIp)
                first=False
            else:
                otherIpsVal+=", %s" % otherIp

        self.log.debug("otherIpsVal %s", otherIpsVal)

        args[self.ZONE_NAME_ARG]=name
        args[self.ZONE_IPLIST_ARG]=otherIpsVal

        cmndRtn=self._rootCmnd(leadSpkrRoot, self.CREATE_ZONE_CMND, args)
        zoneUuid=cmndRtn.args[self.ZONE_UUID_ARG]

        time.sleep(.5)
        self.log.debug("Zone UUID %s", zoneUuid)
        self._checkZoneUUID(zoneUuid)

        return zoneUuid

    def _deleteZone(self, spkrRoot, zoneUuid):
        args=OrderedDict()
        args[self.ZONE_UUID_ARG]=zoneUuid
        cmndRtn=self._rootCmnd(spkrRoot, self.ZONE_DEL_CMND)
        return cmndRtn

    def _getZoneConnectList(self, spkrRoot, zoneUuid):
        args=OrderedDict()
        args[self.ZONE_UUID_ARG]=zoneUuid
        cmndRtn=self._rootCmnd(spkrRoot, self.ZONE_CONN_LIST_CMND, args)

        return cmndRtn.args[self.ZONE_CONN_LIST_ARG]

    def _getZoneUUID(self, spkrRoot):
        cmndRtn=self._rootCmnd(spkrRoot, self.ZONE_UUID_CMND)
        zoneUuid=cmndRtn.args[self.ZONE_UUID_ARG]
        self.log.debug("Zone UUID for %s %s" % (spkrRoot.host, zoneUuid))
        return zoneUuid

    def _checkZoneUUID(self, checkUuid):
        for spkrRoot in self.spkrRoots:
            self.log.debug("Check Zone UUID %s on %s", checkUuid, spkrRoot.host)
            zoneUuid=self._getZoneUUID(spkrRoot)
            if checkUuid != zoneUuid:
                raise ShoeBondZoneErr("UUID %s Not Correct for %s Uuid %s" %
                        (zoneUuid, spkrRoot.host, checkUuid))
        return

    def _rootCmnd(self, spkrRoot, cmnd, args=None):
        self.log.debug("cmnd %s args %s spkrRoot %s", cmnd, args, spkrRoot.host)
        return spkrRoot.sendCmnd(cmnd, args, devName=self.BOND_DEV)

###############################Exceptions#################################
class ShoeBondDevErr(Exception):
    pass

class ShoeBondZoneErr(Exception):
    pass

class ShoeBondGroupErr(Exception):
    pass

##############################UNIT TESTS########################################
from test_shoe import *
from copy import deepcopy

class TestShoeBond(TestShoeHttp):
    class TestShoeBondHttpHandler(TestShoeHttp.TestShoeHttpHandler):
        bondCmnds=None

        def postRtn(self, params, host):
            srvRxCmnd=params.srvRxCmnd
            cmnd=self.bondCmnds[host][params.srvRxCmnd]
            params.setTestCmnd(cmnd)
            super().postRtn(params, host)
            return

    def setUp(self):
        super().setUp()

        hosts= ['127.0.0.1', '127.0.0.2']

        self.bondName='KITDEN'

        self.leadHost=hosts[0]
        self.otherHosts=[hosts[1],]

        self.svcName=None
        self.setHosts(hosts)
        self.testCbFunc=self._setUp
        self.spkrRoots=[]
        self.cmndRtn=None

        self.bondCmnds={}

        allTestCmnds={}
        allTestCmnds.update(self.testGroupCtrlSvc.cmnds)
        allTestCmnds.update(self.testZoneCtrlSvc.cmnds)

        self.setHandler(self.TestShoeBondHttpHandler)

        for host in hosts:
            print("^^^^^^^^^^^^^^^Host^^^^^^^^^^^^^^^^^^^^^^^^^^",
                    host)
            hostCmnds=deepcopy(allTestCmnds)

            spkrRoot=ShoeRoot(host=host, port=self.srvPort, loglvl=logging.DEBUG)
            self.spkrRoots.append(spkrRoot)

            if host == self.leadHost:
                print("^^^^^^^^^^^^^^^Lead Host^^^^^^^^^^^^^^^^^^",
                    spkrRoot, host)
                hostCmnds['GetGroupMemberChannel'].\
                        rtn['AudioChannel']='RIGHT'

                hostCmnds['GetGroupStatus'].\
                        rtn['GroupStatus']='LEADER'

            else:
                hostCmnds['GetGroupMemberChannel'].\
                        rtn['AudioChannel']='LEFT'

                hostCmnds['GetGroupStatus'].\
                        rtn['GroupStatus']='SLAVE'

                hostCmnds['GetZoneConnectedList'].\
                        rtn['ZoneConnectedList']=''

            self.bondCmnds[host]=hostCmnds

        self.TestShoeBondHttpHandler.bondCmnds=self.bondCmnds

        self.httpTest()

        self.shoeBond=ShoeBond(spkrRoots=self.spkrRoots, loglvl=logging.DEBUG)
        self.testCbFunc=self._sendTestMsgs
        return

    def _setUp(self):
        print(self.spkrRoots, len(self.spkrRoots))
        for spkrRoot in self.spkrRoots:
            print("^^^^^^^^^^^^^^^^^^^^^^Setup Root^^^^^^^^^^^^^^^^^^^^^^^^^^",
                    spkrRoot.host)
            spkrRoot.setUp()
        return

class TestShoeBondSwap(TestShoeBond):
    def _sendTestMsgs(self):
        self.cmndRtn=self.shoeBond.swapStereoSpkrs()
        return

    def setUp(self):
        super().setUp()
        return

    def runTest(self):
        self.httpTest()
        print(self.cmndRtn)
        return

class TestShoeUnBondSpkrs(TestShoeBond):
    class TestShoeUnBondHttpHandler(TestShoeBond.TestShoeBondHttpHandler):
        def postRtn(self, params, host):
            bondCmnds=TestShoeBond.TestShoeBondHttpHandler.bondCmnds
            srvRxCmnd=params.srvRxCmnd
            if srvRxCmnd=='DestroyGroup':
                bondCmnds[host]['GetGroupUUID'].rtn['GroupUUID']=\
                            '00000000000000000000000000000000'

            super().postRtn(params, host)
            return

    def _sendTestMsgs(self):
        self.cmndRtn=self.shoeBond.unbondSpkrs()
        return

    def setUp(self):
        super().setUp()
        self.setHandler(self.TestShoeUnBondHttpHandler)
        return

    def runTest(self):
        self.httpTest()
        print(self.cmndRtn)
        return

class TestShoeBondSpkrs(TestShoeBond):
    def _sendTestMsgs(self):
        self.cmndRtn=self.shoeBond.bondSpkrs(self.bondName)
        return

    def setUp(self):
        super().setUp()
        return

    def runTest(self):
        self.httpTest()
        print(self.cmndRtn)
        return
