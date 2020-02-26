##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#ut_shoeDev.py
#Unit test for shoeDev module.
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
###############################Unittests#################################
from .testShoeHttp import *
from shoelib.shoeDev import *

class TestShoeAiosDev(unittest.TestCase):
    HOST='127.0.0.1'

    def setUp(self):
        self.testRoot=TestRootDev()
        self.testDevNames=['AiosServices', 'ACT-Denon']

        return

    def runTest(self):
        for name in self.testDevNames:
            dev=self.testRoot.devs[name]
            self._devTest(dev)
        return

    def _devTest(self, dev):
        print("@@@@@@@@@@@@@@@@@@Dev Test %s@@@@@@@@@@@@@@@@@@@@@@@"\
                % dev.name)

        shoeDev=ShoeDev(host=self.HOST,
                        cfg=dev.cfg,
                        loglvl=logging.DEBUG)

        shoeDev.setUp()

        self.assertEqual(dev.cfg, shoeDev.cfg)

        self.assertEqual(dev.uuid, shoeDev.uuid)

        self.assertEqual(dev.name, shoeDev.name)

        return
