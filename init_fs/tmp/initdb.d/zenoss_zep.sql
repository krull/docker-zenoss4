-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: zenoss_zep
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
-- Table structure for table `agent`
--

DROP TABLE IF EXISTS `agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent`
--

LOCK TABLES `agent` WRITE;
/*!40000 ALTER TABLE `agent` DISABLE KEYS */;
INSERT INTO `agent` VALUES (7,'zencommand'),(12,'zeneventlog'),(14,'zenjmx'),(5,'zenmodeler'),(6,'zenperfsnmp'),(2,'zenping'),(8,'zenprocess'),(15,'zenpython'),(3,'zenstatus'),(1,'zensyslog'),(4,'zentrap'),(11,'zenwin'),(13,'zenwinperf');
/*!40000 ALTER TABLE `agent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `config`
--

DROP TABLE IF EXISTS `config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config` (
  `config_name` varchar(64) NOT NULL,
  `config_value` varchar(4096) NOT NULL,
  PRIMARY KEY (`config_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='ZEP configuration data.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config`
--

LOCK TABLES `config` WRITE;
/*!40000 ALTER TABLE `config` DISABLE KEYS */;
/*!40000 ALTER TABLE `config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daemon_heartbeat`
--

DROP TABLE IF EXISTS `daemon_heartbeat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `daemon_heartbeat` (
  `monitor` varchar(255) NOT NULL COMMENT 'The monitor sending heartbeats.',
  `daemon` varchar(255) NOT NULL DEFAULT '' COMMENT 'The daemon sending heartbeats.',
  `timeout_seconds` int(11) NOT NULL COMMENT 'Amount of time in seconds before heartbeat events are sent.',
  `last_time` bigint(20) NOT NULL COMMENT 'Last time the heartbeat was received.',
  PRIMARY KEY (`monitor`,`daemon`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Daemon heartbeats.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daemon_heartbeat`
--

LOCK TABLES `daemon_heartbeat` WRITE;
/*!40000 ALTER TABLE `daemon_heartbeat` DISABLE KEYS */;
INSERT INTO `daemon_heartbeat` VALUES ('localhost','zenactiond',180,1398440391021),('localhost','zencommand',900,1398440348232),('localhost','zeneventd',180,1398440375610),('localhost','zeneventlog',900,1398440358317),('localhost','zenhub',90,1398440401987),('localhost','zenjmx',900,1398440366748),('localhost','zenmodeler',90,1398440402205),('localhost','zenperfsnmp',900,1398440345214),('localhost','zenping',900,1398440325563),('localhost','zenprocess',540,1398440351210),('localhost','zenpython',900,1398440370783),('localhost','zenstatus',180,1398440387717),('localhost','zenwin',900,1398440354701),('localhost','zenwinperf',900,1398440362131);
/*!40000 ALTER TABLE `daemon_heartbeat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_archive`
--

DROP TABLE IF EXISTS `event_archive`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_archive` (
  `uuid` binary(16) NOT NULL,
  `fingerprint` varchar(255) NOT NULL COMMENT 'Dynamically generated fingerprint that allows the system to perform de-duplication on repeating events that share similar characteristics.',
  `status_id` tinyint(4) NOT NULL,
  `event_group_id` int(11) DEFAULT NULL COMMENT 'Can be used to group similar types of events. This is primarily an extension point for customization.',
  `event_class_id` int(11) NOT NULL,
  `event_class_key_id` int(11) DEFAULT NULL COMMENT 'Used as the first step in mapping an unknown event into an event class.',
  `event_class_mapping_uuid` binary(16) DEFAULT NULL COMMENT 'If this event was matched by one of the configured event class mappings, contains the UUID of that mapping rule.',
  `event_key_id` int(11) DEFAULT NULL,
  `severity_id` tinyint(4) NOT NULL,
  `element_uuid` binary(16) DEFAULT NULL,
  `element_type_id` tinyint(4) DEFAULT NULL,
  `element_identifier` varchar(255) NOT NULL,
  `element_title` varchar(255) DEFAULT NULL,
  `element_sub_uuid` binary(16) DEFAULT NULL,
  `element_sub_type_id` tinyint(4) DEFAULT NULL,
  `element_sub_identifier` varchar(255) DEFAULT NULL,
  `element_sub_title` varchar(255) DEFAULT NULL,
  `update_time` bigint(20) NOT NULL COMMENT 'Last time any modification was made to the event.',
  `first_seen` bigint(20) NOT NULL COMMENT 'UTC Time. First time that the event occurred.',
  `status_change` bigint(20) NOT NULL COMMENT 'Last time that the event status changed.',
  `last_seen` bigint(20) NOT NULL COMMENT 'UTC time. Most recent time that the event occurred.',
  `event_count` int(11) NOT NULL COMMENT 'Number of occurrences of the event.',
  `monitor_id` int(11) DEFAULT NULL COMMENT 'In a distributed setup, contains the name of the collector from which the event originated.',
  `agent_id` int(11) DEFAULT NULL COMMENT 'Typically the name of the daemon that generated the event. For example, an SNMP threshold event will have zenperfsnmp as its agent.',
  `syslog_facility` int(11) DEFAULT NULL COMMENT 'The syslog facility.',
  `syslog_priority` tinyint(4) DEFAULT NULL COMMENT 'The syslog priority.',
  `nt_event_code` int(11) DEFAULT NULL COMMENT 'The Windows NT Event Code.',
  `current_user_uuid` binary(16) DEFAULT NULL COMMENT 'UUID of the user who acknowledged this event.',
  `current_user_name` varchar(32) DEFAULT NULL COMMENT 'Name of the user who acknowledged this event.',
  `cleared_by_event_uuid` binary(16) DEFAULT NULL COMMENT 'The UUID of the event that cleared this event (for events with status == CLEARED).',
  `summary` varchar(255) NOT NULL DEFAULT '',
  `message` varchar(4096) NOT NULL DEFAULT '',
  `details_json` mediumtext COMMENT 'JSON encoded event details.',
  `tags_json` mediumtext COMMENT 'JSON encoded event tags.',
  `notes_json` mediumtext COMMENT 'JSON encoded event notes (formerly log).',
  `audit_json` mediumtext COMMENT 'JSON encoded event audit log.',
  PRIMARY KEY (`uuid`,`last_seen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY RANGE (last_seen)
(PARTITION p20140126_000000 VALUES LESS THAN (1390694400000) ENGINE = InnoDB,
 PARTITION p20140127_000000 VALUES LESS THAN (1390780800000) ENGINE = InnoDB,
 PARTITION p20140128_000000 VALUES LESS THAN (1390867200000) ENGINE = InnoDB,
 PARTITION p20140129_000000 VALUES LESS THAN (1390953600000) ENGINE = InnoDB,
 PARTITION p20140130_000000 VALUES LESS THAN (1391040000000) ENGINE = InnoDB,
 PARTITION p20140131_000000 VALUES LESS THAN (1391126400000) ENGINE = InnoDB,
 PARTITION p20140201_000000 VALUES LESS THAN (1391212800000) ENGINE = InnoDB,
 PARTITION p20140202_000000 VALUES LESS THAN (1391299200000) ENGINE = InnoDB,
 PARTITION p20140203_000000 VALUES LESS THAN (1391385600000) ENGINE = InnoDB,
 PARTITION p20140204_000000 VALUES LESS THAN (1391472000000) ENGINE = InnoDB,
 PARTITION p20140205_000000 VALUES LESS THAN (1391558400000) ENGINE = InnoDB,
 PARTITION p20140206_000000 VALUES LESS THAN (1391644800000) ENGINE = InnoDB,
 PARTITION p20140207_000000 VALUES LESS THAN (1391731200000) ENGINE = InnoDB,
 PARTITION p20140208_000000 VALUES LESS THAN (1391817600000) ENGINE = InnoDB,
 PARTITION p20140209_000000 VALUES LESS THAN (1391904000000) ENGINE = InnoDB,
 PARTITION p20140210_000000 VALUES LESS THAN (1391990400000) ENGINE = InnoDB,
 PARTITION p20140211_000000 VALUES LESS THAN (1392076800000) ENGINE = InnoDB,
 PARTITION p20140212_000000 VALUES LESS THAN (1392163200000) ENGINE = InnoDB,
 PARTITION p20140213_000000 VALUES LESS THAN (1392249600000) ENGINE = InnoDB,
 PARTITION p20140214_000000 VALUES LESS THAN (1392336000000) ENGINE = InnoDB,
 PARTITION p20140215_000000 VALUES LESS THAN (1392422400000) ENGINE = InnoDB,
 PARTITION p20140216_000000 VALUES LESS THAN (1392508800000) ENGINE = InnoDB,
 PARTITION p20140217_000000 VALUES LESS THAN (1392595200000) ENGINE = InnoDB,
 PARTITION p20140218_000000 VALUES LESS THAN (1392681600000) ENGINE = InnoDB,
 PARTITION p20140219_000000 VALUES LESS THAN (1392768000000) ENGINE = InnoDB,
 PARTITION p20140220_000000 VALUES LESS THAN (1392854400000) ENGINE = InnoDB,
 PARTITION p20140221_000000 VALUES LESS THAN (1392940800000) ENGINE = InnoDB,
 PARTITION p20140222_000000 VALUES LESS THAN (1393027200000) ENGINE = InnoDB,
 PARTITION p20140223_000000 VALUES LESS THAN (1393113600000) ENGINE = InnoDB,
 PARTITION p20140224_000000 VALUES LESS THAN (1393200000000) ENGINE = InnoDB,
 PARTITION p20140225_000000 VALUES LESS THAN (1393286400000) ENGINE = InnoDB,
 PARTITION p20140226_000000 VALUES LESS THAN (1393372800000) ENGINE = InnoDB,
 PARTITION p20140227_000000 VALUES LESS THAN (1393459200000) ENGINE = InnoDB,
 PARTITION p20140228_000000 VALUES LESS THAN (1393545600000) ENGINE = InnoDB,
 PARTITION p20140301_000000 VALUES LESS THAN (1393632000000) ENGINE = InnoDB,
 PARTITION p20140302_000000 VALUES LESS THAN (1393718400000) ENGINE = InnoDB,
 PARTITION p20140303_000000 VALUES LESS THAN (1393804800000) ENGINE = InnoDB,
 PARTITION p20140304_000000 VALUES LESS THAN (1393891200000) ENGINE = InnoDB,
 PARTITION p20140305_000000 VALUES LESS THAN (1393977600000) ENGINE = InnoDB,
 PARTITION p20140306_000000 VALUES LESS THAN (1394064000000) ENGINE = InnoDB,
 PARTITION p20140307_000000 VALUES LESS THAN (1394150400000) ENGINE = InnoDB,
 PARTITION p20140308_000000 VALUES LESS THAN (1394236800000) ENGINE = InnoDB,
 PARTITION p20140309_000000 VALUES LESS THAN (1394323200000) ENGINE = InnoDB,
 PARTITION p20140310_000000 VALUES LESS THAN (1394409600000) ENGINE = InnoDB,
 PARTITION p20140311_000000 VALUES LESS THAN (1394496000000) ENGINE = InnoDB,
 PARTITION p20140312_000000 VALUES LESS THAN (1394582400000) ENGINE = InnoDB,
 PARTITION p20140313_000000 VALUES LESS THAN (1394668800000) ENGINE = InnoDB,
 PARTITION p20140314_000000 VALUES LESS THAN (1394755200000) ENGINE = InnoDB,
 PARTITION p20140315_000000 VALUES LESS THAN (1394841600000) ENGINE = InnoDB,
 PARTITION p20140316_000000 VALUES LESS THAN (1394928000000) ENGINE = InnoDB,
 PARTITION p20140317_000000 VALUES LESS THAN (1395014400000) ENGINE = InnoDB,
 PARTITION p20140318_000000 VALUES LESS THAN (1395100800000) ENGINE = InnoDB,
 PARTITION p20140319_000000 VALUES LESS THAN (1395187200000) ENGINE = InnoDB,
 PARTITION p20140320_000000 VALUES LESS THAN (1395273600000) ENGINE = InnoDB,
 PARTITION p20140321_000000 VALUES LESS THAN (1395360000000) ENGINE = InnoDB,
 PARTITION p20140322_000000 VALUES LESS THAN (1395446400000) ENGINE = InnoDB,
 PARTITION p20140323_000000 VALUES LESS THAN (1395532800000) ENGINE = InnoDB,
 PARTITION p20140324_000000 VALUES LESS THAN (1395619200000) ENGINE = InnoDB,
 PARTITION p20140325_000000 VALUES LESS THAN (1395705600000) ENGINE = InnoDB,
 PARTITION p20140326_000000 VALUES LESS THAN (1395792000000) ENGINE = InnoDB,
 PARTITION p20140327_000000 VALUES LESS THAN (1395878400000) ENGINE = InnoDB,
 PARTITION p20140328_000000 VALUES LESS THAN (1395964800000) ENGINE = InnoDB,
 PARTITION p20140329_000000 VALUES LESS THAN (1396051200000) ENGINE = InnoDB,
 PARTITION p20140330_000000 VALUES LESS THAN (1396137600000) ENGINE = InnoDB,
 PARTITION p20140331_000000 VALUES LESS THAN (1396224000000) ENGINE = InnoDB,
 PARTITION p20140401_000000 VALUES LESS THAN (1396310400000) ENGINE = InnoDB,
 PARTITION p20140402_000000 VALUES LESS THAN (1396396800000) ENGINE = InnoDB,
 PARTITION p20140403_000000 VALUES LESS THAN (1396483200000) ENGINE = InnoDB,
 PARTITION p20140404_000000 VALUES LESS THAN (1396569600000) ENGINE = InnoDB,
 PARTITION p20140405_000000 VALUES LESS THAN (1396656000000) ENGINE = InnoDB,
 PARTITION p20140406_000000 VALUES LESS THAN (1396742400000) ENGINE = InnoDB,
 PARTITION p20140407_000000 VALUES LESS THAN (1396828800000) ENGINE = InnoDB,
 PARTITION p20140408_000000 VALUES LESS THAN (1396915200000) ENGINE = InnoDB,
 PARTITION p20140409_000000 VALUES LESS THAN (1397001600000) ENGINE = InnoDB,
 PARTITION p20140410_000000 VALUES LESS THAN (1397088000000) ENGINE = InnoDB,
 PARTITION p20140411_000000 VALUES LESS THAN (1397174400000) ENGINE = InnoDB,
 PARTITION p20140412_000000 VALUES LESS THAN (1397260800000) ENGINE = InnoDB,
 PARTITION p20140413_000000 VALUES LESS THAN (1397347200000) ENGINE = InnoDB,
 PARTITION p20140414_000000 VALUES LESS THAN (1397433600000) ENGINE = InnoDB,
 PARTITION p20140415_000000 VALUES LESS THAN (1397520000000) ENGINE = InnoDB,
 PARTITION p20140416_000000 VALUES LESS THAN (1397606400000) ENGINE = InnoDB,
 PARTITION p20140417_000000 VALUES LESS THAN (1397692800000) ENGINE = InnoDB,
 PARTITION p20140418_000000 VALUES LESS THAN (1397779200000) ENGINE = InnoDB,
 PARTITION p20140419_000000 VALUES LESS THAN (1397865600000) ENGINE = InnoDB,
 PARTITION p20140420_000000 VALUES LESS THAN (1397952000000) ENGINE = InnoDB,
 PARTITION p20140421_000000 VALUES LESS THAN (1398038400000) ENGINE = InnoDB,
 PARTITION p20140422_000000 VALUES LESS THAN (1398124800000) ENGINE = InnoDB,
 PARTITION p20140423_000000 VALUES LESS THAN (1398211200000) ENGINE = InnoDB,
 PARTITION p20140424_000000 VALUES LESS THAN (1398297600000) ENGINE = InnoDB,
 PARTITION p20140425_000000 VALUES LESS THAN (1398384000000) ENGINE = InnoDB,
 PARTITION p20140426_000000 VALUES LESS THAN (1398470400000) ENGINE = InnoDB,
 PARTITION p20140427_000000 VALUES LESS THAN (1398556800000) ENGINE = InnoDB,
 PARTITION p20140428_000000 VALUES LESS THAN (1398643200000) ENGINE = InnoDB) */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_archive`
--

LOCK TABLES `event_archive` WRITE;
/*!40000 ALTER TABLE `event_archive` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_archive` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `event_archive_index_queue_insert` AFTER INSERT ON `event_archive`
  FOR EACH ROW BEGIN
    INSERT INTO `event_archive_index_queue` SET uuid=NEW.uuid, last_seen=NEW.last_seen, update_time=NEW.update_time;
  END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `event_archive_index_queue_update` AFTER UPDATE ON `event_archive`
  FOR EACH ROW BEGIN
    INSERT INTO `event_archive_index_queue` SET uuid=NEW.uuid, last_seen=NEW.last_seen, update_time=NEW.update_time;
  END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `event_archive_index_queue_delete` AFTER DELETE ON `event_archive`
  FOR EACH ROW BEGIN
    INSERT INTO `event_archive_index_queue` SET uuid=OLD.uuid, last_seen=OLD.last_seen, update_time=OLD.update_time;
  END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `event_archive_index_queue`
