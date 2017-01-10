#!/usr/bin/env python
##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from optparse import OptionParser
import sys
import httplib
import re

class ZenossApacheStatsPlugin:
    def __init__(self, host, port, ssl, url, ngregex, ngerror):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.url = url
        self.ngregex = ngregex
        self.ngerror = ngerror

    def run(self):
        metrics = {}

        if self.ssl:
            conn = httplib.HTTPSConnection(self.host, self.port)
        else:
            conn = httplib.HTTPConnection(self.host, self.port)

        try:
            conn.request('GET', self.url)
            response = conn.getresponse()
            if response.status != 200:
                print 'Server replied: %d %s to action GET %s' % (
                        response.status, response.reason, self.url)
                sys.exit(1)
            data = response.read()

            line_regex = re.compile(r'^([^:]+): (.+)$')
            for line in data.split("\n"):
                match = line_regex.search(line)
                if not match: continue
                name, value = match.groups()

                if name == 'Total Accesses':
                    metrics['totalAccesses'] = value
                elif name == 'Total kBytes':
                    metrics['totalKBytes'] = value
                elif name == 'CPULoad':
                    metrics['cpuLoad'] = value
                elif name == 'ReqPerSec':
                    metrics['reqPerSec'] = value
                elif name == 'BytesPerSec':
                    metrics['bytesPerSec'] = value
                elif name == 'BytesPerReq':
                    metrics['bytesPerReq'] = value
                elif name == 'BusyServers' or name == 'BusyWorkers':
                    metrics['busyServers'] = value
                elif name == 'IdleServers' or name == 'IdleWorkers':
                    metrics['idleServers'] = value
                elif name == 'Scoreboard':
                    metrics['slotWaiting'] = 0
                    metrics['slotStartingUp'] = 0
                    metrics['slotReadingRequest'] = 0
                    metrics['slotSendingReply'] = 0
                    metrics['slotKeepAlive'] = 0
                    metrics['slotDNSLookup'] = 0
                    metrics['slotLogging'] = 0
                    metrics['slotGracefullyFinishing'] = 0
                    metrics['slotOpen'] = 0
                    for code in value:
                        if code == '_':
                            metrics['slotWaiting'] += 1
                        elif code == 'S':
                            metrics['slotStartingUp'] += 1
                        elif code == 'R':
                            metrics['slotReadingRequest'] += 1
                        elif code == 'W':
                            metrics['slotSendingReply'] += 1
                        elif code == 'K':
                            metrics['slotKeepAlive'] += 1
                        elif code == 'D':
                            metrics['slotDNSLookup'] += 1
                        elif code == 'L':
                            metrics['slotLogging'] += 1
                        elif code == 'G':
                            metrics['slotGracefullyFinishing'] += 1
                        elif code == '.':
                            metrics['slotOpen'] += 1

            if self.ngregex:
                line_regex = re.compile(self.ngregex)
                msg = ""
                for line in data.split("\n"):
                    match = line_regex.search(line)
                    if not match: continue

                    for k, v in match.groupdict().items():
                        if v is None:
                            # We get here in a case like the following:
                            #     re.match("(1)(?P<group>[^2])?.?(3)", "123")
                            # This is useful because we can use this fact to
                            # generate a custom error message if only some of our
                            # groups match.
                            msg = self.ngerror
                        else:
                            metrics[k] = v
                if msg:
                    print msg + "|" + " ".join(["%s=%s" % (k, v) for k,v in metrics.items()])
                    sys.exit(1)

        except SystemExit:
            sys.exit(1)
        except Exception, e:
            print str(e)
            sys.exit(1)

        if not metrics:
            print "no metrics were returned"
            sys.exit(1)

        print "STATUS OK|%s" % (' '.join([ "%s=%s" % (m[0],m[1]) \
            for m in metrics.items() ]))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host',
        help='Hostname of Apache server')
    parser.add_option('-p', '--port', dest='port',
        type='int', default=80,
        help='Port of Apache server')
    parser.add_option('-s', '--ssl', dest='ssl',
        action='store_true', default=False,
        help='Use HTTPS for the connection')
    parser.add_option('-u', '--url', dest='url',
        default='/server-status?auto',
        help='Relative URL of server status page')
    parser.add_option('-r', '--regex', dest='ngregex',
        default='',
        help='A named group (!) regular expression')
    parser.add_option('-e', '--error', dest='ngerror',
        default='',
        help='Error message to send if one of the named groups return None')
    options, args = parser.parse_args()

    if not options.host:
        print "You must specify the host parameter."
        sys.exit(1)

    cmd = ZenossApacheStatsPlugin(
        options.host, options.port, options.ssl, options.url, options.ngregex, options.ngerror)
    cmd.run()
