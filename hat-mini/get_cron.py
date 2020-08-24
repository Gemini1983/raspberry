from crontab import CronTab
from crontab import CronSlices
import json

my_tasks = []

#lista dei crontab
my_cron = CronTab(user='pi')
for job in my_cron:
    mylist = job.command.split(" ")
    data_set = {"descrizione": job.comment, 
                "minuto": job.minute,
                "ora": job.hour,
                "giorno_mese": job.day,
                "mese": job.month,
                "giorno_settimana": job.dow,
                "numero_elettrovalvola": mylist[3],
                "tempo_apertura": mylist[4]
                 }
    my_tasks.append(data_set)
    print(data_set)
    print(data_set["minuto"])
    
    #convertire questo in una risposta JSON

    
    
#print(my_tasks[1].__dict__)
   
    
"""    
    print (obj.comment)
    
    print (obj.minute)
    print (obj.hour)
    print (obj.day)
    print (obj.month)
    print (obj.dow)
    
    mylist = obj.command.split(" ")
    print (mylist[3])
    print (mylist[4])

"""