--

DROP TABLE IF EXISTS `event_archive_index_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_archive_index_queue` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `uuid` binary(16) NOT NULL,
  `last_seen` bigint(20) NOT NULL,
  `update_time` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_archive_index_queue`
--

LOCK TABLES `event_archive_index_queue` WRITE;
/*!40000 ALTER TABLE `event_archive_index_queue` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_archive_index_queue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_class`
--

DROP TABLE IF EXISTS `event_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_class`
--

LOCK TABLES `event_class` WRITE;
/*!40000 ALTER TABLE `event_class` DISABLE KEYS */;
INSERT INTO `event_class` VALUES (1,'/App/Start'),(5,'/App/Stop'),(3,'/Perf'),(10,'/Status/JMX'),(2,'/Status/Ping'),(4,'/Unknown');
/*!40000 ALTER TABLE `event_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_class_key`
--

DROP TABLE IF EXISTS `event_class_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_class_key` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL COMMENT 'Free-form text field that is used as the first step in mapping an unknown event into an event class.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_class_key`
--

LOCK TABLES `event_class_key` WRITE;
/*!40000 ALTER TABLE `event_class_key` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_class_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_detail_index_config`
--

DROP TABLE IF EXISTS `event_detail_index_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_detail_index_config` (
  `detail_item_name` varchar(255) NOT NULL COMMENT 'EventDetailItem.name',
  `proto_json` mediumtext NOT NULL COMMENT 'JSON serialized EventDetailItem',
  PRIMARY KEY (`detail_item_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Event detail index configuration.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_detail_index_config`
--

LOCK TABLES `event_detail_index_config` WRITE;
/*!40000 ALTER TABLE `event_detail_index_config` DISABLE KEYS */;
INSERT INTO `event_detail_index_config` VALUES ('zenoss.device.device_class','{\"key\":\"zenoss.device.device_class\",\"type\":7,\"name\":\"Device Class\"}'),('zenoss.device.groups','{\"key\":\"zenoss.device.groups\",\"type\":7,\"name\":\"Groups\"}'),('zenoss.device.ip_address','{\"key\":\"zenoss.device.ip_address\",\"type\":6,\"name\":\"IP Address\"}'),('zenoss.device.location','{\"key\":\"zenoss.device.location\",\"type\":7,\"name\":\"Location\"}'),('zenoss.device.priority','{\"key\":\"zenoss.device.priority\",\"type\":2,\"name\":\"Priority\"}'),('zenoss.device.production_state','{\"key\":\"zenoss.device.production_state\",\"type\":2,\"name\":\"Production State\"}'),('zenoss.device.systems','{\"key\":\"zenoss.device.systems\",\"type\":7,\"name\":\"Systems\"}');
/*!40000 ALTER TABLE `event_detail_index_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_group`
--

DROP TABLE IF EXISTS `event_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL COMMENT 'Free-form text field that can be used to group similar types of events. This is primarily an extension point for customization. Currently not used in a standard system.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_group`
--

LOCK TABLES `event_group` WRITE;
/*!40000 ALTER TABLE `event_group` DISABLE KEYS */;
INSERT INTO `event_group` VALUES (1,'Ping');
/*!40000 ALTER TABLE `event_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_key`
--

DROP TABLE IF EXISTS `event_key`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_key` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL COMMENT 'Free-form text field that allows another specificity key to be used to drive the de-duplication and auto-clearing correlation process.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_key`
--

LOCK TABLES `event_key` WRITE;
/*!40000 ALTER TABLE `event_key` DISABLE KEYS */;
INSERT INTO `event_key` VALUES (1,''),(3,'high event queue'),(2,'nmap_missing'),(4,'zenmodeler cycle time');
/*!40000 ALTER TABLE `event_key` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_summary`
--

DROP TABLE IF EXISTS `event_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_summary` (
  `uuid` binary(16) NOT NULL,
  `fingerprint_hash` binary(20) NOT NULL COMMENT 'SHA-1 hash of the fingerprint.',
  `fingerprint` varchar(255) NOT NULL COMMENT 'Dynamically generated fingerprint that allows the system to perform de-duplication on repeating events that share similar characteristics.',
  `status_id` tinyint(4) NOT NULL,
  `event_group_id` int(11) DEFAULT NULL COMMENT 'Can be used to group similar types of events. This is primarily an extension point for customization.',
  `event_class_id` int(11) NOT NULL,
  `event_class_key_id` int(11) DEFAULT NULL COMMENT 'Used as the first step in mapping an unknown event into an event class.',
  `event_class_mapping_uuid` binary(16) DEFAULT NULL COMMENT 'If this event was matched by one of the configured event class mappings, contains the UUID of that mapping rule.',
  `event_key_id` int(11) DEFAULT NULL,
  `severity_id` tinyint(4) NOT NULL,
  `element_uuid` binary(16) DEFAULT NULL,
  `element_type_id` tinyint(4) DEFAULT NULL,
  `element_identifier` varchar(255) NOT NULL,
  `element_title` varchar(255) DEFAULT NULL,
  `element_sub_uuid` binary(16) DEFAULT NULL,
  `element_sub_type_id` tinyint(4) DEFAULT NULL,
  `element_sub_identifier` varchar(255) DEFAULT NULL,
  `element_sub_title` varchar(255) DEFAULT NULL,
  `update_time` bigint(20) NOT NULL COMMENT 'Last time any modification was made to the event.',
  `first_seen` bigint(20) NOT NULL COMMENT 'UTC Time. First time that the event occurred.',
  `status_change` bigint(20) NOT NULL COMMENT 'Last time that the event status changed.',
  `last_seen` bigint(20) NOT NULL COMMENT 'UTC time. Most recent time that the event occurred.',
  `event_count` int(11) NOT NULL COMMENT 'Number of occurrences of the event.',
  `monitor_id` int(11) DEFAULT NULL COMMENT 'In a distributed setup, contains the name of the collector from which the event originated.',
  `agent_id` int(11) DEFAULT NULL COMMENT 'Typically the name of the daemon that generated the event. For example, an SNMP threshold event will have zenperfsnmp as its agent.',
  `syslog_facility` int(11) DEFAULT NULL COMMENT 'The syslog facility.',
  `syslog_priority` tinyint(4) DEFAULT NULL COMMENT 'The syslog priority.',
  `nt_event_code` int(11) DEFAULT NULL COMMENT 'The Windows NT Event Code.',
  `current_user_uuid` binary(16) DEFAULT NULL COMMENT 'UUID of the user who acknowledged this event.',
  `current_user_name` varchar(32) DEFAULT NULL COMMENT 'Name of the user who acknowledged this event.',
  `clear_fingerprint_hash` binary(20) DEFAULT NULL COMMENT 'Hash of clear fingerprint used for clearing events.',
  `cleared_by_event_uuid` binary(16) DEFAULT NULL COMMENT 'The UUID of the event that cleared this event (for events with status == CLEARED).',
  `summary` varchar(255) NOT NULL DEFAULT '',
  `message` varchar(4096) NOT NULL DEFAULT '',
  `details_json` mediumtext COMMENT 'JSON encoded event details.',
  `tags_json` mediumtext COMMENT 'JSON encoded event tags.',
  `notes_json` mediumtext COMMENT 'JSON encoded event notes (formerly log).',
  `audit_json` mediumtext COMMENT 'JSON encoded event audit log.',
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `fingerprint_hash` (`fingerprint_hash`),
  KEY `element_uuid` (`element_uuid`,`element_type_id`,`element_identifier`),
  KEY `element_sub_uuid` (`element_sub_uuid`,`element_sub_type_id`,`element_sub_identifier`),
  KEY `event_summary_clear_idx` (`clear_fingerprint_hash`,`status_id`,`last_seen`),
  KEY `event_summary_age_idx` (`severity_id`,`status_id`,`last_seen`),
  KEY `event_summary_archive_idx` (`status_id`,`last_seen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_summary`
--

LOCK TABLES `event_summary` WRITE;
/*!40000 ALTER TABLE `event_summary` DISABLE KEYS */;
INSERT INTO `event_summary` VALUES ('\0\'ny,óï„Ãé¸≠¸î','á˘±⁄7÷ÀeJs˚Ä%g˙ÄÖWb','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.PySamba',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440024793,1398440024753,1398440024753,1398440024753,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.PySamba','Installed ZenPacks ZenPacks.zenoss.PySamba',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè∂¬Â','z·’j”øÀ˜⁄∏Û9púÙi∂Ø','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.WindowsMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440039950,1398440039870,1398440039870,1398440039870,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.WindowsMonitor','Installed ZenPacks ZenPacks.zenoss.WindowsMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèUÉ6','´Ü_Ht[˝s¿ ¸[ãÿ4]“áKœ','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.ActiveDirectory',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440049379,1398440049320,1398440049320,1398440049320,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.ActiveDirectory','Installed ZenPacks ZenPacks.zenoss.ActiveDirectory',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèI‰','∂0?&@Ï≤\\∑ﬁg∏n83çà˝1˜','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.IISMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440054336,1398440054275,1398440054275,1398440054275,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.IISMonitor','Installed ZenPacks ZenPacks.zenoss.IISMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèÈ©','3 ëm{I“≤Xª∫Å›?œ','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.MSExchange',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440062090,1398440062046,1398440062046,1398440062046,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.MSExchange','Installed ZenPacks ZenPacks.zenoss.MSExchange',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãèu7 ','òÀj/≠îö}µ-è≠ø-∑aı|È','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.MSMQMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440066363,1398440066324,1398440066324,1398440066324,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.MSMQMonitor','Installed ZenPacks ZenPacks.zenoss.MSMQMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãèœ_K','(IÑÓ„œt/y–IÄL¢•','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.MSSQLServer',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440071987,1398440071950,1398440071950,1398440071950,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.MSSQLServer','Installed ZenPacks ZenPacks.zenoss.MSSQLServer',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè2l','cŒ‹‰ØKÄ£9∫ùUd`Ó3÷˜$','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.ApacheMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440077446,1398440077413,1398440077413,1398440077413,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.ApacheMonitor','Installed ZenPacks ZenPacks.zenoss.ApacheMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè\"Tm',')d‚AéÓfÓõÜö6ñ\'f','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.DellMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440082598,1398440082560,1398440082560,1398440082560,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.DellMonitor','Installed ZenPacks ZenPacks.zenoss.DellMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè!ámé','Tı9R˜µWl„¸ì*Æ∂ﬁ(“¶—','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.DigMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440086616,1398440086586,1398440086586,1398440086586,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.DigMonitor','Installed ZenPacks ZenPacks.zenoss.DigMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè$Ø','Áe◊(úîEû7_Ω~\'(o«ãî','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.DnsMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440090793,1398440090756,1398440090756,1398440090756,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.DnsMonitor','Installed ZenPacks ZenPacks.zenoss.DnsMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè&|YP','Í\Z_ü®$áú•T<B≥˝/*∆í8','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.FtpMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440094932,1398440094897,1398440094897,1398440094897,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.FtpMonitor','Installed ZenPacks ZenPacks.zenoss.FtpMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè)‘]Ò','W≥¯cæçÚC“ie,íjA8˝z','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.HPMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440100542,1398440100514,1398440100514,1398440100514,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.HPMonitor','Installed ZenPacks ZenPacks.zenoss.HPMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè,wjr',')uÿw–“¡›§ƒïΩaD¨\0>b','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.HttpMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440104965,1398440104929,1398440104929,1398440104929,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.HttpMonitor','Installed ZenPacks ZenPacks.zenoss.HttpMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè/˜S','rW›*Û0LX≤\0OZGBÊü`–','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.IRCDMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440109236,1398440109205,1398440109205,1398440109205,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.IRCDMonitor','Installed ZenPacks ZenPacks.zenoss.IRCDMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè1yú§','9’™fKqéƒÆßõœïÌXûGﬁb','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.JabberMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440113369,1398440113338,1398440113338,1398440113338,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.JabberMonitor','Installed ZenPacks ZenPacks.zenoss.JabberMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè3Ì\r•','@M4#≠¶hXäÎ≥å˝≥N∫æj','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.LDAPMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440117481,1398440117449,1398440117449,1398440117449,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.LDAPMonitor','Installed ZenPacks ZenPacks.zenoss.LDAPMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè8·6','% YJ˛poˇªµú¡»›ZŒ`˙','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.NNTPMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440124466,1398440124434,1398440124434,1398440124434,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.NNTPMonitor','Installed ZenPacks ZenPacks.zenoss.NNTPMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè:âéÁ','5ˆ4¸Hñ_{£u~jı4Ñ\"QÒF','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.NtpMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440128573,1398440128541,1398440128541,1398440128541,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.NtpMonitor','Installed ZenPacks ZenPacks.zenoss.NtpMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèA5†à','2Î√Ë;Ùız^ˆg—∫)\"+','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.ZenJMX',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440139767,1398440139736,1398440139736,1398440139736,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.ZenJMX','Installed ZenPacks ZenPacks.zenoss.ZenJMX',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèD@Hy','#ÓËK÷√¶LàiÚú@Üú 0ñ','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.LinuxMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440144869,1398440144826,1398440144826,1398440144826,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.LinuxMonitor','Installed ZenPacks ZenPacks.zenoss.LinuxMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèF∑ä\n','w¸\rG\nI §∞åπTdâ3Ÿë	Z','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.ZenossVirtualHostMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440149006,1398440148973,1398440148973,1398440148973,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.ZenossVirtualHostMonitor','Installed ZenPacks ZenPacks.zenoss.ZenossVirtualHostMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèI}’˚','’AÕcEêq¥Èﬁìüƒê™mSI','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.EsxTop',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440153661,1398440153636,1398440153636,1398440153636,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.EsxTop','Installed ZenPacks ZenPacks.zenoss.EsxTop',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèK˝Ò,','~Qah?%ŸŒ Hd®ôøÀÚæá','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.XenMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440157857,1398440157826,1398440157826,1398440157826,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.XenMonitor','Installed ZenPacks ZenPacks.zenoss.XenMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèNh]','¨(ˆcz¬(ÎÇa2·€ÑÈ∞óÒ\n','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.DeviceSearch',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440161908,1398440161873,1398440161873,1398440161873,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.DeviceSearch','Installed ZenPacks ZenPacks.zenoss.DeviceSearch',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèTDxÓ','ù-CCª5Ky“æÄpm<øú∞|3','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.PythonCollector',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440171741,1398440171706,1398440171706,1398440171706,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.PythonCollector','Installed ZenPacks ZenPacks.zenoss.PythonCollector',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„ÃèV∆Aœ','’ºâ˜·ò§\'˝éE°Òˆë^@','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.WBEM',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440175947,1398440175915,1398440175915,1398440175915,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.WBEM','Installed ZenPacks ZenPacks.zenoss.WBEM',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãè^\0Ä','Ω∏ÃW[√=ãà^/‡=Õ·','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.Microsoft.Windows',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440188070,1398440187889,1398440187889,1398440187889,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.Microsoft.Windows','Installed ZenPacks ZenPacks.zenoss.Microsoft.Windows',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,óï„Ãèo ë','0áØù$ç3¥-ìfÁUy3==”K','localhost|zencommand|/App/Stop|2|stopped',4,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zencommand',NULL,1398440343258,1398440216653,1398440343258,1398440216653,1,1,7,NULL,NULL,NULL,NULL,NULL,'∑…q9ÕP©öQ>≠Ú¸ËL’ÎÒ','\0\'ny,™~„Ãè∫n ','stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,'{\"timestamp\":1398440343258,\"new_status\":4}'),('\0\'ny,óï„Ãèo˛‚','∆ñ•é∆_óJ‰¿ZzÉé5ﬁ°','localhost|zenperfsnmp|/App/Stop|2|stopped',4,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenperfsnmp',NULL,1398440340236,1398440216703,1398440340236,1398440216703,1,1,6,NULL,NULL,NULL,NULL,NULL,'Ø¿≈|ç•C∑Ω˝ $í˛™–˛','\0\'ny,™~„Ãè∏≤OÈ','stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,'{\"timestamp\":1398440340236,\"new_status\":4}'),('\0\'ny,óï„Ãèo$˜3','GpS∑\Z\ZLÂuçÎ^úêÒ1p','localhost|zenmodeler|/App/Stop|2|stopped',4,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenmodeler',NULL,1398440337200,1398440216781,1398440337200,1398440216781,1,1,5,NULL,NULL,NULL,NULL,NULL,'ÖÖ\'Ä0U¬kk}ã/âr\\','\0\'ny,™~„Ãè∂„(','stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,'{\"timestamp\":1398440337200,\"new_status\":4}'),('\0\'ny,óï„Ãèo7‚Ù','¢‡ø‘€Í≠]ÁLó{1ø–√¿º','localhost|zenprocess|/App/Stop|2|stopped',4,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenprocess',NULL,1398440346225,1398440216625,1398440346225,1398440216625,1,1,8,NULL,NULL,NULL,NULL,NULL,'g˘—w|7˙{\Z‘ı0G+≥w÷','\0\'ny,™~„ÃèºD);','stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,'{\"timestamp\":1398440346225,\"new_status\":4}'),('\0\'ny,óï„ÃèoC{µ','$%^,]i/cUb‰Óªùzıoi0','localhost|zenstatus|/App/Stop|2|stopped',4,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenstatus',NULL,1398440327727,1398440216991,1398440327727,1398440216991,1,1,3,NULL,NULL,NULL,NULL,NULL,'¸]ﬂ≥Q\n‡DöG9°‰^ÿ¢IÿΩ','\0\'ny,™~„Ãè±=ó','stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,'{\"timestamp\":1398440327727,\"new_status\":4}'),('\0\'ny,óï„ÃèoWQ÷','%ñ$∆hÕÇ˘wÖû·«„\\r√ß','localhost|zenping|/App/Stop|2|stopped',4,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenping',NULL,1398440323643,1398440217130,1398440323643,1398440217130,1,1,2,NULL,NULL,NULL,NULL,NULL,'R\nIéÆ§–Ñq:6´Op?√–ÈÓ','\0\'ny,™~„ÃèÆƒÄ∆','stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,'{\"timestamp\":1398440323643,\"new_status\":4}'),('\0\'ny,™~„ÃèÆƒÄ∆','öN·´ÜÖ√‰ﬁB¡+f0ŸlŒ`Ú','localhost|zenping|/App/Start|0|started',3,NULL,1,NULL,NULL,1,0,NULL,1,'localhost',NULL,NULL,2,'zenping',NULL,1398440323568,1398440320552,1398440320552,1398440320552,1,1,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'started','started','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\",\"0111c5ff-3150-4f1b-b139-3000de3a6840\"]}]',NULL,NULL),('\0\'ny,™~„Ãè±=ó','`ui÷ô≤÷}≈áP†œQñú¡','localhost|zenstatus|/App/Start|0|started',3,NULL,1,NULL,NULL,1,0,NULL,1,'localhost',NULL,NULL,2,'zenstatus',NULL,1398440327722,1398440327671,1398440327671,1398440327671,1,1,3,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'started','started','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\",\"0111c5ff-3150-4f1b-b139-3000de3a6840\"]}]',NULL,NULL),('\0\'ny,™~„Ãè∂„(','ˇ3ÈåCMxŒüúöfÌuäıÌ','localhost|zenmodeler|/App/Start|0|started',3,NULL,1,NULL,NULL,1,0,NULL,1,'localhost',NULL,NULL,2,'zenmodeler',NULL,1398440337195,1398440337158,1398440337158,1398440337158,1,1,5,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'started','started','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\",\"0111c5ff-3150-4f1b-b139-3000de3a6840\"]}]',NULL,NULL),('\0\'ny,™~„Ãè∏≤OÈ','©h√¸_h–h-?05JÔY2','localhost|zenperfsnmp|/App/Start|0|started',3,NULL,1,NULL,NULL,1,0,NULL,1,'localhost',NULL,NULL,2,'zenperfsnmp',NULL,1398440340231,1398440340202,1398440340202,1398440340202,1,1,6,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'started','started','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\",\"0111c5ff-3150-4f1b-b139-3000de3a6840\"]}]',NULL,NULL),('\0\'ny,™~„Ãè∫n ','4xjËöUΩwB©Ô¿T)ÇNV,°','localhost|zencommand|/App/Start|0|started',3,NULL,1,NULL,NULL,1,0,NULL,1,'localhost',NULL,NULL,2,'zencommand',NULL,1398440343246,1398440343218,1398440343218,1398440343218,1,1,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'started','started','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\",\"0111c5ff-3150-4f1b-b139-3000de3a6840\"]}]',NULL,NULL),('\0\'ny,™~„ÃèºD);','|ﬁ÷qi¸ÁÕ\0⁄˚ìLñ8¨÷','localhost|zenprocess|/App/Start|0|started',3,NULL,1,NULL,NULL,1,0,NULL,1,'localhost',NULL,NULL,2,'zenprocess',NULL,1398440346221,1398440346198,1398440346198,1398440346198,1,1,8,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'started','started','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\",\"0111c5ff-3150-4f1b-b139-3000de3a6840\"]}]',NULL,NULL),('\0\'ny,™~„Ãè“§ƒ¨','ùu˛¡7≈·CÃÔHπ:.≤„Å ‹','ubuntu||/Unknown|2|Installed ZenPacks ZenPacks.zenoss.MySqlMonitor',0,NULL,4,NULL,NULL,1,2,NULL,1,'ubuntu',NULL,NULL,NULL,NULL,NULL,1398440383764,1398440383666,1398440383666,1398440383666,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,' ·_ì¿aÀûrmX‚:ù˝—5Ë%',NULL,'Installed ZenPacks ZenPacks.zenoss.MySqlMonitor','Installed ZenPacks ZenPacks.zenoss.MySqlMonitor',NULL,'[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"24d7b68b-a994-4ec8-a698-2661923e1ef4\"]}]',NULL,NULL),('\0\'ny,™~„Ãè‚éh=','Èô0˝æÏc‰Çﬂù˘P$.“Ä','localhost|zenpython|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenpython',NULL,1398440410462,1398440410395,1398440410395,1398440410395,1,1,15,NULL,NULL,NULL,NULL,NULL,'W∆©⁄l0’wMõv@kò@∫@°Y',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè‚•$é','îÃ¡ÛW©!û≥àâ≠-LøH<ò','localhost|zenjmx|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenjmx',NULL,1398440410611,1398440410549,1398440410549,1398440410549,1,1,14,NULL,NULL,NULL,NULL,NULL,'Âby˛|âY∏L‚\ZYŒ‘ˆ',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè‚∏O','Uó˘\'»ÆL7\'“€óı»—Ív¬','localhost|zenwinperf|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenwinperf',NULL,1398440410735,1398440410703,1398440410703,1398440410703,1,1,13,NULL,NULL,NULL,NULL,NULL,'K«)˙÷õÏáÎÆ‰Ë£è»˙àf',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè‚ _–','K)√ ¯u.ŒâÑ∑Ò~abKπ¿','localhost|zeneventlog|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zeneventlog',NULL,1398440410855,1398440410829,1398440410829,1398440410829,1,1,12,NULL,NULL,NULL,NULL,NULL,'XkR9•r%Œ&Ë?ÈZÅ›\Zé)',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè‚Ëñ1','<áØ+ùÀ8&Ú	ãÂÂuhd','localhost|zenwin|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenwin',NULL,1398440411053,1398440411029,1398440411029,1398440411029,1,1,11,NULL,NULL,NULL,NULL,NULL,'Z∏A3RÙtd_ó€ÕœOõ´q',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè‚˙óí','≥ŸäTË” ›=1‘›ıg©No©Ó','localhost|zenprocess|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenprocess',NULL,1398440411171,1398440411141,1398440411141,1398440411141,1,1,8,NULL,NULL,NULL,NULL,NULL,'g˘—w|7˙{\Z‘ı0G+≥w÷',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè„\Z¢≥','’ƒCkzk«ßÁh¥[}4:~','localhost|zencommand|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zencommand',NULL,1398440411381,1398440411335,1398440411335,1398440411335,1,1,7,NULL,NULL,NULL,NULL,NULL,'∑…q9ÕP©öQ>≠Ú¸ËL’ÎÒ',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè„8<‘','˘ˇƒÈU÷∫ñõ~®C‹äÄ522','localhost|zenperfsnmp|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenperfsnmp',NULL,1398440411575,1398440411539,1398440411539,1398440411539,1,1,6,NULL,NULL,NULL,NULL,NULL,'Ø¿≈|ç•C∑Ω˝ $í˛™–˛',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè„<˜≈','7,◊æÂ¥+ü?¡Á›d*Sx˙26','localhost|zenmodeler|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenmodeler',NULL,1398440411606,1398440411583,1398440411583,1398440411583,1,1,5,NULL,NULL,NULL,NULL,NULL,'ÖÖ\'Ä0U¬kk}ã/âr\\',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè„[U6','€ø‘˘G›lËK@äW¬õÖ[€fô','localhost|zenstatus|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenstatus',NULL,1398440411804,1398440411773,1398440411773,1398440411773,1,1,3,NULL,NULL,NULL,NULL,NULL,'¸]ﬂ≥Q\n‡DöG9°‰^ÿ¢IÿΩ',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL),('\0\'ny,™~„Ãè„n@˜','≠ÓO¡”Îß…∏çﬂ∂ª≠˛\r∑¨K','localhost|zenping|/App/Stop|2|stopped',0,NULL,5,NULL,NULL,1,2,NULL,1,'localhost',NULL,NULL,2,'zenping',NULL,1398440411929,1398440411884,1398440411884,1398440411884,1,1,2,NULL,NULL,NULL,NULL,NULL,'R\nIéÆ§–Ñq:6´Op?√–ÈÓ',NULL,'stopped','stopped','[{\"name\":\"manager\",\"value\":[\"ubuntu\"]}]','[{\"type\":\"zenoss.event.event_class\",\"uuid\":[\"a95da791-4d9e-45bc-a3e5-49bf713a9bc7\",\"5f8945a3-30c8-41a8-a691-9ceee11e6e15\"]}]',NULL,NULL);
/*!40000 ALTER TABLE `event_summary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_summary_index_queue`
--

DROP TABLE IF EXISTS `event_summary_index_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_summary_index_queue` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `uuid` binary(16) NOT NULL,
  `update_time` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_summary_index_queue`
--

LOCK TABLES `event_summary_index_queue` WRITE;
/*!40000 ALTER TABLE `event_summary_index_queue` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_summary_index_queue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_time`
--

DROP TABLE IF EXISTS `event_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_time` (
  `summary_uuid` binary(16) NOT NULL COMMENT 'UUID of the event summary this occurrence was de-duplicated into.',
  `processed` bigint(20) NOT NULL COMMENT 'UTC Time. Time the event processed by zep ',
  `created` bigint(20) NOT NULL COMMENT 'UTC Time. Time that the event occurred.',
  `first_seen` bigint(20) NOT NULL COMMENT 'UTC Time. Time that the event was first seen.',
  KEY `processed` (`processed`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8
/*!50100 PARTITION BY RANGE (processed)
(PARTITION p20140425_160000 VALUES LESS THAN (1398441600000) ENGINE = MyISAM,
 PARTITION p20140425_170000 VALUES LESS THAN (1398445200000) ENGINE = MyISAM) */;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_time`
--

LOCK TABLES `event_time` WRITE;
/*!40000 ALTER TABLE `event_time` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_trigger`
--

DROP TABLE IF EXISTS `event_trigger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_trigger` (
  `uuid` binary(16) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `enabled` tinyint(4) NOT NULL,
  `rule_api_version` tinyint(4) NOT NULL,
  `rule_type_id` tinyint(4) NOT NULL,
  `rule_source` varchar(8192) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_trigger`
--

LOCK TABLES `event_trigger` WRITE;
/*!40000 ALTER TABLE `event_trigger` DISABLE KEYS */;
INSERT INTO `event_trigger` VALUES ('•∂ê\r£WL•åBàxÄŒ±¢','MSExchangeISWMTotal16MBFreeBlocks',1,1,1,'(dev.production_state < 1000) and (dev.device_class == \"/Server/Windows/MSExchange\") and (evt.event_class == \"/Win/Exchange\")');
/*!40000 ALTER TABLE `event_trigger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_trigger_signal_spool`
--

DROP TABLE IF EXISTS `event_trigger_signal_spool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_trigger_signal_spool` (
  `uuid` binary(16) NOT NULL,
  `event_trigger_subscription_uuid` binary(16) NOT NULL,
  `event_summary_uuid` binary(16) NOT NULL,
  `flush_time` bigint(20) NOT NULL DEFAULT '0' COMMENT 'A signal will be sent when the flush_time is reached',
  `created` bigint(20) NOT NULL,
  `event_count` int(11) NOT NULL DEFAULT '1' COMMENT 'The number of times the event occurred while the signal was in the spool.',
  `sent_signal` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `event_trigger_subscription_uuid` (`event_trigger_subscription_uuid`,`event_summary_uuid`),
  KEY `fk_event_summary_uuid` (`event_summary_uuid`),
  KEY `flush_time` (`flush_time`),
  KEY `created` (`created`),
  CONSTRAINT `fk_event_summary_uuid` FOREIGN KEY (`event_summary_uuid`) REFERENCES `event_summary` (`uuid`) ON DELETE CASCADE,
  CONSTRAINT `fk_event_trigger_subscription_uuid` FOREIGN KEY (`event_trigger_subscription_uuid`) REFERENCES `event_trigger_subscription` (`uuid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Spool for event flapping.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_trigger_signal_spool`
--

LOCK TABLES `event_trigger_signal_spool` WRITE;
/*!40000 ALTER TABLE `event_trigger_signal_spool` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_trigger_signal_spool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_trigger_subscription`
--

DROP TABLE IF EXISTS `event_trigger_subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_trigger_subscription` (
  `uuid` binary(16) NOT NULL,
  `event_trigger_uuid` binary(16) NOT NULL,
  `subscriber_uuid` binary(16) NOT NULL,
  `delay_seconds` int(11) NOT NULL DEFAULT '0',
  `repeat_seconds` int(11) NOT NULL DEFAULT '0',
  `send_initial_occurrence` tinyint(4) NOT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `event_trigger_uuid` (`event_trigger_uuid`,`subscriber_uuid`),
  CONSTRAINT `fk_event_trigger_uuid` FOREIGN KEY (`event_trigger_uuid`) REFERENCES `event_trigger` (`uuid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_trigger_subscription`
--

LOCK TABLES `event_trigger_subscription` WRITE;
/*!40000 ALTER TABLE `event_trigger_subscription` DISABLE KEYS */;
INSERT INTO `event_trigger_subscription` VALUES ('\0\'ny,óï„Ãè±Q¯','•∂ê\r£WL•åBàxÄŒ±¢',' ËX˘jE8ípZ@¬±Ê',0,0,1);
/*!40000 ALTER TABLE `event_trigger_subscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `index_metadata`
--

DROP TABLE IF EXISTS `index_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `index_metadata` (
  `zep_instance` binary(16) NOT NULL,
  `index_name` varchar(32) NOT NULL,
  `index_version` int(11) NOT NULL COMMENT 'Version number of index. Used to determine when it should be rebuilt.',
  `index_version_hash` binary(20) DEFAULT NULL COMMENT 'Optional SHA-1 hash of index configuration. Used as secondary factor to determine if it should be rebuilt.',
  PRIMARY KEY (`zep_instance`,`index_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `index_metadata`
--

LOCK TABLES `index_metadata` WRITE;
/*!40000 ALTER TABLE `index_metadata` DISABLE KEYS */;
INSERT INTO `index_metadata` VALUES ('\0\'ny,óï„Ãé”Q¬£','event_archive',0,'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'),('\0\'ny,óï„Ãé”Q¬£','event_summary',8,'%gí÷jB\"ﬁ`@õﬂs∑Nª;’ó©');
/*!40000 ALTER TABLE `index_metadata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitor`
--

DROP TABLE IF EXISTS `monitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitor`
--

LOCK TABLES `monitor` WRITE;
/*!40000 ALTER TABLE `monitor` DISABLE KEYS */;
INSERT INTO `monitor` VALUES (1,'localhost');
/*!40000 ALTER TABLE `monitor` ENABLE KEYS */;
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
INSERT INTO `schema_version` VALUES (1,'2014-04-25 10:13:27'),(2,'2014-04-25 10:13:27'),(3,'2014-04-25 10:13:27'),(4,'2014-04-25 10:13:27'),(5,'2014-04-25 10:13:28'),(6,'2014-04-25 10:13:28');
/*!40000 ALTER TABLE `schema_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `v_daemon_heartbeat`
--

DROP TABLE IF EXISTS `v_daemon_heartbeat`;
/*!50001 DROP VIEW IF EXISTS `v_daemon_heartbeat`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_daemon_heartbeat` (
  `monitor` tinyint NOT NULL,
  `daemon` tinyint NOT NULL,
  `timeout_seconds` tinyint NOT NULL,
  `last_time` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_event_archive`
--

DROP TABLE IF EXISTS `v_event_archive`;
/*!50001 DROP VIEW IF EXISTS `v_event_archive`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_event_archive` (
  `uuid` tinyint NOT NULL,
  `fingerprint` tinyint NOT NULL,
  `status_id` tinyint NOT NULL,
  `event_group` tinyint NOT NULL,
  `event_class` tinyint NOT NULL,
  `event_class_key` tinyint NOT NULL,
  `event_class_mapping_uuid` tinyint NOT NULL,
  `event_key` tinyint NOT NULL,
  `severity_id` tinyint NOT NULL,
  `element_uuid` tinyint NOT NULL,
  `element_type_id` tinyint NOT NULL,
  `element_identifier` tinyint NOT NULL,
  `element_title` tinyint NOT NULL,
  `element_sub_uuid` tinyint NOT NULL,
  `element_sub_type_id` tinyint NOT NULL,
  `element_sub_identifier` tinyint NOT NULL,
  `element_sub_title` tinyint NOT NULL,
  `update_time` tinyint NOT NULL,
  `first_seen` tinyint NOT NULL,
  `status_change` tinyint NOT NULL,
  `last_seen` tinyint NOT NULL,
  `event_count` tinyint NOT NULL,
  `monitor` tinyint NOT NULL,
  `agent` tinyint NOT NULL,
  `syslog_facility` tinyint NOT NULL,
  `syslog_priority` tinyint NOT NULL,
  `nt_event_code` tinyint NOT NULL,
  `current_user_uuid` tinyint NOT NULL,
  `current_user_name` tinyint NOT NULL,
  `cleared_by_event_uuid` tinyint NOT NULL,
  `summary` tinyint NOT NULL,
  `message` tinyint NOT NULL,
  `details_json` tinyint NOT NULL,
  `tags_json` tinyint NOT NULL,
  `notes_json` tinyint NOT NULL,
  `audit_json` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_event_archive_index_queue`
--

DROP TABLE IF EXISTS `v_event_archive_index_queue`;
/*!50001 DROP VIEW IF EXISTS `v_event_archive_index_queue`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_event_archive_index_queue` (
  `id` tinyint NOT NULL,
  `uuid` tinyint NOT NULL,
  `last_seen` tinyint NOT NULL,
  `update_time` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_event_summary`
--

DROP TABLE IF EXISTS `v_event_summary`;
/*!50001 DROP VIEW IF EXISTS `v_event_summary`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_event_summary` (
  `uuid` tinyint NOT NULL,
  `fingerprint_hash` tinyint NOT NULL,
  `fingerprint` tinyint NOT NULL,
  `status_id` tinyint NOT NULL,
  `event_group` tinyint NOT NULL,
  `event_class` tinyint NOT NULL,
  `event_class_key` tinyint NOT NULL,
  `event_class_mapping_uuid` tinyint NOT NULL,
  `event_key` tinyint NOT NULL,
  `severity_id` tinyint NOT NULL,
  `element_uuid` tinyint NOT NULL,
  `element_type_id` tinyint NOT NULL,
  `element_identifier` tinyint NOT NULL,
  `element_title` tinyint NOT NULL,
  `element_sub_uuid` tinyint NOT NULL,
  `element_sub_type_id` tinyint NOT NULL,
  `element_sub_identifier` tinyint NOT NULL,
  `element_sub_title` tinyint NOT NULL,
  `update_time` tinyint NOT NULL,
  `first_seen` tinyint NOT NULL,
  `status_change` tinyint NOT NULL,
  `last_seen` tinyint NOT NULL,
  `event_count` tinyint NOT NULL,
  `monitor` tinyint NOT NULL,
  `agent` tinyint NOT NULL,
  `syslog_facility` tinyint NOT NULL,
  `syslog_priority` tinyint NOT NULL,
  `nt_event_code` tinyint NOT NULL,
  `current_user_uuid` tinyint NOT NULL,
  `current_user_name` tinyint NOT NULL,
  `clear_fingerprint_hash` tinyint NOT NULL,
  `cleared_by_event_uuid` tinyint NOT NULL,
  `summary` tinyint NOT NULL,
  `message` tinyint NOT NULL,
  `details_json` tinyint NOT NULL,
  `tags_json` tinyint NOT NULL,
  `notes_json` tinyint NOT NULL,
  `audit_json` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_event_summary_index_queue`
--

DROP TABLE IF EXISTS `v_event_summary_index_queue`;
/*!50001 DROP VIEW IF EXISTS `v_event_summary_index_queue`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_event_summary_index_queue` (
  `id` tinyint NOT NULL,
  `uuid` tinyint NOT NULL,
  `update_time` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_event_time`
--

DROP TABLE IF EXISTS `v_event_time`;
/*!50001 DROP VIEW IF EXISTS `v_event_time`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_event_time` (
  `summary_uuid` tinyint NOT NULL,
  `processed` tinyint NOT NULL,
  `created` tinyint NOT NULL,
  `first_seen` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_event_trigger`
--

DROP TABLE IF EXISTS `v_event_trigger`;
/*!50001 DROP VIEW IF EXISTS `v_event_trigger`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_event_trigger` (
  `uuid` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `enabled` tinyint NOT NULL,
  `rule_api_version` tinyint NOT NULL,
  `rule_type_id` tinyint NOT NULL,
  `rule_source` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_event_trigger_signal_spool`
--

DROP TABLE IF EXISTS `v_event_trigger_signal_spool`;
/*!50001 DROP VIEW IF EXISTS `v_event_trigger_signal_spool`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_event_trigger_signal_spool` (
  `uuid` tinyint NOT NULL,
  `event_trigger_subscription_uuid` tinyint NOT NULL,
  `event_summary_uuid` tinyint NOT NULL,
  `flush_time` tinyint NOT NULL,
  `created` tinyint NOT NULL,
  `event_count` tinyint NOT NULL,
  `sent_signal` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_event_trigger_subscription`
--

DROP TABLE IF EXISTS `v_event_trigger_subscription`;
/*!50001 DROP VIEW IF EXISTS `v_event_trigger_subscription`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_event_trigger_subscription` (
  `uuid` tinyint NOT NULL,
  `event_trigger_uuid` tinyint NOT NULL,
  `subscriber_uuid` tinyint NOT NULL,
  `delay_seconds` tinyint NOT NULL,
  `repeat_seconds` tinyint NOT NULL,
  `send_initial_occurrence` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `v_index_metadata`
--

DROP TABLE IF EXISTS `v_index_metadata`;
/*!50001 DROP VIEW IF EXISTS `v_index_metadata`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `v_index_metadata` (
  `zep_instance` tinyint NOT NULL,
  `index_name` tinyint NOT NULL,
  `index_version` tinyint NOT NULL,
  `index_version_hash` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `v_daemon_heartbeat`
--

/*!50001 DROP TABLE IF EXISTS `v_daemon_heartbeat`*/;
/*!50001 DROP VIEW IF EXISTS `v_daemon_heartbeat`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_daemon_heartbeat` AS select `daemon_heartbeat`.`monitor` AS `monitor`,`daemon_heartbeat`.`daemon` AS `daemon`,`daemon_heartbeat`.`timeout_seconds` AS `timeout_seconds`,`UNIX_MS_TO_DATETIME`(`daemon_heartbeat`.`last_time`) AS `last_time` from `daemon_heartbeat` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_event_archive`
--

/*!50001 DROP TABLE IF EXISTS `v_event_archive`*/;
/*!50001 DROP VIEW IF EXISTS `v_event_archive`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_event_archive` AS select `BINARY_UUID_TO_STR`(`event_archive`.`uuid`) AS `uuid`,`event_archive`.`fingerprint` AS `fingerprint`,`event_archive`.`status_id` AS `status_id`,`event_group`.`name` AS `event_group`,`event_class`.`name` AS `event_class`,`event_class_key`.`name` AS `event_class_key`,`BINARY_UUID_TO_STR`(`event_archive`.`event_class_mapping_uuid`) AS `event_class_mapping_uuid`,`event_key`.`name` AS `event_key`,`event_archive`.`severity_id` AS `severity_id`,`BINARY_UUID_TO_STR`(`event_archive`.`element_uuid`) AS `element_uuid`,`event_archive`.`element_type_id` AS `element_type_id`,`event_archive`.`element_identifier` AS `element_identifier`,`event_archive`.`element_title` AS `element_title`,`BINARY_UUID_TO_STR`(`event_archive`.`element_sub_uuid`) AS `element_sub_uuid`,`event_archive`.`element_sub_type_id` AS `element_sub_type_id`,`event_archive`.`element_sub_identifier` AS `element_sub_identifier`,`event_archive`.`element_sub_title` AS `element_sub_title`,`UNIX_MS_TO_DATETIME`(`event_archive`.`update_time`) AS `update_time`,`UNIX_MS_TO_DATETIME`(`event_archive`.`first_seen`) AS `first_seen`,`UNIX_MS_TO_DATETIME`(`event_archive`.`status_change`) AS `status_change`,`UNIX_MS_TO_DATETIME`(`event_archive`.`last_seen`) AS `last_seen`,`event_archive`.`event_count` AS `event_count`,`monitor`.`name` AS `monitor`,`agent`.`name` AS `agent`,`event_archive`.`syslog_facility` AS `syslog_facility`,`event_archive`.`syslog_priority` AS `syslog_priority`,`event_archive`.`nt_event_code` AS `nt_event_code`,`BINARY_UUID_TO_STR`(`event_archive`.`current_user_uuid`) AS `current_user_uuid`,`event_archive`.`current_user_name` AS `current_user_name`,`BINARY_UUID_TO_STR`(`event_archive`.`cleared_by_event_uuid`) AS `cleared_by_event_uuid`,`event_archive`.`summary` AS `summary`,`event_archive`.`message` AS `message`,`event_archive`.`details_json` AS `details_json`,`event_archive`.`tags_json` AS `tags_json`,`event_archive`.`notes_json` AS `notes_json`,`event_archive`.`audit_json` AS `audit_json` from ((((((`event_archive` left join `event_group` on((`event_archive`.`event_group_id` = `event_group`.`id`))) join `event_class` on((`event_archive`.`event_class_id` = `event_class`.`id`))) left join `event_class_key` on((`event_archive`.`event_class_key_id` = `event_class_key`.`id`))) left join `event_key` on((`event_archive`.`event_key_id` = `event_key`.`id`))) left join `monitor` on((`event_archive`.`monitor_id` = `monitor`.`id`))) left join `agent` on((`event_archive`.`agent_id` = `agent`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_event_archive_index_queue`
--

/*!50001 DROP TABLE IF EXISTS `v_event_archive_index_queue`*/;
/*!50001 DROP VIEW IF EXISTS `v_event_archive_index_queue`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_event_archive_index_queue` AS select `event_archive_index_queue`.`id` AS `id`,`BINARY_UUID_TO_STR`(`event_archive_index_queue`.`uuid`) AS `uuid`,`UNIX_MS_TO_DATETIME`(`event_archive_index_queue`.`last_seen`) AS `last_seen`,`UNIX_MS_TO_DATETIME`(`event_archive_index_queue`.`update_time`) AS `update_time` from `event_archive_index_queue` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_event_summary`
--

/*!50001 DROP TABLE IF EXISTS `v_event_summary`*/;
/*!50001 DROP VIEW IF EXISTS `v_event_summary`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_event_summary` AS select `BINARY_UUID_TO_STR`(`event_summary`.`uuid`) AS `uuid`,`BINARY_SHA1_TO_STR`(`event_summary`.`fingerprint_hash`) AS `fingerprint_hash`,`event_summary`.`fingerprint` AS `fingerprint`,`event_summary`.`status_id` AS `status_id`,`event_group`.`name` AS `event_group`,`event_class`.`name` AS `event_class`,`event_class_key`.`name` AS `event_class_key`,`BINARY_UUID_TO_STR`(`event_summary`.`event_class_mapping_uuid`) AS `event_class_mapping_uuid`,`event_key`.`name` AS `event_key`,`event_summary`.`severity_id` AS `severity_id`,`BINARY_UUID_TO_STR`(`event_summary`.`element_uuid`) AS `element_uuid`,`event_summary`.`element_type_id` AS `element_type_id`,`event_summary`.`element_identifier` AS `element_identifier`,`event_summary`.`element_title` AS `element_title`,`BINARY_UUID_TO_STR`(`event_summary`.`element_sub_uuid`) AS `element_sub_uuid`,`event_summary`.`element_sub_type_id` AS `element_sub_type_id`,`event_summary`.`element_sub_identifier` AS `element_sub_identifier`,`event_summary`.`element_sub_title` AS `element_sub_title`,`UNIX_MS_TO_DATETIME`(`event_summary`.`update_time`) AS `update_time`,`UNIX_MS_TO_DATETIME`(`event_summary`.`first_seen`) AS `first_seen`,`UNIX_MS_TO_DATETIME`(`event_summary`.`status_change`) AS `status_change`,`UNIX_MS_TO_DATETIME`(`event_summary`.`last_seen`) AS `last_seen`,`event_summary`.`event_count` AS `event_count`,`monitor`.`name` AS `monitor`,`agent`.`name` AS `agent`,`event_summary`.`syslog_facility` AS `syslog_facility`,`event_summary`.`syslog_priority` AS `syslog_priority`,`event_summary`.`nt_event_code` AS `nt_event_code`,`BINARY_UUID_TO_STR`(`event_summary`.`current_user_uuid`) AS `current_user_uuid`,`event_summary`.`current_user_name` AS `current_user_name`,`BINARY_SHA1_TO_STR`(`event_summary`.`clear_fingerprint_hash`) AS `clear_fingerprint_hash`,`BINARY_UUID_TO_STR`(`event_summary`.`cleared_by_event_uuid`) AS `cleared_by_event_uuid`,`event_summary`.`summary` AS `summary`,`event_summary`.`message` AS `message`,`event_summary`.`details_json` AS `details_json`,`event_summary`.`tags_json` AS `tags_json`,`event_summary`.`notes_json` AS `notes_json`,`event_summary`.`audit_json` AS `audit_json` from ((((((`event_summary` left join `event_group` on((`event_summary`.`event_group_id` = `event_group`.`id`))) join `event_class` on((`event_summary`.`event_class_id` = `event_class`.`id`))) left join `event_class_key` on((`event_summary`.`event_class_key_id` = `event_class_key`.`id`))) left join `event_key` on((`event_summary`.`event_key_id` = `event_key`.`id`))) left join `monitor` on((`event_summary`.`monitor_id` = `monitor`.`id`))) left join `agent` on((`event_summary`.`agent_id` = `agent`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_event_summary_index_queue`
--

/*!50001 DROP TABLE IF EXISTS `v_event_summary_index_queue`*/;
/*!50001 DROP VIEW IF EXISTS `v_event_summary_index_queue`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_event_summary_index_queue` AS select `event_summary_index_queue`.`id` AS `id`,`BINARY_UUID_TO_STR`(`event_summary_index_queue`.`uuid`) AS `uuid`,`UNIX_MS_TO_DATETIME`(`event_summary_index_queue`.`update_time`) AS `update_time` from `event_summary_index_queue` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_event_time`
--

/*!50001 DROP TABLE IF EXISTS `v_event_time`*/;
/*!50001 DROP VIEW IF EXISTS `v_event_time`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_event_time` AS select `BINARY_UUID_TO_STR`(`event_time`.`summary_uuid`) AS `summary_uuid`,`UNIX_MS_TO_DATETIME`(`event_time`.`processed`) AS `processed`,`UNIX_MS_TO_DATETIME`(`event_time`.`created`) AS `created`,`UNIX_MS_TO_DATETIME`(`event_time`.`first_seen`) AS `first_seen` from `event_time` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_event_trigger`
--

/*!50001 DROP TABLE IF EXISTS `v_event_trigger`*/;
/*!50001 DROP VIEW IF EXISTS `v_event_trigger`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_event_trigger` AS select `BINARY_UUID_TO_STR`(`event_trigger`.`uuid`) AS `uuid`,`event_trigger`.`name` AS `name`,`event_trigger`.`enabled` AS `enabled`,`event_trigger`.`rule_api_version` AS `rule_api_version`,`event_trigger`.`rule_type_id` AS `rule_type_id`,`event_trigger`.`rule_source` AS `rule_source` from `event_trigger` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_event_trigger_signal_spool`
--

/*!50001 DROP TABLE IF EXISTS `v_event_trigger_signal_spool`*/;
/*!50001 DROP VIEW IF EXISTS `v_event_trigger_signal_spool`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_event_trigger_signal_spool` AS select `BINARY_UUID_TO_STR`(`event_trigger_signal_spool`.`uuid`) AS `uuid`,`BINARY_UUID_TO_STR`(`event_trigger_signal_spool`.`event_trigger_subscription_uuid`) AS `event_trigger_subscription_uuid`,`BINARY_UUID_TO_STR`(`event_trigger_signal_spool`.`event_summary_uuid`) AS `event_summary_uuid`,`UNIX_MS_TO_DATETIME`(`event_trigger_signal_spool`.`flush_time`) AS `flush_time`,`UNIX_MS_TO_DATETIME`(`event_trigger_signal_spool`.`created`) AS `created`,`event_trigger_signal_spool`.`event_count` AS `event_count`,`event_trigger_signal_spool`.`sent_signal` AS `sent_signal` from `event_trigger_signal_spool` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_event_trigger_subscription`
--

/*!50001 DROP TABLE IF EXISTS `v_event_trigger_subscription`*/;
/*!50001 DROP VIEW IF EXISTS `v_event_trigger_subscription`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_event_trigger_subscription` AS select `BINARY_UUID_TO_STR`(`event_trigger_subscription`.`uuid`) AS `uuid`,`BINARY_UUID_TO_STR`(`event_trigger_subscription`.`event_trigger_uuid`) AS `event_trigger_uuid`,`BINARY_UUID_TO_STR`(`event_trigger_subscription`.`subscriber_uuid`) AS `subscriber_uuid`,`event_trigger_subscription`.`delay_seconds` AS `delay_seconds`,`event_trigger_subscription`.`repeat_seconds` AS `repeat_seconds`,`event_trigger_subscription`.`send_initial_occurrence` AS `send_initial_occurrence` from `event_trigger_subscription` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_index_metadata`
--

/*!50001 DROP TABLE IF EXISTS `v_index_metadata`*/;
/*!50001 DROP VIEW IF EXISTS `v_index_metadata`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_index_metadata` AS select `BINARY_UUID_TO_STR`(`index_metadata`.`zep_instance`) AS `zep_instance`,`index_metadata`.`index_name` AS `index_name`,`index_metadata`.`index_version` AS `index_version`,`BINARY_SHA1_TO_STR`(`index_metadata`.`index_version_hash`) AS `index_version_hash` from `index_metadata` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-25 10:46:48
