from crontab import CronTab, CronSlices
import json, sys, os

def get_tasks():
    tasks = []
    # lista dei crontab
    my_cron = CronTab(user='pi')
    for job in my_cron:
        mylist = job.command.split(" ")
        data_set = {"descrizione": job.comment,
                    "minuto": str(job.minute),
                    "ora": str(job.hour),
                    "giorno_mese": str(job.day),
                    "mese": str(job.month),
                    "giorno_settimana": str(job.dow),
                    "numero_elettrovalvola": mylist[3],
                    "tempo_apertura": mylist[4],
                    "abilitato": job.is_enabled()
                    }
        tasks.append(data_set)

    # converte in struttura JSON
    # responce=json.dumps(my_tasks)
    return tasks


def up_task(mytask):
    found = False
    path_project=os.path.abspath(os.path.dirname(sys.argv[0]))
    period=mytask["minuto"],mytask["ora"],mytask["giorno_mese"],mytask["mese"],mytask["giorno_settimana"]
        
    if CronSlices.is_valid(period):
        print("Periodo Corretto")
        #Cancella per aggiornare se ha trovato l'elettrovalvola
        my_cron = CronTab(user='pi')
        for job in my_cron:
            if job.comment == mytask["descrizione"]:
                my_cron.remove(job)
                my_cron.write()
                found=True

        if found is False:
            return []
        
        #Ricreiamo il task
        new_cron = CronTab(user='pi')
        new_job = new_cron.new(command='sudo /usr/bin/python3 '+path_project+'/apri_saracinesca.py '+mytask["numero_elettrovalvola"]+' '+mytask["tempo_apertura"]+' >> '+path_project+'/log.log', comment=mytask["descrizione"])

        new_job.setall(period)
        new_job.enable(mytask["abilitato"])
        new_cron.write()
        return mytask
    else:
        print("perido non valido")
        return []
    
def new_task(mytask):
    path_project=os.path.abspath(os.path.dirname(sys.argv[0]))
    period=mytask["minuto"],mytask["ora"],mytask["giorno_mese"],mytask["mese"],mytask["giorno_settimana"]
        
    if CronSlices.is_valid(period):
        print("Periodo Corretto")
        #Errore se esiste già un task con la descrizione uguale
        my_cron = CronTab(user='pi')
        for job in my_cron:
            if job.comment == mytask["descrizione"]:
                print("Descrizione già esiste")
                return []

        #Creiamo il task
        new_cron = CronTab(user='pi')
        new_job = new_cron.new(command='sudo /usr/bin/python3 '+path_project+'/apri_saracinesca.py '+mytask["numero_elettrovalvola"]+' '+mytask["tempo_apertura"]+' >> '+path_project+'/log.log', comment=mytask["descrizione"])

        new_job.setall(period)
        new_job.enable(mytask["abilitato"])
        new_cron.write()
        return mytask
    else:
        print("perido non valido")
        return []
    
def del_task(descrizione):
    my_cron = CronTab(user='pi')
    for job in my_cron:
        if job.comment == descrizione:
            my_cron.remove(job)
            my_cron.write()
            return True

    return False

def find_task_comment(descrizione):
    my_cron = CronTab(user='pi')
    for job in my_cron:
        if descrizione==job.comment:
            mylist = job.command.split(" ")
            data_set = {"descrizione": job.comment,
                        "minuto": str(job.minute),
                        "ora": str(job.hour),
                        "giorno_mese": str(job.day),
                        "mese": str(job.month),
                        "giorno_settimana": str(job.dow),
                        "numero_elettrovalvola": mylist[3],
                        "tempo_apertura": mylist[4],
                        "abilitato": job.is_enabled()
                        }
            return data_set

    return False


def find_tasks_valve(valvola):
    tasks = []
    # lista dei crontab
    my_cron = CronTab(user='pi')
    for job in my_cron:
        mylist = job.command.split(" ")
        if valvola==mylist[3]:
            data_set = {"descrizione": job.comment,
                        "minuto": str(job.minute),
                        "ora": str(job.hour),
                        "giorno_mese": str(job.day),
                        "mese": str(job.month),
                        "giorno_settimana": str(job.dow),
                        "numero_elettrovalvola": mylist[3],
                        "tempo_apertura": mylist[4],
                        "abilitato": job.is_enabled()
                        }
            tasks.append(data_set)
    # converte in struttura JSON
    # responce=json.dumps(my_tasks)
    return tasks

print(sys.version_info[0])
"""
print(up_task({"descrizione": "nuovo 5",
                        "minuto": "2",
                        "ora": "3",
                        "giorno_mese": "*",
                        "mese": "*",
                        "giorno_settimana": "*",
                        "numero_elettrovalvola": "2",
                        "tempo_apertura": "10",
                        "abilitato": True
                        }))


if find_task("nuovo 2")!=False:
    print("trovato")
else:
    print("NON trovato")


#print(find_tasks_valve("3"))
print(get_tasks())
"""