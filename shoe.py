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
from collections import OrderedDict
import shoe_lib
from shoe_lib.shoeRoot import *
from shoe_lib.shoeDev import *
from shoe_lib.shoeOp import *

parser = argparse.ArgumentParser()

parser.add_argument('-q', '--quiet', help="make output quiet",
                    action='store_true')

parser.add_argument('-v', '--verbose', action='count', default=0,\
                    help="Increase output verbosity.  \'-vv\' and \'-vvv\' "\
                        "will show more.")

parser.add_argument('-H', '--Host', dest='hosts', nargs='+', required=True,
                        action='append',
                    help="This will set the host for the operation, usually "\
                            "an IP address.  At least one host is required.  "\
                            "For some operations (e.g. -b) multiple hosts "\
                            "can be given.  If only one host is required for "\
                            "the command, then the first host will be used. \n"\
                                "Port can be specified with \':\' as in "\
                                "\'<host>:<port>\'")

parser.add_argument('-i', '--info', dest='info', action='count', default=0,
                        help="Displays info for devices. \'-ii\' and \'-iii\' "\
                                "will show more")

parser.add_argument('-t', '--tree', dest='showTree', action='count', default=0,
                        help="Displays Command Tree. Defaults to showing commands "\
                                "from AIOS, Group, and  Zone services.  Add a "\
                                "second t, \'-tt\' to show commands from all services.")

parser.add_argument('-n', '--name', dest='spkrName', default=None,
                            metavar='<Speaker Name>',
                        help="This will name a speaker.  If multiple hosts "\
                               "are given, multiple names may also be "\
                               "given.  Names will be assigned in order of"\
                               "hosts given by the (-H) command")

parser.add_argument('-u', '--unBond', action='store_true',
                        help="This will delete the bond")

parser.add_argument('-b', '--bond', dest='bondName', nargs=1,
                                   metavar='<Bond Name>',
                        help="This will bond all hosts given on command "\
                                "line with the (-H) command, making a "\
                                "multichannel speaker grouping with the name "\
                                "<Bond Name>. The channel assignment will be "\
                                "based on the order of hosts given by the "\
                                "(-H) command: Left, Right, RearL, RearR, "\
                                "Center, Sub. If two speakers are given, "\
                                "the pair will be stereo, and surround "\
                                "speakers will be added for more than two "\
                                "speakers. Speaker channels can be modified "\
                                "with the (-s) command.")

parser.add_argument('-s', '--swap', action='store_true',
                        help="Swaps left and right speakers")

parser.add_argument('-f', '--force', action='store_true',
                        help="Send commmand without parameter checks. Requires "\
                                "\'-D\' and \'-S\' options to work correctly" )

parser.add_argument('-D', '--device', dest='device', default=None,
                        metavar='<Device Name>',
                    help="Select a device. ")

parser.add_argument('-F', '--rootFileName', default=None,
                        metavar='<Root File Name>',
                    help="Use file given by <Root File Name> for the root "\
                            "configuration, rather than URL.")

parser.add_argument('-S', '--service', dest='service', default=None,
                        metavar='<Service Name>',
                    help="Select a service. ")

parser.add_argument('-x', '--rootUrlPath', default=ShoeRoot.AIOS_CFG_PATH,
                        metavar='<Root URL Path>',
                    help="Specifies a URL for the root XML configuration file. "\
                            "By default, this is the config path is \"%s\", for HEOS1 "\
                            "running firmware version 1.520.200" % \
                                ShoeRoot.AIOS_CFG_PATH)

parser.add_argument('-c', '--cmnd', dest='cmnd', default=None,
                        metavar='<Command>',
                    help="Select a command.  The command can be "\
                            "followed by (-a) to give arguments for "\
                            "the command.  If multiple hosts are "\
                            "given with the (-H) option, the command "\
                            "will be run on all hosts.  If device and "\
                            "service are not specified with (-d) and "\
                            "(-s) options, and the command name is "\
                            "duplicated across services, it will be "\
                            "run on all matching services.")

parser.add_argument('-a', '--arg', dest='cmndArgs', nargs=2 , action='append',
                        metavar=('<Name>', '<Value>'),
                    help="Set an argument given to an expert command (-e). "\
                            "Must give two values:  \n"\
                        "<Name> indicates the name of the argument.  "\
                        "<Value> indicates the value of the argument.  "\
                        "For commands that require multiple arguments, "\
                        "use more (-a). If all required arguments are "\
                        "given, with -e, the command will run.")

parser.add_argument('-p', '--param', nargs='+', dest='parmaArgs',
                       metavar='<Command>',
                    help="List command argument parameters. Returns "\
                            "hints for argument parameters for the "\
                            "command given by (-c)." )

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

    hostRoots=OrderedDict()

    #Host IPs come in as list of lists.  Flatten it here.
    hosts=[host for argHosts in args.hosts for host in argHosts]

    for host in hosts:
        hostIpPort=host.split(':')
        hostIp=hostIpPort[0]
        hostPort=ShoeRoot.DFLT_PORT
        if len(hostIpPort) == 2:
            hostPort=hostIpPort[1]

        hostRoots[host]=ShoeRoot(host=hostIp,
                                    port=hostPort,
                                    path=args.rootUrlPath,
                                    fileName=args.rootFileName,
                                    force=args.force,
                                    loglvl=loglvl)
        hostRoots[host].setUp()

    if args.bondName is not None:
        bondOp=ShoeBond(spkrRoots=list(hostRoots.values()), loglvl=loglvl)
        bondRtn=bondOp.bondSpkrs(args.bondName[0])
        print(bondRtn)

    elif args.unBond is True:
        bondOp=ShoeBond(spkrRoots=list(hostRoots.values()), loglvl=loglvl)
        try:
            bondRtn=bondOp.unbondSpkrs()
            print(bondRtn)
        except ShoeBondGroupErr as e:
            print(str(e))

    elif args.swap is True:
        bondOp=ShoeBond(spkrRoots=list(hostRoots.values()), loglvl=loglvl)
        bondRtn=bondOp.swapStereoSpkrs()
        print(bondRtn)

    else:
        ops={}
        for host in hosts:
            ops[host]=ShoeOp(shoeRoot=hostRoots[host],
                                loglvl=loglvl)

        if args.info > 0:
            for host in hosts:
                infoRtn=ops[host].getInfo(args.info-1)
                print("\nInfo for", host)
                print("----------------")
                print(infoRtn)

        if args.showTree > 0:
            showAll = True if args.showTree == 2 else False
            for host in hosts:
                fmtCmndTree=ops[host].showCmndTree(args.device, showAll)
                print(fmtCmndTree)

        if args.parmaArgs is not None:
            for host in hosts:
                for listArgsCmnd in args.parmaArgs:
                    listArgsFmt=\
                            ops[host].showCmndInfo(listArgsCmnd,
                                                    args.service,
                                                    args.device)
                    print(listArgsFmt)

        cmndArgs = OrderedDict() if args.cmndArgs is None \
                else OrderedDict(args.cmndArgs)

        if args.cmnd is not None:
            for host in hosts:
                cmndRtnFmt=ops[host].runCmnd(args.cmnd,
                                                cmndArgs,
                                                args.service,
                                                args.device)

                print(cmndRtnFmt)

        if args.spkrName is not None:
            cmndRtn=ops[hosts[0]].setName(args.spkrName)
            print("Set name to", cmndRtn)

    return

if __name__=="__main__":
    main()
