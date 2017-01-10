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
from Products.Zuul.facades import getFacade, ObjectNotFoundException

import logging
log = logging.getLogger("zen.migrate")

class FixBlockUtilization(ZenPackMigration):
    version = Version(1, 1, 99)

    def migrate(self, pack):
        try:
            log.info('Fixing the SSH-Linux FileSystem template')
            facade = getFacade("template")
            template_uid = "/zport/dmd/Devices/Server/SSH/Linux/rrdTemplates/FileSystem"
            threshold_id = "Free Space 90 Percent"
            threshold_uid = "{template_uid}/thresholds/{threshold_id}".format(**locals())

            try:
                facade.removeThreshold(threshold_uid)
            except ObjectNotFoundException:
                log.info("'Free Space 90 Percent' threshold does not exist.")

            def delete_graph_point(graph_points_uid, graph_point_id):
                graph_point_uid = "{graph_points_uid}/{graph_point_id}".format(**locals())
                try:
                    facade.deleteGraphPoint(graph_point_uid)
                except ObjectNotFoundException:
                    log.info("'Block Utilization' graph does not have '{graph_point_id}' graph point.".format(**locals()))

            graph_points_uid = "{template_uid}/graphDefs/Block Utilization/graphPoints".format(**locals())
            delete_graph_point(graph_points_uid, threshold_id)
            delete_graph_point(graph_points_uid, "usedBlocks")

        except Exception, e:
            log.error('Failed to fix the SSH-Linux FileSystem template. {e.__class__.__name__}: {e}'.format(**locals()))

FixBlockUtilization()
