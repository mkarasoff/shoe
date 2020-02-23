##########################################################################
#consoleLog.py
#Generic console logger in a class
# This does some things differently than the stock logger:
# 1. It checks for duplicate logger names in the specified manager (default
#       is the standard 'root' manager), and refuses to log if the
#       same name exists.
# 2. It allows for an alternative manager, or, more helpful, no manager.
# 3. It manages level changes for the stream handler and log simultaniously.
# 4. It is a simple class, which I think is less unwieldy than the module
#       implementation normally seen in examples.
#
##########################################################################
#MIT License
#
#Copyright (c) 2020  Mike Karasoff, mike@karatronics.com
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#
############################################################################
import logging

class ConsoleLog(logging.getLoggerClass()):
    RT_FORMAT='[%(relativeCreated)d] %(levelname)s: %(message)s'
    DBUG_FORMAT='[%(asctime)s] '\
                '%(filename)s:%(lineno)s:%(funcName)s()  '\
                '%(levelname)s: %(message)s'

    DEBUG2  = logging.DEBUG-1
    DEBUG   = logging.DEBUG
    INFO    = logging.INFO
    WARNING = logging.WARNING
    ERROR   = logging.ERROR

    def __init__(self, name,
                    level=logging.WARNING,
                    manager=logging.root.manager):

        if level is None:
            level=self.WARNING

        self.name=self._getName(name, manager)
        super().__init__(self.name, level)

        self.ch = self._makeConsoleHndlr(level)

        self._setManager(manager)
        return

    def _setFormatter(self, fmt):
        if fmt is not None:
            self.formatter=logging.Formatter(fmt)

        return

    def _getName(self, name, manager):
        nameIter=0
        mgrNames=[]

        if manager is not None:
            mgrNames=manager.loggerDict.keys()

        for mgrName in mgrNames:
            (baseName, baseIter)=mgrName.split('.')
            if baseName == name:
                if nameIter <= int(baseIter):
                    nameIter=int(baseIter)+1

        return '%s.%s' % (name,nameIter)

    def _setManager(self, manager):
        self.manager=manager

        if manager is not None:
            logging._acquireLock()
            manager.loggerDict[self.name]=self
            #manager._fixupParents(self)
            logging._releaseLock()

        return

    def _makeConsoleHndlr(self, level):
        if level<=logging.WARNING:
            self._setFormatter(self.DBUG_FORMAT)
        else:
            self._setFormatter(self.RT_FORMAT)

        ch=logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(self.formatter)
        self.addHandler(ch)
        return ch

    def debug2(self, msg, *args, **kwargs):
        return self.log(self.DEBUG2, msg, *args, **kwargs)

    def setLevel(self, level):
        self.ch.setLevel(level)
        self.setLevel(level)
        return

class ConsoleLogError(Exception):
    pass

##############################UNIT TESTS########################################
import unittest
import io
import sys
from contextlib import redirect_stderr
from contextlib import redirect_stdout
import time

class TestConsoleLog(unittest.TestCase):
    def setUp(self):
        self.setUpLogger()
        self.clogPrtLvls=("WARNING", "ERROR")
        return

    def runTest(self):
        self.rply={}

        self.clog.warning("WARNING")
        self.rply["WARNING"]=self.logOut()

        self.clog.info("INFO")
        self.rply["INFO"]=self.logOut()

        self.clog.debug("DEBUG")
        self.rply["DEBUG"]=self.logOut()

        self.clog.error("ERROR")
        self.rply["ERROR"]=self.logOut()

        print("----------", self.__class__.__name__, "------------")
        for name in self.lvlNames:
            if name in self.clogPrtLvls:
                parseLst=self.rply[name].split()
                self.assertEqual(parseLst[-1], name)
            else:
                self.assertEqual(self.rply[name], '')
            print(name)
            print("*%s*" % self.rply[name])
        return

    def setUpLogger(self, level=None):
        self.name=self.__class__.__name__

        self.lvlNames=("ERROR", "WARNING", "INFO", "DEBUG")

        self.clog=None

        self.buf = io.StringIO()
        self.buf.truncate(0)

        if level is None:
            self.clog=ConsoleLog(self.name)
        else:
            self.clog=ConsoleLog(self.name, level)

        self.clog.ch.setStream(self.buf)
        return

    def logOut(self):
        logOut=self.buf.getvalue()
        self.buf.truncate(0)
        return logOut

class TestConsoleLogWarningLvl(TestConsoleLog):
    def setUp(self):
        self.clogPrtLvls=("WARNING", "ERROR")
        self.setUpLogger(logging.WARNING)
        return

class TestConsoleLogInfoLvl(TestConsoleLog):
    def setUp(self):
        self.clogPrtLvls=("ERROR", "WARNING", "INFO")
        self.setUpLogger(logging.INFO)
        return

class TestConsoleLogDbugLvl(TestConsoleLog):
    def setUp(self):
        self.clogPrtLvls=("ERROR", "WARNING", "INFO", "DEBUG")
        self.setUpLogger(logging.DEBUG)
        self.setUpLogger(logging.DEBUG)
        return

class TestConsoleLogErrorLvl(TestConsoleLog):
    def setUp(self):
        self.clogPrtLvls=("ERROR")
        self.setUpLogger(logging.ERROR)
        return
