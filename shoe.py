#!/usr/bin/python3
##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#Top level script.  Run This!
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

import argparse
import sys
from console_log import ConsoleLog
from collections import OrderedDict
from shoeOp import *
from shoeRoot import *
from shoeMsg import *

parser = argparse.ArgumentParser()

parser.add_argument('-q', '--quiet', help="make output quiet",
                    action='store_true')

parser.add_argument('-v', '--verbose', help="increase output verbosity",
                    action='count', default=0)

parser.add_argument('-H', '--Host', dest='hostIps', nargs='+', required=True,
                        action='append',
                    help="This will set the host for the operation, usually "\
                            "an IP address.  At least one host is required.  "\
                            "For some operations (e.g. -b) multiple hosts "\
                            "can be given.  If only one host is required for "\
                            "the command, then the first host will be used")

parser.add_argument('-i', '--info', dest='info', action='count', default=0,
                        help="Displays info for devices.")

parser.add_argument('-t', '--tree', dest='showTree', action='count', default=0,
                        help="Displays Command Tree.")

parser.add_argument('-n', '--name', dest='spkrName', default=None,
                            metavar='<Speaker Name>',
                        help="This will name a speaker.  If multiple hosts "\
                               "are given, multiple names may also be "\
                               "given.  Names will be assigned in order of"\
                               "hosts given by the (-H) command")

#parser.add_argument('-b', '--bond', dest='bondName', metavar='<Bond Name>',
#                                    nargs=1,
#                        help="This will bond all hosts given on command "\
#                                "line with the (-H) command, making a "\
#                                "multichannel speaker grouping with the name "\
#                                "<Bond Name>. The channel assignment will be "\
#                                "based on the order of hosts given by the "\
#                                "(-H) command: Right, Left, RearR, RearL, "\
#                                "Center, Sub. If two speakers are given, "\
#                                "the pair will be stereo, and surround "\
#                                "speakers will be added for more than two "\
#                                "speakers. Speaker channels can be modified "\
#                                "with the (-s) command.")
#
#parser.add_argument('-s', '--schan', metavar='<Speaker Channel>',
#                         nargs='+', action='append',
#                        choices=['NORMAL', 'LEFT', 'RIGHT',
#                                'REAR_LEFT', 'REAR_RIGHT', 'LOW_FREQUENCY'],
#                        help="Sets the speaker channel for the host given by"\
#                                "(-H). If multiple hosts are given, then "\
#                                "multiple channels can be assigned in order "\
#                                "of hosts. Can be one of the following: "\
#                               "['NORMAL', 'LEFT', 'RIGHT', 'REAR_LEFT', "\
#                                   "'REAR_RIGHT', 'LOW_FREQUENCY']" )

parser.add_argument('-d', '--device', dest='device', default=None,
                        metavar='<Device Name>',
                    help="Select a device. ")

parser.add_argument('-s', '--service', dest='service', default=None,
                        metavar='<Service Name>',
                    help="Select a service. ")

parser.add_argument('-e', '--expert', dest='expertCmnd', default=None,
                        metavar='<Expert Command>',
                    help="Select an expert command.  This can only be done "\
                            "on a single host.  If no argument is given, "\
                            "then the command will list all available expert "\
                            "commands for the host given by (-H).")

parser.add_argument('-a', '--arg', dest='cmndArgs', nargs=2 , action='append',
                        metavar=('<Name>', '<Value>'),
                    help="Set an argument given to an expert command (-e). "\
                            "Must give two values:  \n"\
                        "<Name> indicates the name of the argument.  "\
                        "<Value> indicates the value of the argument.  "\
                        "For commands that require multiple arguments, "\
                        "use more (-a). If all required arguments are "\
                        "given, with -e, the command will run.")

parser.add_argument('-l', '--list', nargs='+', dest='listArgsCmnds',
                       metavar='<Command>',
                    help="List expert commands arguments. Returns a list "\
                            "of args and arg value types for the "\
                            "command given by (-e)." )

def main():
    args=parser.parse_args()

    quite=False

    loglvl=ConsoleLog.WARNING

    if args.verbose==1:
        loglvl=ConsoleLog.INFO
    elif args.verbose==2:
        loglvl=ConsoleLog.DEBUG
    elif args.verbose >= 3:
        loglvl=ConsoleLog.DEBUG2
    elif args.quiet==True:
        loglvl=ConsoleLog.ERROR
        quite=True

    log=ConsoleLog("shoe", loglvl)
    log.info("ARGS:%s", args)

    hostRoot=OrderedDict()

    hostIps=[ip for argIps in args.hostIps for ip in argIps]

    for hostIp in hostIps:
        hostRoot[hostIp]=ShoeRoot(host=hostIp, loglvl=loglvl)
        hostRoot[hostIp].setUp()

    ops={}
    for hostIp in hostIps:
        ops[hostIp]=ShoeOp(shoeRoot=hostRoot[hostIp],
                            loglvl=loglvl)

    if args.info > 0:
        for hostIp in hostIps:
            infoRtn=ops[hostIp].getInfo(args.info-1)
            print("\nInfo for", hostIp)
            print("----------------")
            print(infoRtn)

    if args.showTree > 0:
        showAll = True if args.showTree == 2 else False
        for hostIp in hostIps:
            fmtCmndTree=ops[hostIp].showCmndTree(args.device, showAll)
            print(fmtCmndTree)

    if args.listArgsCmnds is not None:
        for hostIp in hostIps:
            for listArgsCmnd in args.listArgsCmnds:
                listArgsFmt=\
                        ops[hostIp].showCmndInfo(listArgsCmnd,
                                                args.service,
                                                args.device)
                print(listArgsFmt)

    cmndArgs = OrderedDict() if args.cmndArgs is None \
            else OrderedDict(args.cmndArgs)

    if args.expertCmnd is not None:
        for hostIp in hostIps:
            cmndRtnFmt=ops[hostIp].runCmnd(args.expertCmnd,
                                            cmndArgs,
                                            args.service,
                                            args.device)

            print(cmndRtnFmt)

    if args.spkrName is not None:
        cmndRtn=ops[hostIps[0]].setName(args.spkrName)
        print("Set name to", cmndRtn)

    return

if __name__=="__main__":
    main()
