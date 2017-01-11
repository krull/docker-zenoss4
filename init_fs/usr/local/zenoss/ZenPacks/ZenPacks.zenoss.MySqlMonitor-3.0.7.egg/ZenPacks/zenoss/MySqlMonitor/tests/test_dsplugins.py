######################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is
# installed.
#
######################################################################

import unittest
from mock import Mock, patch, sentinel

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ZenPacks.zenoss.MySqlMonitor import NAME_SPLITTER
from ZenPacks.zenoss.MySqlMonitor import dsplugins


class TestMysqlBasePlugin(BaseTestCase):
    def setUp(self):
        self.plugin = dsplugins.MysqlBasePlugin()

    def test_onSuccess_clears_event(self):
        result = {'events': [], 'values': {"test": "test"}}

        self.plugin.onSuccess(result, sentinel.any_value)

        event = result['events'][0]
        self.assertEquals(event['severity'], 0)
        self.assertEquals(event['eventKey'], 'mysql_result')

    @patch.object(dsplugins, 'log')
    def test_onError_event(self, log):
        config = ds = Mock()
        ds.severity = 4
        config.datasources = [ds]
        result = self.plugin.onError(sentinel.some_result, config)

        event = result['events'][0]
        self.assertEquals(event['severity'], 4)
        self.assertEquals(event['eventKey'], 'mysql_result')
        log.error.assertCalledWith(sentinel.some_result)


class TestMySqlMonitorPlugin(BaseTestCase):

    def test_results_to_values(self):
        results = (
            ('Value', sentinel.value),
        )

        plugin = dsplugins.MySqlMonitorPlugin()
        values = plugin.query_results_to_values(results)

        self.assertEquals(values, {
            'value': (sentinel.value, 'N')
        })

    def test_empty_results_to_values(self):
        results = ()

        plugin = dsplugins.MySqlMonitorPlugin()
        values = plugin.query_results_to_values(results)

        self.assertEquals(values, {})


