############################################################
# Dockerfile - Zenoss v4.2.5-2108-03c on Debian Wheezy
# https://github.com/krull/docker-zenoss4
############################################################

# set base image debian wheezy
FROM debian:wheezy

# file maintainer author
MAINTAINER brendan jocson <brendan@jocson.eu>

# docker build environments
ENV ZENOSSHOME="/home/zenoss"
ENV ZENHOME="/usr/local/zenoss"

# docker build arguments
ARG ZEN_DEF_DAEMONS="zeneventserver\nzopectl\nzenrrdcached\nzenhub\nzenjobs\nzeneventd\nzenping\nzensyslog\nzenstatus\nzenactiond\nzentrap\nzenmodeler\nzenperfsnmp\nzencommand\nzenprocess\nzenwinperf\nzenwin\nzeneventlog\nzenjmx\nzenpython"

#ARG SUPER_ZEN_TMPL="[program:@@REPLACEMETOO@@]\npriority=@@REPLACEME@@\nstartsecs=3\nautostart=false\nautorestart=false\nstartinorder=true\nuser=zenoss\ncommand=/usr/local/zenoss/bin/@@REPLACEMETOO@@%1sstart\n"

ARG DEBIAN_FRONTEND="noninteractive"

ARG BUILD_SRC="/usr/local/src"

ARG ZENOSS_BUILD_DEPS_DEV="\
    rrdtool \
    nagios-plugins \
    swig \
    unzip \
    zip \
    g++ \
    maven \
    libmaven-compiler-plugin-java \
    libssl1.0.0 \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libncurses5-dev \
    libreadline6-dev \
    libreadline6 \
    librrd-dev \
    python-dev \
    openjdk-7-jre \
    python-twisted \
    python-gnutls \
    python-twisted-web \
    python-samba \
#    python-pip \
    libsnmp-base \
    bc \
    libncurses5 \
    python-setuptools \
    smistrip \
    net-tools \
    snmp \
    wget \
    netcat \
#    supervisor \
    "

ARG ZENOSS_BUILD_DEPS_TESTING="\
    libc6 \
    libc6-dev \
    "

ARG ZENOSS_BUILD_DEPS_EXT="\
    autoconf \
    build-essential \
    "

# execute
RUN \
## init build env & install apt deps
    /usr/sbin/groupadd -g 999 zenoss \
    && /usr/sbin/useradd -m -u 999 -g 999 -s /bin/bash zenoss \
    && /usr/bin/apt-get update \
    && /usr/bin/apt-get -y --no-install-recommends install ${ZENOSS_BUILD_DEPS_DEV} ${ZENOSS_BUILD_DEPS_EXT} \
    && /bin/cp /etc/apt/sources.list /etc/apt/sources.list.org \
    && /bin/sed 's/wheezy/testing/g' /etc/apt/sources.list >> /etc/apt/sources.list \
    && /usr/bin/apt-get update \
    && /usr/bin/apt-get -y --no-install-recommends -t testing install ${ZENOSS_BUILD_DEPS_TESTING} \
    && /bin/cp /etc/apt/sources.list.org /etc/apt/sources.list \
    && /usr/bin/apt-get update \
## download all the things!
    && /usr/bin/wget --no-check-certificate https://raw.githubusercontent.com/krull/docker-zenoss4/master/init_fs/usr/local/src/snmp-mibs-downloader_1.1_all.deb -O ${BUILD_SRC}/snmp-mibs-downloader_1.1_all.deb \
    && /usr/bin/wget --no-check-certificate https://raw.githubusercontent.com/krull/docker-zenoss4/master/init_fs/usr/local/src/zenoss-core-425-2108_03c_amd64.deb.tar.gz.00 -O ${BUILD_SRC}/zenoss-core-425-2108_03c_amd64.deb.tar.gz.00 \
    && /usr/bin/wget --no-check-certificate https://raw.githubusercontent.com/krull/docker-zenoss4/master/init_fs/usr/local/src/zenoss-core-425-2108_03c_amd64.deb.tar.gz.01 -O ${BUILD_SRC}/zenoss-core-425-2108_03c_amd64.deb.tar.gz.01 \
    && /bin/cat ${BUILD_SRC}/zenoss-core-425-2108_03c_amd64.deb.tar.gz.00 ${BUILD_SRC}/zenoss-core-425-2108_03c_amd64.deb.tar.gz.01 > ${BUILD_SRC}/zenoss-core-425-2108_03c_amd64.deb.tar.gz \
    && /usr/bin/wget --no-check-certificate https://raw.githubusercontent.com/krull/docker-zenoss4/master/init_fs/usr/local/bin/docker-entrypoint.sh -O /usr/local/bin/docker-entrypoint.sh \
    && /usr/bin/wget --no-check-certificate https://raw.githubusercontent.com/krull/docker-zenoss4/master/init_fs/etc/insserv/overrides/zenoss -O /etc/insserv/overrides/zenoss \
    && /usr/bin/wget --no-check-certificate https://raw.githubusercontent.com/krull/docker-zenoss4/master/init_fs/etc/init.d/zenoss -O /etc/init.d/zenoss \
