from crontab import CronTab

#Pulitura del crontab
my_cron = CronTab(user='pi')
for job in my_cron:
    my_cron.remove(job)
    my_cron.write()
