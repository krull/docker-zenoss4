#!/bin/bash
set -e
set -x

/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE zenoss_zep;"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE zodb;"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE zodb_session;"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -f -D zenoss_zep < /tmp/initdb.d/zenoss_zep.sql
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -f -D zodb < /tmp/initdb.d/zodb.sql
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -f -D zodb_session < /tmp/initdb.d/zodb_session.sql
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE USER 'zenoss'@'localhost' IDENTIFIED BY 'zenoss';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT REPLICATION SLAVE ON *.* TO 'zenoss'@'localhost' IDENTIFIED BY PASSWORD '*3715D7F2B0C1D26D72357829DF94B81731174B8C';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON zodb.* TO 'zenoss'@'localhost';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON zenoss_zep.* TO 'zenoss'@'localhost';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON zodb_session.* TO 'zenoss'@'localhost';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT SELECT ON mysql.proc TO 'zenoss'@'localhost';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "CREATE USER 'zenoss'@'%' IDENTIFIED BY 'zenoss';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT REPLICATION SLAVE ON *.* TO 'zenoss'@'%' IDENTIFIED BY PASSWORD '*3715D7F2B0C1D26D72357829DF94B81731174B8C';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON zodb.* TO 'zenoss'@'%';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON zenoss_zep.* TO 'zenoss'@'%';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON zodb_session.* TO 'zenoss'@'%';"
/usr/bin/mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "GRANT SELECT ON mysql.proc TO 'zenoss'@'%';"
