# using flask_restful
from tasks import get_tasks, up_task, new_task, del_task, find_task_comment,find_tasks_valve
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import sys
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')




path_project = os.path.abspath(os.path.dirname(sys.argv[0]))

# creating the flask app
app = Flask("Valve")
# creating an API object
api = Api(app)

# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.


class Get_valves(Resource):

    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
        host = config['valves']
        result=get_tasks()
        return jsonify(get_tasks())

    # Corresponds to POST request
    def post(self):

        data = request.get_json()	 # status code
        return jsonify({'data': data}), 201


class Delete(Resource):

    def get(self):

        os.system('python3 '+path_project+'/deletecron.py')
        return jsonify({'delete': 'OK'})
    
class Createcron(Resource):

    def get(self,saracinesca,tempo,ora,minuti):

        os.system('python3 '+path_project+'/createcron.py '+saracinesca+' '+tempo+' '+ora+' '+minuti)
        return jsonify({'create': 'OK'})

# another resource to calculate the square of a number


class Square(Resource):

    def get(self, num):

        return jsonify({'square': num**2})

# delete all crontab


# adding the defined resources along with their corresponding urls
api.add_resource(Get_valves, '/valves')
api.add_resource(Square, '/square/<int:num>')
api.add_resource(Delete, '/delete/')
api.add_resource(Createcron, '/createcron/saracinesca/<string:saracinesca>/tempo/<string:tempo>/ora/<string:ora>/minuti/<string:minuti>')


# driver function
if __name__ == '__main__':

    #	app.run(debug = True)
    app.run(host='0.0.0.0')