class TestMySqlDeadlockPlugin(BaseTestCase):

    def test_query_status_ok_to_events(self):
        results = (
            ('1', '2', '''
=====================================
130926 17:18:15 INNODB MONITOR OUTPUT
=====================================
Per second averages calculated from the last 35 seconds
-----------------
BACKGROUND THREAD
-----------------
srv_master_thread loops: 18395 1_second, 18394 sleeps,
1839 10_second, 4 background, 4 flush
srv_master_thread log flush and writes: 18448
----------
SEMAPHORES
----------
OS WAIT ARRAY INFO: reservation count 1688, signal count 1681
Mutex spin waits 67, rounds 2010, OS waits 64
RW-shared spins 1593, rounds 47790, OS waits 1593
RW-excl spins 11, rounds 930, OS waits 29
Spin rounds per wait: 30.00 mutex, 30.00 RW-shared, 84.55 RW-excl
------------
TRANSACTIONS
------------
Trx id counter 1BE0DD
Purge done for trx's n:o < 1BD432 undo n:o < 0
History list length 559
LIST OF TRANSACTIONS FOR EACH SESSION:
---TRANSACTION 0, not started
MySQL thread id 1497, OS thread handle 0x7f2ff0d94700,
query id 217512 localhost root
show engine innodb status
---TRANSACTION 1BD3F2, not started
MySQL thread id 1397, OS thread handle 0x7f2fed4c9700,
query id 206785 localhost zenoss
---TRANSACTION 1BD3F1, not started
MySQL thread id 1396, OS thread handle 0x7f2ff0e57700,
query id 206784 localhost zenoss
---TRANSACTION 1BE0CF, not started
MySQL thread id 1395, OS thread handle 0x7f2ff0c4f700,
query id 217472 localhost zenoss
---TRANSACTION 1BD3FD, not started
MySQL thread id 1394, OS thread handle 0x7f2fed6d1700,
query id 206832 localhost zenoss
---TRANSACTION 1BD2A4, not started
MySQL thread id 1392, OS thread handle 0x7f2fed60e700,
query id 205722 localhost zenoss
---TRANSACTION 1BD29E, not started
MySQL thread id 1390, OS thread handle 0x7f2fed5cd700,
query id 205670 localhost zenoss
---TRANSACTION 1BD3EE, not started
MySQL thread id 1389, OS thread handle 0x7f2fed58c700,
query id 206771 localhost zenoss
---TRANSACTION 1BD3F6, not started
MySQL thread id 1388, OS thread handle 0x7f2ff0ed9700,
query id 206799 localhost zenoss
---TRANSACTION 1BD3ED, not started
MySQL thread id 1387, OS thread handle 0x7f2ff10a0700,
query id 206770 localhost zenoss
---TRANSACTION 1BD3F5, not started
MySQL thread id 1386, OS thread handle 0x7f2ff0f1a700,
query id 206798 localhost zenoss
---TRANSACTION 1BE0D4, not started
MySQL thread id 1384, OS thread handle 0x7f2fed64f700,
query id 217486 localhost zenoss
---TRANSACTION 1BE0D3, not started
MySQL thread id 1379, OS thread handle 0x7f2ff0f9c700,
query id 217485 localhost zenoss
---TRANSACTION 1BE0DC, not started
MySQL thread id 1170, OS thread handle 0x7f2fed50a700,
query id 217510 localhost 127.0.0.1 zenoss
---TRANSACTION 1BB3B5, not started
MySQL thread id 1, OS thread handle 0x7f2ff11e5700,
query id 171474 localhost 127.0.0.1 zenoss
---TRANSACTION 1BE061, not started
MySQL thread id 2, OS thread handle 0x7f2ff11a4700,
query id 217132 localhost 127.0.0.1 zenoss
---TRANSACTION 1BE0C2, ACTIVE 14 sec
MySQL thread id 1412, OS thread handle 0x7f2ff10e1700,
query id 217419 localhost zenoss
Trx read view will not see trx with id >= 1BE0C3, sees < 1BD425
---TRANSACTION 1BE0C1, ACTIVE 14 sec
MySQL thread id 1385, OS thread handle 0x7f2fed690700,
query id 217417 localhost zenoss
Trx read view will not see trx with id >= 1BE0C2, sees < 1BD425
---TRANSACTION 1BE093, ACTIVE 23 sec
MySQL thread id 27, OS thread handle 0x7f2ff105f700,
query id 217296 localhost zenoss
Trx read view will not see trx with id >= 1BE094, sees < 1BD425
---TRANSACTION 1BE091, ACTIVE 23 sec
MySQL thread id 21, OS thread handle 0x7f2ff0fdd700,
query id 217290 localhost zenoss
Trx read view will not see trx with id >= 1BE092, sees < 1BD425
---TRANSACTION 1BE090, ACTIVE 23 sec
MySQL thread id 26, OS thread handle 0x7f2ff0f5b700,
query id 217287 localhost zenoss
Trx read view will not see trx with id >= 1BE091, sees < 1BD425
---TRANSACTION 1BE08E, ACTIVE 23 sec
MySQL thread id 19, OS thread handle 0x7f2ff101e700,
query id 217281 localhost zenoss
Trx read view will not see trx with id >= 1BE08F, sees < 1BD425
---TRANSACTION 1BD426, ACTIVE 1169 sec
MySQL thread id 1410, OS thread handle 0x7f2ff0d12700,
query id 207014 localhost zenoss
Trx read view will not see trx with id >= 1BD427, sees < 1BD25E
---TRANSACTION 1BD425, ACTIVE 1169 sec
MySQL thread id 1409, OS thread handle 0x7f2ff0c90700,
query id 207007 localhost zenoss
Trx read view will not see trx with id >= 1BD426, sees < 1BD25E
--------
FILE I/O
--------
I/O thread 0 state: waiting for completed aio requests (insert buffer thread)
I/O thread 1 state: waiting for completed aio requests (log thread)
I/O thread 2 state: waiting for completed aio requests (read thread)
I/O thread 3 state: waiting for completed aio requests (read thread)
I/O thread 4 state: waiting for completed aio requests (read thread)
I/O thread 5 state: waiting for completed aio requests (read thread)
I/O thread 6 state: waiting for completed aio requests (write thread)
I/O thread 7 state: waiting for completed aio requests (write thread)
I/O thread 8 state: waiting for completed aio requests (write thread)
I/O thread 9 state: waiting for completed aio requests (write thread)
Pending normal aio reads: 0 [0, 0, 0, 0] , aio writes: 0 [0, 0, 0, 0] ,
 ibuf aio reads: 0, log i/o's: 0, sync i/o's: 0
Pending flushes (fsync) log: 0; buffer pool: 0
1557 OS file reads, 45979 OS file writes, 12579 OS fsyncs
0.00 reads/s, 0 avg bytes/read, 3.00 writes/s, 0.80 fsyncs/s
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 3, seg size 5, 11 merges
merged operations:
 insert 0, delete mark 381, delete 0
discarded operations:
 insert 0, delete mark 0, delete 0
Hash table size 553229, node heap has 48 buffer(s)
4.54 hash searches/s, 4.80 non-hash searches/s
---
LOG
---
Log sequence number 549033793
Log flushed up to   549033793
Last checkpoint at  549033793
0 pending log writes, 0 pending chkp writes
9114 log i/o's done, 0.63 log i/o's/second
----------------------
BUFFER POOL AND MEMORY
----------------------
Total memory allocated 274726912; in additional pool allocated 0
Dictionary memory allocated 549651
Buffer pool size   16383
Free buffers       14304
Database pages     2031
Old database pages 760
Modified db pages  0
Pending reads 0
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 10, not young 0
0.00 youngs/s, 0.00 non-youngs/s
Pages read 1546, created 485, written 34930
0.00 reads/s, 0.00 creates/s, 2.26 writes/s
Buffer pool hit rate 1000 / 1000, young-making rate 0 / 1000 not 0 / 1000
Pages read ahead 0.00/s, evicted without
access 0.00/s, Random read ahead 0.00/s
LRU len: 2031, unzip_LRU len: 0
I/O sum[0]:cur[0], unzip sum[0]:cur[0]
--------------
ROW OPERATIONS
--------------
0 queries inside InnoDB, 0 queries in queue
9 read views open inside InnoDB
Main thread process no. 2182, id 139843834029824, state: sleeping
Number of rows inserted 22379, updated 5922, deleted 18763, read 341468
0.63 inserts/s, 0.46 updates/s, 0.63 deletes/s, 4.83 reads/s
----------------------------
END OF INNODB MONITOR OUTPUT
============================
'''), )

        plugin = dsplugins.MySqlDeadlockPlugin()
        ds = Mock()
        ds.deadlock_info = None
        ds.component = sentinel.component
        events = plugin.query_results_to_events(results, ds)
        self.assertEquals(len(events), 0)

    def test_query_status_deadlock_to_events(self):
        results = (
            ('1', '2', '''
=====================================
130927 10:27:05 INNODB MONITOR OUTPUT
=====================================
Per second averages calculated from the last 15 seconds
-----------------
BACKGROUND THREAD
-----------------
srv_master_thread loops: 28 1_second, 28 sleeps, 2 10_second,
11 background, 11 flush
srv_master_thread log flush and writes: 30
----------
SEMAPHORES
----------
OS WAIT ARRAY INFO: reservation count 7, signal count 7
Mutex spin waits 4, rounds 51, OS waits 0
RW-shared spins 6, rounds 180, OS waits 6
RW-excl spins 0, rounds 0, OS waits 0
Spin rounds per wait: 12.75 mutex, 30.00 RW-shared, 0.00 RW-excl
------------------------
LATEST DETECTED DEADLOCK
------------------------
130927 10:17:13
*** (1) TRANSACTION:
TRANSACTION 11703, ACTIVE 71 sec starting index read
mysql tables in use 1, locked 1
LOCK WAIT 5 lock struct(s), heap size 1024, 3 row lock(s)
MySQL thread id 40, OS thread handle 0xa4b6cb40, query id 131 localhost
bunyk Searching rows for update
update test.innodb_deadlock_maker set a = 0 where a <> 0
*** (1) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 0 page no 635 n bits 72 index `PRIMARY`
of table `test`.`innodb_deadlock_maker` trx id 11703 lock_mode X waiting
Record lock, heap no 3 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 80000001; asc     ;;
 1: len 6; hex 000000011701; asc       ;;
 2: len 7; hex 82000001f8011d; asc        ;;

*** (2) TRANSACTION:
TRANSACTION 11702, ACTIVE 78 sec starting index read
mysql tables in use 1, locked 1
4 lock struct(s), heap size 320, 2 row lock(s)
MySQL thread id 41, OS thread handle 0xa4b3bb40, query id 132 localhost
bunyk Searching rows for update
update test.innodb_deadlock_maker set a = 1 where a <> 1
*** (2) HOLDS THE LOCK(S):
RECORD LOCKS space id 0 page no 635 n bits 72 index `PRIMARY`
of table `test`.`innodb_deadlock_maker` trx id 11702 lock
mode S locks rec but not gap
Record lock, heap no 3 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 80000001; asc     ;;
 1: len 6; hex 000000011701; asc       ;;
 2: len 7; hex 82000001f8011d; asc        ;;

*** (2) WAITING FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 0 page no 635 n bits 72 index
`PRIMARY` of table `test`.`innodb_deadlock_maker`
trx id 11702 lock_mode X waiting
Record lock, heap no 2 PHYSICAL RECORD: n_fields 3; compact format; info bits 0
 0: len 4; hex 80000000; asc     ;;
 1: len 6; hex 000000011701; asc       ;;
 2: len 7; hex 82000001f80110; asc        ;;

*** WE ROLL BACK TRANSACTION (2)
------------
TRANSACTIONS
------------
Trx id counter 11705
Purge done for trx's n:o < 11705 undo n:o < 0
History list length 1927
LIST OF TRANSACTIONS FOR EACH SESSION:
---TRANSACTION 0, not started
MySQL thread id 46, OS thread handle 0xa4b6cb40, query id 144 localhost root
show engine innodb status
--------
FILE I/O
--------
I/O thread 0 state: waiting for i/o request (insert buffer thread)
I/O thread 1 state: waiting for i/o request (log thread)
I/O thread 2 state: waiting for i/o request (read thread)
I/O thread 3 state: waiting for i/o request (read thread)
I/O thread 4 state: waiting for i/o request (read thread)
I/O thread 5 state: waiting for i/o request (read thread)
I/O thread 6 state: waiting for i/o request (write thread)
I/O thread 7 state: waiting for i/o request (write thread)
I/O thread 8 state: waiting for i/o request (write thread)
I/O thread 9 state: waiting for i/o request (write thread)
Pending normal aio reads: 0 [0, 0, 0, 0] , aio writes: 0 [0, 0, 0, 0] ,
 ibuf aio reads: 0, log i/o's: 0, sync i/o's: 0
Pending flushes (fsync) log: 0; buffer pool: 0
559 OS file reads, 29 OS file writes, 19 OS fsyncs
0.00 reads/s, 0 avg bytes/read, 0.00 writes/s, 0.00 fsyncs/s
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 0, seg size 2, 0 merges
merged operations:
 insert 0, delete mark 0, delete 0
discarded operations:
 insert 0, delete mark 0, delete 0
Hash table size 553193, node heap has 1 buffer(s)
0.00 hash searches/s, 0.00 non-hash searches/s
---
LOG
---
Log sequence number 15404422
Log flushed up to   15404422
Last checkpoint at  15404422
0 pending log writes, 0 pending chkp writes
16 log i/o's done, 0.00 log i/o's/second
----------------------
BUFFER POOL AND MEMORY
----------------------
Total memory allocated 135987200; in additional pool allocated 0
Dictionary memory allocated 138491
Buffer pool size   8191
Free buffers       7641
Database pages     549
Old database pages 222
Modified db pages  0
Pending reads 0
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 0, not young 0
0.00 youngs/s, 0.00 non-youngs/s
Pages read 548, created 1, written 17
0.00 reads/s, 0.00 creates/s, 0.00 writes/s
No buffer pool page gets since the last printout
Pages read ahead 0.00/s, evicted without access 0.00/s,
Random read ahead 0.00/s
LRU len: 549, unzip_LRU len: 0
I/O sum[0]:cur[0], unzip sum[0]:cur[0]
--------------
ROW OPERATIONS
--------------
0 queries inside InnoDB, 0 queries in queue
1 read views open inside InnoDB
Main thread process no. 1127, id 2771835712, state: waiting for server activity
Number of rows inserted 2, updated 0, deleted 0, read 6
0.00 inserts/s, 0.00 updates/s, 0.00 deletes/s, 0.00 reads/s
----------------------------
END OF INNODB MONITOR OUTPUT
============================
'''), )

        plugin = dsplugins.MySqlDeadlockPlugin()
        ds = Mock()
        ds.deadlock_info = None
        ds.component = 'component'
        events = plugin.query_results_to_events(results, ds)

        self.assertEquals(len(events), 2)
        self.assertEquals(events[1]['eventKey'], 'innodb_deadlock')
        self.assertEquals(events[1]['component'], 'component(.)test')
        self.assertEquals(events[1]['severity'], 2)


