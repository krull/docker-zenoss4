#!/usr/bin/env python
##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
import sys
import subprocess
import os
import Products.ZenUtils.Utils

from optparse import OptionParser

class ZenossIRCDPlugin:
    def __init__(self, hostname, port, warning_num, critical_num):
        self.hostname = hostname
        self.port = port
        self.warning_num = warning_num
        self.critical_num = critical_num

    def run(self):
        check_ircd = Products.ZenUtils.Utils.binPath('check_ircd')
        parts = [check_ircd]
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.warning_num:
            parts.append('-w %s' % self.warning_num)
        if self.critical_num:
            parts.append('-c %s' % self.critical_num)
        cmd = ' '.join(parts)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result = p.wait()
        output = p.stdout.read()
        #Critical Number Of Clients Connected : 7581 (Limit = 100)
        #Somthing is Taking a Long Time, Increase Your TIMEOUT (Currently Set At 15 Seconds)
        #Critical Number Of Clients Connected : 7522 (Limit = 100) |number=7522
        #OK - HTTP/1.1 301 Moved Permanently - 1.050 second response time |time=1.050099s;;;0.000000 size=650B;;;0
        if result in (0,1,2):
            number = output.split(':',1)[1].split()[0]
            output = output.strip() + '|' + number
            print output
        else:
            output = p.stdout.read()
            print output
        return result


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--hostname', dest='hostname',
                      help='Hostname of ircd server')
    parser.add_option('-p', '--port', dest='port', default=6667, type='int',
                      help='Port of ircd server')
    parser.add_option('-w', '--warning_num', dest='warning_num', default=50,
                      type='int', help='ircd user warning number')
    parser.add_option('-c', '--critical_num', dest='critical_num', default=100,
                      type='int', help='ircd user critical number')
    options, args = parser.parse_args()

    if not options.hostname:
        print "You must specify the hostname parameter."
        sys.exit(1)

    cmd = ZenossIRCDPlugin(options.hostname, options.port, options.warning_num,
                           options.critical_num)

    result = cmd.run()
    sys.exit(result)
