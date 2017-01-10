##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

import logging
log = logging.getLogger("zen.migrate")

def getSshLinux( dmd ):
    ssh = None
    sshLinux = None
    if dmd.Devices.Server.hasObject('SSH'):
        ssh = dmd.Devices.Server.SSH
    if ssh and ssh.hasObject('Linux'):
        sshLinux = ssh.Linux
    return sshLinux

class FixCpuAlias( ZenPackMigration ):
    """
    The former cpu alias formula was incorrect.  It was
       '__EVAL:str(len(here.hw.cpus())) + ',/,1,EXC,-'
    but should have been
       '__EVAL:str(len(here.hw.cpus())) + ',/,100,EXC,-'
    """

    version = Version(1, 0, 0)

    def migrate(self, pack):
        try:
            log.info( 'Fixing cpu__pct alias if necessary')
            sshLinux = getSshLinux( pack.dmd )
            if sshLinux:
                deviceTemplate = sshLinux.rrdTemplates.Device
                cpuIdleDp = deviceTemplate.datasources.cpu.datapoints.ssCpuIdle
                if cpuIdleDp.hasAlias( 'cpu__pct' ):
                    cpuAlias = cpuIdleDp.aliases.cpu__pct
                    # If it has been changed already, leave it alone
                    if cpuAlias.formula == "__EVAL:str(len(here.hw.cpus())) + ',/,1,EXC,-'":
                        log.debug( 'Modifying cpu__pct alias on cpuIdle datapoint' )
                        cpuAlias.formula == "__EVAL:str(len(here.hw.cpus())) + ',/,100,EXC,-'"
        except Exception, e:
            log.debug( 'Exception trying to modify cpu__pct alias' )


FixCpuAlias()
