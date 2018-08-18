#!/usr/bin/env python3
from crontab import CronTab

#start crontab
cron = CronTab(user='pi')
cron.remove_all()

#add job
job = cron.new(command='/home/pi/A1_proto/main.py')

#settings which allow the cron to run every hour
job.hour.every(1)
cron.write()
