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
from shoeMsg import *
from shoeEventParser import *
from collections import OrderedDict
import copy
import sys
from collections import defaultdict

class ShoeCmnd(ShoeMsg):
    def __init__(self,
                host, path, urn,
                cmnd, argsIn=OrderedDict(), argsCfg=None,
                port=60006,
                loglvl=None):

        super().__init__(host=host,
                        path=path,
                        cmnd=cmnd,
                        urn=urn,
                        loglvl=loglvl)

        self.argsIn = argsIn
        self.argsCfg = argsCfg
        self.cmndReply=None

        self.log.debug("Cmnd %s" % cmnd)
        self.log.debug("Args %s" % argsIn)
        self.log.debug("ArgsCfg %s" % self.argsCfg)

        return

    def send(self):
        self.log.debug("Send Cmnd: %s \nArgs: %s \nArgsCfg: %s" %
                        (self.cmnd, self.argsIn, self.argsCfg))
        self.args=self._formatCmnd(self.argsIn, self.argsCfg)
        super().send()
        return

    def parse(self):
        msgReply = super().parse()

        self.log.debug("Cmnd %s" % self.cmnd)
        self.log.debug("Args %s" % self.args)
        self.log.debug("ArgsCfg %s" % self.argsCfg)

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

            self._checkAllowedVals(fmtArgVal, argCfg)
            self._checkAllowedRange(fmtArgVal, argCfg)

            fmtArgs[argName] = fmtArgVal

        return fmtArgs

    def _formatReplyArg(self, arg, argCfg):
        stateCfg=argCfg['state']
        cfgArgType=stateCfg['dataType']
        event=stateCfg['@sendEvents']
        replyTrue=['true', 'True', 'TRUE', True]
        replyFalse=['false', 'False', 'FALSE', False]

        self.log.debug("ArgType %s Event %s", cfgArgType, event)

        errMsg='Incorrect Type %s for reply arg %s' %\
                (cfgArgType, arg)

        if (cfgArgType == 'string'):
            if (type(arg) is not str):
                raise ShoeCmndErr(errMsg)
            if event == 'yes':
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
                argRtn=int(arg)
            except ValueError:
                raise ShoeCmndErr(errMsg)
            except:
                raise

        return argRtn

    def _formatCmndArg(self, argVal, argCfg):
        cmndArgs={}

        stateCfg=argCfg['state']
        cfgArgType=stateCfg['dataType']

        errMsg='Incorrect Type %s for send argVal %s' %\
                (cfgArgType, argVal)

        if (cfgArgType == 'string'):
            if (type(argVal) is not str):
                raise ShoeCmndErr(errMsg)
            argRtn=argVal

        elif (cfgArgType == 'boolean'):
            if(type(argVal) is not bool):
                raise ShoeCmndErr(errMsg)

            if argVal == True:
                argRtn = 'true'
            else:
                argRtn = 'false'

        elif (cfgArgType[:2] == 'ui'):
            try:
                argRtn=str(int(argVal))
            except ValueError:
                raise ShoeCmndErr(errMsg)
            except:
                raise

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
        self.cmnds=self.testRootDev.cmnds
        self.cmnd = None
        return

    def _sendTestMsgs(self):
        self.shoeCmnd = ShoeCmnd(host=self.host,
                                path=self.path,
                                urn=self.urn,
                                cmnd=self.cmnd.name,
                                argsIn=self.cmnd.args,
                                argsCfg=self.cmnd.argsCfg,
                                loglvl=logging.DEBUG)
        self.shoeCmnd.send()
        self.shoeCmnd.parse()
        self._checkMsg(self.cmnd)
        return

class TestShoeCmnds(TestShoeCmnd):
    def runTest(self):
        for cmnd in self.cmnds:
            self.cmnd = cmnd
            print("@@@@@@@@@@@@@@@@@@@@@@@ %s: Test %s @@@@@@@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, cmnd.name))
            self.httpTest(cmnd)
            print("@@@@@@@@@@@@@@@@@@@@@ %s: Test Done %s @@@@@@@@@@@@@@@@@@@@@@@@"\
                    % (self.__class__.__name__, cmnd.name))

            if self.FAST_TEST>0 and self.sendCnt > self.FAST_TEST:
                    break

        return

    def _checkMsg(self, cmnd):
        self.assertEqual(self.shoeCmnd.cmnd, cmnd.name, 'Parse error: cmnd')
        self.assertEqual(self.shoeCmnd.urn, cmnd.urn, 'Parse error: urn')
        self.assertEqual(self.shoeCmnd.args, cmnd.args, 'Parse error: urn')
        self.assertEqual(self.srvRxMsg, cmnd.msg)
        self.assertEqual(self.srvRxHdr, cmnd.hdr)

        reply=self.shoeCmnd.cmndReply

        print("reply", reply.args)
        print("expected", cmnd.rtn)

        self.assertEqual(reply.cmnd, cmnd.name + "Response", 'ParseErr: cmnd')
        self.assertEqual(reply.urn, cmnd.urn, 'ParseErr: urn')
        self.assertDictEqual(reply.args, cmnd.rtn)
        #self.assertDictEqual(reply.args, cmnd.msgReplyArgs, 'Parse error: args\r %s \r %s' %
        #        (reply.args, cmnd.msgReplyArgs) )

        return
