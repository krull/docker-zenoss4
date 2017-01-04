-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: zodb_session
-- ------------------------------------------------------
-- Server version	5.5.37-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blob_chunk`
--

DROP TABLE IF EXISTS `blob_chunk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blob_chunk` (
  `zoid` bigint(20) NOT NULL,
  `chunk_num` bigint(20) NOT NULL,
  `tid` bigint(20) NOT NULL,
  `chunk` longblob NOT NULL,
  PRIMARY KEY (`zoid`,`chunk_num`),
  KEY `blob_chunk_lookup` (`zoid`),
  CONSTRAINT `blob_chunk_fk` FOREIGN KEY (`zoid`) REFERENCES `object_state` (`zoid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blob_chunk`
--

LOCK TABLES `blob_chunk` WRITE;
/*!40000 ALTER TABLE `blob_chunk` DISABLE KEYS */;
/*!40000 ALTER TABLE `blob_chunk` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `connection_info`
--

DROP TABLE IF EXISTS `connection_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `connection_info` (
  `connection_id` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `info` varchar(60000) NOT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`connection_id`),
  KEY `pid` (`pid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `connection_info`
--

LOCK TABLES `connection_info` WRITE;
/*!40000 ALTER TABLE `connection_info` DISABLE KEYS */;
INSERT INTO `connection_info` VALUES (87,2700,'pid=2700 tid=139745586784000\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 316, in install_tempfolder_and_sdc\n    tf = getattr(app, \'temp_folder\', None)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 225, in __of__\n    return self._getOrOpenObject(parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 247, in _getOrOpenObject\n    conn = self._getMountedConnection(anyjar)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 142, in _getMountedConnection\n    self._getDB()\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 152, in _getDB\n    return getConfiguration().getDatabase(self._path)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 287, in getDatabase\n    db = factory.open(name, self.databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 185, in open\n    DB = self.createDB(database_name, databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 182, in createDB\n    return ZODBDatabase.open(self, databases)\n  File \"/usr/local/zenoss/lib/python/ZODB/config.py\", line 101, in open\n    storage = section.storage.open()\n  File \"/usr/local/zenoss/lib/python/relstorage/config.py\", line 33, in open\n    return RelStorage(adapter, name=config.name, options=options)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 167, in __init__\n    self._adapter.schema.prepare()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/schema.py\", line 856, in prepare\n    self.connmanager.open_and_call(callback)\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/connmanager.py\", line 73, in open_and_call\n    conn, cursor = self.open()\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:32:44'),(91,2700,'pid=2700 tid=139745586784000\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 316, in install_tempfolder_and_sdc\n    tf = getattr(app, \'temp_folder\', None)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 225, in __of__\n    return self._getOrOpenObject(parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 247, in _getOrOpenObject\n    conn = self._getMountedConnection(anyjar)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 142, in _getMountedConnection\n    self._getDB()\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 152, in _getDB\n    return getConfiguration().getDatabase(self._path)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 287, in getDatabase\n    db = factory.open(name, self.databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 185, in open\n    DB = self.createDB(database_name, databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 182, in createDB\n    return ZODBDatabase.open(self, databases)\n  File \"/usr/local/zenoss/lib/python/ZODB/config.py\", line 127, in open\n    **options)\n  File \"/usr/local/zenoss/lib/python/ZODB/DB.py\", line 444, in __init__\n    temp_storage.load(z64, \'\')\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 460, in load\n    self._before_load()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 452, in _before_load\n    self._restart_load_and_poll()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 1207, in _restart_load_and_poll\n    self._adapter.poller.poll_invalidations, prev, ignore_tid)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 251, in _restart_load_and_call\n    self._open_load_connection()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 218, in _open_load_connection\n    conn, cursor = self._adapter.connmanager.open_for_load()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/mysql.py\", line 260, in open_for_load\n    return self.open(self.isolation_repeatable_read)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:32:44'),(92,2700,'pid=2700 tid=139745586784000\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 316, in install_tempfolder_and_sdc\n    tf = getattr(app, \'temp_folder\', None)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 225, in __of__\n    return self._getOrOpenObject(parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 247, in _getOrOpenObject\n    conn = self._getMountedConnection(anyjar)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 142, in _getMountedConnection\n    self._getDB()\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 152, in _getDB\n    return getConfiguration().getDatabase(self._path)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 287, in getDatabase\n    db = factory.open(name, self.databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 185, in open\n    DB = self.createDB(database_name, databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 182, in createDB\n    return ZODBDatabase.open(self, databases)\n  File \"/usr/local/zenoss/lib/python/ZODB/config.py\", line 127, in open\n    **options)\n  File \"/usr/local/zenoss/lib/python/ZODB/DB.py\", line 457, in __init__\n    temp_storage.tpc_begin(t)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 657, in tpc_begin\n    self._restart_store()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 286, in _restart_store\n    self._open_store_connection()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 273, in _open_store_connection\n    conn, cursor = self._adapter.connmanager.open_for_store()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/connmanager.py\", line 109, in open_for_store\n    conn, cursor = self.open()\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:32:44'),(93,2700,'pid=2700 tid=139745586784000\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 316, in install_tempfolder_and_sdc\n    tf = getattr(app, \'temp_folder\', None)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 225, in __of__\n    return self._getOrOpenObject(parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 247, in _getOrOpenObject\n    conn = self._getMountedConnection(anyjar)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 144, in _getMountedConnection\n    return anyjar.get_connection(self._getDBName())\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 374, in get_connection\n    before=self.before,\n  File \"/usr/local/zenoss/lib/python/ZODB/DB.py\", line 751, in open\n    result.open(transaction_manager)\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 1045, in open\n    self._flush_invalidations()\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 492, in _flush_invalidations\n    invalidated = self._storage.poll_invalidations()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 1233, in poll_invalidations\n    changes, new_polled_tid = self._restart_load_and_poll()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 1207, in _restart_load_and_poll\n    self._adapter.poller.poll_invalidations, prev, ignore_tid)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 251, in _restart_load_and_call\n    self._open_load_connection()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 218, in _open_load_connection\n    conn, cursor = self._adapter.connmanager.open_for_load()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/mysql.py\", line 260, in open_for_load\n    return self.open(self.isolation_repeatable_read)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:32:44'),(94,2700,'pid=2700 tid=139745586784000\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 316, in install_tempfolder_and_sdc\n    tf = getattr(app, \'temp_folder\', None)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 225, in __of__\n    return self._getOrOpenObject(parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 249, in _getOrOpenObject\n    obj = self._traverseToMountedRoot(root, parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 190, in _traverseToMountedRoot\n    transaction.savepoint(optimistic=True)\n  File \"/usr/local/zenoss/lib/python/transaction/_manager.py\", line 101, in savepoint\n    return self.get().savepoint(optimistic)\n  File \"/usr/local/zenoss/lib/python/transaction/_transaction.py\", line 260, in savepoint\n    savepoint = Savepoint(self, optimistic, *self._resources)\n  File \"/usr/local/zenoss/lib/python/transaction/_transaction.py\", line 697, in __init__\n    savepoint = savepoint()\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 1123, in savepoint\n    self._commit(None)\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 623, in _commit\n    self._store_objects(ObjectWriter(obj), transaction)\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 658, in _store_objects\n    p = writer.serialize(obj)  # This calls __getstate__ of obj\n  File \"/usr/local/zenoss/lib/python/ZODB/serialize.py\", line 422, in serialize\n    return self._dump(meta, obj.__getstate__())\n  File \"/usr/local/zenoss/lib/python/ZODB/serialize.py\", line 431, in _dump\n    self._p.dump(state)\n  File \"/usr/local/zenoss/lib/python/ZODB/serialize.py\", line 332, in persistent_id\n    oid = obj._p_oid = self._jar.new_oid()\n  File \"/usr/local/zenoss/lib/python/ZODB/DB.py\", line 953, in new_oid\n    return self.storage.new_oid()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 931, in new_oid\n    preallocated = self._with_store(f)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 305, in _with_store\n    self._open_store_connection()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 273, in _open_store_connection\n    conn, cursor = self._adapter.connmanager.open_for_store()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/connmanager.py\", line 109, in open_for_store\n    conn, cursor = self.open()\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:32:44'),(95,2700,'pid=2700 tid=139745586784000\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 391, in install_tempfolder_and_sdc\n    self.commit(\'Added session_data to temp_folder\')\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 266, in commit\n    transaction.commit()\n  File \"/usr/local/zenoss/lib/python/transaction/_manager.py\", line 89, in commit\n    return self.get().commit()\n  File \"/usr/local/zenoss/lib/python/transaction/_transaction.py\", line 333, in commit\n    self._commitResources()\n  File \"/usr/local/zenoss/lib/python/transaction/_transaction.py\", line 445, in _commitResources\n    rm.tpc_begin(self)\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 551, in tpc_begin\n    self._normal_storage.tpc_begin(transaction)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 657, in tpc_begin\n    self._restart_store()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 286, in _restart_store\n    self._open_store_connection()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 273, in _open_store_connection\n    conn, cursor = self._adapter.connmanager.open_for_store()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/connmanager.py\", line 109, in open_for_store\n    conn, cursor = self.open()\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:32:44'),(96,2700,'pid=2700 tid=139745586784000\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 391, in install_tempfolder_and_sdc\n    self.commit(\'Added session_data to temp_folder\')\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 266, in commit\n    transaction.commit()\n  File \"/usr/local/zenoss/lib/python/transaction/_manager.py\", line 89, in commit\n    return self.get().commit()\n  File \"/usr/local/zenoss/lib/python/transaction/_transaction.py\", line 333, in commit\n    self._commitResources()\n  File \"/usr/local/zenoss/lib/python/transaction/_transaction.py\", line 447, in _commitResources\n    rm.commit(self)\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 562, in commit\n    self._commit_savepoint(transaction)\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 1159, in _commit_savepoint\n    self._log.debug(\"Committing savepoints of size %s\", src.getSize())\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 374, in getSize\n    return self._adapter.stats.get_db_size()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/stats.py\", line 47, in get_db_size\n    conn, cursor = self.connmanager.open()\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:32:44'),(282,10331,'pid=10331 tid=140441732478720\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 316, in install_tempfolder_and_sdc\n    tf = getattr(app, \'temp_folder\', None)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 225, in __of__\n    return self._getOrOpenObject(parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 247, in _getOrOpenObject\n    conn = self._getMountedConnection(anyjar)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 142, in _getMountedConnection\n    self._getDB()\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 152, in _getDB\n    return getConfiguration().getDatabase(self._path)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 287, in getDatabase\n    db = factory.open(name, self.databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 185, in open\n    DB = self.createDB(database_name, databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 182, in createDB\n    return ZODBDatabase.open(self, databases)\n  File \"/usr/local/zenoss/lib/python/ZODB/config.py\", line 101, in open\n    storage = section.storage.open()\n  File \"/usr/local/zenoss/lib/python/relstorage/config.py\", line 33, in open\n    return RelStorage(adapter, name=config.name, options=options)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 167, in __init__\n    self._adapter.schema.prepare()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/schema.py\", line 856, in prepare\n    self.connmanager.open_and_call(callback)\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/connmanager.py\", line 73, in open_and_call\n    conn, cursor = self.open()\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:38:28'),(283,10331,'pid=10331 tid=140441732478720\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 316, in install_tempfolder_and_sdc\n    tf = getattr(app, \'temp_folder\', None)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 225, in __of__\n    return self._getOrOpenObject(parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 247, in _getOrOpenObject\n    conn = self._getMountedConnection(anyjar)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 142, in _getMountedConnection\n    self._getDB()\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 152, in _getDB\n    return getConfiguration().getDatabase(self._path)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 287, in getDatabase\n    db = factory.open(name, self.databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 185, in open\n    DB = self.createDB(database_name, databases)\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/datatypes.py\", line 182, in createDB\n    return ZODBDatabase.open(self, databases)\n  File \"/usr/local/zenoss/lib/python/ZODB/config.py\", line 127, in open\n    **options)\n  File \"/usr/local/zenoss/lib/python/ZODB/DB.py\", line 444, in __init__\n    temp_storage.load(z64, \'\')\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 460, in load\n    self._before_load()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 452, in _before_load\n    self._restart_load_and_poll()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 1207, in _restart_load_and_poll\n    self._adapter.poller.poll_invalidations, prev, ignore_tid)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 251, in _restart_load_and_call\n    self._open_load_connection()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 218, in _open_load_connection\n    conn, cursor = self._adapter.connmanager.open_for_load()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/mysql.py\", line 260, in open_for_load\n    return self.open(self.isolation_repeatable_read)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:38:28'),(284,10331,'pid=10331 tid=140441732478720\n/usr/local/zenoss/zopehome/runzope -C /usr/local/zenoss/etc/zope.conf\n  File \"/usr/local/zenoss/zopehome/runzope\", line 8, in <module>\n    load_entry_point(\'Zope2==2.13.13\', \'console_scripts\', \'runzope\')()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/run.py\", line 21, in run\n    starter.prepare()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 86, in prepare\n    self.startZope()\n  File \"/usr/local/zenoss/lib/python/Zope2/Startup/__init__.py\", line 259, in startZope\n    Zope2.startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/__init__.py\", line 47, in startup\n    _startup()\n  File \"/usr/local/zenoss/lib/python/Zope2/App/startup.py\", line 129, in startup\n    OFS.Application.initialize(application)\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 251, in initialize\n    initializer.initialize()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 271, in initialize\n    self.install_tempfolder_and_sdc()\n  File \"/usr/local/zenoss/lib/python/OFS/Application.py\", line 316, in install_tempfolder_and_sdc\n    tf = getattr(app, \'temp_folder\', None)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 225, in __of__\n    return self._getOrOpenObject(parent)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 247, in _getOrOpenObject\n    conn = self._getMountedConnection(anyjar)\n  File \"/usr/local/zenoss/lib/python/Products/ZODBMountPoint/MountedObject.py\", line 144, in _getMountedConnection\n    return anyjar.get_connection(self._getDBName())\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 374, in get_connection\n    before=self.before,\n  File \"/usr/local/zenoss/lib/python/ZODB/DB.py\", line 751, in open\n    result.open(transaction_manager)\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 1045, in open\n    self._flush_invalidations()\n  File \"/usr/local/zenoss/lib/python/ZODB/Connection.py\", line 492, in _flush_invalidations\n    invalidated = self._storage.poll_invalidations()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 1233, in poll_invalidations\n    changes, new_polled_tid = self._restart_load_and_poll()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 1207, in _restart_load_and_poll\n    self._adapter.poller.poll_invalidations, prev, ignore_tid)\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 251, in _restart_load_and_call\n    self._open_load_connection()\n  File \"/usr/local/zenoss/lib/python/relstorage/storage.py\", line 218, in _open_load_connection\n    conn, cursor = self._adapter.connmanager.open_for_load()\n  File \"/usr/local/zenoss/lib/python/relstorage/adapters/mysql.py\", line 260, in open_for_load\n    return self.open(self.isolation_repeatable_read)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 47, in open\n    record_pid(conn, cursor)\n  File \"/usr/local/zenoss/Products/ZenUtils/patches/mysqladaptermonkey.py\", line 34, in record_pid\n    stacktrace = \'\'.join(traceback.format_stack())\n','2014-04-25 15:38:28');
/*!40000 ALTER TABLE `connection_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `new_oid`
--

DROP TABLE IF EXISTS `new_oid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `new_oid` (
  `zoid` bigint(20) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`zoid`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `new_oid`
--

LOCK TABLES `new_oid` WRITE;
/*!40000 ALTER TABLE `new_oid` DISABLE KEYS */;
INSERT INTO `new_oid` VALUES (1),(2),(3);
/*!40000 ALTER TABLE `new_oid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_ref`
--

DROP TABLE IF EXISTS `object_ref`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_ref` (
  `zoid` bigint(20) NOT NULL,
  `to_zoid` bigint(20) NOT NULL,
  `tid` bigint(20) NOT NULL,
  PRIMARY KEY (`zoid`,`to_zoid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_ref`
--

LOCK TABLES `object_ref` WRITE;
/*!40000 ALTER TABLE `object_ref` DISABLE KEYS */;
/*!40000 ALTER TABLE `object_ref` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_refs_added`
--

DROP TABLE IF EXISTS `object_refs_added`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_refs_added` (
  `zoid` bigint(20) NOT NULL,
  `tid` bigint(20) NOT NULL,
  PRIMARY KEY (`zoid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_refs_added`
--

LOCK TABLES `object_refs_added` WRITE;
/*!40000 ALTER TABLE `object_refs_added` DISABLE KEYS */;
/*!40000 ALTER TABLE `object_refs_added` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `object_state`
--

DROP TABLE IF EXISTS `object_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `object_state` (
  `zoid` bigint(20) NOT NULL,
  `tid` bigint(20) NOT NULL,
  `state_size` bigint(20) NOT NULL,
  `state` longblob,
  PRIMARY KEY (`zoid`),
  KEY `object_state_tid` (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPRESSED;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `object_state`
--

LOCK TABLES `object_state` WRITE;
/*!40000 ALTER TABLE `object_state` DISABLE KEYS */;
INSERT INTO `object_state` VALUES (0,263010623444214596,119,'cpersistent.mapping\nPersistentMapping\nq.}qUdataq}qUApplicationq(U\0\0\0\0\0\0\0qcOFS.Application\nApplication\nqtQss.'),(1,263010623444214596,369,'cOFS.Application\nApplication\nq.}q(U_objectsq(}q(U	meta_typeqUUser FolderqUidqU	acl_usersqu}q	(hU\rControl Panelq\nhU\rControl_Panelqu}q(hUFolderq\rhUtemp_folderqutqh(U\0\0\0\0\0\0\0qcOFS.userfolder\nUserFolder\nqtQU__allow_groups__q(hhtQUtemp_folderq(U\0\0\0\0\0\0\0qcOFS.Folder\nFolder\nqtQh(U\0\0\0\0\0\0\0qcApp.ApplicationManager\nApplicationManager\nqtQu.'),(2,263010623444214596,121,'cOFS.userfolder\nUserFolder\nq.}q(U\r_ofs_migratedqI01\nUdataq(U\0\0\0\0\0\0\0qcPersistence.mapping\nPersistentMapping\nqtQu.'),(3,263010623444214596,107,'cApp.ApplicationManager\nApplicationManager\nq.}qUProductsq(U\0\0\0\0\0\0\0qcApp.Product\nProductFolder\nqtQs.'),(4,263010623444214596,34,'cApp.Product\nProductFolder\nq.}q.'),(5,263010623444214596,58,'cPersistence.mapping\nPersistentMapping\nq.}qUdataq}qs.'),(6,263010623444214596,232,'cOFS.Folder\nFolder\nq.}q(U_reserved_namesq(Usession_dataqtqh(U\0\0\0\0\0\0\0qcProducts.Transience.Transience\nTransientObjectContainer\nqtQUidqUtemp_folderq	U_objectsq\n(}q(U	meta_typeqU\ZTransient Object Containerq\rhhutqu.'),(7,263010623444214596,523,'cProducts.Transience.Transience\nTransientObjectContainer\nq.}q(U_addCallbackqNU\r_timeout_secsqM°UgetLenq(U\0\0\0\0\0\0\0qcProducts.Transience.Transience\nLength2\nqtQU_delCallbackqNU_last_finalized_timesliceq	(U\0\0\0\0\0\0\0	q\ncProducts.Transience.Transience\nIncreaser\nqtQU_limitqJ †\0U_periodq\rKU_timeout_slicesqK<U_lengthq(hhtQUtitleqUSession Data ContainerqU_dataq(U\0\0\0\0\0\0\0\nqcBTrees.IOBTree\nIOBTree\nqtQUidqUsession_dataqU_last_gc_timesliceq(U\0\0\0\0\0\0\0qhtQU_max_timesliceq(U\0\0\0\0\0\0\0q\ZhtQu.'),(8,263010623444214596,84,'cProducts.Transience.Transience\nLength2\nq.}q(UceilingqK\0UvalueqK\0UfloorqK\0u.'),(9,263010623444214596,51,'cProducts.Transience.Transience\nIncreaser\nq.Jìÿÿÿ.'),(10,263010623444214596,722,'cBTrees.IOBTree\nIOBTree\nq.((((J€ZS(U\0\0\0\0\0\0\0\rqcBTrees.OOBTree\nOOBTree\nqtQJ,€ZS(U\0\0\0\0\0\0\0qhtQJ@€ZS(U\0\0\0\0\0\0\0qhtQJT€ZS(U\0\0\0\0\0\0\0qhtQJh€ZS(U\0\0\0\0\0\0\0qhtQJ|€ZS(U\0\0\0\0\0\0\0qhtQJ€ZS(U\0\0\0\0\0\0\0q	htQJ¤€ZS(U\0\0\0\0\0\0\0q\nhtQJ¸€ZS(U\0\0\0\0\0\0\0qhtQJÌ€ZS(U\0\0\0\0\0\0\0qhtQJà€ZS(U\0\0\0\0\0\0\0q\rhtQJô€ZS(U\0\0\0\0\0\0\0qhtQJZS(U\0\0\0\0\0\0\0qhtQJZS(U\0\0\0\0\0\0\0\ZqhtQJ0ZS(U\0\0\0\0\0\0\0qhtQJDZS(U\0\0\0\0\0\0\0qhtQJXZS(U\0\0\0\0\0\0\0qhtQJlZS(U\0\0\0\0\0\0\0qhtQJ€ZS(U\0\0\0\0\0\0\0qhtQJ”ZS(U\0\0\0\0\0\0\0 qhtQJ¨ZS(U\0\0\0\0\0\0\0!qhtQJ¼ZS(U\0\0\0\0\0\0\0\"qhtQJÐZS(U\0\0\0\0\0\0\0#qhtQJäZS(U\0\0\0\0\0\0\0$q\ZhtQJøZS(U\0\0\0\0\0\0\0%qhtQJ‚ZS(U\0\0\0\0\0\0\0&qhtQJ ‚ZS(U\0\0\0\0\0\0\0\'qhtQJ4‚ZS(U\0\0\0\0\0\0\0(qhtQJH‚ZS(U\0\0\0\0\0\0\0)qhtQJ\\‚ZS(U\0\0\0\0\0\0\0*q htQttttq!.'),(11,263010623444214596,51,'cProducts.Transience.Transience\nIncreaser\nq.Jìÿÿÿ.'),(12,263010623444214596,51,'cProducts.Transience.Transience\nIncreaser\nq.J\\‚ZS.'),(13,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(14,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(15,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(16,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(17,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(18,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(19,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(20,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(21,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(22,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(23,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(24,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(25,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(26,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(27,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(28,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(29,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(30,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(31,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(32,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(33,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(34,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(35,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(36,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(37,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(38,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(39,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(40,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(41,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.'),(42,263010623444214596,29,'cBTrees.OOBTree\nOOBTree\nq.N.');
/*!40000 ALTER TABLE `object_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pack_object`
--

DROP TABLE IF EXISTS `pack_object`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pack_object` (
  `zoid` bigint(20) NOT NULL,
  `keep` tinyint(1) NOT NULL,
  `keep_tid` bigint(20) NOT NULL,
  `visited` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`zoid`),
  KEY `pack_object_keep_zoid` (`keep`,`zoid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pack_object`
--

LOCK TABLES `pack_object` WRITE;
/*!40000 ALTER TABLE `pack_object` DISABLE KEYS */;
/*!40000 ALTER TABLE `pack_object` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schema_version`
--

DROP TABLE IF EXISTS `schema_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schema_version` (
  `version` int(11) NOT NULL,
  `installed_time` datetime NOT NULL,
  PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schema_version`
--

LOCK TABLES `schema_version` WRITE;
/*!40000 ALTER TABLE `schema_version` DISABLE KEYS */;
INSERT INTO `schema_version` VALUES (1,'2014-04-25 10:13:26'),(2,'2014-04-25 10:13:26'),(3,'2014-04-25 10:13:26');
/*!40000 ALTER TABLE `schema_version` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-25 10:46:49
