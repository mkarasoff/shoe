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
from shoeSvcAct import *
from shoeSvcGroup import *
from shoeSvcZone import *
from shoeCmnd import *
from collections import OrderedDict
import copy
import sys
from collections import defaultdict
from consoleLog import *

class ShoeCmnd(ShoeMsg):
    def __init__(self,
                host, path, urn,
                cmnd, argsIn=OrderedDict(), argsCfg=None,
                port=60006,
                loglvl=0
                ):

        super.__init__(host=host,
                        path=path,
                        cmnd=cmnd,
                        urn=urn)

        self.log=ConsoleLog(self.__class__.__name__, loglvl)

        self.cmnd = cmnd
        self.argsIn = argsIn
        self.argsCfg = argsCfg

        self.loglvl = loglvl
        self.cmndReply=None
        return

    def send(self):
        self.args=self._formatCmnd(self.argsIn, self.argsCfg)
        super().send()
        return

    def parse(self):
        msgReply = super.parse()

        replyArgs=self._formatReply(msgReply.args, self.argsCfg)

        self.cmndReply = ShoeMsgXml.ShoeMsgParse(cmnd=cmndReply.cmnd,
                                            urn=cmndReply.urn,
                                            args=replyArgs)

        self.log.debug("CmndReplys %s" % self.cmndReply)

        return self.cmndReply

    def _formatReply(self, args, argsCfg):
        return self._formatArgs(args, argsCfg,
                                self._formatReplyArg)

    def _formatCmnd(self, args, argsCfg):
        return self._formatArgs(args, argsCfg,
                                self._formatCmndArg)

    def _formatArgs(self, args, argsCfg, formatFunc=None):
        fmtArgs=OrderedDict()

        for argName, argVal in args.items():
            try:
                argCfg=self.argsCfg[argName]
            except KeyError:
                errMsg="Invalid Arg %s" % argName
                raise ShoeCmndErr(errMsg)
            except:
                raise

            if formatFunc is not None:
                fmtArgVal = formatFunc(argVal, argCfg)

            self._checkAllowedVals(argVal, argCfg)
            self._checkAllowedRange(argVal, argCfg)

            fmtArgs[argName] = fmtArgVal

        return fmtArgs

    def _formatReplyArg(self, arg, argCfg):
        if argCfg['direction'] is not 'out':
            errMsg="Not Output Arg %s" % argName
            raise ShoeCmndErr(errMsg)

        stateCfg=argCfg['state']
        cfgArgType=stateCfg['dataType']
        event=stateCfg['@sendEvents']
        replyTrue=['true', 'True', 'TRUE', True]
        replyFalse=['false', 'False', 'FALSE', False]

        errMsg='Incorrect Type %s for reply arg %s' %\
                (cfgArgType, arg)

        if (cfgArgType == 'string'):
            if (type(arg) is not str):
                raise ShoeCmndErr(errMsg)
            if event is 'yes':
                eventParser=ShoeEventParser(arg, self.loglvl)
                argRtn=eventParser.parse()
            else:
                argRtn=arg

        elif (cfgArgType == 'boolean'):
            if arg in replyTrue:
                argRtn = True
            elif arg == replyFalse:
                argRtn = False
            else:
                raise ShoeCmndErr(errMsg)

        elif (cfgArgType[:2] == 'ui'):
            try:
                argRtn=int(str(arg))
            except ValueError:
                raise ShoeCmndErr(errMsg)
            except:
                raise

        return argRtn

    def _formatCmndArg(self, argVal, argCfg):
        if argCfg['direction'] is not 'in':
            errMsg="Not Input Arg %s" % argName
            raise ShoeCmndErr(errMsg)

        stateCfg=argCfg['state']
        cfgArgType=stateCfg['dataType']
        argType=type(argVal)

        errMsg='Incorrect Type %s for send argVal %s' %\
                (cfgArgType, argVal)

        if (cfgArgType == 'string'):
            if (argType is not str):
                raise ShoeCmndErr(errMsg)
            argRtn=argVal

        elif (cfgArgType == 'boolean'):
            if(argType is not bool):
                raise ShoeCmndErr(errMsg)

            if argVal == True:
                argRtn = 'true'
            else:
                argRtn = 'false'

        elif (cfgArgType[:2] == 'ui'):
            if(argType is not int):
                raise ShoeCmndErr(errMsg)
            argRtn=argVal

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

            if argVal<minVal or argVal>maxVal:
                raise ShoeCmndErr(errMsg)

            if ((argVal-minVal)%step) != 0:
                raise ShoeCmndErr(errMsg)
        except KeyError:
            pass
        except:
            raise
        return

##############################UNIT TESTS########################################
from test_shoe import *

class TestShoeCmnd(TestShoeHttp):
    #Set to 0 to do the long test.  Set to a number N>0 to itereate N
    FAST_TEST=0

    def setUp(self):
        super().setUp()

        self.port=60006
        self.host='127.0.0.1'
        self.testRootDev=TestRootDev()
        self.testCmnds=self.testRootDev.cmnds
        return

    def _sendTestMsgs(self):
        self.shoeCmnd = ShoeCmnd(host=self.host,
                                path=self.path,
                                urn=self.urn,
                                cmnd=self.cmnd,
                                argsIn=self.args,
                                argsCfg=self.argsCfg,
                                loglvl=logging.DEBUG)
        self.shoeCmnd.send()
        self.shoeCmnd.parse()
        self._checkMsg(self.testCmnd)
        return

class TestShoeCmnds(TestShoeCmnd):
    def runTest(self):
        for testCmnd in self.testCmnds:
            print("@@@@@@@@@@@@@@@@@@@@@@@ %s: Test %s @@@@@@@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, testCmnd.name))
            self.httpTest(testCmnd)
            print("@@@@@@@@@@@@@@@@@@@@@ %s: Test Done %s @@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, testCmnd.name))

            if self.FAST_TEST>0 and self.sendCnt > self.FAST_TEST:
                    break

        return

    def _checkMsg(self, testCmnd):
        self.assertEqual(self.shoeCmnd.cmnd, testCmnd.name, 'Parse error: cmnd')
        self.assertEqual(self.shoeCmnd.urn, testCmnd.urn, 'Parse error: urn')
        self.assertEqual(self.shoeCmnd.args, testCmnd.args, 'Parse error: urn')
        self.assertEqual(self.srvRxMsg, testCmnd.msg)
        self.assertEqual(self.srvRxHdr, testCmnd.hdr)

        reply=self.shoeCmnd.reply

        self.assertEqual(reply.cmnd, testCmnd.name + "Response", 'ParseErr: cmnd')
        self.assertEqual(reply.urn, testCmnd.urn, 'ParseErr: urn')
        self.assertDictEqual(reply.args, testCmnd.msgReplyArgs, 'Parse error: args\r %s \r %s' %
                (reply.args, testCmnd.msgReplyArgs) )

        return
