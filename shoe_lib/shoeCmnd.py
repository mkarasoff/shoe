##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#shoeCmnd.py
#Class that impliments commands for HEOS.
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
from .shoeMsg import *
from .shoeEventParser import *
from collections import OrderedDict
import copy
import sys
from collections import defaultdict

class ShoeCmnd(ShoeMsg):
    EVENT_TAG='<Event'
    EVENT_IDX=6

    def __init__(self,
                host, path, urn,
                cmnd, argsIn=OrderedDict(),
                argsCfg=None,
                port=60006,
                loglvl=None,
                force=False):

        super().__init__(host=host,
                        path=path,
                        cmnd=cmnd,
                        urn=urn,
                        loglvl=loglvl)

        self.argsIn = argsIn
        self.argsCfg = argsCfg
        self.cmndReply=None
        self.force=force

        self.log.debug("Cmnd %s" % cmnd)
        self.log.debug("Args %s" % argsIn)
        self.log.debug("ArgsCfg %s" % self.argsCfg)

        return

    def send(self):
        self.log.debug("Send Cmnd: %s \nArgs: %s \nArgsCfg: %s" %
                        (self.cmnd, self.argsIn, self.argsCfg))

        if self.force:
            self.args=self.argsIn
        else:
            self.args=self._formatCmnd(self.argsIn, self.argsCfg)
        super().send()
        return

    def parse(self):
        msgReply = super().parse()

        self.log.debug("Cmnd %s" % self.cmnd)
        self.log.debug("Args %s" % self.args)
        self.log.debug("ArgsCfg %s" % self.argsCfg)

        replyArgs={}

        if self.force:
            replyArgs=msgReply.args
        else:
            replyArgs=self._formatReply(msgReply.args, self.argsCfg)

        self.cmndReply = ShoeMsgXml.ShoeMsgParse(cmnd=msgReply.cmnd,
                                            urn=msgReply.urn,
                                            args=replyArgs)

        self.log.debug("CmndReplys %s" % str(self.cmndReply))

        return self.cmndReply

    def _formatReply(self, args, argsCfg):
        self.log.debug("ArgsCfg %s" % self.argsCfg)

        replyArgsCfg={}
        for argCfg in argsCfg:
            self.log.debug("ArgCfg: %s" % argCfg)
            if argCfg['direction'] == 'out':
                replyArgsCfg[argCfg['name']]=argCfg

        return self._formatArgs(args, replyArgsCfg,
                                self._formatReplyArg)

    def _formatCmnd(self, args, argsCfg):
        cmndArgsCfg=OrderedDict()
        for argCfg in argsCfg:
            if argCfg['direction'] == 'in':
                cmndArgsCfg[argCfg['name']]=argCfg

        self.log.debug("CmndArgsCfg: %s" % cmndArgsCfg)
        return self._formatArgs(args, cmndArgsCfg,
                                self._formatCmndArg)

    def _formatArgs(self, args, argsCfg, formatFunc=None):
        fmtArgs=OrderedDict()

        if args is None:
            args={}

        for argName, argVal in args.items():
            try:
                self.log.debug("Args Cfg: %s", argsCfg)
                argCfg=argsCfg[argName]
            except KeyError:
                errMsg="Invalid Arg %s" % argName
                raise ShoeCmndErr(errMsg)
            except:
                raise

            if formatFunc is not None:
                fmtArgVal = formatFunc(argVal, argCfg)

            fmtArgs[argName] = fmtArgVal

        return fmtArgs

    def _formatReplyArg(self, arg, argCfg):
        stateCfg=argCfg['state']
        cfgArgType=stateCfg['dataType']
        replyTrue=['true', 'True', 'TRUE', True]
        replyFalse=['false', 'False', 'FALSE', False]

        self.log.debug("ArgType %s", cfgArgType)
        self.log.debug("Arg %s", arg)

        errMsg='Incorrect Type %s for reply arg %s' %\
                (cfgArgType, arg)

        if (cfgArgType == 'string'):
            if (type(arg) is not str):
                raise ShoeCmndErr(errMsg)

            if arg[:self.EVENT_IDX] == self.EVENT_TAG:
                eventParser=ShoeEventParser(arg, self.loglvl)
                argRtn=eventParser.parse()
            else:
                argRtn=arg

        elif (cfgArgType == 'boolean'):
            if(int(arg) != 0 and int(arg) != 1):
                raise ShoeCmndErr(errMsg)

            argRtn = str(int(arg))

        elif (cfgArgType[:2] == 'ui'):
            try:
                argRtn=int(arg)
            except ValueError:
                raise ShoeCmndErr(errMsg)
            except:
                raise

        return argRtn

    def _formatCmndArg(self, arg, argCfg):
        cmndArgs={}

        self.log.debug("Arg %s Cfg %s", arg, argCfg)
        stateCfg=argCfg['state']

        self.log.debug("StateCfg %s", stateCfg)
        cfgArgType=stateCfg['dataType']

        errMsg='Incorrect Type %s for send arg %s' %\
                (cfgArgType, arg)

        if (cfgArgType == 'string'):
            if (type(arg) is not str):
                raise ShoeCmndErr(errMsg)
            argRtn=arg

        elif (cfgArgType == 'boolean'):
            if(int(arg) != 0 and int(arg) != 1):
                raise ShoeCmndErr(errMsg)

            argRtn = str(int(arg))

        elif (cfgArgType[:2] == 'ui'):
            try:
                argRtn=str(int(arg))
            except ValueError:
                raise ShoeCmndErr(errMsg)
            except:
                raise

        self._checkAllowedVals(argRtn, argCfg)
        self._checkAllowedRange(argRtn, argCfg)

        return argRtn

    def _checkAllowedVals(self, argVal, argCfg):
        stateCfg=argCfg['state']
        try:
            errMsg='Value %s not allowed' % argVal
            allowedVals=stateCfg['allowedValueList']['allowedValues']
            if argVal not in allowedVals:
                raise ShoeCmndErr(errMsg)
        except KeyError:
            pass
        except:
            raise
        return

    def _checkAllowedRange(self, argVal, argCfg):
        stateCfg=argCfg['state']

        try:
            errMsg='Value %s out of bounds' % argVal
            allowedRange=stateCfg['allowedValueRange']
            minVal=int(allowedRange['minimum'])
            maxVal=int(allowedRange['maximum'])
            step=int(allowedRange['step'])

            argVal=int(argVal)

            if argVal<minVal or argVal>maxVal:
                raise ShoeCmndErr(errMsg)

            if ((argVal-minVal)%step) != 0:
                raise ShoeCmndErr(errMsg)

        except KeyError:
            pass

        except:
            raise

        return
###############################Exceptions#################################
class ShoeCmndErr(Exception):
    pass
