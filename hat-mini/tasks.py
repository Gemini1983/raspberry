from crontab import CronTab, CronSlices
import json
import sys
import os
import random


def get_tasks():
    tasks = []
    # lista dei crontab
    my_cron = CronTab(user='pi')
    for job in my_cron:
        mylist = job.command.split(" ")
        data_set = {
            "id": mylist[5],
            "descrizione": job.comment,
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


def up_task(mytask, id_valvola, id_task):

    # controllo dati
    if not 'tempo_apertura' in mytask:

 # mytask["descrizione"] and mytask["minuto"] and mytask["ora"] and mytask["giorno_mese"] and mytask["mese"] and mytask["giorno_settimana"]:
        print("dati non completi")
        return False

    # Posso cambiare la descrizione del task solo se non esiste già (eccetto lui stesso)
    if find_task_comment(mytask["descrizione"]) and not find_task_comment(mytask["descrizione"])["id"] == id_task:
        print("descrizione già esistente")
        return False

    # controllo periodo
    period = mytask["minuto"], mytask["ora"], mytask["giorno_mese"], mytask["mese"], mytask["giorno_settimana"]
    if not CronSlices.is_valid(period):
        print("perido non valido")
        return False

    found = False
    path_project = os.path.abspath(os.path.dirname(sys.argv[0]))

    # Cancella per aggiornare se ha trovato l'identificativo del task
    my_cron = CronTab(user='pi')
    for job in my_cron:
        mylist = job.command.split(" ")
        if id_task == mylist[5]:
            my_cron.remove(job)
            my_cron.write()
            found = True

    if found is False:
        print("id non trovato")
        return False

    # Ricreiamo il task
    new_cron = CronTab(user='pi')
    new_job = new_cron.new(command='sudo /usr/bin/python3 '+path_project+'/apri_saracinesca.py ' +
                           id_valvola+' '+mytask["tempo_apertura"]+' '+id_task+' >> '+path_project+'/log.log', comment=mytask["descrizione"])

    new_job.setall(period)
    new_job.enable(mytask["abilitato"])
    new_cron.write()
    mytask["id"] = id_task
    return mytask


def new_task(mytask, id_elettrovalvola):
    path_project = os.path.abspath(os.path.dirname(sys.argv[0]))
    period = mytask["minuto"], mytask["ora"], mytask["giorno_mese"], mytask["mese"], mytask["giorno_settimana"]
    id = str(random.getrandbits(50))

    if CronSlices.is_valid(period):
        print("Periodo Corretto")
        # Errore se esiste già un task con la descrizione uguale
        my_cron = CronTab(user='pi')
        for job in my_cron:
            if job.comment == mytask["descrizione"]:
                print("Descrizione già esiste")
                return []

        # Creiamo il task
        new_cron = CronTab(user='pi')
        new_job = new_cron.new(command='sudo /usr/bin/python3 '+path_project+'/apri_saracinesca.py '+id_elettrovalvola +
                               ' '+mytask["tempo_apertura"]+' '+id+' >> '+path_project+'/log.log', comment=mytask["descrizione"])

        new_job.setall(period)
        new_job.enable(mytask["abilitato"])
        new_cron.write()
        mytask["id"] = id
        return mytask
    else:
        print("perido non valido")
        return []


def del_task(id):
    my_cron = CronTab(user='pi')
    for job in my_cron:
        mylist = job.command.split(" ")
        if mylist[5] == id:
            my_cron.remove(job)
            my_cron.write()
            return True

    return False


def find_task_comment(descrizione):
    my_cron = CronTab(user='pi')
    for job in my_cron:
        if descrizione == job.comment:
            mylist = job.command.split(" ")
            data_set = {
                "id": mylist[5],
                "descrizione": job.comment,
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
        if valvola == mylist[3]:
            data_set = {
                "id": mylist[5],
                "descrizione": job.comment,
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


def find_a_task(id_valvola, id_task):

    # lista dei crontab
    my_cron = CronTab(user='pi')
    for job in my_cron:
        mylist = job.command.split(" ")
        if id_valvola == mylist[3] and id_task == mylist[5]:
            data_set = {
                "id": mylist[5],
                "descrizione": job.comment,
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


