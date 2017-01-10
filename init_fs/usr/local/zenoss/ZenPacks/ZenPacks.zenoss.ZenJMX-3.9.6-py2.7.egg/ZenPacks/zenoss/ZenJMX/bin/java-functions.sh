##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


replace() {
    SEARCH=$1
    REPLACE=$2
    FILE=$3
    TEMP=/tmp/`basename $FILE`

    sed -e "s%${SEARCH}%${REPLACE}%g" < ${FILE} > ${TEMP}
    mv ${TEMP} ${FILE}
}

running() {
    if [ -f $PIDFILE ]; then
        PID=`cat $PIDFILE`
	      kill -0 $PID 2>/dev/null || $PS | grep -q "^ *$PID$"
	      return $?
    fi

    return 1
}

restart() {
    stop
    for i in 1 2 3 4 5 6 7 8 9 10
    do
       sleep 0.24 2>/dev/null || sleep 1
       test -f $PIDFILE || break
    done
    start "$@"
}

jmx_args() {
    JMX_ARGS=""
    if [ ! -z "${JMX_LISTEN_PORT}" ]; then
        JMX_ARGS="-Dcom.sun.management.jmxremote.port=${JMX_LISTEN_PORT}"
        JMX_ARGS="${JMX_ARGS} -Dcom.sun.management.jmxremote.authenticate=false"
        JMX_ARGS="${JMX_ARGS} -Dcom.sun.management.jmxremote.ssl=false"
    fi
    echo $JMX_ARGS
}

run() {
    exec java \
        ${JVM_ARGS} \
        -cp "./*:$ZENHOME/zenjmx-libs/*:${CLASSPATH}" \
        com.zenoss.zenpacks.zenjmx.ZenJmxMain \
        ${RUN_ARGS}
}

runjmxenabled() {
    JVM_ARGS="${JVM_ARGS} `jmx_args`"
    exec java \
        ${JVM_ARGS} \
        -cp "./*:$ZENHOME/zenjmx-libs/*:${CLASSPATH}" \
        com.zenoss.zenpacks.zenjmx.ZenJmxMain \
        ${RUN_ARGS}
}

start() {
    if running; then    
        echo is already running
    else
        echo starting...
        JVM_ARGS="${JVM_ARGS} `jmx_args`"
        eval exec java \
            ${JVM_ARGS} \
            -cp "./*:$ZENHOME/zenjmx-libs/*:${CLASSPATH}" \
            com.zenoss.zenpacks.zenjmx.ZenJmxMain \
            ${START_ARGS} > /dev/null 2>&1 &
        PID=$!
        echo $PID > $PIDFILE
    fi
}

stop() {
    if running; then
        PID=`cat $PIDFILE`
        echo stopping...
        kill $PID
        if [ $? -gt 0 ]; then
            rm -f $PIDFILE
            echo clearing pid file
        fi
    else
        echo already stopped
    fi
}

status() {
    if running; then
            echo program running\; pid=$PID
            exit 109
    else
        rm -f $PIDFILE
        echo not running
        exit 100
    fi
}

generic() {
    case "$CMD" in
      run)
	    run "$@"
	    ;;
      runjmxenabled)
	    runjmxenabled "$@"
	    ;;
      start)
	    start "$@"
	    ;;
      stop)
	    stop
	    ;;
      restart)
	    restart "$@"
	    ;;
      status)
	    status
	    ;;
      help)
	    help
	    ;;
      *)
	    cat - <<HELP
Usage: $0 {run|start|stop|restart|status|help} [options]

  where the commands are:

    run     - start the program but don't put it in the background.
              NB: This mode is good for debugging.

    start   - start the program in daemon mode -- running in the background,
              detached from the shell

    stop    - stop the program

    restart - stop and then start the program
              NB: Sometimes the start command will run before the daemon
                  has terminated.  If this happens just re-run the command.

    status  - Check the status of a daemon.  This will print the current
              process nuber if it is running.

    help    - display the options available for the daemon


HELP
	    exit 1
    esac
    exit $?
}