#    && /usr/bin/wget --no-check-certificate https://github.com/jasoncorbett/ordered-startup-supervisord/archive/master.zip -O ${BUILD_SRC}/ordered-startup-supervisord-master.zip \
    && /bin/tar zxvf ${BUILD_SRC}/zenoss-core-425-2108_03c_amd64.deb.tar.gz -C ${BUILD_SRC}/ \
## install all the things!
    && /usr/bin/dpkg -i ${BUILD_SRC}/snmp-mibs-downloader_1.1_all.deb \
    && /usr/bin/dpkg -i ${BUILD_SRC}/zenoss-core-425-2108_03c_amd64.deb \
    && /usr/bin/wget --no-check-certificate https://raw.githubusercontent.com/krull/docker-zenoss4/master/init_fs/usr/local/zenoss/etc/zeneventserver.conf -O ${ZENHOME}/etc/zeneventserver.conf \
    && /usr/bin/apt-get -f install \
## os cleanup/conditioning
#    && /usr/bin/pip install --upgrade meld3==0.6.5 supervisor==3.2.0 \
#    && /usr/bin/unzip ${BUILD_SRC}/ordered-startup-supervisord-master.zip -d ${BUILD_SRC}/ \
#    && /usr/bin/pip install -e ${BUILD_SRC}/ordered-startup-supervisord-master/ \
    && /bin/chown -R zenoss:zenoss ${ZENOSSHOME} \
    && /bin/chown -R zenoss:zenoss ${ZENHOME} \
    && /bin/ln -s /usr/local/zenoss /opt \
    && /bin/ln -s libnetsnmp.so.15 /usr/lib/libnetsnmp.so \
    && /bin/ln -s /lib/x86_64-linux-gnu/libssl.so.1.0.0 /usr/lib/libssl.so.10 \
    && /bin/ln -s /lib/x86_64-linux-gnu/libcrypto.so.1.0.0 /usr/lib/libcrypto.so.10 \
    && /bin/ln -s /usr/local/zenoss/zenup /opt \
#    && /bin/ln -s zope.conf ${ZENHOME}/etc/zopectl.conf \
    && /bin/chmod +x /usr/local/zenoss/zenup/bin/zenup \
    && /bin/echo 'watchdog True' >> ${ZENHOME}/etc/zenwinperf.conf \
    && /usr/bin/touch ${ZENHOME}/var/Data.fs \
    && /bin/sed -i 's/mibs/#mibs/g' /etc/snmp/snmp.conf \
    && /usr/bin/touch ${ZENHOME}/etc/DAEMONS_TXT_ONLY \
#    && /usr/bin/touch ${ZENHOME}/etc/zenrrdcached.conf \
    && /usr/bin/printf ${ZEN_DEF_DAEMONS} > ${ZENHOME}/etc/daemons.txt \
## fix ownerships and permissions
    && /bin/chmod -c 755 /etc/init.d/zenoss \
    && /bin/chmod -c 755 /usr/local/bin/docker-entrypoint.sh \
#    && /bin/chown -h -c zenoss:zenoss ${ZENHOME}/etc/zopectl.conf \
#    && /bin/chown -c zenoss:zenoss ${ZENHOME}/etc/zenrrdcached.conf \
    && /bin/chown -c root:zenoss ${ZENHOME}/bin/pyraw \
    && /bin/chown -c root:zenoss ${ZENHOME}/bin/zensocket \
    && /bin/chown -c root:zenoss ${ZENHOME}/bin/nmap \
    && /bin/chmod -c 04750 ${ZENHOME}/bin/pyraw \
    && /bin/chmod -c 04750 ${ZENHOME}/bin/zensocket \
    && /bin/chmod -c 04750 ${ZENHOME}/bin/nmap \