class TestMySQLMonitorDatabasesPlugin(BaseTestCase):

    def test_no_results_to_values(self):
        results = ((0, None, None, None),)

        plugin = dsplugins.MySQLMonitorDatabasesPlugin()
        values = plugin.query_results_to_values(results)

        self.assertEquals(values, dict(
            (k, (0))
            for k in ('table_count', 'size', 'data_size', 'index_size')
        ))

    def test_results_to_values(self):
        results = ((
            sentinel.table_count,
            sentinel.size,
            sentinel.data_size,
            sentinel.index_size,
        ),)

        plugin = dsplugins.MySQLMonitorDatabasesPlugin()
        values = plugin.query_results_to_values(results)

        self.assertEquals(values, dict(
            table_count=(sentinel.table_count),
            size=(sentinel.size),
            data_size=(sentinel.data_size),
            index_size=(sentinel.index_size),
        ))

    def test_tables_number_event(self):
        results = ((4, 1, 1, 1),)
        plugin = dsplugins.MySQLMonitorDatabasesPlugin()

        ds = Mock()
        ds.component = "test" + NAME_SPLITTER + "test"
        ds.table_count = None
        events = plugin.query_results_to_events(results, ds)
        self.assertEquals(len(events), 1)
        self.assertEquals(events[0]['summary'], '4 tables were added.')
        self.assertEquals(events[0]['severity'], 2)

        ds.table_count = 3
        events = plugin.query_results_to_events(results, ds)
        self.assertEquals(events[0]['summary'], '1 table was added.')
        self.assertEquals(events[0]['severity'], 2)

        ds.table_count = 5
        events = plugin.query_results_to_events(results, ds)
        self.assertEquals(events[0]['summary'], '1 table was dropped.')
        self.assertEquals(events[0]['severity'], 3)


