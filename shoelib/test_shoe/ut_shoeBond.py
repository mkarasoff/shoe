##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeBond.py
#Unit test for shoeBond.py Module.
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
##############################UNIT TESTS####################################
from .testShoeHttp import *
from shoelib.shoeBond import *
from shoelib.shoeRoot import *

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