## conditioning for docker service instances
    && /bin/sed -i 's/zodb-host localhost/zodb-host zenoss4-mariadb/g' ${ZENHOME}/etc/global.conf \
    && /bin/sed -i 's/host localhost/host zenoss4-mariadb/g' ${ZENHOME}/etc/zodb_db_main.conf \
    && /bin/sed -i 's/host localhost/host zenoss4-mariadb/g' ${ZENHOME}/etc/zodb_db_session.conf \
    && /bin/sed -i 's/zep-host localhost/zep-host zenoss4-mariadb/g' ${ZENHOME}/etc/global.conf \
    && /bin/sed -i 's/amqphost localhost/amqphost zenoss4-rabbitmq/g' ${ZENHOME}/etc/global.conf \
    && /bin/sed -i 's/zodb-cacheservers 127.0.0.1:11211/zodb-cacheservers zenoss4-memcached:11211/g' ${ZENHOME}/etc/global.conf \
    && /bin/sed -i 's/127.0.0.1:11211/zenoss4-memcached:11211/g' ${ZENHOME}/etc/zope.conf \
## supervisord zenoss
#    && /bin/sed -i '/\[supervisord\]/c\[inet_http_server\]\nport=:9001\n\n\[supervisord\]\nnodaemon=true' /etc/supervisor/supervisord.conf \
#    && /bin/sed -i '/\[supervisorctl\]/c\[eventlistener:inorder\]\ncommand=\/usr\/local\/bin\/ordered-startup-listener\nautostart=true\nevents=PROCESS_STATE\n\n\[supervisorctl\]' /etc/supervisor/supervisord.conf \
#    && /bin/sed -i 's/serverurl=unix:\/\/\/var\/run\/\/supervisor.sock/serverurl=http:\/\/127.0.0.1:9001/' /etc/supervisor/supervisord.conf \
#    && while read zd; do /usr/bin/printf ${SUPER_ZEN_TMPL} > /etc/supervisor/conf.d/$zd.conf; done < ${ZENHOME}/etc/daemons.txt \
#    && PRTY=100; while read zdd; do /bin/sed -i 's/@@REPLACEME@@/'"$PRTY"'/g; s/@@REPLACEMETOO@@/'"$zdd"'/g' /etc/supervisor/conf.d/$zdd.conf && PRTY=$(($PRTY + 50)); done < ${ZENHOME}/etc/daemons.txt \
## make zenoss processes foreground for supervisor
#    && while read zddd; do /bin/sed -i 's/#daemon False/daemon False/' ${ZENHOME}/etc/$zddd.conf; done < ${ZENHOME}/etc/daemons.txt \
## build cleanup
    && for lf in ${ZENHOME}/log/*.log; do /usr/bin/truncate -s 0 $lf; done \
#    && /bin/rm -rf ${ZENOSSHOME}/zenoss425-srpm_install ${ZENOSSHOME}/z*.sql ${ZENOSSHOME}/.bash_history ${ZENOSSHOME}/.viminfo ${ZENOSSHOME}/.gnupg ${ZENOSSHOME}/.subversion ${ZENHOME}/etc/*.example ${ZENHOME}/log/z*-stdio.*.log ${BUILD_SRC}/*.deb ${BUILD_SRC}/*.tar.gz* ${BUILD_SRC}/ordered-startup-supervisord-master.zip /usr/share/locale/* /var/cache/debconf/*-old /usr/share/doc/* /var/lib/apt/* \
    && /bin/rm -rf ${ZENOSSHOME}/zenoss425-srpm_install ${ZENOSSHOME}/z*.sql ${ZENOSSHOME}/.bash_history ${ZENOSSHOME}/.viminfo ${ZENOSSHOME}/.gnupg ${ZENOSSHOME}/.subversion ${ZENHOME}/etc/*.example ${ZENHOME}/log/z*-stdio.*.log ${BUILD_SRC}/*.deb ${BUILD_SRC}/*.tar.gz* /usr/share/locale/* /var/cache/debconf/*-old /usr/share/doc/* /var/lib/apt/* \
    && /usr/bin/apt-get -y --auto-remove purge ${ZENOSS_BUILD_DEPS_EXT} \
    && /usr/bin/apt-get -y autoremove \
    && /usr/bin/apt-get -y autoclean \
    && /usr/bin/apt-get -y clean

# zenoss4 admin console
EXPOSE 8080

# start supervisord in foreground
#ENTRYPOINT ["/usr/local/bin/supervisord"]
# start docker-entrypoint script
ENTRYPOINT ["docker-entrypoint.sh"]

# invoke supervisord help
#CMD ["--help"]
