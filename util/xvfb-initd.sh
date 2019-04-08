#!/bin/bash
# Script taken from docker image: travisci/ci-garnet:packer-1496954857

set -x

XVFB=/usr/bin/Xvfb
XVFBARGS=":99 -ac -screen 0 1024x768x24"
PIDFILE=/tmp/cucumber_xvfb_99.pid

ps -ef | grep "$XVFB $XVFBARGS"
ps -ef | grep "$XVFB $XVFBARGS" | wc -l

case "$1" in
  start)
    echo -n "Starting virtual X frame buffer: Xvfb"
    if [ `lsb_release -si` != "CentOS" ]; then
	     /sbin/start-stop-daemon --start --quiet --pidfile $PIDFILE --make-pidfile --background --exec $XVFB -- $XVFBARGS
    elif [ "$(ps -ef | grep "$XVFB $XVFBARGS" | wc -l)" != "2" ]; then
      $XVFB $XVFBARGS &
    fi
    echo "."
    ;;
  stop)
    echo -n "Stopping virtual X frame buffer: Xvfb"
    if [ `lsb_release -si` != "CentOS" ]; then
      /sbin/start-stop-daemon --stop --quiet --pidfile $PIDFILE
    elif [ "$(ps -ef | grep "$XVFB $XVFBARGS" | wc -l)" == "2" ]; then
      pkill -f "$XVFB $XVFBARGS"
    fi
    rm -f $PIDFILE
    echo "."
    ;;
  restart)
    $0 stop
    $0 start
    ;;
  *)
  echo "Usage: xvfb-initd.sh {start|stop|restart}"
  exit 1
esac
exit 0
