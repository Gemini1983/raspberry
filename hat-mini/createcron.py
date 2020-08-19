import sys
from crontab import CronTab

valvola=sys.argv[1]
minuti_apertura=sys.argv[2]
ora=sys.argv[3]
minuti=sys.argv[4]
comment_cron='Pianificazione apertura valvola '+valvola


#Pulitura del crontab
my_cron = CronTab(user='pi')
for job in my_cron:
    if job.comment == comment_cron:
        my_cron.remove(job)
        my_cron.write()

 
my_cron2 = CronTab(user='pi')
job2 = my_cron2.new(command='sudo /usr/bin/python3 /home/pi/example/automation-hat/examples/hat-mini/apri_saracinesca.py '+valvola+' '+minuti_apertura+' >> /home/pi/example/automation-hat/examples/hat-mini/log.log', comment=comment_cron)
#job2.minute.every(1)
job2.hour.on(ora)
job2.minute.on(minuti)
my_cron2.write()