##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenReports import Utils, Utilization
from Products.ZenUtils import Time

class MSExchangeAvailability:
    "MSExchange ZenPack Availability Report"

    winservices = [
        'MSExchangeES',
        'IMAP4Svc',
        'MSExchangeIS',
        'MSExchangeMGMT',
        'MSExchangeMTA',
        'POP3Svc',
        'RESvc',
        'MSExchangeSRS',
        'MSExchangeSA',
        'SMTPSVC',
        'W3SVC',
        'IISADMIN',
        'SMTPSVC',
        ]

    def run(self, dmd, args):
        report = []
        zem = dmd.ZenEventManager
        windows_class = None

        # Guard against people removing the /Server/Windows device class.
        try:
            windows_class = dmd.getObjByPath('Devices/Server/Windows')
        except KeyError:
            return []

        for d in windows_class.getSubDevices():
            if "MSExchangeIS" not in d.zDeviceTemplates: continue
            if not d.monitorDevice(): continue

            availability = d.availability()
            uptime = d.sysUpTime()
            uptime_string = "unknown"
            if uptime and uptime != -1:
                uptime = uptime / 100
                uptime_string = Time.Duration(uptime)
            else:
                uptime = None

            r = Utils.Record(
                device=d.titleOrId(),
                deviceUrl=d.getPrimaryUrlPath(),
                availability=float(availability),
                availability_string=str(availability),
                uptime=uptime,
                uptime_string=uptime_string,
                )

            for winservice in self.winservices:
                ws = getattr(d.os.winservices, winservice, None)
                if ws:
                    r.values[winservice] = ws.getStatusString(
                        '/Status/WinService')

                    r.values[winservice+'_img'] = d.getStatusImgSrc(
                        ws.getStatus())

            report.append(r)

        return report
