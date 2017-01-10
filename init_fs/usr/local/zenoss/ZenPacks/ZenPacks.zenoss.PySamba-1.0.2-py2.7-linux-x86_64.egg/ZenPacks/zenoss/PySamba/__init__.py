##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2012, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import os.path
from Products.ZenUtils.Utils import zenPath
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import atomicWrite

class ZenPack(ZenPackBase):

    binUtilities = ['wmic', 'winexe']

    def __init__(self, *args):
        super(ZenPack,self).__init__(*args)
        self.thisZenPackLibDir = os.path.join(os.path.dirname(__file__), 'lib')
        self.easyInstallPthFileName = zenPath('ZenPacks', 'easy-install.pth')

    def _getEasyInstallPthFileLines(self):
        with open(self.easyInstallPthFileName) as easyInstallPthFile:
            return easyInstallPthFile.read().splitlines()

    def _rewriteEasyInstallPthFile(self, data):
        if isinstance(data, list):
            data = '\n'.join(data)
        atomicWrite(self.easyInstallPthFileName, data)

    def install(self, *args):
        super(ZenPack,self).install(*args)

        # must add this zenpack's lib directory to the list of directories in 'easy_install.pth'
        easyInstallPthLines = self._getEasyInstallPthFileLines()
        easyInstallPthLines.insert(1, self.thisZenPackLibDir)

        self._rewriteEasyInstallPthFile(easyInstallPthLines)

        # add symlinks for command line utilities
        for utilname in self.binUtilities:
            self.installBinFile(utilname)

    def remove(self, *args):
        super(ZenPack,self).remove(*args)

        # must remove this zenpack's lib directory from the list of directories in 'easy_install.pth'
        easyInstallPthLines = [line for line in self._getEasyInstallPthFileLines()
                               if line != self.thisZenPackLibDir]

        self._rewriteEasyInstallPthFile(easyInstallPthLines)

        # remove symlinks for command line utilities
        for utilname in self.binUtilities:
            self.removeFile(utilname)

