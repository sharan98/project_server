from flask import Flask, request, send_file
from flask_cors import CORS
from app import Project
from json import dumps, loads
from bson.json_util import dumps as bsonDumps # to convert cursor object to json
from defaults import *
api = Flask(__name__)
CORS(api)
project = Project(uri="mongodb://localhost:27017/", dbName= 'food', collection="FAO")

@api.route('/head')
def hello_world():
    return str(project.head())

@api.route('/plot')
def get_plot():
    bytes_obj = project.plot()
    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')

# requests.get(url, params={'filter': json.dumps(filter), 'limit': json.dumps(limit)})
@api.route('/crud/find', methods=['GET'])
def find_from_db():
    args = request.args
    # j = loads(dumps(args))
    argsJSON = parseRequestArgs(findArgsJSON, args)
    print (argsJSON)
    cursor = project.find(**argsJSON)
    response_list = bsonDumps(cursor)
    # cursor = project.find(filter=argsJSON['filter'], limit=argsJSON['limit'])
    print(response_list)
    return response_list

@api.route('/crud/insertOne', methods=['POST'])
def insert_one():
    args = bytesToJSON(request.data)
    argsJSON = parseRequestArgs(insertArgsJSON, args)
    print (argsJSON)
    cursor = project.insertOne(**argsJSON)
    print (str(cursor))
    print (cursor.inserted_id)
    # response_list = bsonDumps(cursor)
    return 'inserted {}'.format(cursor.inserted_id)

@api.route('/crud/insertMany', methods=['POST'])
def insert_many():
    args = bytesToJSON(request.data)
    argsJSON = parseRequestArgs(insertArgsJSON, args)
    print (argsJSON)
    result = project.insertMany(**argsJSON)
    print (str(result))
    print (result.inserted_id)
    return 'inserted {}'.format(result.inserted_id)

@api.route('/crud/updateOne', methods=['POST'])
def update_one():
    args = bytesToJSON(request.data)
    argsJSON = parseRequestArgs(updateArgsJSON, args)
    print (argsJSON)
    result = project.updateOne(**argsJSON)
    print (str(result))
    print (result.modified_count)
    return 'modified {}'.format(result.modified_count)

@api.route('/crud/updateMany', methods=['POST'])
def update_many():
    args = bytesToJSON(request.data)
    argsJSON = parseRequestArgs(updateArgsJSON, args)
    print (argsJSON)
    result = project.updateMany(**argsJSON)
    print (str(result))
    print (result.modified_count)
    return 'modified {}'.format(result.modified_count)

@api.route('/crud/deleteOne', methods=['POST'])
def delete_one():
    args = bytesToJSON(request.data)
    argsJSON = parseRequestArgs(deleteArgsJSON, args)
    print (argsJSON)
    result = project.deleteOne(**argsJSON)
    print (str(result))
    print (result.deleted_count)
    return 'deleted {}'.format(result.deleted_count)

@api.route('/crud/deleteMany', methods=['POST'])
def delete_many():
    args = bytesToJSON(request.data)
    argsJSON = parseRequestArgs(deleteArgsJSON, args)
    print (argsJSON)
    result = project.deleteMany(**argsJSON)
    print (str(result))
    print (result.deleted_count)
    return 'deleted {}'.format(result.deleted_count)

def parseRequestArgs(defArgs, args):
    print ('parsing')
    print (args)
    print (type(args))
    keys = list(args.keys())
    json = defArgs.copy()
    for key in keys:
        print (key + ':' + str(args.get(key)))
        json[key] = loads(args.get(key))
    return (json)

def bytesToJSON(args):
    my_json = args.decode('utf8').replace("'", '"')
    data = loads(my_json)
    # s = dumps(data)
    return data
# https://stackoverflow.com/questions/30333299/pymongo-bson-convert-python-cursor-cursor-object-to-serializable-json-object
