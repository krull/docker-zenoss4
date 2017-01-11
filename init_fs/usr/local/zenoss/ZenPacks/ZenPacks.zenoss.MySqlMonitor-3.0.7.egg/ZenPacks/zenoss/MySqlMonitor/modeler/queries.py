##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################


DB_QUERY = """
    SELECT schema_name title, default_character_set_name,
        default_collation_name, size, data_size,
        index_size, table_count
    FROM information_schema.schemata LEFT JOIN
        (SELECT table_schema, count(table_name) table_count,
            sum(data_length + index_length) size,
            sum(data_length) data_size, sum(index_length) index_size
        FROM information_schema.TABLES
        GROUP BY table_schema) as sizes
    ON schema_name = sizes.table_schema;
"""

SERVER_QUERY = """
    SHOW GLOBAL STATUS LIKE "Handler_read%";
"""

SERVER_SIZE_QUERY = """
    SELECT sum(data_length + index_length) size,
        sum(data_length) data_size, sum(index_length) index_size
    FROM information_schema.TABLES;
"""

MASTER_QUERY = """
    SHOW MASTER STATUS;
"""

SLAVE_QUERY = """
    SHOW SLAVE STATUS;
"""

VERSION_QUERY = """
    SHOW VARIABLES LIKE "version%";
"""
