##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeOp.py
#Base class for CLI functions
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
from console_log import *
from .shoeRoot import *
from .shoeMsg import *
from collections.abc import Iterable
from collections import OrderedDict
from .shoeVer import SHOE_VERSION

class ShoeOp():
    CURRSTATE_CMND='GetCurrentState'
    FMT_LBL_LEN=16
    FMT_TAB_LEN=4

    CFG_DEV='ACT-Denon'
    CFG_SVC='ACT'
    CFG_TOKEN_CMND='GetConfigurationToken'

    CFG_SET_NAME_CMND='SetFriendlyName'
    CFG_GET_NAME_CMND='GetFriendlyName'

    CFG_APPLY_CHANGE='ApplyChanges'

    def __init__(self, shoeRoot, loglvl=0):
        self.log=ConsoleLog(self.__class__.__name__, loglvl)
        self.shoeRoot=shoeRoot
        self.loglvl=loglvl
        return

    def getInfo(self, infoLvl=0):
        infoFmt=self._fmtOp(self.shoeRoot.info)
        self.log.info("Info Level %s", infoLvl)
        if infoLvl > 0:
            devNames=[]
            if infoLvl==1:
                devNames=ShoeRoot.PREFERRED_DEVS
            elif infoLvl >= 2:
                devNames=self.shoeRoot.devNames

            self.log.debug("Info Level Devs %s", devNames)

            currStLocs=OrderedDict()
            for devName in devNames:
                self.log.debug("Find Dev %s", devName)
                cmndLocs=self.shoeRoot.findCmnd(self.CURRSTATE_CMND, None, devName)
                self.log.debug("Found Locs %s", cmndLocs)
                currStLocs.update(cmndLocs)

            self.log.debug("Curr State Locs %s" % currStLocs)

            for devName, svcNames in currStLocs.items():
                for svcName in svcNames:
                    self.log.debug("Getting CurrSt %s %s" % (svcName, devName))
                    try:
                        cmndResp=self.runCmnd(self.CURRSTATE_CMND, None, svcName, devName)
                    except ShoeMsgHttpRtnStatusErr:
                        pass

                    self.log.debug("Cmnd Resp %s" % str(cmndResp))
                    infoFmt += self._fmtOp(cmndResp)

        return infoFmt

    def getCfgToken(self):
        cmndRtn=self.shoeRoot.sendCmnd(self.CFG_TOKEN_CMND,
                                        None,
                                        self.CFG_SVC,
                                        self.CFG_DEV)

        return cmndRtn.args['configurationToken']

    def applyChanges(self):
        self.shoeRoot.sendCmnd(self.CFG_APPLY_CHANGE, None, self.CFG_SVC, self.CFG_DEV)
        return

    def setName(self, name):
        args=OrderedDict()
        args['configurationToken']=self.getCfgToken()
        args['friendlyName']=name

        self.shoeRoot.sendCmnd(self.CFG_SET_NAME_CMND, args, self.CFG_SVC, self.CFG_DEV)
        self.applyChanges()

        cmndRtn=self.shoeRoot.sendCmnd(self.CFG_GET_NAME_CMND, None,
                                        self.CFG_SVC, self.CFG_DEV)

        return cmndRtn.args['friendlyName']

    def runCmnd(self, cmnd, args, svcName=None, devName=None, shoeRoot=None):
        if shoeRoot is None:
            shoeRoot=self.shoeRoot

        cmndLocs=shoeRoot.findCmnd(cmnd, svcName, devName)
        cmndRtnStr = ''

        for devName, svcNames in cmndLocs.items():
            for svcName in svcNames:
                try:
                    cmndRtn=shoeRoot.sendCmnd(cmnd, args, svcName, devName)
                    self.log.debug("Command Return:\n%s" % str(cmndRtn))
                    cmndRtnStr += "\nCmnd: %s   Service: %s   Device: %s\n" % \
                               (cmndRtn.cmnd, svcName, devName)
                    cmndRtnStr += self._fmtOp(cmndRtn.args)

                except ShoeMsgHttpRtnStatusErr as e:
                    self.log.debug("HTTP Return Error Code %s, \
                            cmnd %s: svcName %s, devName %s, \
                            host %s: \n" % \
                            (str(e), cmnd, svcName, devName, shoeRoot.host))
                    cmndRtnStr += "HTTP Return Error Code %s\n" % (str(e))

                self.log.debug("Cmnd Return String:\n%s" % cmndRtnStr)

        return cmndRtnStr

    def showCmndTree(self, devName=None, showAll=False):
        cmndTree=self.shoeRoot.getCmndTree()

        showDevs=None
        showTree={}

        if devName is not None:
            showDevs=[devName,]
        elif not showAll:
            showDevs=ShoeRoot.PREFERRED_DEVS

        if showDevs is None:
            devCmndTree=cmndTree
        else:
            self.log.debug(showDevs)
            devCmndTree=OrderedDict([(devName, cmndTree[devName]) for devName in showDevs])

        for devName, svcCmndTree in devCmndTree.items():
            devLbl="Device: %s" % devName
            svcShowTree={}

            for svcName, cmndList in svcCmndTree.items():
                svcLbl="Service: %s" % svcName
                svcShowTree[svcLbl]=cmndList

            showTree[devLbl]=svcShowTree

        self.log.debug("ShowTree %s", showTree)

        fmtTree = self._fmtOp(showTree)
        self.log.debug("Fmt Tree:\n %s", fmtTree)
        return fmtTree

    def showCmndInfo(self, cmnd, svcName=None, devName=None):
        cmndLocs=self.shoeRoot.findCmnd(cmnd, svcName, devName)
        self.log.debug("Cmnd %s Device: %s Service: %s", cmnd, devName, svcName)

        cmndInfoStr=""

        self.log.debug("Cmnd Locs %s" % cmndLocs)
        for devName, svcNames in cmndLocs.items():
            for svcName in svcNames:
                cmndInfoStr += "Cmnd:    %s \nDevice:  %s \nService: %s\n" % \
                                (cmnd, devName, svcName)
                self.log.debug("Cmnd %s Device: %s Service: %s", cmnd, devName, svcName)
                cmndParams=self.shoeRoot.getCmndParams(cmnd, svcName, devName)

                #Remove redundant info for display
                for cmndParam in cmndParams:
                    try:
                        del cmndParam[ShoeSvc.STATEVAR_KEY]
                    except KeyError:
                        pass

                    try:
                        del cmndParam[ShoeSvc.STATE_KEY][ShoeSvc.NAME_KEY]
                    except KeyError:
                        pass

                fmtParams=self._fmtOp({'Parameters' : cmndParams})
                cmndInfoStr += fmtParams
                cmndInfoStr += "\n"
                self.log.debug2("Command Info:\n %s" % fmtParams)

        return cmndInfoStr

    def getVersion(self):
        return SHOE_VERSION

    def _fmtOp(self, opData, tab=0):
        fmt= '{0:>%s}{1:%s} : {2:<0}\n'%(tab, self.FMT_LBL_LEN)
        lblessFmt= '{0:>%s}{1:%s}   {2:<0}\n'%(tab, self.FMT_LBL_LEN)
        fmtStr=''

        try:
            self.log.debug2("OpData %s", opData)

            for lbl,val in opData.items():
                self.log.debug2("OpData Value [lbl]: %s [val]: %s [type]: %s",
                        lbl, val, type(val))
                valType=type(val)
                if valType is dict or valType is OrderedDict:
                    fmtStr=fmtStr+fmt.format('', str(lbl), '')
                    fmtStr=fmtStr+self._fmtOp(val, tab+self.FMT_TAB_LEN)
                elif valType is list:
                    fmtStr=fmtStr+fmt.format('', lbl, '')
                    lstBreak='-'*self.FMT_LBL_LEN
                    fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')
                    first=True
                    for valEl in val:
                        if first:
                            first=False
                        else:
                            if isinstance(valEl, Iterable) and type(valEl) != str:
                                fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')

                        self.log.debug2("List Element %s", valEl)
                        listElStr=self._fmtOp(valEl, tab+self.FMT_TAB_LEN)
                        self.log.debug2("List Element String %s", listElStr)
                        fmtStr=fmtStr+listElStr
                    fmtStr=fmtStr+lblessFmt.format('', lstBreak, '')
                elif valType is bytes:
                    fmtStr=fmtStr+fmt.format('', str(lbl), str(val.decode()))
                else:
                    fmtStr=fmtStr+fmt.format('', str(lbl), str(val))

        except AttributeError:
            self.log.debug2("OpData Not Iterable %s", opData)
            fmtStr=fmtStr+lblessFmt.format('', '', str(opData))
            pass

        except:
            raise

        return fmtStr
