##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeRootDev.py
#Class that manages HEOS root device configuration.  It automatically
#instantiates other HEOS devices.  It requires an Aiso XML file to work
#will grab it from a HEOS device given by the 'host' variable.
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
from shoeDev import *

class ShoeDevRoot(ShoeDev):

    ROOTDEV_KEYS=('root', 'device')
    DEVLIST_KEYS=('deviceList', 'device')

    AIOS_CFG_PATH='/upnp/desc/aios_device/aios_device.xml'

    def __init__(self, aiosCfg=None, host, dbug=0, port=60006):

        super().__init__(host=host,
                        path=path,
                        port=port,
                        dbug=dbug)

        self.devs={}
        self._aiosCfg=aiosCfg
        return

    def init(self):
        if self.aiosCfg is None:
            self.aiosCfg=self.getCfg(self.AIOS_CFG_PATH)

        self.cfg=self._getRootDevCfg(self.aiosCfg)

        super().init()

        self.devs=self._getDevs(self.cfg)

        try:
            self.sysName=self.cfg[self.SYSNAME_KEYS]
        except KeyError:
            self.sysName = None
            print("WARNING:System name missing from root dev cfg")
        except:
            raise
        return

    def update(self):
        self.aisoCfg=None
        init()
        return

    def _getRootDevCfg(self, aiosCfg):

        try:
            rootDevCfg=\
                aiosCfg[self.ROOTDEV_KEYS[0]]\
                            [self.ROOTDEV_KEYS[1]]
        except KeyError:
            errStr="Bad Aios Device XML File"
            raise ShoeDevErr(errStr)
        except:
            raise

        return rootDevCfg

    def _getDevs(self, rootDevCfg):
        devs={}

        if rootDevCfg is None:
            errStr="No root configuration"
            raise ShoeDevErr(errStr)

        try:
            devList=\
                rootDevCfg[self.DEVLIST_KEYS[0]]\
                            [self.DEVLIST_KEYS[1]]
        except KeyError:
            devList=[]
            pass
        except:
            raise

        for devCfg in devList:
            shoeDev=ShoeDev(devCfg)
            shoeDev.init()
            devs[shoeDev.name]=shoeDev

        return devs

    def getDev(self, name):
        try:
            dev=self._devs[name]
        except TypeError:
            errStr="Device Configuration Not Initialized"
            raise ShoeDevErr(errStr)
        except KeyError:
            errStr="Device Tag %s Not Available. Choices are %s"\
                % (devTag, self._devs.keys())
            raise ShoeDevErr(errStr)
        except:
            raise

        return dev

    def _setSysName(self):
        self.sysName=None
