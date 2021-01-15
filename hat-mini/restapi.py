#!/usr/bin/env python3

# using flask_restful
from tasks import get_tasks, up_task, new_task, del_task, find_task_comment, find_tasks_valve, find_a_task
from gpio import statePIN
from flask import Flask, jsonify, request,render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import sys
import os
import configparser
import automationhat

config = configparser.ConfigParser()
config.read('config.ini')

path_project = os.path.abspath(os.path.dirname(sys.argv[0]))

# creating the flask app
app = Flask("Valve")

CORS(app, resources={r"/*": {"origins": "*"}})
# creating an API object
api = Api(app)



# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.


class Valve_list(Resource):
    # GET VALVES/
    # Lista delle valvole e dei task associati
    def get(self):
        valves = []
        # il numero delle valvole e la descrizione è definito da file di configurazione
        for x in range(int(config['definition']['numero'])):
            valvola = str(x+1)
            config['valves'][valvola]
            valve = {"id": valvola,
                     "descrizione": config['valves'][valvola],
                     "tasks": find_tasks_valve(valvola),
                     "stato": statePIN(valvola)
                     }
            valves.append(valve)
        return jsonify(valves)


class Valve(Resource):
    # GET VALVES/{id}
    # Ritorna la risorsa di una singola valvola
    def get(self, id_valvola):
        try:
            descrizione = (config['valves'][id_valvola])
        except:
            print("Non esiste l'elettrovalvola segnalata")
            return []

        valve = {"id": id_valvola,
                 "descrizione": descrizione,
                 "tasks": find_tasks_valve(id_valvola),
                 "stato": statePIN(id_valvola)
                 }
        return jsonify(valve)

    # POST VALVES/{id}/?stato=<chiusa/aperta>&tempo=<secondiaperta>
    def post(self, id_valvola):
        stato_richiesto = request.args.get('stato')
        tempo = request.args.get('tempo')
        stato_presente = statePIN(id_valvola)
        if not stato_richiesto:
            return '', 400

        if stato_richiesto == 'aperta' and stato_presente == 'chiusa':
            if not tempo:
                pid=os.fork()
                if pid==0: # new process
                    os.system("nohup "+ path_project +"/apri_saracinesca_tempo.py "+ id_valvola +" &")
                    exit()
                return '', 201
            else:
                pid=os.fork()
                if pid==0: # new process
                    os.system("nohup "+ path_project +"/apri_saracinesca_tempo.py "+ id_valvola +" "+tempo+" &")
                    exit()
                return '', 201
        if stato_richiesto == 'chiusa' and stato_presente == 'aperta':
            os.system(path_project+"/chiudi_saracinesca.py "+id_valvola)
            return '', 201
        return '', 200


class Task_list(Resource):
    # POST VALVES/{id}/tasks
    # GET VALVES/{id}/tasks

    # Crea un nuovo task
    def post(self, id_valvola):
        json_data = request.get_json(force=True)
        mytask = new_task(json_data, id_valvola)
        if mytask:
            print("inserito")
            return (mytask), 201
        else:
            return ({'Errore': 'Dati non validi'}), 400

    # Ritorna la lista dei task di una valvola
    def get(self, id_valvola):
        print("catturato dalla get 1")
        try:
            descrizione = (config['valves'][id_valvola])
        except:
            print("Non esiste l'elettrovalvola segnalata")
            return []
        return jsonify(find_tasks_valve(id_valvola))


class Task(Resource):
    # GET VALVES/{id}/tasks/{id}
    # DELETE VALVES/{id}/tasks/{id}
    # UPDATE VALVES/{id}/tasks/{id}
         
    # Ritorna un task di una valvola      
    def get(self, id_valvola, id_task):
        print("catturato dalla get 2")
        print(request.method)
        if find_a_task(id_valvola, id_task):
            return (find_a_task(id_valvola, id_task), 200)
        else:
            return ('', 404)
    # Cancella un task di una elettrovalvola

    def delete(self, id_valvola, id_task):
        try:
            nome_elettrovalvola = (config['valves'][id_valvola])
        except:
            print("Non esiste l'elettrovalvola indicata")
            return 'errore', 400
        if del_task(id_task):
            return '', 204
        else:
            print("Non esiste il task indicato")
            return 'errore', 404

    # Aggiorna un task di una elettrovalvola
    def put(self, id_valvola, id_task):
        # ricercare il task prima
        if find_a_task(id_valvola, id_task):
            task = request.get_json(force=True)
            result = up_task(task, id_valvola, id_task)
            if result:
                print("aggiornato")
                return (result), 201
            else:
                return ('', 400)
        else:
            return ('', 404)


# adding the defined resources along with their corresponding urls
api.add_resource(Valve_list, '/api/valves/')
api.add_resource(Valve, '/api/valves/<string:id_valvola>/')
api.add_resource(Task_list, '/api/valves/<string:id_valvola>/tasks/')
api.add_resource(Task, '/api/valves/<string:id_valvola>/tasks/<string:id_task>/')

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html') # Return index.html 


# driver function
if __name__ == '__main__':

    #	app.run(debug = True)
    app.run(host='0.0.0.0')