class TestMySQLDatabaseExistencePlugin(BaseTestCase):
    def test_db_not_exists(self):
        results = ((0,),)
        ds = Mock()
        ds.component = "test" + NAME_SPLITTER + "test"

        plugin = dsplugins.MySQLDatabaseExistencePlugin()
        events = plugin.query_results_to_events(results, ds)

        self.assertEquals(len(events), 1)
        self.assertEquals(events[0]['eventKey'], 'db_test_dropped')
        self.assertEquals(events[0]['component'], 'test')
        self.assertEquals(events[0]['severity'], 2)

    def test_db_exists(self):
        results = ((1,),)

        plugin = dsplugins.MySQLDatabaseExistencePlugin()
        events = plugin.query_results_to_events(results, Mock())

        self.assertEquals(len(events), 0)
        # self.assertEquals(events[0]['eventKey'], 'db_existence')
        # self.assertEquals(events[0]['component'], sentinel.component)
        # self.assertEquals(events[0]['severity'], 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMysqlBasePlugin))
    suite.addTest(makeSuite(TestMySqlMonitorPlugin))
    suite.addTest(makeSuite(TestMySqlDeadlockPlugin))
    suite.addTest(makeSuite(TestMySQLMonitorDatabasesPlugin))
    suite.addTest(makeSuite(TestMySQLDatabaseExistencePlugin))
    return suite
