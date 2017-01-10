##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__='''WinPerfDataSource.py

Defines datasource for the ZenWinPerf daemon.
Part of the WindowsMonitor zenpack.

'''

import cgi
import os
import re
import time
import sys
import popen2
import select
import fcntl
from sets import Set
from Products.ZenModel.RRDDataSource import RRDDataSource, SimpleRRDDataSource
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenWidgets import messaging


class WinPerfDataSource(ZenPackPersistence, SimpleRRDDataSource):
    
    ZENPACKID = 'ZenPacks.zenoss.WindowsMonitor'

    WINPERF_DSTYPE = 'WinPerf'
    sourcetypes = (WINPERF_DSTYPE,)
    sourcetype = WINPERF_DSTYPE
    
    counter = ''
    
    _properties = RRDDataSource._properties + (
            {'id':'counter', 'type':'string', 'mode':'w'},
        )
        
    _relations = RRDDataSource._relations + (
        )


    factory_type_information = ( 
    { 
        'immediate_view' : 'editWinPerfDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editWinPerfDataSource',
              'permissions'   : ( Permissions.view, ),
            },
            { 'id'            : 'test',
              'name'          : 'Test',
              'action'        : 'testWinPerfDataSource',
              'permissions'   : ( Permissions.view, ),
            },
        )
    },
    )

    security = ClassSecurityInfo()


    def __init__(self, id, title=None, buildRelations=True):
        RRDDataSource.__init__(self, id, title, buildRelations)
        
        
    def getDescription(self):
        return self.counter

    def testDataSourceAgainstDevice(self, testDevice, REQUEST, write, errorLog):
        """
        Does the logic for testing this datasource against a specific windows device.
        @param string testDevice The id of the device we are testing
        @param Dict REQUEST the browers request
        @param Function write The output method we are using to stream the result of the command
        @parma Function errorLog The output method we are using to report errors
        """
        # Determine which device to execute against
        device = None
        if testDevice:
            # Try to get specified device
            device = self.findDevice(testDevice)
            if not device:
                errorLog('Error', 'Cannot find device matching %s' % testDevice)
                return self.callZenScreen(REQUEST)
        elif hasattr(self, 'device'):
            # ds defined on a device, use that device
            device = self.device()
        elif hasattr(self, 'getSubDevicesGen'):
            # ds defined on a device class, use any device from the class
            try:
                device = self.getSubDevicesGen().next()
            except StopIteration:
                # No devices in this class, bail out
                pass
        if not device:
            errorLog('Error', 'Cannot determine a device to test against.')            
            return self.callZenScreen(REQUEST)
        
        # Get the Win Perf Counter (default to using the one from the request otherwise use our setone)
        counter = REQUEST.get('counter', self.counter)
        if not counter:
            errorLog('Error', 'There is no counter to test.')
            return self.callZenScreen(REQUEST)

        # determine if the template we are currently editing has a matching
        # monitored component in the device we will test against. if the
        # component has been modeled it should have a perfmonInstance attribute
        # which must be prepended to the counter to build a fully qualified
        # performance counter path.
        templateMetaType = self.rrdTemplate().getTargetPythonClass().meta_type
        perfmonInstance = None
        for component in device.getMonitoredComponents(type=templateMetaType):
            if hasattr(component, "perfmonInstance"):
                perfmonInstance = component.perfmonInstance
                break
        if perfmonInstance:
            counter = perfmonInstance + counter

        # if at this point the counter does not match the \instance\counter
        # format then we shouldn't use, so toss back an error to the user
        if not re.match("\\\\.+\\\\.+", counter):
            errorLog('Error', '''The counter is invalid or requires a device
            that has been successfully modeled.''')
            return self.callZenScreen(REQUEST)

        # Render
        header = ""
        footer = ""
        if REQUEST.get('renderTemplate', True):
            header, footer = self.winPerfTestOutput().split('OUTPUT_TOKEN')
        write(str(header))
        
        write('Executing zenwinperf on %s' % device.id)
        write('')
        start = time.time()
        try:
            self.testDevice(device, write, counter)
        except:
            write('exception while executing zenwinperf')
            write('type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        write('')
        write('')
        write('DONE in %s seconds' % long(time.time() - start))
        write(str(footer))

        
    security.declareProtected('Change Device', 'manage_testDataSource')
    def manage_testDataSource(self, testDevice, REQUEST):
        ''' Test the datasource by executing the command and outputting the
        non-quiet results.
        '''
        out = REQUEST.RESPONSE

        def write(lines):
            ''' Output (maybe partial) result text.
            '''
            # Looks like firefox renders progressive output more smoothly
            # if each line is stuck into a table row.  
            startLine = '<tr><td class="tablevalues">'
            endLine = '</td></tr>\n'
            if out:
                if not isinstance(lines, list):
                    lines = [lines]
                for l in lines:
                    if not isinstance(l, str):
                        l = str(l)
                    l = l.strip()
                    l = cgi.escape(l)
                    l = l.replace('\n', endLine + startLine)
                    out.write(startLine + l + endLine)
        
        self.testDataSourceAgainstDevice(testDevice, REQUEST, write, messaging.IMessagSeender(self).sendToBrowser)


    def testDevice(self, device, write, counter):
        ''' Execute zenwinperf
        '''
        cmd = "zenwinperf run -v 20 -d '%s' --testCounter '%s' " % (
                str(device.id), counter)
        write(cmd)
        child = popen2.Popen4(cmd)
        flags = fcntl.fcntl(child.fromchild, fcntl.F_GETFL)
        fcntl.fcntl(child.fromchild, fcntl.F_SETFL, flags | os.O_NDELAY)
        timeout = max(device.getProperty('zWinPerfTimeoutSeconds', 1), 1)
        endtime = time.time() + timeout
        pollPeriod = 1
        firstPass = True
        while time.time() < endtime and (firstPass or child.poll() == -1):
            firstPass = False
            r, w, e = select.select([child.fromchild], [], [], pollPeriod)
            if r:
                t = child.fromchild.read()
                # We are sometimes getting to this point without any data
                # from child.fromchild.  I don't think that should happen
                # but the conditional below seems to be necessary.
                if t:
                    write(t)
                
        if child.poll() == -1:
            write('Timed out')
            import signal
            os.kill(child.pid, signal.SIGKILL)
