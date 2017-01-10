##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """FileSystemMap
Use WMI to gather file system information.
"""

import re

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId

def guessBlockSize(bytes):
    """Most of the MS operating systems don't seem to return a value
    for block size.  So, let's try to guess by how the size is rounded
    off.  That is, if the number is divisible by 1024, that's probably
    due to the block size.  Ya, it's a kludge."""
    for i in range(10, 17):
        if bytes / float(1 << i) % 1:
            return 1 << (i - 1)
    return 4096                 # a total fiction
    

class FileSystemMap(WMIPlugin):
    """
    Retrieve file systems
    """
    maptype = "FileSystemMap" 
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties = \
                WMIPlugin.deviceProperties + ('zFileSystemMapIgnoreNames',
                                              'zFileSystemMapIgnoreTypes')

    # create a mapping between the values used in the Zenoss UI and the actual
    # file system types provided via WMI. per the Win32_LogicalDisk and 
    # Win32_Volume documentation:
    # Value Meaning
    # 0 Unknown
    # 1 No Root Directory
    # 2 Removable Disk
    # 3 Local Disk
    # 4 Network Drive
    # 5 Compact Disk
    # 6 RAM Disk
    typemap = {
        "other": "0",
        "removableDisk": "2",
        "floppyDisk": "2",
        "fixedDisk": "3",
        "networkDisk": "4",
        "compactDisk": "5",
        "ram": "6",
        "virtualMemory": "6",
        "ramDisk": "6",
        "flashMemory": "6",
    }


    def queries(self):
        return {
            "Win32_LogicalDisk":"select * from Win32_logicaldisk",
            "Win32_Volume":"select * from Win32_Volume",
            }
        
    def process(self, device, results, log):
        log.info('Collecting filesystems for device %s' % device.id)
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        skipfstypes = getattr(device, 'zFileSystemMapIgnoreTypes', None)
        
        maps = []
        rm = self.relMap()
        
        drives = {}
        for disk in results["Win32_LogicalDisk"]:
            om = self.objectMap()
            om.mount = '%s Label:%s Serial Number: %s' % \
                (disk.volumename, disk.name, disk.volumeserialnumber)
            if skipfsnames and re.search(skipfsnames,om.mount): 
                continue
            for skip in skipfstypes:
                type = self.typemap.get(skip, "0")
                if type == str(disk.drivetype):
                    log.debug("Skipping %s because %s types are excluded",
                              disk.name, skip)
                    break
            else:
                # don't monitor disks that aren't FixedDisk (12) or Unknown (0)
                om.monitor = (disk.size and disk.mediatype in (12, 0))
                om.storageDevice = disk.name
                om.type = disk.filesystem
                if disk.size:
                    if not disk.blocksize:
                        disk.blocksize = guessBlockSize(disk.size)
                    om.blockSize = int(disk.blocksize)
                    om.totalBlocks = int(disk.size) / om.blockSize
                om.maxNameLen = disk.maximumcomponentlength
                om.id = self.prepId(disk.deviceid)
                om.perfmonInstance = self.getPerfmonInstance(disk, log)

                log.debug("File System (logical disk) mount='%s' perfmonInstance='%s'",
                          om.mount, om.perfmonInstance)

                drives[disk.name] = True
                rm.append(om)
            
        for volume in results["Win32_Volume"]:
            # skip volumes we discovered via Win32_LogicalDisk or if the volume
            # doesn't have a label
            if volume.name.rstrip('\\') in drives or not volume.label:
                continue

            om = self.objectMap()
            om.mount = '%s Label:%s Serial Number: %s' % \
                (volume.label, volume.name, volume.serialnumber)
            if skipfsnames and re.search(skipfsnames,om.mount):
                continue
            for skip in skipfstypes:
                type = self.typemap.get(skip, "0")
                if type == str(volume.drivetype):
                    log.debug("Skipping %s because %s types are excluded",
                              volume.name, skip)
                    break
            else:
                om.monitor = volume.capacity and volume.capacity > 0
                om.storageDevice = volume.driveletter
                om.type = volume.filesystem
                om.blockSize = volume.blocksize
                om.totalBlocks = int(volume.capacity) / om.blockSize
                om.id = self.prepId(volume.label)
                om.perfmonInstance = self.getPerfmonInstance(volume, log)

                log.debug("File System (volume) mount='%s' perfmonInstance='%s'",
                          om.mount, om.perfmonInstance)
                rm.append(om)
        
        maps.append(rm)
        return maps

    def getPerfmonInstance(self, disk, log):
        """
        Determines the Perfmon Instance Path for the provided instance of the
        Win32_LogicalDisk class
        """
        
        # The Name attribute will include a trailing path separator, so split
        # that off if present.
        # 
        # BUG: this will not handle volumes that are not presently mounted with
        # a drive letter or path. For example, perfmon may know the instance as
        # HarddiskVolume3 (retrieved from the registry) but WMI may only know
        # the volume as \\?\Volume{3248dc7b-1ddf-11dd-969f-000c29175a10}
        perfmonInstance = '\\LogicalDisk(%s)' % disk.name.rstrip('\\')
        return perfmonInstance
