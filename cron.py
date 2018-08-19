#!/usr/bin/env python3
from crontab import CronTab

#start crontab
cron = CronTab(user='pi')
cron.remove_all()

#add job
job = cron.new(command='python3 /home/pi/A1_proto/main.py')

#settings which allow the cron to run every hour
job.minute.every(30)
cron.write()

job = cron.new(command='python3 /home/pi/A1_proto/bluet_mod.py')
job.every_reboot()  
cron.write()
job = cron.new(command='python3 /home/pi/A1_proto/graph.py')
job.every_reboot() 
cron.write()
