#!/bin/bash
date
/usr/sbin/service apache2 stop
/usr/bin/letsencrypt renew
/usr/sbin/service apache2 start
