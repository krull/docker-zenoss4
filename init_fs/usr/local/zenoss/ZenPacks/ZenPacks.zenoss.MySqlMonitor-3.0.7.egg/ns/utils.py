##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import os
import json

from Products.AdvancedQuery import Eq, Or

from Products.ZenUtils.Utils import prepId
from Products.Zuul.interfaces import ICatalogTool

from zope.event import notify
from Products.Zuul.catalog.events import IndexingEvent


def here(dir, base=os.path.dirname(__file__)):
    return os.path.join(base, dir)


def add_local_lib_path():
    '''
    Helper to add the ZenPack's lib directory to sys.path.
    '''
    #import sys
    import site

    site.addsitedir(here('lib'))
    #sys.path.append(here('lib'))

add_local_lib_path()


def updateToMany(relationship, root, type_, ids):
    '''
    Update ToMany relationship given search root, type and ids.

    This is a general-purpose function for efficiently building
    non-containing ToMany relationships.
    '''
    root = root.primaryAq()

    new_ids = set(map(prepId, ids))
    current_ids = set(o.id for o in relationship.objectValuesGen())
    changed_ids = new_ids.symmetric_difference(current_ids)

    query = Or(*(Eq('id', x) for x in changed_ids))

    obj_map = {}
    for result in ICatalogTool(root).search(types=[type_], query=query):
        obj_map[result.id] = result.getObject()

    for id_ in new_ids.symmetric_difference(current_ids):
        obj = obj_map.get(id_)
        if not obj:
            continue

        if id_ in new_ids:
            relationship.addRelation(obj)
        else:
            relationship.removeRelation(obj)

        # Index remote object. It might have a custom path reporter.
        notify(IndexingEvent(obj, 'path', False))

        # For componentSearch. Would be nice if we could target
        # idxs=['getAllPaths'], but there's a chance that it won't exist
        # yet.
        obj.index_object()


def updateToOne(relationship, root, type_, id_):
    '''
    Update ToOne relationship given search root, type and ids.

    This is a general-purpose function for efficiently building
    non-containing ToOne relationships.
    '''
    old_obj = relationship()

    # Return with no action if the relationship is already correct.
    if (old_obj and old_obj.id == id_) or (not old_obj and not id_):
        return
    # Remove current object from relationship.
    if old_obj:
        relationship.removeRelation()

        # Index old object. It might have a custom path reporter.
        notify(IndexingEvent(old_obj.primaryAq(), 'path', False))

    # No need to find new object if id_ is empty.
    if not id_:
        return

    # Find and add new object to relationship.
    root = root.primaryAq()
    query = Eq('id', id_)

    for result in ICatalogTool(root).search(types=[type_], query=query):
        new_obj = result.getObject()
        relationship.addRelation(new_obj)

        # Index remote object. It might have a custom path reporter.
        notify(IndexingEvent(new_obj.primaryAq(), 'path', False))

        # For componentSearch. Would be nice if we could target
        # idxs=['getAllPaths'], but there's a chance that it won't exist
        # yet.
        new_obj.index_object()

    return


def parse_mysql_connection_string(zMySQLConnectionString):
    """
    Parse zMySQLConnectionString property.

    @param connection_string: zMySQLConnectionString
    @type connection_string: list
    @return: a dict of server id as a key and a dict
    with user, port and password as a value
    """
    data = zMySQLConnectionString
    result = {}

    try:
        if isinstance(data, str):
            data = json.loads(data)

        for el in filter(None, data):
            if isinstance(el, str):
                el = json.loads(el)
            id = el.get('user') + '_' + el.get('port')
            result[id] = dict(
                user=el.get('user'),
                passwd=el.get('passwd'),
                port=int(el.get('port'))
            )

    except (ValueError, TypeError):
        raise ValueError('Invalid connection string')
    except:
        raise ValueError('Bad formatted connection string')
    return result


def adbapi_safe(text):
    """
    Something that replaces quotes with escaped quotes.
    The method is missing in zenoss 5.
    """
    return text.replace("'", "''").replace("\\", "\\\\")
